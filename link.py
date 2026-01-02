from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import NameObject, DictionaryObject, NumberObject, FloatObject
import os

print("\n📎 PDF Full Clickable Link Injector\n")

# إدخال البيانات من المستخدم
input_pdf = input("📄 ادخل مسار ملف PDF الأصلي: ").strip()
link_url = input("🔗 ادخل الرابط اللي عايز تحطه داخل الملف: ").strip()
output_dir = input("📁 ادخل مسار المجلد اللي هيتحفظ فيه الملف النهائي: ").strip()

# إنشاء المجلد لو مش موجود
os.makedirs(output_dir, exist_ok=True)

# اسم الملف النهائي
output_pdf = os.path.join(output_dir, "linked_output.pdf")

# قراءة الملف
reader = PdfReader(input_pdf)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

    page_width = float(page.mediabox.width)
    page_height = float(page.mediabox.height)

    # إنشاء رابط يغطي الصفحة بالكامل
    link = DictionaryObject()
    link.update({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Link"),
        NameObject("/Rect"): [
            FloatObject(0), FloatObject(0),
            FloatObject(page_width), FloatObject(page_height)
        ],
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

# حفظ الملف
with open(output_pdf, "wb") as f:
    writer.write(f)

print("\n✅ تم إنشاء الملف بنجاح!")
print(f"📂 مكان الحفظ: {output_pdf}")
