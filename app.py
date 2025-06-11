import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعداد  الصفحة ---
st.set_page_config(layout="wide", page_title="لوحة مبيعات الفنار")

# --- تحميل البيانات ---
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSr1bKG318tXo1PSOR7yHBWUjwu0Ca60zjHiCA_ryzt7Bo2zcVHrplms1DQBQjXj5Yw7ssAymZEOeYe/pub?gid=0&single=true&output=csv"
    df = pd.read_csv(url)
    df['التاريخ'] = pd.to_datetime(df['التاريخ'])
    return df

df = load_data()

# --- إضافة الشعار واسم الشركة ---
col1, col2 = st.columns([1, 9])
with col1:
    st.image("company_logo.png.png", width=100)
with col2:
    st.markdown("""
        <h1 style='font-size: 50px; color: #0059b3; margin-bottom: 0;'>شركة الفنار لتوزيع الأدوية</h1>
        <h4 style='color: gray;'>لوحة المبيعات اليومية والتراكمية</h4>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- تحليل البيانات ---
today = pd.Timestamp.today().normalize()
df['اليوم'] = df['التاريخ'].dt.date

# مبيعات اليوم
sales_today = df[df['اليوم'] == today.date()]['المبيعات'].sum()

# مبيعات الشهر
sales_month = df[df['التاريخ'].dt.month == today.month]['المبيعات'].sum()

# إجمالي المبيعات
total_sales = df['المبيعات'].sum()

# --- عرض النتائج ---
col1, col2, col3 = st.columns(3)
col1.metric("📅 مبيعات اليوم", f"{sales_today:,.0f} ريال")
col2.metric("🗓️ مبيعات الشهر", f"{sales_month:,.0f} ريال")
col3.metric("💰 إجمالي المبيعات", f"{total_sales:,.0f} ريال")

st.markdown("---")

# --- رسم بياني خطي ---
st.line_chart(df.set_index('التاريخ')['المبيعات'])
