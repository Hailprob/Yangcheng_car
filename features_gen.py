# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 21:53:22 2018

@author: LIU
"""

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn

'''
使用excel转化后的数据
'''
train_data = pd.read_csv('../data/train.csv')


#class_id按照总销量排序,将class_id进行映射成140-1的数
class_list_temp = train_data.groupby(['class_id'],as_index=False).sum()\
            .sort_values(by='sale_quantity', ascending=False)
class_list = pd.DataFrame(class_list_temp.loc[:,'class_id'])
class_list['class_trans'] = np.arange(140,0,-1)
train_trans1 = pd.merge(train_data, class_list).drop('class_id',1)
#del class_list_temp

#sale_date：提取年、月的信息，其中年按照delta方式取，2012为1,2013为2......
sale_date_temp = pd.DataFrame(train_data['sale_date'].unique()).sort_values(by=0)
sale_date_temp['year_delta'] = (sale_date_temp[0]/100).astype('int')-2011
sale_date_temp['month'] = sale_date_temp[0].astype('str').apply(lambda x: x[4:6]).astype('int')
sale_date_temp.rename(columns={0:'sale_date'},inplace=True)
train_trans = pd.merge(train_trans1, sale_date_temp).drop('sale_date',1) 
#del sale_date_temp, train_trans1

#if_charging:L-无增压：1，T-涡轮增压:0
if_charging_temp = train_trans['if_charging'].apply(lambda x: 1 if x=='L' else 0)\
                                .rename('if_charging_trans')
train_trans = pd.concat((train_trans,if_charging_temp),axis=1).drop('if_charging',1)

#Norminal定类变量需要先按照class_id提取出来(假设每种class_id对应的这些)
norm_list = ['gearbox_type','if_charging','price_level']
train_trans_group = train_trans.groupby(['class_trans','year_delta','month'])
feature10 = train_trans_group.agg({'gearbox_type':'nunique'}).rename(columns={'gearbox_type':'gbt_kinds'})
feature11 = train_trans_group.agg({'gearbox_type':'count'}).rename(columns={'gearbox_type':'gbt_record_num'})
features1 = pd.concat((feature10,feature11),axis=1)

feature20 = train_trans_group.agg({'if_charging_trans':'nunique'}).rename(columns={'if_charging_trans':'charge_kinds'})
feature21 = train_trans_group.agg({'if_charging_trans':'count'}).rename(columns={'if_charging_trans':'charge_record_num'})
feature22 = train_trans_group.agg({'if_charging_trans':'sum'}).rename(columns={'if_charging_trans':'charge_type'})
features2 = pd.concat((feature20,feature21,feature22),axis=1)
# charge type:T-1,L-2,L+T-3
for i in range(5587):
   if features2.iloc[i,0]==2:
      features2.iloc[i,2]=3
   else:
      if features2.iloc[i,2]==0:
         features2.iloc[i,2]=1
      else:
         features2.iloc[i,2]=2
         
'''
没写
'''
#Numeric数值变量求均值、总和、标准差构造特征

features = train_trans_group.sum()
