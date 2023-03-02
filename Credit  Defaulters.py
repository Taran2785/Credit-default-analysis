#!/usr/bin/env python
# coding: utf-8

# # Loan Default Analysis

# In[553]:


#import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[554]:


#Data import and Data Exploration
app = pd.read_csv("application_data.csv")
prev_app =pd.read_csv("previous_application.csv")


# In[555]:


app.head()


# In[556]:


prev_app.head()


# In[557]:


app.shape


# In[558]:


#Dataframe of missing values columns
missing_values= pd.DataFrame(app.isnull().sum().sort_values()).reset_index()
missing_values.rename(columns={"index":"col_name",0:"null_count"},inplace="True")
missing_values.head()


# In[559]:


#Converting missing values in percentage
missing_values["missing_pct"]= missing_values["null_count"]/app.shape[0]*100
missing_values


# In[560]:


#Drop missing columns
app.missing_columns= missing_values[missing_values["missing_pct"]>=40]["col_name"].to_list()
app.missing_columns


# In[561]:


app_msng_rem= app.drop(labels=app.missing_columns,axis=1)
app_msng_rem


# In[562]:


#Exploring Flag Columns
flag_col=[]
for col in app_msng_rem.columns:
    if col.startswith("FLAG_"):
        flag_col.append(col)
        
flag_col        


# In[563]:


#Checking relation between Flag and target columns
flag_tgt_col = app_msng_rem[flag_col+["TARGET"]]
flag_tgt_col.head()


# In[564]:


#Plot relationship between flag columns and Target
plt.figure(figsize=(20,20))
for i,col in enumerate(flag_col):
    plt.subplot(7,4,i+1)
    sns.countplot(data=flag_tgt_col, x=col,hue="TARGET")


# In[565]:


#Creating correlation matrix
flag_corr= ['FLAG_OWN_CAR','FLAG_OWN_REALTY','FLAG_MOBIL','FLAG_EMP_PHONE','FLAG_WORK_PHONE','FLAG_CONT_MOBILE','FLAG_PHONE','FLAG_EMAIL','TARGET']
flag_corr_df=app_msng_rem[fig_corr] 


# In[566]:


flag_corr_df['FLAG_OWN_CAR']=flag_corr_df['FLAG_OWN_CAR'].replace({'N':0,'Y':1})
flag_corr_df['FLAG_OWN_REALTY']=flag_corr_df['FLAG_OWN_REALTY'].replace({'N':0,'Y':1})


# In[567]:



corr_df = round(flag_corr_df.corr(),2)
plt.figure(figsize=(10,5))
sns.heatmap(corr_df,cmap='coolwarm',linewidths=.5,annot=True)


# In[568]:


#Drop Flag columns as they do not have good correlation with Target
app_flag_rem=app_msng_rem.drop(labels=flag_col,axis=1)
app_flag_rem.shape


# In[569]:


app_flag_rem.head()


# In[570]:


#DROP EXT_SOURCE column because of poor correlation with Target
app_score_col_rmvd=app_flag_rem.drop(['EXT_SOURCE_2','EXT_SOURCE_3'],axis=1)
app_score_col_rmvd.shape


# ### FEATURE ENGINEERING

# In[571]:


#Missing value imputation
app_score_col_rmvd.isnull().sum().sort_values()/app_score_col_rmvd.shape[0]


# In[572]:


app_score_col_rmvd.groupby("CNT_FAM_MEMBERS").size()


# In[573]:


#Filling missing values

app_score_col_rmvd["CNT_FAM_MEMBERS"]=app_score_col_rmvd["CNT_FAM_MEMBERS"].fillna((app_score_col_rmvd["CNT_FAM_MEMBERS"]).mode()[0])


# In[574]:


app_score_col_rmvd["CNT_FAM_MEMBERS"].isnull().sum()


# In[575]:


app_score_col_rmvd.groupby("OCCUPATION_TYPE").size().sort_values()


# In[576]:


app_score_col_rmvd["OCCUPATION_TYPE"].mode()[0]


# In[577]:


#Filling missing values
app_score_col_rmvd["OCCUPATION_TYPE"]=app_score_col_rmvd["OCCUPATION_TYPE"].fillna((app_score_col_rmvd["OCCUPATION_TYPE"]).mode()[0])


# In[578]:


app_score_col_rmvd["OCCUPATION_TYPE"].isnull().sum()


# In[579]:


app_score_col_rmvd.groupby(["NAME_TYPE_SUITE"]).size()


