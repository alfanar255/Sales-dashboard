import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="لوحة المبيعات", layout="wide")

SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSr1bKG318tXo1PSOR7yHBWUjwu0Ca60zjHiCA_ryzt7Bo2zcVHrplms1DQBQjXj5Yw7ssAymZEOeYe/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(SHEET_URL)
    df['التاريخ'] = pd.to_datetime(df['التاريخ'])
    return df

df = load_data()
today = pd.to_datetime(datetime.today().date())
month_start = today.replace(day=1)

daily_sales = df[df['التاريخ'] == today]['المبيعات'].sum()
monthly_sales = df[df['التاريخ'] >= month_start]['المبيعات'].sum()
total_sales = df['المبيعات'].sum()

st.title("📊 لوحة المبيعات")
st.markdown("### ✅ تحديث تلقائي كل 60 ثانية")

col1, col2, col3 = st.columns(3)
col1.metric("مبيعات اليوم", f"{daily_sales:,.0f} ريال")
col2.metric("مبيعات هذا الشهر", f"{monthly_sales:,.0f} ريال")
col3.metric("إجمالي المبيعات", f"{total_sales:,.0f} ريال")

daily_chart = df.groupby('التاريخ')['المبيعات'].sum().reset_index()
st.line_chart(daily_chart.rename(columns={'التاريخ': 'index'}).set_index('index'))
