import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- إعداد الصفحة ---
st.set_page_config(layout="wide", page_title="لوحة مبيعات الفنار")

# --- تفعيل التحديث التلقائي كل 60 ثانية ---
refresh_interval = 60 * 1000  # 60 ثانية
count = st_autorefresh(interval=refresh_interval, key="refresh")

# --- تحميل البيانات من Google Sheets ---
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSr1bKG318tXo1PSOR7yHBWUjwu0Ca60zjHiCA_ryzt7Bo2zcVHrplms1DQBQjXj5Yw7ssAymZEOeYe/pub?gid=0&single=true&output=csv"
    df = pd.read_csv(url)
    df['التاريخ'] = pd.to_datetime(df['التاريخ'])
    return df

# --- حذف الكاش عند كل تحديث تلقائي (عدا أول مرة) ---
if count != 0:
    load_data.clear()

# --- تحميل البيانات ---
df = load_data()

# --- الشعار ---
logo_url = "https://raw.githubusercontent.com/alfanar255/Sales-dashboard/main/company_logo2.png"
st.image(logo_url, width=120)

# --- تحليل البيانات ---
today = pd.Timestamp.today().normalize()
df['اليوم'] = df['التاريخ'].dt.date

sales_today = df[df['اليوم'] == today.date()]['المبيعات'].sum()
sales_month = df[df['التاريخ'].dt.month == today.month]['المبيعات'].sum()
total_sales = df['المبيعات'].sum()

# --- العنوان ---
st.markdown("""
    <div style="text-align: center; margin-top: -60px;">
        <h1 style='font-size: 50px; color: #0059b3;'>شركة الفنار لتوزيع الأدوية</h1>
        <h4 style='color: gray;'>لوحة المبيعات اليومية والتراكمية</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- مؤشرات المبيعات ---
st.markdown(f"""
    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-title">📅 مبيعات اليوم</div>
            <div class="metric-value">{sales_today:,.0f} جنيه</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">🗓️ مبيعات الشهر</div>
            <div class="metric-value">{sales_month:,.0f} جنيه</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">💰 إجمالي المبيعات</div>
            <div class="metric-value">{total_sales:,.0f} جنيه</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- الرسم البياني ---
st.line_chart(df.set_index('التاريخ')['المبيعات'])

st.markdown("---")

# --- تنسيق CSS ---
st.markdown("""
    <style>
    .metric-container {
        display: flex;
        justify-content: space-around;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .metric-box {
        text-align: center;
        font-weight: bold;
        color: #0066cc;
    }
    .metric-title {
        font-size: 24px;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 30px !important;
    }
    </style>
""", unsafe_allow_html=True)
