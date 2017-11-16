
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# In[52]:


#Load the data
AAPL_Historical = pd.read_csv("nasdaqHistorical/AAPL_Historical.csv")
TSM_Historical = pd.read_csv("nasdaqHistorical/TSM_Historical.csv")
CSCO_Historical = pd.read_csv("nasdaqHistorical/CSCO_Historical.csv")
FB_Historical = pd.read_csv("nasdaqHistorical/FB_Historical.csv")
GOOGL_Historical = pd.read_csv("nasdaqHistorical/GOOGL_Historical.csv")
IBM_Historical = pd.read_csv("nasdaqHistorical/IBM_Historical.csv")
INTC_Historical = pd.read_csv("nasdaqHistorical/INTC_Historical.csv")
MSFT_Historical = pd.read_csv("nasdaqHistorical/MSFT_Historical.csv")
ORCL_Historical = pd.read_csv("nasdaqHistorical/ORCL_Historical.csv")
SAP_Historical = pd.read_csv("nasdaqHistorical/SAP_Historical.csv")


# In[55]:


sns.set(style="darkgrid")

# Plot the response with standard error
sns.tsplot(data=AAPL_Historical.close, color="r")
sns.tsplot(data=TSM_Historical.close, color="g")
sns.tsplot(data=CSCO_Historical.close, color="b")
sns.tsplot(data=FB_Historical.close, color="w")
#sns.tsplot(data=GOOGL_Historical.close, color="g")
sns.tsplot(data=IBM_Historical.close, color="g")
sns.tsplot(data=INTC_Historical.close, color="g")
sns.tsplot(data=MSFT_Historical.close, color="g")
sns.tsplot(data=ORCL_Historical.close, color="g")
sns.tsplot(data=SAP_Historical.close, color="g")

plt.show()

