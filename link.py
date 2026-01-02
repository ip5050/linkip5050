from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, DictionaryObject, NumberObject, FloatObject

# اسم الملف الأصلي
input_pdf = "en.pdf"

# اسم الملف النهائي
output_pdf = r"C:\Users\computer.house\DCIM\en_linked.pdf"  # عدّل حسب مجلد DCIM عندك

# طلب الرابط من المستخدم
link_url = input("💡 من فضلك ادخل الرابط اللي عايز تحطه داخل الملف: ")

# قراءة الملف
reader = PdfReader(input_pdf)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

    # ابعاد الصفحة
    page_width = float(page.mediabox.width)
    page_height = float(page.mediabox.height)

    # إنشاء annotation يغطي كل الصفحة
    link = DictionaryObject()
    link.update({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Link"),
        NameObject("/Rect"): [FloatObject(0), FloatObject(0), FloatObject(page_width), FloatObject(page_height)],
        NameObject("/Border"): [NumberObject(0), NumberObject(0), NumberObject(0)],
        NameObject("/A"): DictionaryObject({
            NameObject("/S"): NameObject("/URI"),
            NameObject("/URI"): NameObject(link_url)
        }),
    })

    if "/Annots" in page:
        page["/Annots"].append(link)
    else:
        page[NameObject("/Annots")] = [link]

# حفظ الملف الجديد
with open(output_pdf, "wb") as f:
    writer.write(f)

print(f"✅ تم إنشاء الملف مع الرابط داخل كل الصفحة وحفظه في: {output_pdf}")
