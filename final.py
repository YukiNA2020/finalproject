from statistics import median_grouped
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.style.use('seaborn')
st.title("The nobel price ")
df_date = pd.read_csv('nobel_prizes_by_date.csv')
df_winner = pd.read_csv('nobel_prize_by_winner.csv')


#处理csv
#df_date.drop(['index', 'overallMotivation',"share"], axis=1, inplace=True)
#df_date = df_date[df_date.firstname.notnull()].copy()
#organisations = df_date[df_date.gender == 'org'].copy()
#df_date = df_date[df_date.gender != 'org'].copy()

#排序赋值
df_winner=df_winner.sort_values(by='id',ascending=True)
df_date=df_date.sort_values(by='id',ascending=True)
df_winner['date']=df_date['year']
df_winner.dropna(subset=['born','firstname'],inplace=True)
df_result= df_winner
df_result = df_result.drop(['index','died','bornCountryCode','bornCity','diedCountryCode','diedCity','share','overallMotivation','name','bornCountry','diedCountry'],axis=1)
df_result

#左边选择框
subject_filter = st.sidebar.multiselect(
     'choose the price type',
     df_winner.category.unique(),  # options
     df_winner.category.unique()) 
df_winner = df_winner[df_winner.category.isin(subject_filter)]
df_result = df_result[df_result.category.isin(subject_filter)]

#上方拉条
pop_filter = st.slider('the year of getting the prize',1901,2016,1945)
df_winner = df_winner[df_winner['year'] <= pop_filter]
df_result = df_result[df_result['year'] <= pop_filter]

#显示国家
st.subheader('the country of the winner')
country = df_winner.country.value_counts()
fig ,ax=plt.subplots()
ax.set_xlabel('Countries',fontsize=10)
ax.set_ylabel('number of person/team',fontsize=10)
country.plot.bar()
st.pyplot(fig)

#显示学科
st.subheader('the subject of the winner')
fig, ax = plt.subplots()
colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, 6))
category = df_winner.category.value_counts()
pie_result = df_winner.category.value_counts()
ax.pie(category, labels = pie_result.index, autopct='%3.1f%%',colors=colors, radius=3, center=(4, 4),       wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True)
st.pyplot(fig)

#显示年龄
st.subheader('the age of the getting award')
df_result['born'] = pd.to_datetime(df_result['born'])
df_result['birth_year'] = df_result.born.dt.year
df_result['awarded_at'] = df_result['year'] - df_result['birth_year']
fig ,ax=plt.subplots(1,2)
df_result.awarded_at.hist(ax=ax[0],bins=15)
ax[0].set_xlabel('age')
ax[0].set_ylabel('the numeber')
df_result.awarded_at.plot.box(ax=ax[1])
st.pyplot(fig)