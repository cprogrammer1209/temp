import json
import csv
from io import StringIO
import openai
from openai import OpenAI
import os
import re
import math
import pymongo
import pandas as pd
from bs4 import BeautifulSoup
# import google.generativeai as genai
from google import genai
from google.genai import types
from json_repair import repair_json
from google.api_core.exceptions import InternalServerError, ResourceExhausted, TooManyRequests
import time

os.environ["OPENAI_API_KEY"] = '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'
os.environ["DEEPSEEK_API_KEY"] = 'sk-a3ddb45eaf01401899f10084e88f8077'
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI() 

GOOGLE_API_KEY='AIzaSyD-Gsdh5u9JamamQdzH-pIi-5q78GOxWV4'
# GOOGLE_API_KEY='AIzaSyCwfg4xDLCh9gHf1wIA2Miy4VAifWuUjdY'
# GOOGLE_API_KEY='AIzaSyDFs31mlJSb4rfCv0vB4SxGv19mpK1sQuA'
# GOOGLE_API_KEY='AIzaSyCba_YtqSiq5jNu4ySEsm-koKpe8DyuslU'
# genai.configure(api_key=GOOGLE_API_KEY)
genaiclient = genai.Client(api_key=GOOGLE_API_KEY)
from difflib import SequenceMatcher
token_usage_all = []
def make_api_call_with_retry(content,model="gemini-2.0-flash", max_retries=5, initial_delay=5):
    delay = initial_delay
    # GOOGLE_API_KEY='AIzaSyDFs31mlJSb4rfCv0vB4SxGv19mpK1sQuA'
    GOOGLE_API_KEY='AIzaSyD-Gsdh5u9JamamQdzH-pIi-5q78GOxWV4'
    genaiclient = genai.Client(api_key=GOOGLE_API_KEY)
    # model = 'gemini-2.5-flash-preview-05-20'
    # model = model
    for attempt in range(max_retries):
        print("attemdp ",attempt)

        try:
            start_time = time.monotonic()
            response = genaiclient.models.generate_content(model=model,contents=content,
                                                           config=types.GenerateContentConfig(
                    temperature=0.1,
                ))
            end_time = time.monotonic()
            usage_metadata = response.usage_metadata
            usage_dict = {
                'duration': end_time - start_time,
                'model': model,
                'input_tokens': usage_metadata.prompt_token_count,
                'output_tokens': usage_metadata.candidates_token_count,
                'total_tokens': usage_metadata.total_token_count
            }
            global token_usage_all
            token_usage_all.append(usage_dict)
            if not response.text:
                print(f"Attempt {attempt + 1} failed with error: {e}")
                if attempt == max_retries - 1:
                    print("Max retries reached. Raising error.")
                    raise
                print(f"Retrying in {delay} seconds...")
                time.sleep(1)
                delay *= 2
            else:
            # response = model.generate_content(content)
                return response
        except Exception as e: # Catch specific retryable errors
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt == max_retries - 1:
                print("Max retries reached. Raising error.")
                raise
            print(f"Retrying in {delay} seconds...")
            time.sleep(1)
            delay *= 2 # Exponential backoff
        
    return None

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#model = genai.GenerativeModel('gemini-1.5-pro-latest')
import argparse
def format_json_llm(text):
    regex_pattern = r'```json(.*?)```'
    match = re.findall(regex_pattern,text, flags=re.S)

    if match:
        repaired_json = repair_json(match[0])
        res = json.loads(repaired_json)
        return res
    else:
        try:
            return json.loads(res)
        except Exception as e:
            return None


def format_csv_to_llm(text):
    json_data = csv_string_to_json(text)
    print("json type ",type(json_data))
    if json_data:
        print("json type after",type(json_data))

        return json_data
    else:
        try:
            return json.load(json_data)
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

def convert_csv_to_json(csv_data):
    """
    Convert CSV data with dot-notation headers to nested JSON structure
    """
    lines = csv_data.strip().split('\n')
    
    # Parse CSV data
    csv_reader = csv.reader(StringIO('\n'.join(lines)))
    all_rows = list(csv_reader)
    
    # Find where Invoice Details end and Items Details begin
    invoice_headers = []
    item_headers = []
    invoice_data_rows = []
    item_data = []
    
    # Parse headers and data
    i = 0
    current_section = None
    
    while i < len(all_rows):
        row = all_rows[i]
        if any('Invoice Details' in cell for cell in row):
            invoice_headers = row
            current_section = 'invoice'
            i += 1
        elif any(cell in ['Item Details', 'ItemDetails', 'Items Details','ItemsDetails'] for cell in row):
            item_headers = row
            current_section = 'items'
            i += 1
        elif current_section == 'invoice':
            # Collect all invoice data rows until we hit Items Details or end
            invoice_data_rows.append(row)
            i += 1
        elif current_section == 'items':
            # Collect all item data rows
            item_data.append(row)
            i += 1
        else:
            i += 1
    
    # Convert invoice data to list of dictionaries (multiple invoices possible)
    invoice_list = []
    for invoice_row in invoice_data_rows:
        invoice_dict = {}
        for j, header in enumerate(invoice_headers):
            if j < len(invoice_row):
                # Remove "Invoice Details." prefix and convert to proper key
                key = header.replace('Invoice Details.', '')
                invoice_dict[key] = invoice_row[j]
        invoice_list.append(invoice_dict)
    
    # Convert item data to list of dictionaries
    items_list = []
    for row in item_data:
        item_dict = {}
        for j, header in enumerate(item_headers):
            if j < len(row):
                # Remove "Items Details." prefix and convert to proper key
                key = header.replace('Item Details.', '').replace('ItemDetails.','').replace('Items Details.','')
                item_dict[key] = row[j]
        items_list.append(item_dict)
    
    # Create final JSON structure
    result =         {
            "Invoice Details": invoice_list,
            "ItemDetails": items_list
        }
    
    return result

def csv_string_to_json(raw_str):
    csv_text = extract_csv_from_codeblock(raw_str)
    if not csv_text:
        return []
    result = convert_csv_to_json(csv_text)
    return result
    
def get_args():
    parser = argparse.ArgumentParser(description='File I/O')
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        help="full path to data files",
        required=True)

    parser.add_argument(
        '-t',
        '--timestamp',
        type=str,
        help="timestamp",
        required=True)

    args = parser.parse_args()
    local_path = args.input
    local_time = args.timestamp

    return local_path, local_time

import concurrent.futures
import threading
from typing import Dict, List, Any

