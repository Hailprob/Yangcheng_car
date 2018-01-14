# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 19:10:22 2018

@author: LIU
"""

import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sn

train_data = pd.read_csv('../data/yancheng_train_20171226.csv')
train_data = pd.read_csv('../data/train.csv')
#-------看销量情况---------#
data0 = train_data.groupby(['class_id','sale_date']).sum()
#class_id按照总销量排序
class_list_temp = train_data.groupby(['class_id'],as_index=False).sum()\
            .sort_values(by='sale_quantity', ascending=False)
class_list = class_list_temp.loc[:,['class_id','sale_quantity']]
#del class_list_temp

#看总销量第一的数据
data_qty_1st = train_data[train_data.class_id==class_list.iloc[:,0].values[0]]\
               .sort_values(by='sale_date', ascending=True)
#销量第二数据               
data_qty_2nd = train_data[train_data.class_id==class_list.iloc[:,0].values[1]]\
               .sort_values(by='sale_date', ascending=True)
# =============================================================================
# data_qty_3rd = train_data[train_data.class_id==class_list.iloc[:,0].values[2]]\
#                .sort_values(by='sale_date', ascending=True)   
# data_qty_4th = train_data[train_data.class_id==class_list.iloc[:,0].values[3]]\
#                .sort_values(by='sale_date', ascending=True)
# data_qty_5th = train_data[train_data.class_id==class_list.iloc[:,0].values[4]]\
#                .sort_values(by='sale_date', ascending=True)   
# data_qty_6th = train_data[train_data.class_id==class_list.iloc[:,0].values[5]]\
#                .sort_values(by='sale_date', ascending=True)  
# data_qty_7th = train_data[train_data.class_id==class_list.iloc[:,0].values[6]]\
#                .sort_values(by='sale_date', ascending=True)
# data_qty_8th = train_data[train_data.class_id==class_list.iloc[:,0].values[7]]\
#                .sort_values(by='sale_date', ascending=True)
# data_qty_9th = train_data[train_data.class_id==class_list.iloc[:,0].values[8]]\
#                .sort_values(by='sale_date', ascending=True)      
# data_qty_10th = train_data[train_data.class_id==class_list.iloc[:,0].values[9]]\
#                .sort_values(by='sale_date', ascending=True)     
#                
# data_qty_last = train_data[train_data.class_id==class_list.iloc[:,0].values[-1]]\
#                .sort_values(by='sale_date', ascending=True)                      
# =============================================================================
#同种车型 变速箱种类和装备质量等会有不同，造成同一时间对应多条记录
diff_list = ['gearbox_type','displacement','power','engine_torque','total_quality','equipment_quality']
            
data_qty_1st_date_unique = data_qty_1st.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
data_qty_2nd_date_unique = data_qty_2nd.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# =============================================================================
# data_qty_3rd_date_unique = data_qty_3rd.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# data_qty_4th_date_unique = data_qty_4th.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# data_qty_5th_date_unique = data_qty_5th.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# data_qty_6th_date_unique = data_qty_6th.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# data_qty_7th_date_unique = data_qty_7th.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# data_qty_8th_date_unique = data_qty_8th.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# data_qty_9th_date_unique = data_qty_9th.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# data_qty_10th_date_unique = data_qty_10th.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# 
# data_qty_last_date_unique = data_qty_last.groupby(['sale_date']).sum().loc[:,'sale_quantity'] 
# =============================================================================

#折线图
plt.figure(figsize=(14,6))
plt.plot(data_qty_1st_date_unique.values,label='qty_1st')           
plt.plot(data_qty_2nd_date_unique.values[9:],label='qty_2nd')
# =============================================================================
# plt.plot(data_qty_3rd_date_unique.values[9:],label='qty_3rd')
# plt.plot(data_qty_4th_date_unique.values[9:],label='qty_4th')
# plt.plot(data_qty_5th_date_unique.values[9:],label='qty_5th')
# plt.plot(np.arange(10,61), data_qty_6th_date_unique.values,label='qty_6th')
# plt.plot(data_qty_7th_date_unique.values[9:],label='qty_7th')
# plt.plot(data_qty_8th_date_unique.values[9:],label='qty_8th')
# plt.plot(data_qty_9th_date_unique.values[5:],label='qty_9th')
# plt.plot(data_qty_10th_date_unique.values[9:],label='qty_10th')
# 
# =============================================================================
plt.legend()
plt.xticks([3,15,27,39,51,60],[201301,201401,201501,201601,201701,201710])

#柱状图
plt.figure(figsize=(14,6))
plt.bar(np.arange(61),data_qty_1st_date_unique.values,label='qty_1st')
plt.bar(np.arange(61),data_qty_2nd_date_unique.values[9:],label='qty_2nd')
plt.xticks([3,15,27,39,51,60],[201301,201401,201501,201601,201701,201710])
plt.legend()

#每个class_id的记录数
records_num = train_data['class_id'].value_counts()
records_num.name = 'records_num'
#总销量
sale_qty = class_list.set_index('class_id')
qty_rec = pd.concat([records_num, sale_qty],axis=1).sort_values(by='sale_quantity',ascending=False)

