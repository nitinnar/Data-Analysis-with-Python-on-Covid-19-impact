#!/usr/bin/env python
# coding: utf-8

# In[38]:


## Importing the Libraries

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


# In[39]:


## Loading the dataframe

df = pd.read_csv('covid_19_clean_complete.csv')

df.head()


# In[40]:


## Configure visualization style

sns.set(style="whitegrid")
plt.rcParams["date.autoformatter.year"] = "%Y"


# In[41]:


## Set the plot size for better visuals

plt.figure(figsize=(12, 8))


# In[42]:


print("First 5 rows of the dataset:")
df.head()


# In[43]:


df.info()


# In[44]:


## Checking the number of rows

df.shape[0]


# In[45]:


## Identiyfing the null values

df[df.duplicated()]


# In[46]:


## Dropping the null values

df.drop_duplicates(inplace=True)


# In[47]:


## Checking the dataframe size

df.shape


# In[48]:


## Displaying the duplicate values removed or not

df[df.duplicated()]


# In[49]:


## Displaying the total count of null values against all columns

(df.isnull()).sum()


# In[50]:


## Displaying the null values from the State column

df[df['Province/State'].isnull()]


# In[51]:


## Displaying the states with not null values 

df[df['Province/State'].notnull()]


# In[52]:


## Unique countries over the dataset

df['Country/Region'].unique().tolist()


# In[53]:


## Total number of unique countries/ regions

len(df['Country/Region'].unique().tolist())


# In[54]:


df['WHO Region'].unique()


# In[55]:


df.head()


# In[56]:


## Converting the date column to date data type

df['Date'] = pd.to_datetime(df['Date'])
df.head()


# In[57]:


df['Date'].dt.year


# In[58]:


df['Confirmed'].diff().tolist()


# In[59]:


df['Daily_Confirmed'] = df['Confirmed'].diff()
df['Daily_Confirmed']


# In[60]:


df['Daily_Deaths'] = df['Deaths'].diff()
df['Daily_Deaths']


# In[64]:


df[df['Daily_Deaths'] >0]


# In[61]:


## Death counts in the Month of February

df[(df['Date'].dt.month == 2) & (df['Confirmed'] != 0)].sort_values(by=['Date','Daily_Confirmed'])


# In[65]:


## Aggregated sum by Country/ Region

df.groupby(['Country/Region','Date']).agg({'Confirmed' : 'sum', 'Deaths': 'sum', 'Recovered': 'sum'}).reset_index()


# In[66]:


## Top Countries with Highest Confirmed Covid-19 cases

df.groupby('Country/Region').agg({'Confirmed':'max'}).sort_values(by = 'Confirmed', ascending = False).head(10)


# In[67]:


## Top Countries with Highest Confirmed Covid-19 cases (Same query as above but with different functions)

pd.DataFrame(df.groupby('Country/Region')['Confirmed'].max().nlargest(10))


# In[68]:


## Grouping the cases count by countries and date

country_group = df.groupby(['Country/Region', 'Date']).agg({
    'Confirmed': 'sum',
    'Deaths': 'sum',
    'Recovered': 'sum',
}).reset_index()
country_group.head()


# In[69]:


## Filtering the data to analyze only top 10 countries

top_countries = country_group.groupby('Country/Region')['Confirmed'].max().nlargest(10).index.tolist()
top_countries


# In[135]:


country_group = country_group[country_group['Country/Region'].isin(top_countries)]
country_group


# In[137]:


## Line Chart to display the cases count for the top 10 countries over the time

top_countries_df = country_group[country_group['Country/Region'].isin(top_countries)]

plt.figure(figsize=(12, 8))
sns.lineplot(data=top_countries_df, x='Date', y='Confirmed', hue='Country/Region')
plt.title("Confirmed Cases in Top 10 Countries")
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[139]:


country_group['Daily_Recovery_Rate'] = country_group['Recovered'].diff().fillna(0) / country_group['Confirmed'].replace(0, np.nan)

country_group


# In[149]:


## Line Chart to display the recovery over the period for the top 10 countries

plt.figure(figsize=(12, 8))
sns.lineplot(data=country_group, x='Date', y='Recovered', hue='Country/Region')
plt.title("Daily Recovery Rate Across Top COVID-19 Affected Countries")
plt.xlabel('Date')
plt.ylabel('Recovery Rate')
plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[151]:


## Region wise analysis of deaths across major continents

df['Continent'] = df['Country/Region'].apply(lambda x: 'Europe' if x in ['Italy', 'Spain', 'Germany'] else
                                                    ('Asia' if x in ['China', 'India', 'Japan'] else
                                                    ('America' if x in ['USA', 'Brazil', 'Argentina'] else 'Others')))


# In[163]:


df.head()


# In[167]:


## Aggregate data by continent over time
continent_group_region = df.groupby(['Continent', 'Date']).agg({
    'Deaths': 'sum',
    'Confirmed':'sum',
    'Recovered':'sum',
}).reset_index()
continent_group_region


# In[169]:


## Visualize the death trends across regions

plt.figure(figsize=(12, 8))
sns.lineplot(data=continent_group_region, x='Date', y='Deaths', hue='Continent')
plt.title("Trends in Deaths by Continent")
plt.xlabel('Date')
plt.ylabel('Number of Deaths')
plt.legend(loc='upper left')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[173]:


## Statistical insights: Correlation Analysis

correlation_df = df[['Confirmed', 'Deaths', 'Recovered']].copy()
correlation_matrix = correlation_df.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.title("Correlation Matrix Between Confirmed, Deaths, and Recovered")
plt.show()


# In[193]:


avg_deaths = df.groupby('Date')['Confirmed'].mean().reset_index()

# Time Series plot for deaths
plt.figure(figsize=(12, 8))
sns.lineplot(data=avg_deaths, x='Date', y='Confirmed')
plt.title("Average Confirmed cases Per Month")
plt.xlabel('Date')
plt.ylabel('Average Number of Confirmed cases')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# In[ ]:




