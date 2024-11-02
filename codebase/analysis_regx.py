#!/usr/bin/env python
# coding: utf-8
import pytesseract
from PIL import Image
import re
import json

# File paths
input_image_path = '/teamspace/studios/this_studio/Result/preprocessed_image.png'
output_json_path = '/teamspace/studios/this_studio/Result/invoice_data.json'

# Extract text from image using Tesseract
image = Image.open(input_image_path)
extracted_text = pytesseract.image_to_string(image, lang='eng+hin')

# Print extracted text for debugging
print(f"Extracted Text:\n{extracted_text}")

# Patterns to extract information
patterns = {
    "company_name": r'^.*?The\s+([\w\s]+) Ltd\.',  # Extracts company name
    "company_address": r'\d{1,5}\s[\w\s]+London',  # Extracts address with "London"
    "company_reg_no": r'Co\. Reg\. No\.\s*([\d]+)',  # Company registration number
    "vat_no": r'VAT No\.\s*([\w\d]+)',  # VAT number
    "email": r'Email:\s*([\w\.-]+@[\w\.-]+)',  # Email
    "phone": r'Phone:\s*([\d\s]+)',  # Phone number
    "invoice_number": r'Invoice:\s*([\w-]+)',  # Invoice number
    "client_name": r'Bill to:\s*(.*?)(?=\s*Invoice:)',  # Client name
    "address": r'Bill to:.*?\n(.*?)(?=\s*Invoice Date:)',  # Address
    "invoice_date": r'Invoice Date:\s*(\d{2}/\d{2}/\d{4})',  # Invoice date
    "due_date": r'Due Date:\s*(\d{2}/\d{2}/\d{4})',  # Due date
    "amount_due": r'Amount Due \(GBP\)\s*([\d.,]+)',  # Amount due
    "amount_paid": r'Amount Paid\s*([\d.,]+)',  # Amount paid
    "total": r'Total GBP\s*([\d.,]+)',  # Total
    "vehicle": r'Vehicle:\s*(.*?)(?=\s*Payment)',  # Vehicle details
    "website": r'Website:\s*([\w\.-]+)',  # Website
}
# Print extracted text for debugging
print(f"Extracted Text:\n{extracted_text}")

# Extract and print data using patterns
def extract_group_or_none(pattern, text):
    match = re.search(pattern, text)
    return match.group(1).strip() if match else 'Not found'

# Extract data using patterns
invoice_data = {
    "company_name": extract_group_or_none(patterns["company_name"], extracted_text),
    "company_address": extract_group_or_none(patterns["company_address"], extracted_text),
    "company_reg_no": extract_group_or_none(patterns["company_reg_no"], extracted_text),
    "vat_no": extract_group_or_none(patterns["vat_no"], extracted_text),
    "email": extract_group_or_none(patterns["email"], extracted_text),
    "phone": extract_group_or_none(patterns["phone"], extracted_text),
    "invoice_number": extract_group_or_none(patterns["invoice_number"], extracted_text),
    "client_name": extract_group_or_none(patterns["client_name"], extracted_text),
    "address": extract_group_or_none(patterns["address"], extracted_text),
    "invoice_date": extract_group_or_none(patterns["invoice_date"], extracted_text),
    "due_date": extract_group_or_none(patterns["due_date"], extracted_text),
    "amount_due": extract_group_or_none(patterns["amount_due"], extracted_text),
    "amount_paid": extract_group_or_none(patterns["amount_paid"], extracted_text),
    "total": extract_group_or_none(patterns["total"], extracted_text),
    "vehicle": extract_group_or_none(patterns["vehicle"], extracted_text),
    "website": extract_group_or_none(patterns["website"], extracted_text)
}

# Print extracted invoice data
#print("Extracted Invoice Data:")
#print(json.dumps(invoice_data, indent=4))

# Save extracted data to JSON file
output_json_path = "/teamspace/studios/this_studio/Result/invoice_data.json"
with open(output_json_path, "w") as save_file:
    json.dump(invoice_data, save_file, indent=4)

print(f"Invoice data saved to: {output_json_path}")
