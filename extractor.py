import os
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from openpyxl import Workbook
from openpyxl.styles import Font

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PROMPT = (
    "Extract the seller company name, invoice date and total amount from this invoice. "
    "Reply ONLY with JSON like this: "
    '{"company": "...", "date": "YYYY-MM-DD", "total": 0}'
)


def ask_gemini(pdf_data):
    for attempt in range(1, 4):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[
                    types.Part.from_bytes(data=pdf_data, mime_type="application/pdf"),
                    PROMPT,
                ],
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"   Koshish {attempt} nakaam: {e}")
            time.sleep(10)
    return None


wb = Workbook()
sheet = wb.active
sheet.title = "Invoices"
sheet.append(["File", "Company", "Date", "Total"])
for cell in sheet[1]:
    cell.font = Font(bold=True)

for file_name in os.listdir("invoices"):
    with open("invoices/" + file_name, "rb") as f:
        pdf_data = f.read()

    data = ask_gemini(pdf_data)

    if data is None:
        print(file_name, "→ ❌ 3 koshishon ke baad bhi nahi hua, agli file par ja rahe hain")
        sheet.append([file_name, "ERROR", "", ""])
    else:
        print(file_name, "→", data["company"], "|", data["date"], "|", data["total"])
        sheet.append([file_name, data["company"], data["date"], data["total"]])
sheet.column_dimensions["A"].width = 18
sheet.column_dimensions["B"].width = 25
sheet.column_dimensions["C"].width = 14
sheet.column_dimensions["D"].width = 12
wb.save("invoices_report.xlsx")
print("\n✅ Excel file ban gayi: invoices_report.xlsx")