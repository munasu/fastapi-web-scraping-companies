import pandas as pd

# โหลดไฟล์ CSV
df = pd.read_csv('company_list.csv')

# ใช้ Regular Expression เพื่อตัดคำว่า "บริษัท" และ "(มหาชน)" ออก
df['company'] = df['company'].str.replace(r'^บริษัท\s*', '', regex=True)


# บันทึกผลลัพธ์กลับไปที่ไฟล์ CSV
df.to_csv('cleaned_company_list_v2.csv', index=False)