def process_single_page_range(itr, page_output, prompt_format, table_obj, isTemplateBased, templateData, index,content, invoice_obj):
    """Process a single page range - this function will be run in parallel"""
    if 'type' in itr:
        response = make_api_call_with_retry(content,'gemini-2.0-flash') #genaiclient.models.generate_content(model='gemini-2.0-flash',contents=content)
        
        invoice_obj = format_json_llm(response.text)
        return {
            'content': invoice_obj,
            'input_tokens': response.usage_metadata.prompt_token_count,
            'output_tokens': response.usage_metadata.candidates_token_count,
            'itr': itr,
            'index': index,  # Add index to maintain order
            'type': "header"
        }
    else:
        print("itr ", itr)
        page = page_output[int(itr['start']):int(itr['end'])+1]
        page = '\n---PAGE END---\n'.join(page)
        print("aaa")
        table_chat_format = prompt_format + '\n' + json.dumps(table_obj) + '\n\n' + page
        
        if isTemplateBased:
            print("Inside template based")
            
            print(type(templateData))
            extra_prompt = f'******The document provided is chunked set of invoices. Actual value of InvoiceSlNo: {itr["invoice_slno"]}******'
            tableTemplate=templateData[0]['input']
            if 'inputTable' in templateData[0]:
                tableTemplate = templateData[0]['inputTable']
            examples = ""
            for idx, item in enumerate(tableTemplate):
                examples += f'''
                    Example Sample {idx}(Input → Output):
                    ***Input*** : {item['input']}
                    ***Output*** : {item['table']}
                '''
            templatePrompt = f'''
                You are a highly accurate and efficient document data extraction assistant.

            
                Below is a sample template showing the structure and style of documents similar to the input:
                {examples}

                The Above Example Input and Example Output is a sample template showing the structure and style of documents similar to the input.
                The output needs to be completly derived or extracted from the  'New Input' provided by the user.  


                *****New Input****:
                {page}
                
                {extra_prompt if itr["invoice_slno"] else ""}

            
                Strictly follow the below rules and instructions to extract the data from the New Input document.

                Rules :
                - Strictly follow the field names and extraction logic as described in the Extraction Rules.
                - If a field's value is missing, leave it blank ("") or null.
                - Do not create any extra fields not mentioned in the extraction rules.
                - Use only the information present in the New Input document.

                Instructions:

                    The Output need to be generated only with the New Input context. 
                    The example input and output is given only for the reference of the structure and style of the document.
                    The output needs to be completly derived or extracted from the  'New Input' provided by the user. 
                    The Reference should not impact the output in any way.
                    Use the Invoice Serial Number to add values for InvoiceSlNo and itemSlNo accordingly.


                The output needs to be completly derived or extracted from the  'New Input' provided by the user. 
                You must extract the information only based on the fields listed below.

                Extraction Fields:
                {json.dumps(table_obj, indent=2)}

                
                You must use the context provided,and strictly populate ALL fields in the  JSON object.
                If any field value is missing or unavailable in the document, leave it as an empty string (""). 
                Populate the output JSON: Respond **only** with this code block:
                ```json{{result}}```
                '''
            table_chat_format = templatePrompt
        
        # Make the API call
        if(len(page_output)<4):
            table_res = make_api_call_with_retry(table_chat_format,"gemini-2.0-flash")
        else:
            table_res = make_api_call_with_retry(table_chat_format,"gemini-2.5-flash")
        
        # Process the response
        table_content = format_json_llm(table_res.text)

        print(table_content)
        return {
            'content': table_content,
            'input_tokens': table_res.usage_metadata.prompt_token_count,
            'output_tokens': table_res.usage_metadata.candidates_token_count,
            'itr': itr,
            'index': index  # Add index to maintain order
        }

def merge_results_in_order(results, table_result, isTemplateBased,invoice_obj):
    """Merge results from parallel processing in original order"""
    total_input_tokens = 0
    total_output_tokens = 0
    
    # Sort results by original index to maintain order
    sorted_results = sorted(results, key=lambda x: x['index'])
    
    for result in sorted_results:
        table_content = result['content']
        total_input_tokens += result['input_tokens']
        total_output_tokens += result['output_tokens']
        if 'type' in result and result['type'] == 'header':
            invoice_obj = result['content']
        elif not isTemplateBased:
            for table in table_content:
                if table in table_result:
                    table_result[table].extend(table_content[table])
                else:
                    table_result[table] = []
                    table_result[table].extend(table_content[table])
        else:
            for table in table_content:
                if table not in table_result:
                    table_result[table] = []

                content_rows = table_content[table]

                if content_rows and isinstance(content_rows[0], dict) and "InvoiceNo" in content_rows[0]:
                    # Get all existing InvoiceNos in table_result
                    existing_invoice_nos = {row["InvoiceNo"] for row in table_result[table] if "InvoiceNo" in row}

                    # Add only those rows which have a new InvoiceNo
                    for row in content_rows:
                        if "InvoiceNo" in row and row["InvoiceNo"] not in existing_invoice_nos:
                            table_result[table].append(row)
                else:
                    # No InvoiceNo key to check, just append all
                    table_result[table].extend(content_rows)
    
    return total_input_tokens, total_output_tokens, invoice_obj

# Main parallel processing implementation with order preservation
def process_page_ranges_parallel(page_ranges, page_output, prompt_format, table_obj, 
                                isTemplateBased, templateData, table_result, content, invoice_obj,
                                max_workers=5):
    """
    Process page ranges in parallel while maintaining original order
    
    Args:
        max_workers: Maximum number of parallel workers (adjust based on API rate limits)
    """
    input_token = 0
    output_token = 0
    # Use ThreadPoolExecutor for I/O bound operations (API calls)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks with their original index
        future_to_index = {
            executor.submit(
                process_single_page_range, 
                itr, page_output, prompt_format, table_obj, 
                isTemplateBased, templateData, index, content, invoice_obj,
            ): index for index, itr in enumerate(page_ranges)
        }
        
        # Collect results as they complete
        results = []
        for future in concurrent.futures.as_completed(future_to_index):
            index = future_to_index[future]
            try:
                result = future.result()
                results.append(result)
                print(f"Completed processing for index: {index}")
            except Exception as exc:
                print(f"Page range at index {index} generated an exception: {exc}")
                # You might want to handle this differently based on your needs
                continue
    
    # Merge all results in order
    total_input_tokens, total_output_tokens, invoice_obj = merge_results_in_order(results, table_result, isTemplateBased,invoice_obj)
    
    return total_input_tokens, total_output_tokens, invoice_obj

# Alternative implementation using executor.map for guaranteed order
def process_page_ranges_parallel_ordered(page_ranges, page_output, prompt_format, table_obj, 
                                        isTemplateBased, templateName, db, table_result, 
                                        max_workers=5):
    """
    Process page ranges in parallel with guaranteed order preservation using executor.map
    """
    input_token = 0
    output_token = 0
    
    def process_with_index(args):
        index, itr = args
        return process_single_page_range(
            itr, page_output, prompt_format, table_obj, 
            isTemplateBased, templateName, db, index
        )
    
    # Create list of (index, itr) pairs
    indexed_page_ranges = [(index, itr) for index, itr in enumerate(page_ranges)]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # executor.map maintains order automatically
        try:
            results = list(executor.map(process_with_index, indexed_page_ranges))
            
            # Process results in order (they're already ordered from executor.map)
            for result in results:
                table_content = result['content']
                input_token += result['input_tokens']
                output_token += result['output_tokens']
                
                if not isTemplateBased:
                    for table in table_content:
                        if table in table_result:
                            table_result[table].extend(table_content[table])
                        else:
                            table_result[table] = []
                            table_result[table].extend(table_content[table])
                else:
                    for table in table_content:
                        if table not in table_result:
                            table_result[table] = []

                        content_rows = table_content[table]

                        if content_rows and isinstance(content_rows[0], dict) and "InvoiceNo" in content_rows[0]:
                            existing_invoice_nos = {row["InvoiceNo"] for row in table_result[table] if "InvoiceNo" in row}
                            for row in content_rows:
                                if "InvoiceNo" in row and row["InvoiceNo"] not in existing_invoice_nos:
                                    table_result[table].append(row)
                        else:
                            table_result[table].extend(content_rows)
                            
        except Exception as exc:
            print(f"Parallel processing failed: {exc}")
            # Fallback to sequential processing if needed
            raise
    
    return input_token, output_token

