from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# โหลดโมเดลที่ train ไว้
model = pickle.load(open("model.pkl","rb"))

# =========================
# รูปร่างผู้หญิง (ตามรูป 5 แบบ)
# =========================
def female_shape(bust, waist, hip):

    bust_waist = bust - waist
    hip_waist = hip - waist
    bust_hip = bust - hip

    # 1) นาฬิกาทราย
    if abs(bust_hip) <= 6 and bust_waist >= 18 and hip_waist >= 18:
        return "นาฬิกาทราย"

    # 2) ลูกแพร์ (สะโพกใหญ่)
    elif hip - bust >= 8 and hip_waist >= 15:
        return "ลูกแพร์"

    # 3) สามเหลี่ยมคว่ำ (อก/ไหล่ใหญ่)
    elif bust - hip >= 8 and bust_waist >= 15:
        return "สามเหลี่ยมคว่ำ"

    # 4) แอปเปิ้ล (ช่วงกลางใหญ่)
    elif waist >= bust and waist >= hip:
        return "แอปเปิ้ล"

    # 5) กระบอก (ทรงตรง)
    else:
        return "กระบอก"


# =========================
# รูปร่างผู้ชาย
# =========================
def male_shape(bust, waist, hip, shoulder):

    chest_waist_ratio = bust / waist

    # พุง
    if waist > bust + 6:
        return "สามเหลี่ยม"

    # นักกีฬา V-shape
    elif chest_waist_ratio >= 1.20:
        return "สามเหลี่ยมหัวกลับ"

    # ไหล่กว้างปกติ
    elif chest_waist_ratio >= 1.10:
        return "สี่เหลี่ยมคางหมู"

    # อ้วนช่วงกลาง
    elif waist > hip and waist > bust:
        return "รูปไข่"

    # ตัวตรง
    else:
        return "สี่เหลี่ยม"


# =========================
# เลือกรูปให้ตรงผลลัพธ์
# =========================
def get_shape_image(shape):

    image_map = {
        # ผู้หญิง
        "นาฬิกาทราย": "hourglass.png",
        "กระบอก": "cylinder.png",
        "ลูกแพร์": "pear.png",
        "สามเหลี่ยมคว่ำ": "inverted_triangle_famale.png",
        "แอปเปิ้ล": "apple.png",

        # ผู้ชาย
        "สี่เหลี่ยม": "square.png",
        "สี่เหลี่ยมคางหมู": "trapezoid.png",
        "รูปไข่": "oval.png",
        "สามเหลี่ยม": "triangle.png",
        "สามเหลี่ยมหัวกลับ": "inverted_triangle_male.png"
    }

    return image_map.get(shape, "rectangle.png")


# =========================
# หน้าเว็บหลัก
# =========================
@app.route("/", methods=["GET","POST"])
def home():

    if request.method == "POST":

        gender = request.form["gender"]

        shoulder = float(request.form["shoulder"])
        bust = float(request.form["bust"])
        waist = float(request.form["waist"])
        hip = float(request.form["hip"])
        weight = float(request.form["weight"])
        height = float(request.form["height"])

        # ---------- Machine Learning ทำนาย WHR ----------
        data = np.array([[shoulder, bust, waist, hip, weight, height]])
        whr_pred = model.predict(data)[0]

        # ---------- จำแนกรูปร่าง ----------
        if gender == "female":
            shape = female_shape(bust, waist, hip)
        else:
            shape = male_shape(bust, waist, hip, shoulder)

        # ---------- เลือกรูป ----------
        image_file = get_shape_image(shape)

        return render_template(
            "index.html",
            prediction=round(whr_pred, 3),
            shape=shape,
            image_file=image_file
        )

    return render_template("index.html")


# รันเซิร์ฟเวอร์
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
