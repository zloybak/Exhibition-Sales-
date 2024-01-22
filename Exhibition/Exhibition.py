from logging import Manager
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

#change the directory 
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)


df = pd.read_excel(r"data\exhibition_EU_clients1.xlsx")

# ---- MAINPAGE ----
st.title(":bar_chart: Exhibition Sales Dashboard")
st.markdown("##")

# CREATE Side Filter Sales Manager
st.sidebar.header('Choose your filter: ')
staff = st.sidebar.multiselect('Sales Manager', df['Sales Manager'].unique())
if staff:
    df = df[df['Sales Manager'].isin(staff)]
    
year = st.sidebar.multiselect('Year', df['Year'].unique())
if year:
    df = df[df['Year'].isin(year)]

# TOP KPI's
total_sales = int(df["Sales Amount"].sum())
average_rating = round(df["Success Rate"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df["Sales Amount"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Total Sales:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
   print()
with right_column:
    st.subheader("Average Rating:")
    st.subheader(f"{average_rating} {star_rating}")

st.markdown("""---""")

# Create charts

# 1. Bar chart
fig1 = px.bar(df, y='Exhibition Type', x='Sales Amount', color='Exhibition Type', height=500,
              category_orders={"Exhibition Type": df.groupby("Exhibition Type")["Sales Amount"].sum().sort_values(ascending=False).index})
fig1.update_layout(xaxis_title='Total Sales', yaxis_title='Category', title='Sales by Each Manager')

# 2. Bar chart
fig2 = px.bar(df, x='Sales Manager', y='Sales Amount', color='Sales Manager', height=500,
              category_orders={"Sales Manager": df.groupby("Sales Manager")["Sales Amount"].sum().sort_values(ascending=False).index})
fig2.update_layout(xaxis_title='Sales Staff', yaxis_title='Total Sales', title='Sales by Each Manager')

# 3. Line graph
df_yearly = df.groupby('Year')['Sales Amount'].sum()
fig_line = px.line(df_yearly, x=df_yearly.index, y='Sales Amount', markers=True, title='Yearly Total Sales')
fig_line.update_layout(xaxis_title='Year', yaxis_title='Total Sales')

# 4. Donut chart
fig_donut = px.pie(df, names='Customer Country', values='Sales Amount', hole=0.5)
fig_donut.update_traces(textinfo='percent+label', pull=0.1)

#Display charts

st.subheader("Sales Distribution by Exhibition Type:")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Sales by Each Manager:")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Sales by years:")
st.plotly_chart(fig_line, use_container_width=True)

st.subheader("Sales Distribution by Customer Country:")
st.plotly_chart(fig_donut, use_container_width=True)