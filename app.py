import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('startup.csv')
st.set_page_config(layout='wide',page_title='Startup Analysis')
df['date'] = pd.to_datetime(df['date'])
df['year']=df['date'].dt.year
df['month']=df['date'].dt.month

def load_investor_detail(investor):
    st.title(investor)
    # load the recent 5 investment
    investment_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','rounds','amount']]
    st.subheader('Recent 5 Investment')
    st.dataframe(investment_df)
    
    col1,col2 = st.columns(2)
    # Biggest investmen
    with col1:
        big_df = (df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum()).head()
        st.subheader("Biggest Investment")
        fig, ax = plt.subplots()
        ax.bar(big_df.index,big_df.values)

        st.pyplot(fig)
    with col2:
        area_of_interest = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader("sector invested")
        fig1, ax1 = plt.subplots()
        ax1.pie(area_of_interest,labels=area_of_interest.index,autopct='%0.01f%%')
        st.pyplot(fig1)
    col3,col4 = st.columns(2)
    with col3:
        area_of_interest = df[df['investors'].str.contains(investor)].groupby('rounds')['amount'].sum()
        st.subheader("stages")
        fig1, ax1 = plt.subplots()
        ax1.pie(area_of_interest,labels=area_of_interest.index,autopct='%0.01f%%')
        st.pyplot(fig1)
    with col4:
        investing_city = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum()
        st.subheader("city")
        fig2,ax2 = plt.subplots()
        ax2.pie(investing_city,labels=investing_city.index,autopct='%0.01f%%')
        st.pyplot(fig2)
    
    val = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader("Year wise investment")
    fig3,ax3 = plt.subplots()
    ax3.plot(val.index,val.values)
    st.pyplot(fig3)
    st.subheader('Similar investors')
    investments = df[df['investors'].str.contains(investor, case=False, na=False)]
    vertical = investments['vertical'].unique()
    similar_investors = df[df['vertical'].isin(vertical) & (-df['investors'].str.contains(investor))].groupby('investors')['vertical'].nunique().reset_index(name='overlap_count')
    similar_investors = similar_investors[similar_investors['overlap_count'] >2]
    val = similar_investors.sort_values(by='overlap_count',ascending=False)['investors']
    st.dataframe(val)

def load_startup_details(startup):
    st.title(startup)
    st.write('Investors',df[df['startup'] == startup]['investors'].unique())
    
    col1,col2 = st.columns(2)
    with col1:
        startup_funding = df[df['startup']==startup]
        st.write('Funding:',startup_funding['amount'].sum())
        st.write('Number of funding:',startup_funding['amount'].count())
        st.write('vertical:',startup_funding['vertical'].unique())
    with col2:
        startup_funding = df[df['startup']==startup]
        st.write('City:',startup_funding['city'].iloc[0])
        st.write('Number of Rounds:',startup_funding['rounds'].count())
        st.write('Rounds:',startup_funding['rounds'].unique())
    col3,col4 = st.columns(2)
    with col3:
        st.header('startup funding year by year')
        temp_df = df[df['startup']==startup]
        fig,ax = plt.subplots()
        ax.plot(temp_df['year'],temp_df['amount'])
        st.pyplot(fig)
    with col4:
        st.header('startup funding by rounds')
        temp_df = df[df['startup']==startup]
        fig,ax = plt.subplots()
        ax.plot(temp_df['rounds'],temp_df['amount'])
        st.pyplot(fig)
    st.header('investors amount')
    temp_df = df[df['startup']==startup].reset_index(drop=True)
    st.dataframe(temp_df[['investors','amount']])
        
def load_overall_analysis():
    st.title("Overall Analysis")  
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        total = round(df['amount'].sum())
        st.metric('Total',str(total)+'cr')
    with col2:
        max = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Max',str(max)+'cr')
    with col3:
        max = df.groupby('startup')['amount'].sum().mean()
        st.metric('Mean',str(max)+'cr')
    # total funded startup
    with col4:
        funded_startup = df['startup'].nunique()
        st.metric('funded startup',str(funded_startup))

    col5,col6 = st.columns(2)
    with col5:
        st.header('month on month graph')
        select_option = st.selectbox('Select type',['Total','Cost'])
        if select_option == 'Total':
            temp_df = df.groupby(['year','month'])['amount'].sum().reset_index()
        else:
            temp_df = df.groupby(['year','month'])['amount'].count().reset_index()

        temp_df['x-axis']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')    
        fig,ax = plt.subplots()
        ax.plot(temp_df['x-axis'],temp_df['amount'])
        st.pyplot(fig)
    with col6:
        st.header('startups in particular year')
        select_year = st.selectbox('Choose year',[2016,2017,2018,2019,2020])
        temp_year = df[df['year']==select_year]
        total_startups = temp_year.groupby('month')['startup'].count()
        monthly_data = total_startups.reset_index()
        fig1,ax1 = plt.subplots()
        ax1.plot(monthly_data['month'],monthly_data['startup'])
        st.pyplot(fig1)

    col7,col8 = st.columns(2)
    with col7:
        st.header('state wise fundings')
        states = df.groupby('city')['startup'].count()
        states = states.sort_values(ascending=False).head()
        fig2,ax2 = plt.subplots()
        ax2.pie(states,labels=states.index,autopct='%1.1f%%',startangle=90)
        st.pyplot(fig2)
    with col8:
        st.header('vertical behaviours')
        states = df.groupby('city')['startup'].count()
        states = states.sort_values(ascending=False).head()
        fig2,ax2 = plt.subplots()
        ax2.pie(states,labels=states.index,autopct='%1.1f%%',startangle=90)
        st.pyplot(fig2)

st.sidebar.title("startup funding analysis")

option = st.sidebar.selectbox('select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
        load_overall_analysis()
elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup',df['startup'].unique().tolist())
    bttn1 = st.sidebar.button("serch startup details")
    if bttn1:
        load_startup_details(selected_startup)
elif option == 'Investor':
    selected_investor = st.sidebar.selectbox('select startup',sorted(set(df['investors'].str.split(',').sum())))
    bttn2 = st.sidebar.button("serch investors details")
    if bttn2:
        load_investor_detail(selected_investor)



    