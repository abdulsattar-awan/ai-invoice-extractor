# AI Invoice Extractor

Reads PDF invoices in **different formats** and extracts the **seller company, invoice date and total amount** using Google Gemini AI, then saves everything to a clean **Excel report**.

## The problem it solves

Businesses receive invoices from many vendors, and every vendor uses a different layout: *"Invoice Date"*, *"Dated"*, *"Bill Date"*; dates like `03/10/2026`, `Oct 15, 2026` or `21 October 2026`. Typing these into a spreadsheet by hand is slow and error-prone. This tool does it automatically.

## Example output

| File | Company | Date | Total |
|---|---|---|---|
| invoice_1.pdf | Al-Noor Stationers | 2026-10-03 | 19200 |
| invoice_2.pdf | Green Leaf Catering | 2026-10-15 | 25500 |
| invoice_3.pdf | Rapid Print House | 2026-09-28 | 27100 |
| invoice_4.pdf | TechFix Computers | 2026-10-21 | 19700 |

All dates are normalised to `YYYY-MM-DD`, whatever format the invoice used.

## Features

- Sends each PDF directly to Gemini (no separate text-extraction step)
- Forces a **structured JSON** response, so the output is reliable to parse
- **Retry logic**: if the API fails, it waits and tries again (up to 3 times)
- One failed file does **not** stop the batch; it is marked `ERROR` in the report for manual review
- Writes a formatted Excel file with bold headers and sized columns

## Tech stack

Python · Google Gemini API (`google-genai`) · openpyxl · python-dotenv

## How to run

1. Install the packages:
   ```
   pip install google-genai python-dotenv openpyxl
   ```
2. Create a `.env` file with your API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```
3. Put your PDF invoices in the `invoices/` folder
4. Run:
   ```
   python extractor.py
   ```
5. Open `invoices_report.xlsx`

> The sample invoices in this repo are fictional and made for testing only.

## Author

**Abdul Sattar Awan**, Librarian and AI automation learner, Lahore, Pakistan