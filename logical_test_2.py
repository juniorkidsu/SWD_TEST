
"""
Convert Arabic Number to Roman Number.
เขียนโปรแกรมรับค่าจาก user เพื่อแปลง input ของ user ที่เป็นตัวเลขอราบิก เป็นตัวเลขโรมัน
โดยที่ค่าที่รับต้องมีค่ามากกว่า 0 จนถึง 1000

*** อนุญาตให้ใช้แค่ตัวแปรพื้นฐาน, built-in methods ของตัวแปรและ function พื้นฐานของ Python เท่านั้น
ห้ามใช้ Library อื่น ๆ ที่ต้อง import ในการทำงาน(ยกเว้น ใช้เพื่อการ test การทำงานของฟังก์ชัน).

"""
Data_set_roman = [[1000, 'M'], [900, 'CM'], [500, 'D'], [400, 'CD'],
                [ 100, 'C'], [ 90, 'XC'], [ 50, 'L'], [ 40, 'XL'],
                [  10, 'X'], [  9, 'IX'], [  5, 'V'], [  4, 'IV'],
                [   1, 'I']]


numberInput = int(input(": "))
summary = 0
result = ""
position=0
if numberInput ==0 or numberInput > 1000:
    print("DATA OUT OF RANGE TESTING")
else:
    while numberInput > 1:
        if numberInput >= Data_set_roman[position][0]:
            result= result + Data_set_roman[position][1]
            numberInput-=Data_set_roman[position][0]
            summary = numberInput
            while numberInput >= Data_set_roman[position][0]:
                result= result + Data_set_roman[position][1]
                numberInput-=Data_set_roman[position][0]
                summary = numberInput

        position+=1
    print(result)

