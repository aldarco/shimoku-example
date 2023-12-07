#!/usr/bin/env python
# coding: utf-8


# The code of this script wa initially developed in a notebook
# then the plots in here are commented/omitted

# # Example code usinf shimoku SDK
# This Jupyter notebook was run using Windows subsystem for Linux sice there were some dependencies for shimoku_api_python that could not be installed on Windows directly.

# In[1]:


from os import getenv
import shimoku_api_python as Shimoku


# In[2]:





# In[3]:


import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np


# using the values directly insead of system variables
access_token = "ae095c1d-4620-44d6-9314-9752db105df3"      #getenv('SHIMOKU_TOKEN')
universe_id: str = "0d2e9d92-7f6a-44d6-9542-ef642f264bfc"  #getenv('UNIVERSE_ID')
workspace_id: str = "2af107a6-6e0d-4a07-aaff-9240a13ece3e" #getenv('WORKSPACE_ID')

s = Shimoku.Client(
    access_token=access_token,
    universe_id=universe_id,
)
s.set_workspace(uuid=workspace_id)

# In[4]:


plt.rcParams["figure.figsize"] = (8,6)
plt.rcParams["font.size"] = 12


# ## Data from Githhub using pandas
# The data consists of a bunch of scores (points) assigned to several brands of coffee from diffrent countries, and also include some features like flavour, altitude color etc

# In[5]:


url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-07-07/coffee_ratings.csv"
df = pd.read_csv(url, sep=",", on_bad_lines="skip") # some badlines are skipped


# In[6]:


print("Dataframe shape:", df.shape)
#df[df.columns].head()


# In[7]:


df["processing_method"].unique()


# In[8]:


mean_score_by_country = df.groupby(by="country_of_origin")[["total_cup_points", "acidity"]].mean()


# ### Analyzing the total scores by averaging the participants for countries

# In[9]:


#fig = plt.figure(figsize=(12,6))
#mean_score_by_country.plot(kind="bar")


# In[10]:


# sorting descendent way
mean_score_by_country.sort_values(by="total_cup_points",axis=0, ascending=False, inplace=True )


# In[11]:


#mean_score_by_country.plot(y="total_cup_points", kind="bar")#,logy=True)


# In[12]:


df.columns


# In[13]:


mean_score_flavor = df.groupby(by="country_of_origin")[["total_cup_points", "flavor", "acidity"]].mean()
mean_score_flavor.sort_values(by="total_cup_points",axis=0, ascending=False, inplace=True )


# In[14]:


#fig = plt.figure(figsize=(12,6))
#mean_score_flavor.plot(y=["total_cup_points", "flavor", "acidity"], kind="bar")
mean_score_flavor.head()


# ### Removing outliers

# In[15]:

#fig = plt.figure()
#df.plot(x="total_cup_points", y="altitude_mean_meters", kind="scatter")
#plt.ylim(0,10000)


# In[16]:


df_clean = df[(df["altitude_mean_meters"] < 10000) & (df["total_cup_points"] > 0)]


# ### Correlation between score and mean altitude

# In[17]:

#plt.figure()
#df_clean.plot(x="total_cup_points", y="altitude_mean_meters", c=df_clean["flavor"],kind="scatter", linewidth=1, edgecolor="k", s=30, colorbar=True)
#ax = plt.gcf()
#ax.get_axes()[1].set_ylabel("Flavor")


# #### Grouping by country

# In[18]:


df_clean_country_mean = df.groupby(by="country_of_origin",as_index=False)[["total_cup_points", "acidity","flavor", "altitude_mean_meters"]].mean()


# In[27]:


df_clean_country_mean


# ##### Direct relation between total points and the flavour score

# In[20]:

#plt.figure()
#df_clean.plot(y="total_cup_points", x="flavor", kind="scatter", linewidth=1, edgecolor="k", s=30)


# #### Brands per country

# In[21]:


country_participations =df_clean["country_of_origin"].value_counts()

#country_participations.plot(kind = "bar")


# In[22]:


country_participations = pd.DataFrame(country_participations).reset_index()
country_participations.head()


# In[23]:


df_peru = df_clean[df_clean["country_of_origin"]=="Peru"]
df_peru


# #### Loading to Shimoku dashboard

# In[33]:


# coffee board
s.set_board('Coffee Rank Board')

s.set_menu_path('catalog', 'bar-example')
s.plt.bar(
    data=df_clean_country_mean[['country_of_origin','acidity', "flavor"]],
    y=['acidity', "flavor"],
    order=0, title='Acidity and flavor by country',
     x='country_of_origin',
    y_axis_name="Grade",
    x_axis_name="Country"
)
s.pop_out_of_menu_path()

# catalog of 

# points by country
s.set_menu_path('catalog', 'Scores')
s.plt.bar(
    data=df_clean_country_mean.sort_values(by="total_cup_points", ascending=False),
    y=['total_cup_points'],
    order=0, title='Mean points by coutry',
     x='country_of_origin',
    y_axis_name="Total points",
    x_axis_name="Country"
)

# number of participants by country
s.set_menu_path('catalog', 'Participats by country')
s.plt.bar(
        data=country_participations[["count","country_of_origin"]], y="count",x=["country_of_origin"],
        x_axis_name='Number of participants',
        order=0, show_values=["count"]
    )


# flavour influence in total points
# correlation
s.set_menu_path('catalog', 'Flavour predominance in total points')
s.plt.scatter(
    point_fields=[( "flavor" ,"total_cup_points")],
    data=df_clean[["total_cup_points", "flavor"]],
    order=0, title='Flavour predominance in total points',
     
    x_axis_name="Flavor",
    y_axis_name="Total points"

)

# correlation between the altitude and  flavour
s.set_menu_path('catalog', 'Correlation: Flavour-Altitude')
s.plt.scatter(
    point_fields=[("altitude_mean_meters",'flavor')],
    data=df_clean[["altitude_mean_meters",'flavor']],
    order=0, title='Flavor and mean altitude',
    y_axis_name="Flavor",
    x_axis_name="Mean altitude (m)"
)



# In[30]:


df_clean[['acidity', "flavor"]]


# In[ ]:




