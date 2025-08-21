import csv
import json
from io import StringIO
import re

def format_csv_to_llm(text):
    json_data = csv_string_to_json(text)
    if json_data:
        res = json.dumps(json_data, indent=2)
        return res
    else:
        try:
            return json.dumps(json_data, indent=2)
        except Exception as e:
            return None
def extract_csv_from_codeblock(raw_str):
    """Extracts CSV data from a markdown-style code block"""
    pattern = r'```csv(.*?)```'
    matches = re.findall(pattern, raw_str, flags=re.S)
    return matches[0].strip() if matches else None

def quote_unquoted_commas(csv_text):
    """
    Detects fields with embedded commas and wraps them in quotes.
    This is a naive fixer based on known field count.
    """
    lines = csv_text.strip().split('\n')
    header = lines[0].split(',')
    expected_columns = len(header)
    fixed_lines = [lines[0]]  # keep header as is

    for row in lines[1:]:
        # If the row has more columns than expected due to unquoted commas:
        fields = row.split(',')
        if len(fields) > expected_columns:
            new_fields = []
            buffer = ''
            for f in fields:
                if buffer:
                    buffer += ',' + f
                    if len(new_fields) + 1 == expected_columns:
                        new_fields.append(buffer.strip())
                        buffer = ''
                elif len(new_fields) < expected_columns - 1:
                    new_fields.append(f.strip())
                else:
                    buffer = f.strip()
            if buffer:
                new_fields.append(buffer.strip())
            fixed_lines.append(','.join(f'"{f}"' if ',' in f else f for f in new_fields))
        else:
            fixed_lines.append(row)
    return '\n'.join(fixed_lines)

def csv_string_to_json(raw_str):
    csv_text = extract_csv_from_codeblock(raw_str)
    if not csv_text:
        return []

    # csv_text = quote_unquoted_commas(csv_text)
    csv_file = StringIO(csv_text)
    reader = csv.DictReader(csv_file)
    return [row for row in reader]



csv_data = """```csv
"InvoiceSLNo","InvoiceNo","InvoiceDate","QtyCode","Currency","Terms","TermsofPayment","InvoiceValue","SupplierName","SupplierAdd1","SupplierAdd2","SupplierAdd3","SupplierAdd4"
"1","SP20250269","MAR.20,2025","PCS","USD","","","3,033.99","NOBLELIFT INTELLIGENT EQUIPMENT CO.,LTD.","NO.528 CHANGZHOU ROAD,","TAIHU SUB-DISTRICT,","CHANGXING,","ZHEJIANG 313100 CHINA."
```"""



print(format_csv_to_llm(csv_data))
