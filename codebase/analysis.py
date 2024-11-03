import pytesseract
from PIL import Image
input_image_path = '/teamspace/studios/this_studio/Result/preprocessed_image.png'
output_txt_path = '/teamspace/studios/this_studio/Result/invoice_data.txt'
image = Image.open(input_image_path)
extracted_text = pytesseract.image_to_string(image, lang='eng+hin')
print(f"Extracted Text:\n{extracted_text}")
with open(output_txt_path, "w") as save_file:
    save_file.write(extracted_text)

print(f"Invoice data saved to: {output_txt_path}")
