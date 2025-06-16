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
        url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRz88_P5wG3NAxD1VXqDAAHU0Jm-lrr-lk8Ze1KO8p8iEIYiWw7PoHAvwhEYLs5YyzAbZt-JKd1pwkF/pub?gid=0&single=true&output=csv"
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

# حساب بيانات اليوم
daily = df[df['اليوم'] == today.date()].groupby('المندوب').agg({
    'المبيعات': 'sum',
    'التحصيل': 'sum',
    'تارقت المبيعات': 'sum',
    'تارقت التحصيل': 'sum'
}).reset_index()

# حساب بيانات الشهر
monthly = df[(df['التاريخ'].dt.month == today.month) & (df['التاريخ'].dt.year == today.year)].groupby('المندوب').agg({
    'المبيعات': 'sum',
    'التحصيل': 'sum',
    'تارقت المبيعات': 'sum',
    'تارقت التحصيل': 'sum'
}).reset_index()

# --- العنوان ---
st.markdown("""
    <div style="text-align: center; margin-top: -60px;">
        <h1 style='font-size: 50px; color: #0059b3;'>شركة الفنار لتوزيع الأدوية</h1>
        <h4 style='color: gray;'>لوحة متابعة المناديب اليومية والشهرية</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- بيانات اليوم ---
st.subheader("📅 مبيعات وتحصيل اليوم")

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

# --- بيانات الشهر ---
st.subheader("🗓️ مبيعات وتحصيل الشهر")

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
