import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from tabulate import tabulate

# Function to extract tables from an image
def extract_tables_from_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Detect horizontal and vertical lines
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((1, 50), np.uint8))
    vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((50, 1), np.uint8))

    # Combine horizontal and vertical lines
    table_structure = cv2.addWeighted(horizontal, 0.5, vertical, 0.5, 0.0)

    # Find contours of tables
    contours, _ = cv2.findContours(table_structure, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    table_data = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cell_img = image[y:y+h, x:x+w]
        cell_text = pytesseract.image_to_string(cell_img, config="--psm 6").strip()
        table_data.append(cell_text.split("\n"))  # Each row is extracted

    return table_data

# Function to process PDF and extract tables
def process_pdf_for_tables(pdf_path):
    pages = convert_from_path(pdf_path, dpi=300)
    extracted_tables = []

    for page in pages:
        image = np.array(page)
        table_data = extract_tables_from_image(image)
        
        if table_data:
            formatted_table = tabulate(table_data, tablefmt="grid")  # Convert to ASCII table
            extracted_tables.append(formatted_table)

    return "\n\n".join(extracted_tables)

# Example Usage
pdf_path = "/home/yuvaraj/Documents/temp/python/LAND CAAU9154855-8.pdf"  # Replace with your PDF
table_output = process_pdf_for_tables(pdf_path)
print("Extracted Tables:\n", table_output)
