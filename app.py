import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- إعداد الصفحة ---
st.set_page_config(layout="wide", page_title="لوحة مبيعات الفنار")

# --- التحديث التلقائي كل 60 ثانية ---
refresh_interval = 60 * 1000  # 60 ثانية
count = st_autorefresh(interval=refresh_interval, key="refresh")

# --- تحميل البيانات من Google Sheets مع الكاش ---
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRz88_P5wG3NAxD1VXqDAAHU0Jm-lrr-lk8Ze1KO8p8iEIYiWw7PoHAvwhEYLs5YyzAbZt-JKd1pwkF/pubhtml?gid=0&single=true"
    df = pd.read_csv(url)
    df['التاريخ'] = pd.to_datetime(df['التاريخ'], errors='coerce')
    df = df.dropna(subset=['التاريخ'])
    return df

df = load_data()

# --- الشعار ---
logo_url = "https://raw.githubusercontent.com/alfanar255/Sales-dashboard/main/company_logo2.png"
st.image(logo_url, width=120)

# --- تحليل البيانات ---
today = pd.Timestamp.today().normalize()
df['اليوم'] = df['التاريخ'].dt.date

# --- المؤشرات الإجمالية ---
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

# --- تفاصيل المناديب ---
st.header("📊 أداء المناديب")

# بيانات اليوم لكل مندوب
daily = df[df['اليوم'] == today.date()].groupby('المندوب').agg({
    'المبيعات': 'sum',
    'التحصيل': 'sum',
    'تارقت المبيعات': 'sum',
    'تارقت التحصيل': 'sum'
}).reset_index()

st.subheader("مبيعات وتحصيل اليوم")
if not daily.empty:
    daily['فرق المبيعات عن التارقت'] = daily['المبيعات'] - daily['تارقت المبيعات']
    daily['فرق التحصيل عن التارقت'] = daily['التحصيل'] - daily['تارقت التحصيل']
    st.dataframe(daily.style.format({
        'المبيعات': '{:,.0f}',
        'التحصيل': '{:,.0f}',
        'تارقت المبيعات': '{:,.0f}',
        'تارقت التحصيل': '{:,.0f}',
        'فرق المبيعات عن التارقت': '{:,.0f}',
        'فرق التحصيل عن التارقت': '{:,.0f}',
    }))
else:
    st.warning("لا توجد بيانات متاحة لليوم.")

# بيانات الشهر لكل مندوب
monthly = df[df['التاريخ'].dt.month == today.month].groupby('المندوب').agg({
    'المبيعات': 'sum',
    'التحصيل': 'sum',
    'تارقت المبيعات': 'sum',
    'تارقت التحصيل': 'sum'
}).reset_index()

st.subheader("مبيعات وتحصيل الشهر")
if not monthly.empty:
    monthly['فرق المبيعات عن التارقت'] = monthly['المبيعات'] - monthly['تارقت المبيعات']
    monthly['فرق التحصيل عن التارقت'] = monthly['التحصيل'] - monthly['تارقت التحصيل']
    st.dataframe(monthly.style.format({
        'المبيعات': '{:,.0f}',
        'التحصيل': '{:,.0f}',
        'تارقت المبيعات': '{:,.0f}',
        'تارقت التحصيل': '{:,.0f}',
        'فرق المبيعات عن التارقت': '{:,.0f}',
        'فرق التحصيل عن التارقت': '{:,.0f}',
    }))
else:
    st.warning("لا توجد بيانات متاحة لهذا الشهر.")

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
