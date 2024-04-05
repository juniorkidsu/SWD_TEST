
"""
Convert Number to Thai Text.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลข เป็นตัวหนังสือภาษาไทย
โดยที่ค่าที่รับต้องมีค่ามากกว่าหรือเท่ากับ 0 และน้อยกว่า 10 ล้าน

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""

thaiword = ["เก้า","แปด","เจ็ด","หก","ห้า","สี่","สาม","สอง","หนึ่ง",""]
unit_test = ["ล้าน","แสน","หมื่น","พัน","ร้อย","สิบ",""]

thaiText = ""
numberInput = list(map(int, list(input(": "))))
length = len(numberInput)
unit_test = unit_test[-length:]

for k, v in enumerate(numberInput):
    current = length - k
    numThai = thaiword[::-1][v]
    if v == 0:
        continue
    if v == 2 and unit_test[k] == "สิบ":
        numThai = "ยี่"
    if v ==2 and current == 8:
        numThai = "ยี่สิบ"
    if v == 1 and current % 6 == 1 and current != length:
        numThai = "เอ็ด"
    if v ==1 and current == 8:
        numThai = "สิบเอ็ด"
    thaiText += numThai + unit_test[k]

print(f"แปลงเป็น {thaiText} บาทถ้วน")
