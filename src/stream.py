from filter import filter_dataframe
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
from io import StringIO
import re

st.title('Logging app')


src = Path(r"src\logs\ENV_0 copy.log")
data = src.open('r')
df = pd.read_csv(StringIO(data.read()), sep=' - ', names=['time', 'module', 'level', 'message'], engine='python')

# len episode / episode

len_ep = []
timestep = 0
for step in df['message']:
    if re.search(r"(@timestep )", step):
        timestep += 1
    elif re.search(r"_terminated with reward ", step):
        len_ep += {timestep}
        timestep = 0
    elif re.search("_truncated ", step):
        len_ep += {timestep}
        timestep = 0 

chart_data = pd.DataFrame(np.array(len_ep), columns=['len ep'])
filter_df = filter_dataframe(df)

# mean attained index per episode

st.write(filter_df)
st.bar_chart(chart_data)
