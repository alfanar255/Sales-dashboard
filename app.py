import streamlit as st
import pandas as pd
from datetime import datetime
from google.oauth2 import service_account
import gspread

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="لوحة مبيعات الفنار")

# الاتصال بـ Google Sheets
creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"],
)
gc = gspread.authorize(creds)
spreadsheet = gc.open_by_url(st.secrets["google_sheets"]["sheet_url"])

# تحميل البيانات
df = pd.DataFrame(spreadsheet.worksheet("المبيعات").get_all_records())
df["التاريخ"] = pd.to_datetime(df["التاريخ"], errors="coerce")

# الفلاتر العامة
today = pd.to_datetime(datetime.now().date())
df["شهر"] = df["التاريخ"].dt.to_period("M")
df["يوم"] = df["التاريخ"].dt.date

# معالجة المرتجعات بالسالب
df["صافي"] = df["المبلغ"]
df.loc[df["نوع"] == "مرتجع", "صافي"] *= -1

# قوائم المناديب
reps = df["المندوب"].unique()

# قراءة التارقت
try:
    target_df = pd.DataFrame(spreadsheet.worksheet("التارقت").get_all_records())
    target_df["تاريخ"] = pd.to_datetime(target_df["تاريخ"], errors="coerce")
except:
    target_df = pd.DataFrame(columns=["المندوب", "تاريخ", "تارقت شهري", "تارقت يومي", "تارقت تحصيل"])

# دالة استخراج التارقت
def get_target(rep, today):
    row = target_df[(target_df["المندوب"] == rep)].sort_values("تاريخ", ascending=False).head(1)
    if not row.empty:
        return row.iloc[0]["تارقت شهري"], row.iloc[0]["تارقت يومي"], row.iloc[0]["تارقت تحصيل"]
    return 0, 0, 0

# === 👥 عرض إجمالي الشركة ===
st.title("📊 لوحة مبيعات شركة الفنار لتوزيع الأدوية")

col1, col2, col3 = st.columns(3)
col1.metric("إجمالي المبيعات", f"{df['صافي'].sum():,.0f} ريال")
col2.metric("مبيعات هذا الشهر", f"{df[df['شهر'] == today.to_period('M')]['صافي'].sum():,.0f} ريال")
col3.metric("مبيعات اليوم", f"{df[df['يوم'] == today.date()]['صافي'].sum():,.0f} ريال")

st.divider()

# === 👤 لكل مندوب ===
for rep in reps:
    st.subheader(f"مندوب: {rep}")
    rep_df = df[df["المندوب"] == rep]

    total_sales = rep_df["صافي"].sum()
    monthly_sales = rep_df[rep_df["شهر"] == today.to_period("M")]["صافي"].sum()
    daily_sales = rep_df[rep_df["يوم"] == today.date()]["صافي"].sum()
    collection = rep_df[rep_df["نوع"] == "تحصيل"]["المبلغ"].sum()

    t_month, t_day, t_collect = get_target(rep, today)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("💰 المبيعات الكلية", f"{total_sales:,.0f} ريال")
    col2.metric("📅 هذا الشهر", f"{monthly_sales:,.0f}")
    col3.metric("🕒 اليوم", f"{daily_sales:,.0f}")
    col4.metric("✅ التحصيل", f"{collection:,.0f}")
    col5.metric("📉 المرتجعات", f"{rep_df[rep_df['نوع']=='مرتجع']['المبلغ'].sum():,.0f}")

    # النسب
    col6, col7 = st.columns(2)
    if t_month > 0:
        col6.progress(min(monthly_sales / t_month, 1.0), text=f"نسبة تحقيق التارقت الشهري: {monthly_sales / t_month:.0%}")
    if t_collect > 0:
        col7.progress(min(collection / t_collect, 1.0), text=f"نسبة التحصيل: {collection / t_collect:.0%}")

    st.divider()
