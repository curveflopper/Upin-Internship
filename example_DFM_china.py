# encoding:utf-8
import sys,os
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir+'/functions/')
from functions.load_spec_china import *
from functions.macro_api import *
from functions.split_data import *
from load_data_china import *
import dfm_estimator_china
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pickle
import numpy as np
import pandas as pd

### Dynamic factor model (DFM) ############################################
# This script estimates a dynamic factor model (DFM) using a panel of
# monthly and quarterly series.
###########################################################################

## User inputs.
vintage = '2020/08/01'
country = 'China'

sample_start = '2005/01/01'
print('sample_start:\n',sample_start)

## Load model specification and dataset.
# Load model specification structure `Spec`
Spec = load_spec('spec_china.csv')
# Parse `Spec`
SeriesID = Spec['SeriesID']
SeriesName = Spec['SeriesName']
Units = Spec['Units']
UnitsTransformed = Spec['UnitsTransformed']

# Load data
# mysql指标列表
mysql_indicator_lst = ["IAV", "EXPDEL", "PROFIT", "STEPRO", "FREITURN", "ELEPRO", "FREIVOL",
                       "INVPFA", "PFREV", "PFEXP", "IMPEXP", "BALANCE", "RSAFS", "VELSAL", "CPI", "CPINFO",
                       "PPI","REPI170","REPI270", "PMI", "PMIM", "PMINO", "PMINEO", "PMIOIH", "PMIPVI", "PMIOQ",
                       "PMIIMP", "PMIPMRM", "PMIRMI", "PMIE", "PMISDT", "M2", "Loan"]
# Oracle指标列表
Oracle_indicator_lst = ["INVFIX", "INVRSD", "RPI","SOFIN", "RGDP"]
# 生成观测指标数据
datafile = get_data(mysql_indicator_lst,Oracle_indicator_lst)

datafile = split(datafile,vintage)
X,Time,Z = load_data(datafile,Spec,sample_start)
# summarize(X,Time,Spec,vintage)

###########################################################################
## Run dynamic factor model (DFM) and save estimation output as 'ResDFM'.
threshold = 1.5e-4
dfm = dfm_estimator_china.DFM(X,Spec,threshold)
Res,xNaN = dfm.dfm()
pickle.dump({'Res':Res,"Spec":Spec,"xNaN":xNaN},open('./data/China/ResDFM2008','wb'))
# 导入已算好的结果
# Res = pickle.load(open('./data/China/ResDFM2008','rb'))['Res']


#############################################################
## Plot common factor and standardized data.
_Res = Res['x_sm']
idxSeries = [ind for ind,x in enumerate(SeriesID) if x== "REPI270"][0]
plt.figure(num='Common Factor and Standardized Data',figsize=(14, 8))
_Res = Res['x_sm']
h0 = plt.plot(_Res,':')
h=plt.plot(Res['Z'][:,0],color='k',label='common factor')
plt.legend(frameon=False)
plt.xlim((0, len(_Res) + 6))
index = np.array([ind[:4] for ind in list(Time)])
new_ticks = np.array(range(0, len(_Res), 12))
plt.xticks(new_ticks, index[new_ticks], rotation=45,fontsize=6)
plt.xlabel('Date')
# plt.tight_layout()
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1,wspace=0.1,hspace=0.2)
plt.savefig("./figure/data_common_factor.png")

####################################################################
## Plot all factors
plt.figure(figsize=(14, 8))
h1 = plt.plot(Res['Z'][:,0]*Res['C'][idxSeries,0],color = 'b',label = 'global factor')
h2 = plt.plot(Res['Z'][:,3]*Res['C'][idxSeries,0],color = 'y',label = 'real factor')
h3 = plt.plot(Res['Z'][:,6]*Res['C'][idxSeries,0],color = 'g',label = 'finance factor')
h4 = plt.plot(Res['Z'][:,9]*Res['C'][idxSeries,0],color = 'r',label = 'sentimental factor')
h5 = plt.plot(Res['Z'][:,12]*Res['C'][idxSeries,0],color = 'm',label = 'price factor')
plt.legend(frameon=False)
plt.xlim((0, len(_Res) + 6))
index = np.array([ind[:4] for ind in list(Time)])
new_ticks = np.array(range(0, len(_Res), 24))
plt.xticks(new_ticks, index[new_ticks], rotation=45,fontsize=6)
plt.xlabel('Date')
# plt.tight_layout()
plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1,wspace=0.1,hspace=0.2)
plt.savefig("./figure/5_fatcors_historical_process.png")

#########################################################################
## Plot real factor, GDP and IAV
#数据标准化
_Res = Res['x_sm']
iav = [ind for ind,x in enumerate(SeriesID) if x== "IAV"][0]
gdp = [ind for ind,x in enumerate(SeriesID) if x== "RGDP"][0]
plt.figure(figsize=(14, 8))
quarter_index = [ind for ind in range(_Res.shape[0]) if (ind+1)%3==0]
h1 = plt.scatter(quarter_index, _Res[quarter_index,gdp], color='r', label='GDP')
h2 = plt.plot(Res['Z'][:,3], color = 'k',label='实际产出因子')
h3 = plt.plot(_Res[:,iav], color='b', label='工业增加值')
index = np.array([ind[:4] for ind in list(Time)])
new_ticks = np.array(range(0, len(_Res), 24))
plt.xticks(new_ticks, index[new_ticks], rotation=45,fontsize=6)
plt.xlabel('Date')
plt.savefig("./figure/real_factor_and_related_variable.png")