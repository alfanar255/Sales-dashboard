import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.title("📄 اختبار الاتصال بجوجل شيت")

# إعداد صلاحيات الوصول
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# فتح الجدول - غيّر الاسم إذا كنت قد استخدمت اسمًا مختلفًا
spreadsheet = client.open("لوحة مبيعات الفنار")

# تجربة قراءة ورقة الفواتير
worksheet = spreadsheet.worksheet("الفواتير")
data = worksheet.get_all_records()
df = pd.DataFrame(data)

st.subheader("📦 بيانات الفواتير:")
st.dataframe(df)
