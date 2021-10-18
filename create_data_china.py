# -*- coding: utf-8 -*-
"""
@Time ： 2020/9/22 16:19
@Auth ： kun
@File ：create_data_china.py
@IDE ：PyCharm
"""

import  sys, os
import pandas as pd
import numpy
from datetime import datetime

root_dir = os.path.dirname(os.path.abspath(__file__))
full_data = pd.read_csv("./data/China/2020-07.csv",index_col=0)
N = full_data.shape[0]
delta = 17
for i in range(delta):
    NN = N-17+i
    created_data = full_data.iloc[264:NN, :]
    end_date = created_data.index[-1]
    end_date = datetime.strptime(end_date,"%Y/%m/%d")
    end_name = datetime.strftime(end_date,"%Y-%m")
    created_data.to_csv("./data/China/"+end_name+".csv")