# Alternative implementation with thread-safe result collection (ordered)
def process_page_ranges_parallel_threadsafe(page_ranges, page_output, prompt_format, table_obj, 
                                           isTemplateBased, templateName, db, table_result, 
                                           max_workers=5):
    """
    Process page ranges in parallel with thread-safe result collection and order preservation
    """
    input_token = 0
    output_token = 0
    lock = threading.Lock()
    ordered_results = [None] * len(page_ranges)  # Pre-allocate list to maintain order
    
    def process_and_store(index, itr):
        nonlocal input_token, output_token
        
        result = process_single_page_range(
            itr, page_output, prompt_format, table_obj, 
            isTemplateBased, templateName, db, index
        )
        
        # Store result in correct position
        ordered_results[index] = result
        
        # Update token counts thread-safely
        with lock:
            input_token += result['input_tokens']
            output_token += result['output_tokens']
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_and_store, index, itr) 
            for index, itr in enumerate(page_ranges)
        ]
        
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as exc:
                print(f"Task generated an exception: {exc}")
    
    # Process ordered results
    for result in ordered_results:
        if result is None:
            continue  # Skip failed tasks
            
        table_content = result['content']
        
        if not isTemplateBased:
            for table in table_content:
                if table in table_result:
                    table_result[table].extend(table_content[table])
                else:
                    table_result[table] = []
                    table_result[table].extend(table_content[table])
        else:
            for table in table_content:
                if table not in table_result:
                    table_result[table] = []

                content_rows = table_content[table]

                if content_rows and isinstance(content_rows[0], dict) and "InvoiceNo" in content_rows[0]:
                    existing_invoice_nos = {row["InvoiceNo"] for row in table_result[table] if "InvoiceNo" in row}
                    for row in content_rows:
                        if "InvoiceNo" in row and row["InvoiceNo"] not in existing_invoice_nos:
                            table_result[table].append(row)
                else:
                    table_result[table].extend(content_rows)
    
    return input_token, output_token

