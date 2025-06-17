import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# إعداد الوصول إلى Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(credentials)

# تحميل البيانات
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1PBhvZlhYwUVsIBAyLzpOvwixlyUBHZA17lgGUEdH72Q")

# تحميل الجداول
sales_df = pd.DataFrame(spreadsheet.worksheet("Sales").get_all_records())
collections_df = pd.DataFrame(spreadsheet.worksheet("Collections").get_all_records())
returns_df = pd.DataFrame(spreadsheet.worksheet("Returns").get_all_records())
targets_df = pd.DataFrame(spreadsheet.worksheet("Targets").get_all_records())

# تحويل الأعمدة للتواريخ وأرقام
for df in [sales_df, collections_df, returns_df]:
    df['التاريخ'] = pd.to_datetime(df['التاريخ'])

today = pd.to_datetime(datetime.today().date())
month = today.month

# حساب المبيعات الصافية (خصم المرتجعات)
returns_grouped = returns_df.groupby('رقم الفاتورة المرتجعة')['قيمة المرتجع'].sum()
sales_df['صافي الفاتورة'] = sales_df.apply(lambda row: row['قيمة الفاتورة'] - returns_grouped.get(row['رقم الفاتورة'], 0), axis=1)

# واجهة Streamlit
st.set_page_config(page_title="لوحة مبيعات الفنار", layout="wide")
st.title("📊 لوحة متابعة المبيعات والتحصيل – شركة الفنار")

# مبيعات وتحصيل إجمالية
total_sales = sales_df['صافي الفاتورة'].sum()
monthly_sales = sales_df[sales_df['التاريخ'].dt.month == month]['صافي الفاتورة'].sum()
daily_sales = sales_df[sales_df['التاريخ'].dt.date == today.date()]['صافي الفاتورة'].sum()

st.subheader("نظرة عامة على الشركة")
st.metric("📦 إجمالي صافي المبيعات", f"{total_sales:,.0f} ريال")
st.metric("🗓️ مبيعات هذا الشهر", f"{monthly_sales:,.0f} ريال")
st.metric("📅 مبيعات اليوم", f"{daily_sales:,.0f} ريال")

st.markdown("---")

# اختيار مندوب
salespeople = targets_df['اسم المندوب'].unique()
selected_rep = st.selectbox("اختر المندوب لعرض تفاصيله", salespeople)

rep_sales = sales_df[sales_df['اسم المندوب'] == selected_rep]
rep_returns = returns_df[returns_df['اسم المندوب'] == selected_rep]
rep_collections = collections_df[collections_df['اسم المندوب'] == selected_rep]
rep_target = targets_df[targets_df['اسم المندوب'] == selected_rep].iloc[0]

# صافي المبيعات والتحصيل للمندوب
rep_total_sales = rep_sales['صافي الفاتورة'].sum()
rep_monthly_sales = rep_sales[rep_sales['التاريخ'].dt.month == month]['صافي الفاتورة'].sum()
rep_daily_sales = rep_sales[rep_sales['التاريخ'].dt.date == today.date()]['صافي الفاتورة'].sum()
rep_total_returns = rep_returns['قيمة المرتجع'].sum()

rep_total_collections = rep_collections['قيمة التحصيل'].sum()
rep_monthly_collections = rep_collections[rep_collections['التاريخ'].dt.month == month]['قيمة التحصيل'].sum()
rep_daily_collections = rep_collections[rep_collections['التاريخ'].dt.date == today.date()]['قيمة التحصيل'].sum()

# نسب التارجت
def calc_percent(actual, target):
    return f"{(actual / target * 100):.1f}%" if target > 0 else "-"

st.subheader(f"تفاصيل المندوب: {selected_rep}")

col1, col2 = st.columns(2)

with col1:
    st.metric("💼 صافي المبيعات الكلية", f"{rep_total_sales:,.0f} ريال")
    st.metric("📅 صافي مبيعات اليوم", f"{rep_daily_sales:,.0f} ريال")
    st.metric("📆 صافي مبيعات الشهر", f"{rep_monthly_sales:,.0f} ريال")

with col2:
    st.metric("💰 التحصيل الكلي", f"{rep_total_collections:,.0f} ريال")
    st.metric("🗓️ تحصيل اليوم", f"{rep_daily_collections:,.0f} ريال")
    st.metric("📆 تحصيل الشهر", f"{rep_monthly_collections:,.0f} ريال")

st.markdown("### 🎯 نسبة التارجت")

st.write(f"🟩 نسبة مبيعات اليوم: **{calc_percent(rep_daily_sales, rep_target['تارجت مبيعات يومي'])}**")
st.write(f"🟨 نسبة مبيعات الشهر: **{calc_percent(rep_monthly_sales, rep_target['تارجت مبيعات شهري'])}**")
st.write(f"🟩 نسبة تحصيل اليوم: **{calc_percent(rep_daily_collections, rep_target['تارجت تحصيل يومي'])}**")
st.write(f"🟨 نسبة تحصيل الشهر: **{calc_percent(rep_monthly_collections, rep_target['تارجت تحصيل شهري'])}**")
