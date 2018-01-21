# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 21:53:22 2018

@author: LIU
"""

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
import re
'''
使用excel转化后的数据
'''
train_data = pd.read_csv('../data/yancheng_train_20171226.csv')
test_data = pd.read_csv('../data/yancheng_test_20171225.csv')

#查看数据信息
train_data.info()
#level_id.isnull().all() = True,只有class_id=178529的有问题,不妨level_id=6
#fuel_type_id,class_id=175962,961962; 同类型的车fti都是1，就补1
#.......
train_data['level_id'] = train_data['level_id'].apply(lambda x: 6 if x=='-' else x).astype('int')
train_data['fuel_type_id'] = train_data['fuel_type_id'].apply(lambda x:1 if x=='-' else x).astype('int')
train_data['power'] = train_data['power'].apply(lambda x:81 if x=='81/70' else x).astype('float')
train_data['engine_torque'] = train_data['engine_torque'].apply(lambda x: 155 if x=='155/140'\
                               else 73 if x=='-' else x).astype('float')
train_data['rated_passenger'] = train_data['rated_passenger'].apply(lambda x: 5 \
                                                 if x=='4-5' else 7 if x=='5-7' or x=='6-7'\
                                                 else 8 if x=='5-8' or x=='6-8' or x=='7-8'\
                                                 else x).astype('int')

#13 categorical fields 
cate_list = ['brand_id','type_id','level_id','department_id','TR','gearbox_type',\
             'if_charging','driven_type_id','fuel_type_id','newenergy_type_id',\
             'emission_standards_id','if_MPV_id','if_luxurious_id']

feature_cate_temp = pd.get_dummies(train_data[cate_list],prefix=cate_list,columns=cate_list)

#---------------------------构造特征准备数据------------------------------------#
#category原始数据drop，concat one-hot之后的数据
feature_temp1 = pd.concat((train_data.drop(cate_list,axis=1),feature_cate_temp),axis=1)

#class_id按照3年总销量排序,将class_id进行映射成140-1的数（更精确考虑每年）
class_list_temp = train_data.groupby(['class_id'],as_index=False).sum()\
            .sort_values(by='sale_quantity', ascending=False)
class_list = pd.DataFrame(class_list_temp.loc[:,'class_id'])
class_list['class_trans'] = np.arange(140,0,-1)
feature_temp2 = pd.merge(feature_temp1, class_list).drop('class_id',1)
#del class_list_temp

#sale_date：提取年、月的信息，其中年按照delta方式取，2012为1,2013为2......
sale_date_temp = pd.DataFrame(train_data['sale_date'].unique()).sort_values(by=0)
sale_date_temp['year_delta'] = (sale_date_temp[0]/100).astype('int')-2011
sale_date_temp['month'] = sale_date_temp[0].astype('str').apply(lambda x: x[4:6]).astype('int')
sale_date_temp.rename(columns={0:'sale_date'},inplace=True)
feature_temp3 = pd.merge(feature_temp2, sale_date_temp).drop('sale_date',1) 
#del sale_date_temp, train_trans1

#15 numerical fields
num_list = ['compartment','displacement','price_level','power','cylinder_number',\
            'engine_torque','car_length','car_width','car_height','total_quality',\
            'equipment_quality','rated_passenger','wheelbase','front_track','rear_track']
#将从price_level提出low_bound, up_bound， mean
price_level_bounds=feature_temp3['price_level'].apply(lambda x: list(map(int,re.findall(r'\d+',x))))
list_low = []
list_high = []
list_center = []
for i in price_level_bounds.values:
   if len(i) == 2:
      list_low.append(i[0])
      list_high.append(i[1])
      list_center.append((i[0]+i[1])/2)
   else:
      list_low.append(i[0])
      list_high.append(i[0])
      list_center.append(i[0])
   
feature_temp3['price_level_low'] = list_low
feature_temp3['price_level_high'] = list_high
feature_temp3['price_level_center'] = list_center

# 车体积/1000000
feature_temp3['car_volume'] = feature_temp3['car_length']*feature_temp3['car_width']*\
                              feature_temp3['car_height']/1000000
#2 key_fields
key_list = ['sale_date','class_id']

# target_field 
target_list = ['sale_quantity']

#***********************************构造特征*********************************#
feature_grouped = feature_temp3.groupby(['class_trans','year_delta','month'])
feature_sum = feature_grouped.sum()
feature_mean = feature_grouped.mean()
feature_std = feature_grouped.std()
feature_record_num = feature_grouped['sale_quantity'].nunique()
#特征命名
feature_sum.columns = ['sum_%s' %x for x in feature_sum.columns]
feature_mean.columns = ['mean_%s' %x for x in feature_mean.columns]
feature_std.columns = ['std_%s' %x for x in feature_std.columns]
feature_record_num.columns = 'record_num'

#选特征concat
features = pd.concat(。。。。。。)


#其它：还可按照销量构造某特征在各个取值的重要性特征
#      构造一条记录里某特征出现了几个取值特征