def fieldDetection(data,timestamp):
    combineLines = data['input']['combineLines']
    documentType = data['input']['mlInput']['documentType']
    model_name = data['input']['ai_model_name']
    config_value_json = data['input']['config_value_json']
    eventId = data['input']['eventId']
    ref_no = data['input']['refNo']
    templateName = data['input']['template_based']
    file_name = data['input']['mlInput']['filePath']
    
    print("3222222          ",documentType)    
    # print("aaaaaaaaaa          ",data['input'])    

    if config_value_json and 'dbConnection' in config_value_json:
        myclient = pymongo.MongoClient(config_value_json['dbConnection'])
        db = myclient[config_value_json['db']]
    else:
        myclient = pymongo.MongoClient(config['dbConnection'])
        db = myclient[config['db']]


    document_type_data = {}
    try:
        for y in db.get_collection("scanningfields").find():
            #print('   233   ',y['documentType'])
            if 'documentType' in y and y['documentType'] == documentType:
                #print("33 ",y)
                document_type_data = y
                break
    except Exception as e:
        print('Valid training file not found',e)
        return json.dumps({'status':400 , 'info':'Valid training file not found'})

    prompt_format = '''You are a helpful assistant. From the content provided by user populate the json, if value not present leave it empty.
    Table data can span across multiple pages too.The content provided by the user is Indian invoice.'''
    document_obj = {}
    table_obj = {}
    invoice_obj = {}
    headerContext = ''
    tableContext = ''
    checkTable = True
    isCSVExtraction = False
    isTemplateBased = False
    chunkSize = 1
    getChunkFromLLM = False
    print("chunk size ",chunkSize)

    if (document_type_data):
        for fields in document_type_data['fields']:
            if 'prompts' in fields and not fields['isTable']:
                document_obj[fields['fieldName']] = fields['prompts']
            elif fields['isTable'] and fields['tableName'] and 'prompts' in fields:
                if fields['tableName'] in table_obj:
                    table_obj[fields['tableName']][0][fields['fieldName']] = fields['prompts']
                else:
                    table_obj[fields['tableName']] = [{}]
                    table_obj[fields['tableName']][0][fields['fieldName']] = fields['prompts']
        
        if 'context' in document_type_data:
            headerContext = document_type_data['context']
        if 'tableContext' in document_type_data:
            tableContext = document_type_data['tableContext']
        if 'checkTable' in document_type_data:
            checkTable = document_type_data['checkTable']
        if 'isTemplateBased' in document_type_data:
            isTemplateBased = document_type_data['isTemplateBased']
        if 'isCSVExtraction' in document_type_data:
            isCSVExtraction = document_type_data['isCSVExtraction']
        if 'chunkSize' in document_type_data:
            chunkSize = get_numeric_value( document_type_data['chunkSize'],10)
            print("chunk size ",chunkSize)
        if 'getChunkFromLLM' in document_type_data:
            getChunkFromLLM = document_type_data['getChunkFromLLM']
            print("chunk size ",getChunkFromLLM)
            
            

    # print("Printing, table obj ,", table_obj)
    def Average(lst): 
        return sum(lst) / len(lst) 
    output = ''
    avg_height = []
    '''for page in combineLines:
        lines = page['lineWithCombineWordsNew']
        if(len(lines))>0:
            height = []
            for line in lines:
                for i, word  in enumerate(line):
                    height.append(int(word['bottomY']-word['topY']))
            avg_height.append(Average(height))

    for ind,page in enumerate(combineLines):
        lines = page['lineWithCombineWordsNew']
        if(len(lines))>0:
            flattened_lines = [word for line in lines for word in line]
            min_left_x = min(flattened_lines, key=lambda w:w['leftX'])['leftX']
            for line in lines:
                line_text = ''
                for i, word  in enumerate(line):
                    text = word['Name']
                    top_left_x = word['leftX']
                    top_left_y = word['topY']
                    bottom_right_x = word['rightX']
                    bottom_right_y = word['bottomY']
                    if i == 0:
                        dist = top_left_x-min_left_x
                        px_space = avg_height[ind]*0.6
                        horizontal_space = int((dist/px_space))
                        tab_space = math.floor(horizontal_space/8)
                        nor_space = horizontal_space%8
                        if horizontal_space > 0:
                            line_text +="\t"*tab_space + " "*nor_space
                    elif i > 0:
                        dist = (top_left_x+bottom_right_x)/2-min_left_x
                        px_space = avg_height[ind]*0.6
                        horizontal_space = math.ceil(dist/px_space)
                        tab_count = line_text.count('\t')
                        length_text = len(line_text) - tab_count + (tab_count*8)
                        final_space = math.floor(horizontal_space - length_text -len(text))
                        tab_space = math.floor(final_space/8)
                        nor_space = final_space%8
                        if final_space > 0:
                            line_text += "\t"*tab_space + " "*nor_space
                        else:
                            line_text += " "
                    line_text += text
                output += line_text
                output += '\n'
            output += '\n---PAGE END---'
    '''
    def ocr_to_html(ocr_data_page):
        html_content_final = []
        for page in ocr_data_page:
            html_content = '<div style="position: relative; width: 3600px; height: 4500px;">\n'
            for line in page['lineWithCombineWordsNew']:
                for item in line:
                    try:
                        leftX = item['leftX']
                        topY = item['topY']
                        rightX = item['rightX']
                        bottomY = item['bottomY']
                        text = item['text'] if 'text' in item else item['Name']

                        # Calculate width and height
                        width = rightX - leftX
                        height = bottomY - topY

                        # Create the span element with inline styles
                        span_element = f'<span style="position: absolute; left: {leftX}px; top: {topY}px; width: {width}px; height: {height}px;">{text}</span>\n'

                        html_content += span_element
                    except Exception as e:
                        print(e)
                        continue
            html_content += '</div>\n'
            html_content_final.append(html_content)
        return html_content_final

    def html_to_positioned_text(html_content, scale_factor=10):
        
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract all text elements with their positions
        positioned_elements = []

        # Find all elements with style attribute (both div and span)
        for element in soup.find_all(['div', 'span'], style=True):
            style = element.get('style', '')

            top_match = re.search(r'top:\s*(\d+(?:\.\d+)?)px', style)
            left_match = re.search(r'left:\s*(\d+(?:\.\d+)?)px', style)
            if top_match and left_match:
            # Scale down the positions for more manageable output
                top = int(float(top_match.group(1)) / scale_factor)
                left = int(float(left_match.group(1)) / scale_factor)
            # Extract top and left positions from style
            
                text = element.get_text().strip()

                if text:  # Only include elements with actual text
                    positioned_elements.append({
                        'text': text,
                        'top': top,
                        'left': left
                    })

        # Sort elements by top position first, then left position
        positioned_elements.sort(key=lambda x: (x['top'], x['left']))

        # Group elements by vertical position (with some tolerance)
        tolerance = 2  # Adjusted for scaled values
        current_line = []
        lines = []
        current_top = None

        for element in positioned_elements:
            if current_top is None:
                current_top = element['top']

            if abs(element['top'] - current_top) <= tolerance:
                current_line.append(element)
            else:
                if current_line:
                    lines.append(sorted(current_line, key=lambda x: x['left']))
                current_line = [element]
                current_top = element['top']

        if current_line:
            lines.append(sorted(current_line, key=lambda x: x['left']))

        # Convert to text output
        output_lines = []

        for line in lines:
            current_line = []
            current_pos = 0

            for element in line:
                # Add spaces to reach the desired horizontal position
                spaces_needed = max(0, element['left'] - current_pos)
                current_line.extend([' '] * spaces_needed)
                current_pos += spaces_needed

                # Add the text
                current_line.append(element['text'])
                current_pos += len(element['text'])

            output_lines.append(''.join(current_line))

        return '\n'.join(output_lines)

    def process_document_layout(combineLines):
        html_content = ocr_to_html(combineLines)
        output = ''
        for i, page in enumerate(html_content):
            res = html_to_positioned_text(page)
            output += res + \
                f'\n--------------PAGE Number: {i}. END OF PAGE-----------------------\n---PAGE END---'
        return output


    output = process_document_layout(combineLines)

    if not output:
        return json.dumps({'status':400 , 'info':'No data'})

    image_file_name = os.path.splitext(os.path.basename(file_name))[0]
    filename = f"{image_file_name}context.txt"
    file_path = '/home/user/save-data-here/public-folder/data/'+filename
    with open(file_path, "w") as file:
        file.write(output)
    table_result = {}
    input_token = 0
    output_token = 0
    if model_name == 'openai':
        if document_obj:
            header_chat_format = [
                {"role": "system", "content": prompt_format+'\n'+json.dumps(document_obj)},
                {"role": "user", "content": output}
            ]
            print("bool ", templateName  and isTemplateBased)
            print("bool ", templateName  ," check ", isTemplateBased)
            if  templateName  and isTemplateBased:
                templateData = list(db.get_collection("Genai_Prompt_Templates").find({'template_name':templateName}))
                print(type(templateData))
                # print("result ",templateData)
                templatePrompt = f'''
                You are an expert in document data extraction. For each invoice template, you are given the OCR data (raw text) and the corresponding expected JSON output that represents the structured data extracted from it. 
                Each template follows specific rules or patterns for extracting fields such as invoice number, date, seller details, buyer details, and line items. 
                Your task is to understand the extraction logic based on the provided OCR and JSON pair, learn the rules used to identify and extract each field, and then apply the same rules to extract structured data from new OCR inputs that follow the same template.
                ***Sample OCR data*** : {templateData[0]['input'][0]['input']}
                *** Expected JSON Output *** : {templateData[0]['input'][0]['header']}
                '''
                header_chat_format.insert(1,{"role": "system", "content": templatePrompt})

                
            if headerContext != '':
                header_chat_format.insert(1,{"role": "system", "content": headerContext})
            
            # print("Prompt ",header_chat_format)
            header_response = client.chat.completions.create(
                model="gpt-4.1",
                messages=header_chat_format,
                temperature=0.1,
                top_p=0.1)
            
            response_content = header_response.choices[0].message.content
            # print (response_content)
            token_info = header_response.usage
            input_token += token_info.prompt_tokens
            output_token += token_info.completion_tokens
            response_content = repair_json(response_content)
            invoice_obj = json.loads(response_content)

            if table_obj:
                invoice_obj['invoiceItems']= []
                invoice_obj['multiTable'] = []
                table_content ={}
                page_output = output.split('\n---PAGE END---')
                print('len gth of page',len(page_output))
                if checkTable is False:
                    print('inside check table for loop')
                    print("chunk size ",chunkSize)

                    for page in page_output[0:len(page_output)-1]:
                        table_chat_format = [
                            {"role": "system", "content": prompt_format+'\n'+json.dumps(table_obj)},
                            {"role": "user", "content": page}
                        ]
                        if  templateName  and isTemplateBased:
                            templateData = list(db.get_collection("Genai_Prompt_Templates").find({'template_name':templateName}))
                            print(type(templateData))
                            # print("result ",templateData)
                            templatePrompt = f'''
                            
                            You are an expert in document data extraction. For each invoice template, you are given the OCR data (raw text) and the corresponding expected JSON output that represents the structured data extracted from it. 
                            Each template follows specific rules or patterns for extracting fields such as invoice number, date, seller details, buyer details, and line items. 
                            Your task is to understand the extraction logic based on the provided OCR and JSON pair, learn the rules used to identify and extract each field, and then apply the same rules to extract structured data from new OCR inputs that follow the same template.
                            ***Sample OCR data*** : {templateData[0]['input'][0]['input']}
                            *** Expected JSON Output *** : {templateData[0]['input'][0]['table']}
                            '''
                            table_chat_format.insert(1,{"role": "system", "content": templatePrompt})
                        if tableContext != '':
                            table_chat_format.insert(1,{"role": "system", "content": tableContext})
                            
                        table_response = client.chat.completions.create(
                            model="gpt-4.1",
                            messages=table_chat_format,
                            temperature=0.1,
                            top_p=0.1)
                        print('completed 1 it')
                        table_content = table_response.choices[0].message.content
                        table_content = repair_json(table_content)
                        table_content = json.loads(table_content)
                        token_info_table = table_response.usage
                        input_token += token_info_table.prompt_tokens
                        output_token += token_info_table.completion_tokens
                        for table in table_content:
                            if (table in table_result):
                                table_result[table].extend(table_content[table])
                            else:
                                table_result[table] = []
                                table_result[table].extend(table_content[table])
                else:
                        print('inside check table single shot')
                        table_chat_format = [
                            {"role": "system", "content": prompt_format+'\n'+json.dumps(table_obj)},
                            {"role": "user", "content": output}
                        ]
                        if  templateName  and isTemplateBased:
                            templateData = list(db.get_collection("Genai_Prompt_Templates").find({'template_name':templateName}))
                            print(type(templateData))
                            # print("result ",templateData)
                            templatePrompt = f'''
                            
                            You are an expert in document data extraction. For each invoice template, you are given the OCR data (raw text) and the corresponding expected JSON output that represents the structured data extracted from it. 
                            Each template follows specific rules or patterns for extracting fields such as invoice number, date, seller details, buyer details, and line items. 
                            Your task is to understand the extraction logic based on the provided OCR and JSON pair, learn the rules used to identify and extract each field, and then apply the same rules to extract structured data from new OCR inputs that follow the same template.
                            ***Sample OCR data*** : {templateData[0]['input'][0]['input']}
                            *** Expected JSON Output *** : {templateData[0]['input'][0]['table']}
                            '''
                            table_chat_format.insert(1,{"role": "system", "content": templatePrompt})
                        if tableContext != '':
                            table_chat_format.insert(1,{"role": "system", "content": tableContext})
                            # print("table chat format",tableContext)
                        # print('table prompt ',table_chat_format)
                        table_response = client.chat.completions.create(
                            model="gpt-4.1",
                            messages=table_chat_format,
                            temperature=0.1,
                            top_p=0.1)
                        print('completed 1 it')
                        table_content = table_response.choices[0].message.content
                        table_content = repair_json(table_content)
                        table_content = json.loads(table_content)
                        token_info_table = table_response.usage
                        input_token += token_info_table.prompt_tokens
                        output_token += token_info_table.completion_tokens
                        for table in table_content:
                            if (table in table_result):
                                table_result[table].extend(table_content[table])
                            else:
                                table_result[table] = []
                                table_result[table].extend(table_content[table])
                
    elif model_name == 'deepseek':
        if document_obj:
            header_chat_format = [
                {"role": "system", "content": prompt_format+'\n'+json.dumps(document_obj)},
                {"role": "user", "content": output}
            ]
            deepClient = OpenAI(
                api_key=os.environ["DEEPSEEK_API_KEY"],
                base_url="https://api.deepseek.com/v1"
            )
            print("bool ", templateName  and isTemplateBased)
            print("bool ", templateName  ," check ", isTemplateBased)
            if  templateName  and isTemplateBased:
                templateData = list(db.get_collection("Genai_Prompt_Templates").find({'template_name':templateName}))
                print(type(templateData))
                # print("result ",templateData)
                templatePrompt = f'''
                You are an expert in document data extraction. For each invoice template, you are given the OCR data (raw text) and the corresponding expected JSON output that represents the structured data extracted from it. 
                Each template follows specific rules or patterns for extracting fields such as invoice number, date, seller details, buyer details, and line items. 
                Your task is to understand the extraction logic based on the provided OCR and JSON pair, learn the rules used to identify and extract each field, and then apply the same rules to extract structured data from new OCR inputs that follow the same template.
                ***Sample OCR data*** : {templateData[0]['input'][0]['input']}
                *** Expected JSON Output *** : {templateData[0]['input'][0]['header']}
                '''
                header_chat_format.insert(1,{"role": "system", "content": templatePrompt})
            if headerContext != '':
                header_chat_format.insert(1,{"role": "system", "content": headerContext})
            # print ('Header query', header_chat_format)
            header_response = deepClient.chat.completions.create(
                model="deepseek-chat",
                messages=header_chat_format,
                temperature=0.1,
                top_p=0.1)
            
            response_content = header_response.choices[0].message.content
            # print (response_content)
            token_info = header_response.usage
            input_token += token_info.prompt_tokens
            output_token += token_info.completion_tokens
            response_content = repair_json(response_content)
            invoice_obj = json.loads(response_content)

            if table_obj:
                invoice_obj['invoiceItems']= []
                invoice_obj['multiTable'] = []
                page_output = output.split('\n---PAGE END---')
                print('len gth of page',len(page_output))
                if checkTable is False:
                    for page in page_output[0:len(page_output)-1]:
                        table_chat_format = [
                            {"role": "system", "content": prompt_format+'\n'+json.dumps(table_obj)},
                            {"role": "user", "content": page}
                        ]
                        if  templateName  and isTemplateBased:
                            templateData = list(db.get_collection("Genai_Prompt_Templates").find({'template_name':templateName}))
                            print(type(templateData))
                            # print("result ",templateData)
                            templatePrompt = f'''
                            You are an expert in document data extraction. For each invoice template, you are given the OCR data (raw text) and the corresponding expected JSON output that represents the structured data extracted from it. 
                            Each template follows specific rules or patterns for extracting fields such as invoice number, date, seller details, buyer details, and line items. 
                            Your task is to understand the extraction logic based on the provided OCR and JSON pair, learn the rules used to identify and extract each field, and then apply the same rules to extract structured data from new OCR inputs that follow the same template.
                            ***Sample OCR data*** : {templateData[0]['input'][0]['input']}
                            *** Expected JSON Output *** : {templateData[0]['input'][0]['table']}
                            '''
                            table_chat_format.insert(1,{"role": "system", "content": templatePrompt})
                        if tableContext != '':
                            table_chat_format.insert(1,{"role": "system", "content": tableContext})
                            # print("table chat format",tableContext)

                        table_response = deepClient.chat.completions.create(
                            model="deepseek-chat",
                            messages=table_chat_format,
                            temperature=0.1,
                            top_p=0.1)
                        print('completed 1 it')
                        table_content = table_response.choices[0].message.content
                        table_content = repair_json(table_content)
                        table_content = json.loads(table_content)
                        token_info_table = table_response.usage
                        input_token += token_info_table.prompt_tokens
                        output_token += token_info_table.completion_tokens
                        for table in table_content:
                            if (table in table_result):
                                table_result[table].extend(table_content[table])
                            else:
                                table_result[table] = []
                                table_result[table].extend(table_content[table])           
                else:
                        print('inside check table single shot')
                        table_chat_format = [
                            {"role": "system", "content": prompt_format+'\n'+json.dumps(table_obj)},
                            {"role": "user", "content": output}
                        ]
                        if  templateName  and isTemplateBased:
                            templateData = list(db.get_collection("Genai_Prompt_Templates").find({'template_name':templateName}))
                            print(type(templateData))
                            # print("result ",templateData)
                            templatePrompt = f'''
                            You are an expert in document data extraction. For each invoice template, you are given the OCR data (raw text) and the corresponding expected JSON output that represents the structured data extracted from it. 
                            Each template follows specific rules or patterns for extracting fields such as invoice number, date, seller details, buyer details, and line items. 
                            Your task is to understand the extraction logic based on the provided OCR and JSON pair, learn the rules used to identify and extract each field, and then apply the same rules to extract structured data from new OCR inputs that follow the same template.
                            ***Sample OCR data*** : {templateData[0]['input'][0]['input']}
                            *** Expected JSON Output *** : {templateData[0]['input'][0]['table']}
                            '''
                            table_chat_format.insert(1,{"role": "system", "content": templatePrompt})
                        if tableContext != '':
                            table_chat_format.insert(1,{"role": "system", "content": tableContext})
                            # print("table chat format",tableContext)
                        print('table prompt ',table_chat_format)
                        table_response = deepClient.chat.completions.create(
                            model="deepseek-chat",
                            messages=table_chat_format,
                            temperature=0.1,
                            top_p=0.1)
                        print('completed 1 it')
                        table_content = table_response.choices[0].message.content
                        table_content = repair_json(table_content)
                        table_content = json.loads(table_content)
                        token_info_table = table_response.usage
                        input_token += token_info_table.prompt_tokens
                        output_token += token_info_table.completion_tokens
                        for table in table_content:
                            if (table in table_result):
                                table_result[table].extend(table_content[table])
                            else:
                                table_result[table] = []
                                table_result[table].extend(table_content[table])
                     
    elif model_name == 'gemini':
        # model = genai.GenerativeModel('gemini-2.0-flash')
        if document_obj:
            content = prompt_format+'\n'+json.dumps(document_obj)+'\n\n'+output
            print("bool ", templateName  and isTemplateBased)
            print("bool ", templateName  ," check ", isTemplateBased)
            if  isTemplateBased:
                print("Inside template based")
                templateData = list(db.get_collection("Genai_Prompt_Templates").find({'template_name':templateName}))
                print(type(templateData))
                # print("result ",templateData)
                print("length of template data ",len(templateData))
                templatePrompt = f'''
                You are a highly accurate and efficient document data extraction assistant.

                Below is a sample template showing the structure and style of documents similar to the input:
                Example Sample (Input → Output):
                ***Input*** : {templateData[0]['input'][0]['input']}
                ***Output*** : {templateData[0]['input'][0]['header']}
                
                The Above Input and Output is a sample template showing the structure and style of documents similar to the input.
                The output needs to be completly derived or extracted from the  'New Input' provided by the user.

                Instructions:
                - Strictly follow the field names and extraction logic as described in the Extraction Rules.
                - If a field's value is missing, leave it blank ("") or null.
                - Do not create any extra fields not mentioned in the extraction rules.
                - Use only the information present in the New Input document.

                New Input:
                {output}
            
                You must extract the information only based on the fields listed below.

                Extraction Fields:
                {json.dumps(document_obj, indent=2)}

                You must use the context provided,and strictly populate ALL fields in the  JSON object.
                If any field value is missing or unavailable in the document, leave it as an empty string (""). 
                Populate the output JSON: Respond **only** with this code block:
                ```json{{result}}```
                '''
                content = templatePrompt
            # print("nnnn    ",content)
            if not table_obj:
                response = make_api_call_with_retry(content,'gemini-2.0-flash') #genaiclient.models.generate_content(model='gemini-2.0-flash',contents=content)
                # response = model.generate_content(content)
                # print("response ", response)
                invoice_obj = format_json_llm(response.text)
                input_token+=response.usage_metadata.prompt_token_count
                output_token+=response.usage_metadata.candidates_token_count
                avg_height = output.split('\n---PAGE END---')
                print('invoice_obj ',invoice_obj)
                invoice_obj['invoiceItems']= []
                invoice_obj['multiTable'] = []
            else:
                invoice_obj = {}
                avg_height = output.split('\n---PAGE END---')
                invoice_obj['invoiceItems']= []
                invoice_obj['multiTable'] = []
            if table_obj:
                table_content ={}
                print("11111111111  ",checkTable)
                page_output = output.split('\n---PAGE END---')
                if checkTable is False:
                    print("222222222  ",len(page_output), ' chunk size ',chunkSize)
                    page_ranges = []
                    for i in range(0, len(page_output), chunkSize):
                        range_end = min(i + chunkSize - 1, len(page_output))
                        page_ranges.append([i, range_end])
                    print("page ranges ", page_ranges)
                    

                    if getChunkFromLLM and len(avg_height)>10:
                        print("get chunk from llm ",getChunkFromLLM)
                        prompt = f'''
                        You are an intelligent document analysis assistant. You will receive the OCR output of a multi-page document. Your task is to determine logical page ranges (chunks) to split the document for downstream processing.
                        
                        Instructions:
                        1. Each chunk should be less than less than or equal to 10 pages.
                        2. If a **table row spans across multiple pages**, ensure that the entire row is contained within the same chunk.
                        - For example, if a row starts on page 10 and ends on page 11, then both pages must be included in the same chunk.
                        - Avoid assigning such pages to separate chunks.
                        3. Your goal is to return a list of page ranges that satisfy both the **page limit** and **row continuity** rules.
                        4. And we are extracting the date only from the Invoice Documents, if there is other than invoice documents, Dont include those page ranges,
                        5. Need only the page ranges that are relevant to the Invoice Documents, if there is any other document, then dont include those page ranges.
                        6. The other documents may be Shipping Documents, Packing List, Delivery Note, etc. Only need to include the Invoice Document page ranges.
                        7. Need to number the invoice_slno based on the numberth of invoice document's order present in the full document
                        8. the invoice_slno should not be taken from the invoice number of the document, it should be generated based on the order of the invoice documents present in the full document.
                        Input:
                        {output}


                        Notes:
                        - Page numbers start from 0.
                        - No chunk should exceed 10 pages unless required to preserve a row spanning across pages.
                        - Ensure that no table row appears partially in one chunk and partially in another.
                        -  Make sure the range should be inclusive of the start and end page numbers.
                        - invoice_numbers should contain the number of invoice starting from 1. If there is more than 1 invoice inside chunk provide it in a list.

                        Output:
                        - Provide a JSON object in this format.
                            ```json{{
                                'page_ranges': [{{start:'',end:'',invoice_slno:[]}},{{start:'',end:'',invoice_slno:[]}},...]
                            }}```                        
                        
                        '''

                        chunkResponse =  make_api_call_with_retry(prompt,"gemini-2.5-flash")
                        # print("Hellooo     hello    ",table_res.text)
                        input_token+=chunkResponse.usage_metadata.prompt_token_count
                        output_token+=chunkResponse.usage_metadata.candidates_token_count
                        chunkJSON = format_json_llm(chunkResponse.text)
                        print("table response ", chunkJSON)
                        if 'page_ranges' in chunkJSON:
                            page_ranges = chunkJSON['page_ranges']
                    else:
                        page_ranges = [{'start':0,'end':len(avg_height)-1,'invoice_slno':None}]


                    print("page ranges ", page_ranges)
                    page_ranges.insert(0,{'type':'header'})
                    input_token, output_token, invoice_obj = process_page_ranges_parallel(
                        page_ranges, page_output, prompt_format, table_obj, 
                        isTemplateBased, templateData, table_result, content, invoice_obj,
                        max_workers=5  # Adjust based on your API rate limits
                    )

                else:
                    print("333333333333  ")
                    
                    table_chat_format = prompt_format+'\n'+json.dumps(table_obj)+'\n\n'+output
                    if  isTemplateBased:
                            print("Inside template based")
                            templateData = list(db.get_collection("Genai_Prompt_Templates").find({'template_name':templateName}))
                            print(type(templateData))
                            # print("result ",templateData)
                            
                            if not isCSVExtraction :
                                print("Inside JSON Extraction")
                                templatePrompt = f'''
                                You are a highly accurate and efficient document data extraction assistant.

                                Below is a sample template showing the structure and style of documents similar to the input:
                                Example Sample (Input → Output):
                                ***Input*** : {templateData[0]['input'][0]['input']}
                                ***Output*** : {templateData[0]['input'][0]['table']}



                                The Above Input and Output is a sample template showing the structure and style of documents similar to the input.
                                The output needs to be completly derived or extracted from the  'New Input' provided by the user.

                                Instructions:
                                - Strictly follow the field names and extraction logic as described in the Extraction Rules.
                                - If a field's value is missing, leave it blank ("") or null.
                                - Do not create any extra fields not mentioned in the extraction rules.
                                - Use only the information present in the New Input document.


                                The Output need to be generated only with the below context. 
                                The example input and output is given only for the reference of the structure and style of the document.
                                The output needs to be completly derived or extracted from the  'New Input' provided by the user. 
                                The Reference should not impact the output in any way.
                                New Input:
                                {output}
                            
                                You must extract the information only based on the fields listed below.

                                Extraction Fields:
                                {json.dumps(table_obj, indent=2)}


                                You must use the context provided,and strictly populate ALL fields in the  JSON object.
                                If any field value is missing or unavailable in the document, leave it as an empty string (""). 
                                Populate the output JSON: Respond **only** with this code block:
                                ```json{{result}}```
                                '''
                                table_chat_format= templatePrompt
                                table_res =  make_api_call_with_retry(table_chat_format,"gemini-2.5-flash")
                                print("Output token ",table_res.usage_metadata.candidates_token_count)
                                input_token+=table_res.usage_metadata.prompt_token_count
                                output_token+=table_res.usage_metadata.candidates_token_count


                                table_content = format_json_llm(table_res.text)


                            else:
                                print("Inside CSV Extraction")
                                table_content={}
                                for key,value in table_obj.items():
                                    temp={}
                                    temp[key] = value
                                    # print("temp ",temp)
                                    templatePrompt = f'''
                                    You are a highly accurate and efficient document data extraction assistant.

                                    Below is a sample template showing the structure and style of documents similar to the input:
                                    Example Sample (Input → Output):
                                    ***Input*** : {templateData[0]['input'][0]['input']}
                                    ***Output*** : {templateData[0]['input'][0]['table']}

                                    Instructions:
                                    - Strictly follow the field names and extraction logic as described in the Extraction Rules.
                                    - If a field's value is missing, leave it blank ("") or null.
                                    - Do not create any extra fields not mentioned in the extraction rules.
                                    - Use only the information present in the New Input document.

                                    The Output need to be generated only with the below context. 
                                    The example input and output is given only for the reference of the structure and style of the document.
                                    The output needs to be completly derived or extracted from the  'New Input' provided by the user. 
                                    The Reference should not impact the output in any way.
                                    
                                    New Input:
                                    {output}
                                
                                    You must extract the information only based on the fields listed below.

                                    Extraction Fields:
                                    {json.dumps(temp, indent=2)}


                                    You must use the context provided, and strictly populate ALL fields in the CSV.
                                    If any field value is missing or unavailable in the document, leave it as an empty string ("").
                                    since we are getting the output as csv data, the comma in numbers or any other place may cause the other discrepencies, 
                                    so always give all the values in the string format(inside quoatation "" )
                                    
                                    Since we are populating the output as CSV, please ensure that the values are properly formatted as CSV.
                                    The First row should contain the header names, and the subsequent rows should contain the corresponding values.
                                    It is very very crucial that the csv data should have the header. And the header and the  number of columns in each row must be same.
                                    Please ensure that the CSV is well-formed and can be easily parsed.

                                    Populate the output CSV: Respond **only** with this code block:
                                    ```csv
                                    <your csv output here>```
                                    '''
                                    table_chat_format= templatePrompt
                                    #gemini API call
                                    table_res =  make_api_call_with_retry(table_chat_format,"gemini-2.5-flash")
                                    #token calculations
                                    input_token+=table_res.usage_metadata.prompt_token_count
                                    output_token+=table_res.usage_metadata.candidates_token_count
                                    print("Output token ",table_res.usage_metadata.candidates_token_count)
                                    #converting csv to json
                                    print("csv response : ",table_res.text)
                                    table_content[key] = format_csv_to_llm(table_res.text)
                                    # print("data " , format_csv_to_llm(table_res.text))
                                    # print("csv JSON response : ",table_content)
                    else:
                        print("chcking   ",table_chat_format)
                        table_res =  make_api_call_with_retry(table_chat_format,"gemini-2.5-flash")
                        input_token+=table_res.usage_metadata.prompt_token_count
                        output_token+=table_res.usage_metadata.candidates_token_count


                        table_content = format_json_llm(table_res.text)




                   
                    # print("table content ", table_content)
                    for table in table_content:
                        print("Inside table, is it workign fine.")

                        if (table in table_result):
                            table_result[table].extend(table_content[table])
                        else:
                            table_result[table] = []
                            table_result[table].extend(table_content[table])

    if (table_result):
        print("Inside table, is it workign fine.")
        if not 'multiTable' in invoice_obj:
            invoice_obj['multiTable'] = []
        for table in table_result:
            invoice_obj['multiTable'].append({table: table_result[table]})

    print ('Prediction result', invoice_obj)
    df = pd.read_csv(file_name)
    prediction = invoice_obj

    df['Property'] = 'undefined'

    '''for key in prediction:
        if isinstance(prediction[key],str):
            prediction_words = prediction[key].split()
            for index, row in df.iterrows():
                name_str = str(row['Name'])
                if len(prediction[key].split())!=0 and (name_str.lower() in prediction_words[0].lower()):
                    match = True
                    if(index+len(prediction_words) < df.shape[0]):
                        for i in range(1, len(prediction_words)):
                            if prediction_words[i].lower() not in str(df.iloc[index + i]['Name']).lower():
                                match = False
                                break

                    if (match):
                        for i in range(0, len(prediction_words)):
                            if (index+len(prediction_words) < df.shape[0]) and (df.iloc[index+i]['Property']) == 'undefined':
                                df.at[index + i, 'Property'] = key
                        break;'''
    
    if not isTemplateBased:
        for key in prediction:
            if isinstance(prediction[key],str):
                prediction_words = prediction[key].split()
                word_length = len(prediction_words)
                match = False
                prediction_value = prediction[key].lower()
                threshold = 0.7
                if(word_length > 12):
                    prediction_value = prediction_words[3:word_length-4]
                    word_length = len(prediction_value)
                    print (word_length)
                    threshold = 0.5
                    prediction_value = ' '.join(prediction_value)
                for index, row in df.iterrows():
                    name_str = str(row['Name']).lower()
                    index_list = [index]
                    for i in range(1,word_length):
                        if(index+len(prediction_words)<df.shape[0]):
                            index_list.append(index+i)
                            name_str += ' '+ str(df.iloc[index + i]['Name']).lower()
                    if(similar((name_str), (prediction_value))>threshold):
                        print(name_str, word_length, index_list)
                        match=True

                    if (match):
                        print (name_str,prediction_words)
                        for i in range(0, len(index_list)):
                            if ((df.iloc[index_list[i]]['Property']) == 'undefined'):
                                df.at[index_list[i], 'Property'] = key
                        break;

    def renumber_items(data_list):
        """
        Renumbers ItemSlNo to be sequential based on InvoiceSlNo grouping.
        Items with the same InvoiceSlNo will have consecutive ItemSlNo values.
        """
        # Group by InvoiceSlNo and renumber within each group
        invoice_groups = {}
        
        # First, group items by InvoiceSlNo
        for item in data_list:
            invoice_no = int(item['InvoiceSlNo'])
            if invoice_no not in invoice_groups:
                invoice_groups[invoice_no] = []
            invoice_groups[invoice_no].append(item)
        
        # Renumber ItemSlNo within each invoice group
        for invoice_no in sorted(invoice_groups.keys()):
            for idx, item in enumerate(invoice_groups[invoice_no], 1):
                item['ItemSlNo'] = idx
        
        return data_list
    
    if isTemplateBased:
        multi_table = invoice_obj.get("multiTable", [])
        templateData = db.get_collection("Genai_Prompt_Templates").find_one({'template_name':templateName})
        print(type(templateData))
        # print("tem[plate data ] ",templateData)
        if templateData :
            print("Inside template data for empting the unwanted keys")
            if 'headerJSON' in templateData:
                
                headerJSON = templateData['headerJSON']

                # print("headerJSON ",headerJSON)
                # print("invoice_obj ",invoice_obj)
                if headerJSON:
                    headerJSON['multiTable']="multiTable"
                    headerJSON['Invoice Details']="Invoice Details"
                    headerJSON['STatus']="STatus"
                    print("headerJSON ")
                    for key in invoice_obj:
                        # print("key ",key in invoice_obj)
                        # if  key in headerJSON:
                        #     # print("key allowed ",key)
                        # else:
                        #     # print("key not allowed ",key)
                        #     invoice_obj[key] = ""  # key not allowed → set empty
                        if not key in headerJSON:                            
                            # print("key not allowed ",key)
                            invoice_obj[key] = ""  # key not allowed → set empty

        for table in multi_table:        
            keys = table.keys()
            print(keys)
            if "Invoice Details" in table:
                print("Invoice Details undwnated keys")

                keys = table.keys()
                print(keys)
                
                
                if 'InvoiceDetails' in templateData:
                    # print("Invoice Details undwnated keys ",templateData['InvoiceDetails'])

                    InvoiceDetails = templateData['InvoiceDetails']
                    InvoiceDetails['multiTable']="multiTable"
                    print("InvoiceDetails ",InvoiceDetails)
                    # print("invoice_obj ",invoice_obj)
                    if InvoiceDetails:
                        print("InvoiceDetails ")
                        for item in table["Invoice Details"]:
                            for key in item:
                                # # print("key ",key in invoice_obj)
                                # if  key in InvoiceDetails:
                                #     print("key allowed ",key)
                                # else:
                                #     print("key not allowed ",key)
                                #     item[key] = ""  # key not allowed → set empty
                                if not key in InvoiceDetails:
                                    item[key] = ""  # key not allowed → set empty
                for idx, invoice in enumerate(table["Invoice Details"], start=1):
                    invoice["InvoiceSLNo"] = idx  # preserve string format

            
            if "Item Details" in table:
                # for item in table['Item Details']:
                #     print(f"Invoice: {item['InvoiceSlNo']}, Item: {item['ItemSlNo']}, Desc: {item['ItemDesc'][:20]}...")
                # for item in table['Item Details']:
                #     print(f"Invoice: {item['InvoiceSlNo']}, Item: {item['ItemSlNo']}, Desc: {item['ItemDesc'][:20]}...")
                print("Invoice Details undwnated keys")

                # for idx, item in enumerate(table["Item Details"], start=1):
                #     item["itemSlNo"] = idx  # keep as int (based on your input)
                
                if 'ItemDetails' in templateData:
                    print("Item Details undwnated keys ",templateData['ItemDetails'])
                    ItemDetails = templateData['ItemDetails']
                    
                    print("ItemDetails ",ItemDetails)
                    # print("invoice_obj ",invoice_obj)
                    if ItemDetails:
                        ItemDetails['ItemSlNo']="ItemSlNo"
                        print("ItemDetails ")
                        for item in table["Item Details"]:
                            for key in item:
                                # print("key ",key in invoice_obj)
                                if  key in ItemDetails:
                                    print("key allowed ",key)
                                else:
                                    print("key not allowed ",key)
                                    item[key] = ""  # key not allowed → set empty

                if documentType == 'EXPORT':
                    for idx, item in enumerate(table["Item Details"], start=1):
                        item["ItemSlNo"] = idx  # keep as int (based on your input)

                else:
                    table['Item Details'] = renumber_items(table['Item Details'])
            if 'ShipmentContainerDetails' in table:  
                print("shipment container details 1st level")
                if 'ShipmentContainerDetails' in templateData  :
                    # print("Item Details undwnated keys ",templateData['ItemDetails'])
                    ShipmentContainerDetails = templateData['ShipmentContainerDetails']
                    
                    print("ShipmentContainerDetails ",ShipmentContainerDetails)
                    # print("invoice_obj ",invoice_obj)
                    if ShipmentContainerDetails:
                        ShipmentContainerDetails['Containerslno']="Containerslno"
                        print(" inside ShipmentContainerDetails ")
                        for item in table["ShipmentContainerDetails"]:
                            for key in item:
                                # print("key ",key in invoice_obj)
                                if  key in ShipmentContainerDetails:
                                    print("key allowed ",key)
                                else:
                                    print("key not allowed ",key)
                                    item[key] = ""  # key not allowed → set empty

                


                if documentType == 'EXPORT':
                    for idx, item in enumerate(table["ShipmentContainerDetails"], start=1):
                        item["Containerslno"] = idx  # keep as int (based on your input)    
       

    import csv
    from bson.objectid import ObjectId
    df.to_csv(file_name,quoting=csv.QUOTE_NONNUMERIC,index=None)
    invoice_obj['referenceNumber'] = ref_no
    invoice_obj['fileName'] = file_name
    invoice_obj['orgId'] = data['input']['orgId']
    invoice_obj['userId'] = ObjectId(data['input']['userId'])
    invoice_obj['subscriberId'] = ObjectId(data['input']['subscriberId'])
    from datetime import datetime
    invoice_obj['createdAt'] = datetime.now()
    invoice_obj['updatedAt'] = datetime.now()
    invoice_obj['isTmp'] = False
    invoice_obj['ocrConfidence'] = []
    invoice_obj['Status'] = 'Pending'
    invoice_obj['Invoice_Status'] = 'InProgress'
   
    try:
        fileUploadHistories = db.get_collection('fileuploadhistories').find_one({'fileRefNum':ref_no},{'filePath':1,'fileName':1})
        # print ('hello   ',fileUploadHistories)
        invoice_obj['filePath'] = fileUploadHistories['filePath']
        invoice_obj['file_name'] = fileUploadHistories['fileName']
    except Exception as e:
        print ("errror ",e)


           
    
    print("invoice_obj ", invoice_obj)
    

    try:
        db.get_collection(documentType).insert_one(invoice_obj)
        # db.get_collection("filequeues").update_one({'fileRefNum':ref_no},{"$set":{'status':"Success"}})
    except Exception as e:
        print (e)
        outputData={'mlOutput':'Not inserted in db' , 'statusCode': '400'}
        with open("file_"+timestamp+".json", "w") as f:
            json.dump(outputData, f)
            return str(1)

    del invoice_obj['_id']
    invoice_obj['createdAt'] = str(invoice_obj['createdAt'])
    del invoice_obj['updatedAt']
    del invoice_obj['subscriberId']
    del invoice_obj['userId']
    del invoice_obj['orgId']
    token_details = {}
    token_details['input_token'] = input_token
    token_details['output_token'] = output_token
    token_details['filename'] = file_name
    token_details['ref_no'] = ref_no
    token_details['page_count'] = len(avg_height)
    token_details['orgId'] = data['input']['orgId']
    token_details['subscriberId'] = data['input']['subscriberId']
    token_details['userId'] = data['input']['userId']
    token_details['model'] = model_name
    from datetime import datetime
    from zoneinfo import ZoneInfo
    ist = ZoneInfo("Asia/Kolkata")
    token_details['createdAt'] = datetime.now(ist)
    token_details['documentType'] = documentType
    token_details['templateName'] = templateName
    token_details['updatedAt'] = datetime.now(ist)
    try:
        db.get_collection('LLM_Tokens').insert_one(token_details)
    except Exception as e:
        print (e)
    if data['input'].get('return',False):
        try:
            db.get_collection('filequeues').update_one({'fileRefNum':ref_no},{'$set':{'status':'Success'}})
        except Exception as e:
            print(e)
    outputData = {'mlOutput':'Done','data':invoice_obj,'statusCode':'200'}
    with open('token_count.json',"w") as fi:
        json.dump(token_usage_all,fi)

    with open("file_"+timestamp+".json", "w") as f:
        json.dump(outputData, f)
    return outputData

def get_numeric_value(value, default=10):
    if value is None:
        return default
    elif isinstance(value, (int, float)):
        return value
    elif isinstance(value, str):
        try:
            return float(value) if '.' in value else int(value)
        except ValueError:
            return default  # If string is not convertible
    else:
        return default  # For any other type



if __name__=="__main__":
    start = time.time()
    print("\n\n\n\n[INFO] FILE TRIGGER ..", get_args()[0],"\t",get_args()[1], "\n\n")
    fieldDetection(json.load(open(get_args()[0], "r")), get_args()[1])
    end = time.time()
    print('Exec', end-start)