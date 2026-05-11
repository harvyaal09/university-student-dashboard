import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title='University Dashboard',
    layout='wide'
)

st.title('University Student Analytics Dashboard')

@st.cache_data
def load_data():
    return pd.read_csv('university_student_data.csv')

df = load_data()

st.sidebar.header('Filters')

selected_year = st.sidebar.multiselect(
    'Select Year',
    options=df['Year'].unique(),
    default=df['Year'].unique()
)

selected_term = st.sidebar.multiselect(
    'Select Term',
    options=df['Term'].unique(),
    default=df['Term'].unique()
)

filtered_df = df[
    (df['Year'].isin(selected_year)) &
    (df['Term'].isin(selected_term))
]

col1, col2, col3 = st.columns(3)

col1.metric(
    'Total Applications',
    int(filtered_df['Applications'].sum())
)

col2.metric(
    'Average Retention',
    f"{filtered_df['Retention Rate (%)'].mean():.1f}%"
)

col3.metric(
    'Average Satisfaction',
    f"{filtered_df['Student Satisfaction (%)'].mean():.1f}%"
)

st.subheader('Retention Rate Trend')

retention = filtered_df.groupby('Year')['Retention Rate (%)'].mean()

fig, ax = plt.subplots()

ax.plot(
    retention.index,
    retention.values,
    marker='o'
)

ax.set_xlabel('Year')
ax.set_ylabel('Retention Rate (%)')

st.pyplot(fig)

st.subheader('Student Satisfaction by Year')

fig2, ax2 = plt.subplots()

sns.barplot(
    data=filtered_df,
    x='Year',
    y='Student Satisfaction (%)',
    ax=ax2
)

st.pyplot(fig2)

st.subheader('Enrollment by Department')

engineering = filtered_df['Engineering Enrolled'].sum()
business = filtered_df['Business Enrolled'].sum()
arts = filtered_df['Arts Enrolled'].sum()
science = filtered_df['Science Enrolled'].sum()

labels = ['Engineering', 'Business', 'Arts', 'Science']
values = [engineering, business, arts, science]

fig3, ax3 = plt.subplots()

ax3.pie(
    values,
    labels=labels,
    autopct='%1.1f%%'
)

st.pyplot(fig3)
