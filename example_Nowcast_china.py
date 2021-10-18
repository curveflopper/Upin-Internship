# encoding:utf-8
import numpy as np
import sys,os
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir+'/functions/')
from load_spec_china import *
from load_data_china import *
from update_nowcast_china import *
from split_data import *
from macro_api import *
import pickle

### Nowcasting ############################################################
# This script produces a nowcast of US real GDP growth for 2016:Q4 
# using the estimated parameters from a dynamic factor model.
###########################################################################

## User inputs.
series = 'RGDP'
period = '2020q3'

###########################################################################
## Load model specification and first vintage of data.
# Load model specification structure `Spec`
Spec = load_spec('spec_china.csv')

## Load DFM estimation results structure `Res`.
Res = pickle.load(open('./data/China/ResDFM2008', 'rb'))['Res']

###########################################################################
## Update nowcast and decompose nowcast changes into news.


mysql_indicator_lst = ["IAV", "EXPDEL", "PROFIT", "STEPRO", "FREITURN", "ELEPRO", "FREIVOL",
                       "INVPFA", "PFREV", "PFEXP", "IMPEXP", "BALANCE", "RSAFS", "VELSAL", "CPI", "CPINFO",
                       "PPI", "REPI170", "REPI270", "PMI", "PMIM", "PMINO", "PMINEO", "PMIOIH", "PMIPVI", "PMIOQ",
                       "PMIIMP", "PMIPMRM", "PMIRMI", "PMIE", "PMISDT", "M2", "Loan"]
# Oracle指标列表
Oracle_indicator_lst = ["INVFIX", "INVRSD", "RPI","SOFIN", "RGDP"]
# 生成观测指标数据
datafile = get_data(mysql_indicator_lst,Oracle_indicator_lst)

### Nowcast update from 2019/12 to 2020/01
# input date form should be yyyy/mm/01
vintage_old = '2020/07/01'
datafile_old = split(datafile,vintage_old)

vintage_new = '2020/08/01'
datafile_new = split(datafile,vintage_new)

# Load datasets for each vintage
sample_start = '2005/01/01'
X_old,__,__ = load_data(datafile_old,Spec,sample=sample_start)
X_new,Time,__ = load_data(datafile_new,Spec,sample=sample_start)

#伪预测 将预测部分填空值
X_new.loc[vintage_new,"RGDP"] = np.nan

# check if spec used in estimation is consistent with the current spec
# if isequal(Res.Spec,Spec):
#     Res = Res.Res
# # example_Nowcast.m:37
# else:
#     threshold = 0.0001
# # example_Nowcast.m:39
#     Res = dfm(X_new,Spec,threshold)
# # example_Nowcast.m:40
#     save('ResDFM','Res','Spec')

update_nowcast(X_old,X_new,Time,Spec,Res,series,period,vintage_old,vintage_new)
###########################################################################