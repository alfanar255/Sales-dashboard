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
    df['التاريخ'] = pd.to_datetime(df['التاريخ'])
    # التأكد من أن القيم الرقمية صحيحة
    for col in ['المبيعات', 'التحصيل', 'تارقت المبيعات', 'تارقت التحصيل']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df

df = load_data()

# --- الشعار ---
logo_url = "https://raw.githubusercontent.com/alfanar255/Sales-dashboard/main/company_logo2.png"
st.image(logo_url, width=120)

# --- تحليل البيانات ---
today = pd.Timestamp.today().normalize()
df['اليوم'] = df['التاريخ'].dt.date

# العنوان الرئيسي
st.markdown("""
    <div style="text-align: center; margin-top: -60px;">
        <h1 style='font-size: 50px; color: #0059b3;'>شركة الفنار لتوزيع الأدوية</h1>
        <h4 style='color: gray;'>لوحة متابعة المبيعات والتحصيل للمناديب</h4>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# --- حساب المؤشرات لكل مندوب ---
grouped = df.groupby('المندوب')

# إنشاء جدول للعرض
result = []

for مندوب, data in grouped:
    # اليوم
    sales_today = data[data['اليوم'] == today.date()]['المبيعات'].sum()
    collection_today = data[data['اليوم'] == today.date()]['التحصيل'].sum()
    
    # الشهر
    sales_month = data[data['التاريخ'].dt.month == today.month]['المبيعات'].sum()
    collection_month = data[data['التاريخ'].dt.month == today.month]['التحصيل'].sum()
    
    # الأهداف الشهرية
    sales_target = data['تارقت المبيعات'].max()
    collection_target = data['تارقت التحصيل'].max()

    # النسب
    sales_ach = (sales_month / sales_target * 100) if sales_target else 0
    collection_ach = (collection_month / collection_target * 100) if collection_target else 0

    result.append({
        'المندوب': مندوب,
        'مبيعات اليوم': sales_today,
        'تحصيل اليوم': collection_today,
        'مبيعات الشهر': sales_month,
        'تحصيل الشهر': collection_month,
        'تارقت المبيعات': sales_target,
        'تارقت التحصيل': collection_target,
        'نسبة تحقيق المبيعات (%)': sales_ach,
        'نسبة تحقيق التحصيل (%)': collection_ach
    })

result_df = pd.DataFrame(result)

# --- عرض النتائج ---
st.dataframe(result_df.style.format({
    'مبيعات اليوم': '{:,.0f} جنيه',
    'تحصيل اليوم': '{:,.0f} جنيه',
    'مبيعات الشهر': '{:,.0f} جنيه',
    'تحصيل الشهر': '{:,.0f} جنيه',
    'تارقت المبيعات': '{:,.0f} جنيه',
    'تارقت التحصيل': '{:,.0f} جنيه',
    'نسبة تحقيق المبيعات (%)': '{:.1f} %',
    'نسبة تحقيق التحصيل (%)': '{:.1f} %'
}), use_container_width=True)

# --- تنسيق CSS ---
st.markdown("""
    <style>
    .stDataFrame th, .stDataFrame td {
        text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

