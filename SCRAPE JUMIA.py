#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json, re


# In[2]:


url = "https://raw.githubusercontent.com/annexare/Countries/master/data/countries.json"
req = requests.get(url)


# In[5]:


data = json.loads(req.text)


# In[7]:


data = pd.DataFrame(data)


# In[12]:


json_file = data.T.reset_index()


# In[13]:


json_file


# In[14]:


json_file.rename(columns={"index":"Country_Code"},inplace = True)


# In[15]:


json_file


# In[48]:


json_file.to_json("jjj.json")


# In[17]:


urls = "https://www.jumia.com.ng/phones-tablets/?page=3#catalog-listing"
r = requests.get(urls)


# In[18]:


from bs4 import BeautifulSoup as soup


# In[ ]:


#html5lib or lxml  used to grab html contents


# In[19]:


import lxml


# In[20]:


content = soup(r.content, 'lxml')


# In[ ]:


#find and find_all function


# In[28]:


data = content.find("div",class_="-paxs row _no-g _4cl-3cm-shs")
details = content.find("div",class_="info")
details.text


# In[29]:


h3 = content.find('h3').text
h3


# In[30]:


pr = content.find("div",class_="prc").text
pr


# In[33]:


name = []
price = []
for a in content.find_all("div",class_="-paxs row _no-g _4cl-3cm-shs"):
    for b in a.find_all("article",class_="prd _fb col c-prd"):
        name.append(b.find('h3').text)
        price.append(b.find("div",class_="prc").text)
df = pd.DataFrame({"Name":name,"Price":price})


# In[34]:


df


# In[36]:


Title = []
Price = []
for page in range(1,6):
    urls = "https://www.jumia.com.ng/phones-tablets/?page="+str(page)+"#catalog-listing"
    r = requests.get(urls)
    content = soup(r.content, 'lxml')
    for a in content.find_all("div",class_="-paxs row _no-g _4cl-3cm-shs"):
        for b in a.find_all("article",class_="prd _fb col c-prd"):
            Title.append(b.find('h3').text)
            Price.append(b.find("div",class_="prc").text)
df = pd.DataFrame({"Name":Title,"Price":Price})


# In[37]:


df


# In[39]:


df.to_excel("file.xlsx")


# In[43]:


df["Price"] = df["Price"].replace({'\₦':'',',':''}, regex=True).astype(int)


# In[44]:


df


# In[45]:


df.dtypes


# In[46]:


get_ipython().system('pip install --upgrade certifi')


# In[49]:


pip install xelatex


# In[ ]:




