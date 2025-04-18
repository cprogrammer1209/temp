import pytesseract
from pdf2image import convert_from_path
import cv2
import numpy as np

# Convert PDF to images
def convert_pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path)
    return images

# Extract text from images using OCR
def extract_text_from_images(images):
    extracted_text = []
    for img in images:
        img_cv = np.array(img)  # Convert to OpenCV format
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)  # Convert to grayscale

        # Use Tesseract OCR
        text = pytesseract.image_to_string(gray)
        extracted_text.append(text)
    
    return extracted_text

# Main function
def main():
    pdf_path = "/home/yuvaraj/Documents/temp/python/LAND CAAU9154855-8.pdf"  # Change this to your invoice PDF file
    images = convert_pdf_to_images(pdf_path)
    extracted_texts = extract_text_from_images(images)

    print("\nExtracted Text from Invoice:")
    for text in extracted_texts:
        print(text)

if __name__ == "__main__":
    main()
