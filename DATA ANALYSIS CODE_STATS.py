#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
get_ipython().run_line_magic('matpotlib', 'inline')


# In[2]:


pwd


# In[3]:


cd Downloads


# In[39]:


transaction = pd.read_excel("QVI_transaction_data.xlsx")


# In[ ]:


purchase = pd.read_csv("QVI_purchase_behaviour.csv")


# In[40]:


transaction.head(10)


# In[23]:


transaction.isnull().sum()


# In[24]:


transaction.dtypes


# In[25]:


purchase.head(10)


# In[10]:


purchase.isnull().sum()


# In[26]:


purchase.dtypes


# In[41]:


transaction['DATE'] = pd.to_datetime((transaction['DATE'] - 25569) * 86400, unit='s')


# In[43]:


transaction


# In[79]:


transaction.PROD_NAME.value_counts()


# In[53]:


New = transaction.PROD_NAME.str.split(" ",expand=True)


# In[138]:


New


# In[56]:


new2 = New.melt()


# In[84]:


new2 = new2[(new2['value'].notnull())&(new2['value'].str.isalpha())&(~new2['value'].str.contains('&'))&(new2['value'] !='')]


# In[85]:


new2["value"].value_counts()


# In[73]:


pd.set_option("display.max_rows",200)


# In[93]:


transaction = transaction[~(transaction['PROD_NAME'].str.lower()).str.contains('salsa')]


# In[94]:


transaction


# In[95]:


transaction.describe()


# In[96]:


transaction[transaction['PROD_QTY']==200]


# In[97]:


transaction[transaction['LYLTY_CARD_NBR']==226000]


# In[98]:


transaction  = transaction[transaction['LYLTY_CARD_NBR']!=226000]


# In[99]:


transaction


# In[123]:


trans_count = transaction['DATE'].value_counts().reset_index()


# In[127]:


trans_count.rename(columns={'DATE':"Count","index":"DATE"}, inplace =True)


# In[128]:


trans_count


# In[112]:


dates = pd.date_range(start='07/01/2018', end='06/30/2019')


# In[113]:


dates = pd.DataFrame(dates)


# In[116]:


dates = dates.sort_values(by=0,ascending=True)


# In[117]:


dates.rename(columns={0:"DATE"}, inplace = True)


# In[118]:


dates


# In[129]:


merg = dates.merge(trans_count, how='left', on='DATE')


# In[130]:


merg


# In[136]:


plt.figure(figsize=(10,8))
merg.plot(x='DATE')
plt.xlabel("Day")
plt.ylabel("Number of transactions")
plt.title("Transactions over time")


# In[137]:


plt.figure(figsize=(10,8))
merg[(merg['DATE']>='2018-12-01')&(merg['DATE']<='2018-12-31')].plot(x='DATE')
plt.xlabel("Day")
plt.ylabel("Number of transactions")
plt.title("Transactions over time")


# In[199]:


transaction['pack_size'] = transaction.PROD_NAME.str.extract(r'\b([0-9]+)[gG]\b',expand = True)


# In[200]:


transaction['pack_size2'] = transaction.PROD_NAME.str.extract(r'\B([0-9]+)[gG]\b',expand = True)


# In[201]:


transaction['pack_size'].fillna(transaction['pack_size2'], inplace=True)


# In[206]:


transaction.drop('pack_size2',axis=1, inplace = True)


# In[209]:


transaction['pack_size']= transaction['pack_size'].astype('int64')


# In[211]:


transaction['pack_size'].max()


# In[212]:


transaction['pack_size'].min()


# In[213]:


transaction['pack_size'].plot(kind='hist')


# In[214]:


transaction


# In[215]:


transaction['Brands'] = transaction.PROD_NAME.str.extract(r'(\w+)\s',expand = True)


# In[219]:


transaction


# In[220]:


transaction.Brands.value_counts()


# In[222]:


transaction.Brands.replace({'Red':'RRD',"Smith":"Smiths"}, inplace =True)


# In[223]:


transaction.Brands.value_counts()


# In[225]:


purchase.dtypes


# In[226]:


purchase.head()


# In[227]:


purchase.LIFESTAGE.value_counts()


# In[228]:


purchase.PREMIUM_CUSTOMER.value_counts()


# In[229]:


data = transaction.merge(purchase, how='left', on='LYLTY_CARD_NBR')


# In[230]:


data


# In[231]:


data.isnull().sum()


# In[232]:


data.to_csv("QVI_data.csv")


# In[238]:


plt.rcParams["figure.figsize"] = (20,8)
data.groupby(['LIFESTAGE','PREMIUM_CUSTOMER'])['TOT_SALES'].sum().sort_values(ascending=False).plot(kind='bar')


# In[242]:


plt.rcParams["figure.figsize"] = (20,8)
data.groupby(['LIFESTAGE','PREMIUM_CUSTOMER'])['LYLTY_CARD_NBR'].count().sort_values(ascending=False).plot(kind='bar')


# In[262]:


plt.rcParams["figure.figsize"] = (20,8)
data.groupby(['LIFESTAGE','PREMIUM_CUSTOMER'])['PROD_QTY'].mean().sort_values(ascending=False).plot(kind='bar')


# In[265]:


plt.rcParams["figure.figsize"] = (20,8)
data.groupby(['LIFESTAGE','PREMIUM_CUSTOMER'])['TOT_SALES'].mean().sort_values(ascending=False).plot(kind='bar')


# In[269]:


import scipy.stats as stats


# In[276]:


grp_1 = data[(data['PREMIUM_CUSTOMER']=='Mainstream')&((data['LIFESTAGE'] == 'YOUNG SINGLES/COUPLES')|(data['LIFESTAGE'] == 'MIDAGE SINGLES/COUPLES'))]
grp_2 = data[((data['PREMIUM_CUSTOMER']=='Premium')|(data['PREMIUM_CUSTOMER']=='Budget'))&((data['LIFESTAGE'] == 'YOUNG SINGLES/COUPLES')|(data['LIFESTAGE'] == 'MIDAGE SINGLES/COUPLES'))]


# In[283]:


result = stats.ttest_ind(grp_1['TOT_SALES'],grp_2['TOT_SALES'])


# In[284]:


result


# In[ ]:


#The t-test results in a p-value of 1.9916804791117584e-239, i.e. the unit price for mainstream,
#young and mid-age singles and couples ARE significantly higher than
#that of budget or premium, young and midage singles and couples.


# In[287]:


from mlxtend.frequent_patterns import apriori, association_rules


# In[309]:


analysis = (data[(data['LIFESTAGE'] == 'YOUNG SINGLES/COUPLES')&(data['PREMIUM_CUSTOMER'] == 'Mainstream')]
          .groupby(['LYLTY_CARD_NBR'])['TOT_SALES']
          .sum().reset_index().set_index('LYLTY_CARD_NBR'))


# In[310]:


def hot_encode(x):
    if(x<= 0):
        return 0
    if(x>= 1):
        return 1


# In[311]:


res = analysis.applymap(hot_encode)


# In[312]:


# Building the model
frq_items = apriori(res, min_support = 0.05, use_colnames = True)
  
# Collecting the inferred rules in a dataframe
rules = association_rules(frq_items, metric ="lift", min_threshold = 1)
rules = rules.sort_values(['confidence', 'lift'], ascending =[False, False])
print(rules.head())


# In[ ]:




