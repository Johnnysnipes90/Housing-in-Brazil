#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt


# # In this Project, We'll work with a dataset of homes for sale in Brazil. Our goal is to determine if there are regional differences in the real estate market. Also, we will look at southern Brazil to see if there is a relationship between home size and price.

# ## In the data directory for this project there are two CSV that we need to import and clean, one-by-one.

# ## Import
# First, we are going to import and clean the data in data/brasil-real-estate-1.xlsx.

# In[34]:


df1 = pd.read_excel('brasil-real-estate-1.xlsx')
df1.head()


# In[35]:


df1.drop(columns = ['Unnamed: 0'], inplace = True)


# In[36]:


df1.info()
df1.head()


# ## Data Cleaning

# Drop all NaN
# from what we noticed using df1.head() we can see that only the 'lat-lon' has missing data and there are not many therefore we just drop all rows with missing data

# In[37]:


df1.isna().sum()


# In[38]:


# Because of the type of column this is we cannot do any imputation on it other than dropping the NaN columns
df1.dropna(inplace = True)
df1.isna().sum()


# Use the "lat-lon" column to create two separate columns in df1: "lat" and "lon". And we make sure that the data type for these new columns is float.

# In[39]:


df1[['lat', 'lon']] = df1['lat-lon'].str.split(',', expand=True).astype(float)
df1.head()


# Use the "place_with_parent_names" column to create a "state" column for df1. (Note that the state name always appears after "|Brasil|" in each string.)

# In[40]:


df1['state'] = df1[
    'place_with_parent_names'
]   .str.split(
    '|', expand = True
)[2]

df1.info()
df1.head()


# Drop the two columns that are not useful anymore 'place_with_parent_names' and 'lat-lon'

# In[41]:


df1.drop(
    columns = ['lat-lon', 'place_with_parent_names'], inplace = True
)


# We noticed that 'price_usd' column is in object data type instead of float therefore we Transform the "price_usd" column of df1 so that all values are floating-point numbers instead of strings

# df1['price_usd'] = (
#     df1['price_usd']
#     .str.replace('$', '', regex=False)
#     .str.replace(',', '')
#     .astype(float)
# )
# 
# df1.head()

# Now that we have cleaned data/brasil-real-estate-1.xlsx and created df1, you are going to import and clean the data from the second file, brasil-real-estate-2.xlsx.

# ### Import the CSV file brasil-real-estate-2.xlsx into the DataFrame df2

# In[47]:


df2 = pd.read_excel('brasil-real-estate-twoo.xlsx')


# In[48]:


df2.info()
df2.head()


# In[49]:


df2.drop(columns = ['Unnamed: 0'], inplace = True)
df2.info()
df2.head()


# We know that we want the price to be in USD just like the df1. We will use the "price_brl" column to create a new column named "price_usd". (Keep in mind that, when this data was collected in 2015 and 2016, a US dollar cost 3.19 Brazilian reals.)

# In[50]:


df2['price_usd'] = (df2['price_brl'] / 3.19)
df2.head()


# Drop the "price_brl" column from df2 since we won't be needing it anymore, as well as any rows that have NaN values.

# In[51]:


df2.drop(columns = ['price_brl'], inplace = True)
df2.dropna(inplace = True)


# In[52]:


df2.info()
df2.head()


# ### Now that we've cleaned the data from both CSV files and created df1 and df2, it's time to combine them into a single DataFrame.

# Concatenate df1 and df2 to create a new DataFrame named df

# In[53]:


df = pd.concat([df1, df2])


# # EXPLORATORY DATA ANALYSIS
# After importing, the next step in many data science projects is exploratory data analysis (EDA), where we get a feel for our data by summarizing its main characteristics using descriptive statistics and data visualization. A good way to plan our EDA is by looking each column and asking ourselves questions what it says about our dataset.

# In[54]:


df.info()
df.head()


# create a scatter_mapbox showing the location of the properties in df.

# In[56]:


# Use plotly express to create figure
fig = px.scatter_mapbox(
    df,
    lat='lat',
    lon= 'lon',
    center={"lat": -14.2, "lon": -51.9},  # Map will be centered on Brazil
    width=600,
    height=600,
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)

fig.update_layout(mapbox_style="open-street-map")

fig.show()


# Looking at this map, are the houses in our dataset distributed evenly throughout the country, or are there states or regions that are more prevalent? Can you guess where Mexico's biggest cities are based on this distribution?

# We want to use the describe method to create a DataFrame summary_stats with the summary statistics for the "area_m2" and "price_usd" columns

# In[57]:


summary_stats = df[['area_m2', 'price_usd']].describe()
summary_stats


# Create a histogram of "price_usd". Make sure that the x-axis has the label "Price [USD]", the y-axis has the label "Frequency", and the plot has the title "Distribution of Home Prices". Use Matplotlib (plt).

# In[58]:


# Build histogram
plt.hist(df['price_usd'])


# Label axes
plt.xlabel('Price [USD]')
plt.ylabel('Frequency')

# Add title
plt.title('Distribution of Home Prices')


# Create a horizontal boxplot of "area_m2". Make sure that the x-axis has the label "Area [sq meters]" and the plot has the title "Distribution of Home Sizes". Use Matplotlib (plt).

# In[34]:


plt.boxplot(df['area_m2'], vert = False)
plt.xlabel('Area [sq meters]')
plt.title('Distribution of Home Sizes')


# Use the groupby method to create a Series named mean_price_by_region that shows the mean home price in each region in Brazil, sorted from smallest to largest.

# In[38]:


mean_price_by_region = df.groupby('region')['price_usd'].mean().sort_values(ascending = False)
mean_price_by_region


# Use mean_price_by_region to create a bar chart. Make sure you label the x-axis as "Region" and the y-axis as "Mean Price [USD]", and give the chart the title "Mean Home Price by Region". Use pandas

# In[40]:


mean_price_by_region.plot(
    kind = 'bar',
    xlabel = 'Region',
    ylabel = 'Mean Price [USD]',
    title = 'Mean Home Price by Region'
);


# Create a DataFrame df_south that contains all the homes from df that are in the "South" region.

# In[42]:


df_south = df[df['region'] == 'South']
df_south.head()


# Use the value_counts method to create a Series homes_by_state that contains the number of properties in each state in df_south.

# In[43]:


homes_by_state = df_south['state'].value_counts()
homes_by_state


# Create a scatter plot showing price vs. area for the state in df_south that has the largest number of properties. Be sure to label the x-axis "Area [sq meters]" and the y-axis "Price [USD]"; and use the title "<name of state>: Price vs. Area". Use Matplotlib (plt).

# In[46]:


#Subset data
df_south_rgs = df_south[df_south['state'] == 'Rio Grande do Sul']

# Build scatter plot
plt.scatter(x= df_south_rgs['area_m2'], y = df_south_rgs['price_usd'])

# Label axes
plt.xlabel('Area [sq meters]')
plt.ylabel('Price [USD]')

# Add title
plt.title("Rio Grande do Sul: Price vs. Area");


# Create a dictionary south_states_corr, where the keys are the names of the three states in the "South" region of Brazil, and their associated values are the correlation coefficient between "area_m2" and "price_usd" in that state.

# In[48]:


df_south['area_m2'].corr(df_south['price_usd'])

#south_states_corr = {
#}


# In[49]:


# Step 1: Identify the states in the South region
south_states = df_south['state'].unique()

# Step 2: Calculate the correlation coefficient for each state
south_states_corr = {}
for state in south_states:
    df_state = df_south[df_south['state'] == state]
    corr = df_state['area_m2'].corr(df_state['price_usd'])
    south_states_corr[state] = corr

# Step 3: Display the dictionary
print(south_states_corr)


# In[ ]:




