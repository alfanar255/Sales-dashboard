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
        url = "رابط ملف Google Sheet بعد تعديله"
        df = pd.read_csv(url)
        df['التاريخ'] = pd.to_datetime(df['التاريخ'], errors='coerce')
        df = df.dropna(subset=['التاريخ'])
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
        return pd.DataFrame(columns=['التاريخ', 'المندوب', 'المبيعات', 'التحصيل', 'تارقت المبيعات', 'تارقت التحصيل'])

df = load_data()

# --- تحليل البيانات ---
today = pd.Timestamp.today().normalize()
df['اليوم'] = df['التاريخ'].dt.date

# حساب إجماليات اليوم
sales_today = df[df['اليوم'] == today.date()]['المبيعات'].sum()
collection_today = df[df['اليوم'] == today.date()]['التحصيل'].sum()

# حساب إجماليات الشهر
sales_month = df[(df['التاريخ'].dt.month == today.month) & (df['التاريخ'].dt.year == today.year)]['المبيعات'].sum()
collection_month = df[(df['التاريخ'].dt.month == today.month) & (df['التاريخ'].dt.year == today.year)]['التحصيل'].sum()

# إجمالي المبيعات والتحصيل الكلي
total_sales = df['المبيعات'].sum()
total_collection = df['التحصيل'].sum()

# --- العنوان ---
st.markdown("""
    <div style="text-align: center; margin-top: -60px;">
        <h1 style='font-size: 50px; color: #0059b3;'>شركة الفنار لتوزيع الأدوية</h1>
        <h4 style='color: gray;'>لوحة متابعة المبيعات والتحصيل</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- المؤشرات العامة ---
st.markdown(f"""
    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-title">📅 مبيعات اليوم</div>
            <div class="metric-value">{sales_today:,.0f} جنيه</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">📅 تحصيل اليوم</div>
            <div class="metric-value">{collection_today:,.0f} جنيه</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">🗓️ مبيعات الشهر</div>
            <div class="metric-value">{sales_month:,.0f} جنيه</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">🗓️ تحصيل الشهر</div>
            <div class="metric-value">{collection_month:,.0f} جنيه</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">💰 إجمالي المبيعات</div>
            <div class="metric-value">{total_sales:,.0f} جنيه</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">💰 إجمالي التحصيل</div>
            <div class="metric-value">{total_collection:,.0f} جنيه</div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- بيانات المناديب اليومية ---
st.subheader("📊 تفاصيل المناديب - بيانات اليوم")

daily = df[df['اليوم'] == today.date()].groupby('المندوب').agg({
    'المبيعات': 'sum',
    'التحصيل': 'sum',
    'تارقت المبيعات': 'sum',
    'تارقت التحصيل': 'sum'
}).reset_index()

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

st.markdown("---")

# --- بيانات المناديب الشهرية ---
st.subheader("📊 تفاصيل المناديب - بيانات الشهر")

monthly = df[(df['التاريخ'].dt.month == today.month) & (df['التاريخ'].dt.year == today.year)].groupby('المندوب').agg({
    'المبيعات': 'sum',
    'التحصيل': 'sum',
    'تارقت المبيعات': 'sum',
    'تارقت التحصيل': 'sum'
}).reset_index()

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
        flex-wrap: wrap;
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
        margin-bottom: 20px;
    }
    .metric-title {
        font-size: 22px;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 28px !important;
        color: #003366;
    }
    </style>
""", unsafe_allow_html=True)
