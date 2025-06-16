import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# --- إعداد الصفحة ---
st.set_page_config(layout="wide", page_title="لوحة مبيعات الفنار")

# --- التحديث التلقائي كل 60 ثانية ---
refresh_interval = 60 * 1000  # 60 ثانية
count = st_autorefresh(interval=refresh_interval, key="refresh")

# --- تحميل البيانات من Google Sheets مع معالجة الأخطاء ---
@st.cache_data(ttl=60)
def load_data():
    try:
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSr1bKG318tXo1PSOR7yHBWUjwu0Ca60zjHiCA_ryzt7Bo2zcVHrplms1DQBQjXj5Yw7ssAymZEOeYe/pub?gid=0&single=true&output=csv"
        df = pd.read_csv(url)
        df['التاريخ'] = pd.to_datetime(df['التاريخ'], errors='coerce')
        df = df.dropna(subset=['التاريخ'])
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
        return pd.DataFrame(columns=['التاريخ', 'المبيعات'])

df = load_data()

# --- الشعار ---
logo_url = "https://raw.githubusercontent.com/alfanar255/Sales-dashboard/main/company_logo2.png"
st.image(logo_url, width=120)

# --- تحليل البيانات ---
today = pd.Timestamp.today().normalize()
df['اليوم'] = df['التاريخ'].dt.date

sales_today = df[df['اليوم'] == today.date()]['المبيعات'].sum()
sales_month = df[(df['التاريخ'].dt.month == today.month) & (df['التاريخ'].dt.year == today.year)]['المبيعات'].sum()
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
if not df.empty:
    st.line_chart(df.set_index('التاريخ')['المبيعات'])
else:
    st.warning("لا توجد بيانات متاحة لعرضها حالياً.")

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
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        width: 30%;
    }
    .metric-title {
        font-size: 24px;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 32px !important;
        color: #003366;
    }
    </style>
""", unsafe_allow_html=True)
