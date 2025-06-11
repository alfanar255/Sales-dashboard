import streamlit as st
import pandas as pd
from datetime import datetime

# --- إعداد الصفحة ---
st.set_page_config(layout="wide", page_title="لوحة مبيعات الفنار")

# --- تحميل البيانات من Google Sheets ---
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSr1bKG318tXo1PSOR7yHBWUjwu0Ca60zjHiCA_ryzt7Bo2zcVHrplms1DQBQjXj5Yw7ssAymZEOeYe/pub?gid=0&single=true&output=csv"
    df = pd.read_csv(url)
    df['التاريخ'] = pd.to_datetime(df['التاريخ'])
    return df

df = load_data()

# --- تحليل البيانات ---
today = pd.Timestamp.today().normalize()
df['اليوم'] = df['التاريخ'].dt.date

sales_today = df[df['اليوم'] == today.date()]['المبيعات'].sum()
sales_month = df[df['التاريخ'].dt.month == today.month]['المبيعات'].sum()
total_sales = df['المبيعات'].sum()

# --- عرض الشعار في اليمين، والعنوان في المنتصف ---
st.markdown("""
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="flex: 1;">
            <!-- شعار في اليمين -->
            <img src="company_logo.png" width="100" style="float: right;"/>
        </div>
        <div style="flex: 2; text-align: center;">
            <h1 style='font-size: 50px; color: #0059b3; margin-bottom: 5px;'>شركة الفنار لتوزيع الأدوية</h1>
            <h4 style='color: gray;'>لوحة المبيعات اليومية والتراكمية</h4>
        </div>
        <div style="flex: 1;">
            <!-- مسافة فارغة من اليسار -->
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- تنسيق الأرقام بخط كبير ---
st.markdown("""
    <style>
    .big-metric {
        font-size: 40px !important;
        font-weight: bold;
        color: #0066cc;
    }
    </style>
""", unsafe_allow_html=True)

# --- عرض المؤشرات ---
col1, col2, col3 = st.columns(3)
col1.markdown(f"<div class='big-metric'>📅 مبيعات اليوم: {sales_today:,.0f} ريال</div>", unsafe_allow_html=True)
col2.markdown(f"<div class='big-metric'>🗓️ مبيعات الشهر: {sales_month:,.0f} ريال</div>", unsafe_allow_html=True)
col3.markdown(f"<div class='big-metric'>💰 إجمالي المبيعات: {total_sales:,.0f} ريال</div>", unsafe_allow_html=True)

st.markdown("---")

# --- الرسم البياني الزمني ---
st.line_chart(df.set_index('التاريخ')['المبيعات'])
