import pandas as pd

df = pd.read_csv("result_shape.csv")

# ลบช่องว่างชื่อคอลัมน์
df.columns = df.columns.str.strip()

print("Columns:", df.columns)

# สร้าง Target (WHR)
df["WHR"] = df["เอว"] / df["สะโพก"]

# ลบ Timestamp ถ้ามี
if "Timestamp" in df.columns:
    df = df.drop(columns=["Timestamp"])

df.to_csv("shape_dataset.csv", index=False)

print("สร้าง shape_dataset.csv สำเร็จ")
