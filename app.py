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

# --- رابط الشعار من GitHub (استبدله برابطك الحقيقي) ---
logo_url = "https://raw.githubusercontent.com/alfanar255/Sales-dashboard/main/company_logo2.png"
st.image(logo_url, width=120)

# --- عرض الشعار والعنوان ---
st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="flex: 1; text-align: right;">
            <img src="{logo_url}" width="120" />
        </div>
        <div style="flex: 2; text-align: center;">
            <h1 style='font-size: 50px; color: #0059b3; margin-bottom: 5px;'>شركة الفنار لتوزيع الأدوية</h1>
            <h4 style='color: gray;'>لوحة المبيعات اليومية والتراكمية</h4>
        </div>
        <div style="flex: 1;"></div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- عرض المؤشرات (العناوين في صف، والقيم في صف أسفلها) ---
st.markdown("""
    <style>
    .metric-row {{
        display: flex;
        justify-content: space-around;
        text-align: center;
        margin-top: 10px;
        margin-bottom: 0;
    }}
    .metric-title {{
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }}
    .metric-value {{
        font-size: 30px;
        font-weight: bold;
        color: #0066cc;
        margin-top: 5px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- صف العناوين ---
st.markdown("""
    <div class="metric-row">
        <div class="metric-title">📅 مبيعات اليوم</div>
        <div class="metric-title">🗓️ مبيعات الشهر</div>
        <div class="metric-title">💰 إجمالي المبيعات</div>
    </div>
""", unsafe_allow_html=True)

# --- صف القيم ---
st.markdown(f"""
    <div class="metric-row">
        <div class="metric-value">{sales_today:,.0f} ريال</div>
        <div class="metric-value">{sales_month:,.0f} ريال</div>
        <div class="metric-value">{total_sales:,.0f} ريال</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- الرسم البياني الزمني ---
st.line_chart(df.set_index('التاريخ')['المبيعات'])