# In[580]:


#Filling missing values
app_score_col_rmvd["NAME_TYPE_SUITE"]=app_score_col_rmvd["NAME_TYPE_SUITE"].fillna((app_score_col_rmvd["NAME_TYPE_SUITE"]).mode()[0])


# In[581]:


app_score_col_rmvd["NAME_TYPE_SUITE"].isnull().sum()


# In[582]:


#Filling missing values
app_score_col_rmvd["AMT_ANNUITY"]=app_score_col_rmvd["AMT_ANNUITY"].fillna((app_score_col_rmvd["AMT_ANNUITY"]).mode()[0])


# In[583]:


app_score_col_rmvd["AMT_ANNUITY"].isnull().sum()


# In[584]:


#Making List of AMT_REQ_CREDIT_BUREAU

amt_req_col= []
for col in app_score_col_rmvd.columns:
    if col. startswith("AMT_REQ_CREDIT_BUREAU"):
        amt_req_col.append(col)
        
amt_req_col        


# In[585]:


for col in amt_req_col:
    app_score_col_rmvd[col]= app_score_col_rmvd[col].fillna((app_score_col_rmvd[col]).median())


# In[586]:


app_score_col_rmvd[col].isnull().sum()


# In[587]:


app_score_col_rmvd["AMT_GOODS_PRICE"].isnull().sum()
   


# In[588]:


app_score_col_rmvd["AMT_GOODS_PRICE"].agg(["min","max","median","mean"])


# In[589]:


app_score_col_rmvd["AMT_GOODS_PRICE"]= app_score_col_rmvd["AMT_GOODS_PRICE"].fillna((app_score_col_rmvd["AMT_GOODS_PRICE"]).median())


# In[590]:


app_score_col_rmvd["AMT_GOODS_PRICE"].isnull().sum()


# In[591]:


app_score_col_rmvd["AMT_CREDIT"].isnull().sum()


# # Value Modification

# In[592]:


#Making list of Days column
days_col=[]
for col in app_score_col_rmvd.columns:
    if col.startswith("DAYS"):
        days_col.append(col)
days_col        
        


# In[593]:


#Converting negative values to positive
for col in days_col:
    app_score_col_rmvd[col]=abs(app_score_col_rmvd[col])
    
app_score_col_rmvd.head()    


# In[594]:


app_score_col_rmvd.info()


# In[595]:


#Outlier detection and treatment
app_score_col_rmvd["AMT_GOODS_PRICE"].agg(["min","max","median"])


# In[596]:


sns.kdeplot(data=app_score_col_rmvd, x="AMT_GOODS_PRICE")


# In[597]:


app_score_col_rmvd["AMT_GOODS_PRICE"].quantile([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99])


# In[598]:


#Binning
bins= [0,100000,200000,300000,400000,500000,600000,700000,800000,900000,4050000]
ranges =["0-100k","100k-200k","200k-300k","300k-400k","400k-500k","500k-600k","600k-700k","700k-800k","800k-900k","Above 900k"]
app_score_col_rmvd["AMT_GOODS_PRICE"]=pd.cut(app_score_col_rmvd["AMT_GOODS_PRICE"],bins,labels=ranges)


# In[599]:


app_score_col_rmvd.groupby(["AMT_GOODS_PRICE"]).size()


# In[600]:


app_score_col_rmvd["AMT_INCOME_TOTAL"].quantile([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99])


# In[601]:


#Binning
bins= [0,100000,150000,200000,250000,300000,350000,400000,472500]
ranges =["0-100k","100k-150k","150k-200k","200k-250k","250k-300k","300k-350k","350k-400k","Above 400k"]
app_score_col_rmvd["AMT_INCOME_TOTAL"]=pd.cut(app_score_col_rmvd["AMT_INCOME_TOTAL"],bins,labels=ranges)


# In[602]:


app_score_col_rmvd.groupby(["AMT_INCOME_TOTAL"]).size()


# In[603]:


app_score_col_rmvd["AMT_CREDIT"].quantile([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99])


# In[604]:


bins= [0,200000,400000,600000,800000,900000,1000000,1854000]
ranges =["0-200k","200k-400k","400k-600k","600k-800k","800k-900k","900k-1M","Above 1M"]
app_score_col_rmvd["AMT_CREDIT"]=pd.cut(app_score_col_rmvd["AMT_CREDIT"],bins,labels=ranges)


# In[605]:


app_score_col_rmvd.groupby(["AMT_CREDIT"]).size()


# In[606]:


app_score_col_rmvd["AMT_ANNUITY"].quantile([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99])


# In[607]:


app_score_col_rmvd["AMT_ANNUITY"].max()


# In[608]:


bins= [0,25000,50000,100000,150000,200000,258025]
ranges =["0-25K","25K-50K","50k-100K","100k-150K","150K-200K","Above 200K"]
app_score_col_rmvd["AMT_ANNUITY_RANGE"]=pd.cut(app_score_col_rmvd["AMT_ANNUITY"],bins,labels=ranges)


# In[609]:


app_score_col_rmvd.groupby(["AMT_ANNUITY"]).size()


# In[610]:


app_score_col_rmvd["DAYS_EMPLOYED"].quantile([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99])


# In[611]:


app_score_col_rmvd["DAYS_EMPLOYED"].max()


# In[612]:


bins= [0,1825,3650,5475,7300,9125,10950,12775,14600,16425,18250,365243]
ranges =["0-5Y","5Y-10Y","10Y-15Y","15Y-20Y","20Y-25Y","25Y-30Y","30Y-35Y","35Y-40Y","40Y-45Y","45Y-50Y","Above 50Y"]
app_score_col_rmvd["DAYS_EMPLOYED_RANGE"]=pd.cut(app_score_col_rmvd["DAYS_EMPLOYED"],bins,labels=ranges)


# In[613]:


app_score_col_rmvd.groupby(["DAYS_EMPLOYED_RANGE"]).size()


# In[614]:


app_score_col_rmvd["DAYS_BIRTH"].quantile([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.99])


# In[615]:


bins= [0,7300,10950,14600,18250,21900,25229]
ranges =["20Y","20Y-30Y","30Y-40Y","40Y-50Y","50Y-60Y","Above 60Y"]
app_score_col_rmvd["DAYS_BIRTH_RANGE"]=pd.cut(app_score_col_rmvd["DAYS_BIRTH"],bins,labels=ranges)


# In[616]:


app_score_col_rmvd.groupby(["DAYS_BIRTH_RANGE"]).size()


# In[617]:


#Data Analysis
app_score_col_rmvd.dtypes.value_counts()


# In[618]:


#Exploring object type
obj_var = app_score_col_rmvd.select_dtypes(include=["object"]).columns
obj_var


# In[619]:


app_score_col_rmvd.groupby(["NAME_CONTRACT_TYPE"]).size()


# In[620]:


sns.countplot(data=app_score_col_rmvd,x="NAME_CONTRACT_TYPE", hue="TARGET")


# In[621]:


data_pct=app_score_col_rmvd[["NAME_CONTRACT_TYPE","TARGET"]].groupby(["NAME_CONTRACT_TYPE"],as_index=False).mean()


# In[622]:


data_pct["PCT"]=data_pct["TARGET"]*100


# In[623]:


data_pct


# In[624]:


sns.barplot(data=data_pct,x= 'NAME_CONTRACT_TYPE',y='PCT')


# In[625]:


obj_var


# In[627]:


plt.figure(figsize=(25,60))
for i, var in enumerate(obj_var):
    data_pct=app_score_col_rmvd[[var,"TARGET"]].groupby([var],as_index=False).mean().sort_values(by="TARGET",ascending=False)
    data_pct["PCT"]=data_pct["TARGET"]*100
    
    plt.subplot(10,2,i+i+1)
    plt.subplots_adjust(wspace=0.1,hspace=1)
    sns.countplot(data= app_score_col_rmvd,x=var,hue="TARGET")
    plt.xticks(rotation=90)
    
    plt.subplot(10,2,i+i+2)
    sns.barplot(data=  data_pct,x=var,y="PCT", palette = "coolwarm")
    plt.xticks(rotation=90)


# # Conclusion
# 

# In[ ]:


1) Most of the customers have taken Cash Loans and are less likely to default
2) Most of the loans are taken by Females and default rates for females are just 7% which is safer and less than male
3) Unacommpanied people have taken most of the loand and default rate is 8.5%
4) The safest segments are working, commercial associates and pensioners
5) Higher education is the safest segment to give laon with default rate of less than 5%
6) Married people are safe to target with default rate 8%
7) People having house or apartment are safe to target with default rate of 8%
8) Low skill laborers and drivers are highest defaulters
9) Accountants are less defaulters
10) Transport types 3 highest defaulters

