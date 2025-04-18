import time
import gc
import json
import math
import os
import re
from json_repair import repair_json
import pandas as pd
import pymongo
import torch
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
config={}
with open('config.json', 'r') as f:
    config = json.load(f)
from bs4 import BeautifulSoup
import requests
from fuzzywuzzy import fuzz, process
from transformers import AutoTokenizer
#tokenizer = AutoTokenizer.from_pretrained('/home/anil/models--NousResearch--Hermes-3-Llama-3.1-8B/snapshots/896ea440e5a9e6070e3d8a2774daf2b481ab425b')
#tokenizer = AutoTokenizer.from_pretrained('/home/anil/Qwen2.5-14B-Instruct-awq')
import argparse
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
def create_temp_format(template):
    if(isinstance(template['input'],str)):
        return f'''Example Sample 1 (Input → Output):
Input:
{template['input']}
Output:
{template['output']}'''
    elif(isinstance(template['input'],list)):
        final_template = ''
        for i,temp in enumerate(template['input']):
            final_template += f'''Example Sample {i+1} (Input → Output):
Input:
{template['input'][i]}
Output:
{template['output'][i]}\n\n'''
        return final_template
    
def create_temp_format_2(template):
    if(isinstance(template['output'],str)):
        return f'''Example Sample 1 (Input → Output):
Input:
{template['output']}
Output:
{template['output2']}'''
    elif(isinstance(template['output'],list)):
        final_template = ''
        for i,temp in enumerate(template['output']):
            final_template += f'''Example Sample {i+1} (Input → Output):
Input:
{template['output'][i]}
Output:
{template['output2'][i]}\n\n'''
        return final_template

from difflib import SequenceMatcher
import csv
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()
import pandas as pd


import subprocess
def get_gpu_memory_usage():
    # Run nvidia-smi command to get GPU memory usage
    result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], stdout=subprocess.PIPE, text=True)
    
    # Extract and return GPU memory usage in MiB
    gpu_memory_usage = int(result.stdout.strip())
    return gpu_memory_usage

def response_generation(instruction, input, max_tokens=1000):
    url = "http://localhost:8000/generate"
    content = f'Input:{input}\nInstruction: Output json use double quotes. {instruction} ```json{{result}}```'
    req_data = {
        "prompt": content,
        "n": 1,
        "best_of": 1,
        "temperature": 0.0,
        "min_tokens": 10,
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(url, json=req_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response_json = response.json()
        
        
        # Updated regex to find only the first JSON object
        regex_pattern = r'```json{result}```[.\s\S]*```json[\s]*(\{[\s]*[.\s\S]{7,}?\})[\s]*```'
        match = re.search(regex_pattern, response_json['text'][0], re.DOTALL)
        if not match:
            regex_pattern = r'```json{{result}}```[.\s\S]*```json[\s]*(\{[\s]*[.\s\S]{7,}?\})[\s]*```'
            match = re.search(regex_pattern, response_json['text'][0], re.DOTALL)
        if match:
            json_text = match.group(1)
            print('Extracted JSON text:', json_text)
            try:
                return json.loads(json_text)
            except Exception as e:
                try:
                    json_text = repair_json(json_text)
                    return json.loads(json_text)
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error with text: {json_text}")
                    print(f"Error: {e}")
                    return None
        
        else:
            print("No JSON found in the output.")
            return None

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        return None

def response_generation_new(content, max_tokens=1000):
    url = "http://localhost:8000/generate"
    
    req_data = {
        "prompt": content,
        "n": 1,
        "best_of": 1,
        "temperature": 0.0,
        "min_tokens": 10,
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(url, json=req_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response_json = response.json()
        
        print(response_json['text'][0])
        # Updated regex to find only the first JSON object
        regex_pattern = r'```json{result}```[.\s\S]*```json[\s]*(\{[\s]*[.\s\S]{7,}?\})[\s]*```'
        match = re.search(regex_pattern, response_json['text'][0], re.DOTALL)
        
        if match:
            json_text = match.group(1)
            print('Extracted JSON text:', json_text)
            try:
                return json.loads(json_text)
            except Exception as e:
                try:
                    json_text = repair_json(json_text)
                    return json.loads(json_text)
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error with text: {json_text}")
                    print(f"Error: {e}")
                    return None
        else:
            print("No JSON found in the output.")
            return None


    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        return None


def response_generation_text(content, max_tokens=1000):
    url = "http://localhost:8000/generate"
    
    req_data = {
        "prompt": content,
        "n": 1,
        "best_of": 1,
        "temperature": 0.0,
        "min_tokens": 10,
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(url, json=req_data)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        response_json = response.json()
        
        start = response_json['text'][0].find('```Text{result}```')+len('```Text{result}```')
        end = response_json['text'][0][start:].find('END OF RESULT')
        result = response_json['text'][0][start:]
        print(result)
        #print(response_json['text'][0])
        # Updated regex to find only the first JSON object
        return response_json['text'][0][start:]

    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON decoding failed: {e}")
        return None


def fieldDetection(data,timestamp):
    combineLines = data['input']['combineLines']
    documentType = data['input']['mlInput']['documentType']
    model_name = data['input']['ai_model_name']
    config_value = data['input']['configValue'] #config values coming from bot input
    org_id = data['input']['orgId']


    if config_value:
        print (config_value)
        config_value = config_value.replace("'", "\"")
        config_value_json = json.loads(config_value)
        data['input']['config_value_json'] = config_value_json
    eventId = data['input']['eventId']
    try:
        type_check = data['input']['type_check']
    except Exception as e:
        print(e)
        print('Making  Type check empty --')
        type_check = 'yes'
    ref_no = data['input']['refNo']
    file_name = data['input']['mlInput']['filePath']
    if config_value_json and 'dbConnection' in config_value_json:
        myclient = pymongo.MongoClient(config_value_json['dbConnection'])
        db = myclient[config_value_json['db']]
    else:
        myclient = pymongo.MongoClient(config['dbConnection'])
        db = myclient[config['db']]
    #fileName =''
    output = ''

   
    def ocr_to_html(ocr_data_page):
        html_content_final = []
        for page in ocr_data_page:
            html_content = '<div style="position: relative; width: 3600px; height: 4500px;">\n'
            for line in page['lineWithCombineWordsNew']:
                for item in line:
                    leftX = item['leftX']
                    topY = item['topY']
                    rightX = item['rightX']
                    bottomY = item['bottomY']
                    text = item['text']
                    
                    # Calculate width and height
                    width = rightX - leftX
                    height = bottomY - topY
                    
                    # Create the span element with inline styles
                    span_element = f'<span style="position: absolute; left: {leftX}px; top: {topY}px; width: {width}px; height: {height}px;">{text}</span>\n'
                    
                    html_content += span_element    
            html_content += '</div>\n'
            html_content_final.append(html_content)
        return html_content_final

    def html_to_positioned_text(html_content, scale_factor=10):
        """
        Converts HTML with positioned text to a plain text representation
        while maintaining relative text positioning.
        
        Args:
            html_content (str): Input HTML content
            scale_factor (int): Factor to scale down pixel positions
            
        Returns:
            str: Formatted text output with preserved positioning
        """
        # Parse HTML
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract all text elements with their positions
        positioned_elements = []
        
        # Find all elements with style attribute (both div and span)
        for element in soup.find_all(['div', 'span'], style=True):
            style = element.get('style', '')
            
            # Extract top and left positions from style
            top_match = re.search(r'top:\s*(\d+)px', style)
            left_match = re.search(r'left:\s*(\d+)px', style)
            
            if top_match and left_match:
                # Scale down the positions for more manageable output
                top = int(int(top_match.group(1)) / scale_factor)
                left = int(int(left_match.group(1)) / scale_factor)
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
        for page in html_content:
            res = html_to_positioned_text(page)
            output += res+'\n--------------PAGE END-----------------------\n'
        return output


    output = process_document_layout(combineLines)
    if not output:
        return json.dumps({'statusCode':'400' ,'mlOutput':'No text in the file.', 'info':'No data'})
    print(type_check)


    document_type_data = {}
    try:
        for y in db.get_collection("scanningfields").find():
            if y['documentType']==documentType:
                document_type_data = y
    except Exception as e:
        print('Valid training file not found',e)
        return json.dumps({'status':400 , 'info':'Valid scanning field not found'})
    
    prompttemplate_data = list(db.get_collection('Genai_Prompt_Templates').find())

    gen_prompt_format = '''You are a helpful and efficient QA assistant. You are a master of logical thinking. You carefully analyze the premises step by step, take detailed notes and draw intermediate conclusions based on which you can find the final answer to any question. From the content provided by user populate the json, if value not present leave it empty. The json has instructions for each field. Dont return the instructions in output. if fields are not mentioned explicitly in document then do not calculates at your own.  DONT DO ANY CALCULATIONS IN JSON OUTPUT.'''
    prompt_format = gen_prompt_format
    if 'headerPrompt' in document_type_data:
        prompt_format = prompt_format + '\nAdditional Instructions: \n'+document_type_data['headerPrompt']
    document_obj = {}
    table_obj = {}
    if (document_type_data):
        for i,fields in enumerate(document_type_data['fields']):
            if 'prompts' in fields and not fields['isTable']:
                if 'document_type' in fields['fieldName'].lower():
                    document_obj[fields['fieldName']] = fields['prompts']
                else:
                    document_obj[fields['fieldName']] = '' #fields['prompts']
            elif 'prompts' in fields and fields['isTable'] and fields['tableName']:
                if fields['tableName'] in table_obj:
                    table_obj[fields['tableName']][0][fields['fieldName']] = fields['prompts']
                else:
                   table_obj[fields['tableName']] = [{}]
                   table_obj[fields['tableName']][0][fields['fieldName']] =  fields['prompts']




    image_file_name = os.path.splitext(os.path.basename(file_name))[0]
    filename = f"{image_file_name}context.txt"
    file_path = '/mountpool/data/'+filename
    with open(file_path, "w") as file:
        file.write(output)  
    model_flag = 'unsloth'

    print(f'-----------token_size-----------',model_name)
    def evaluate_expression(expression):
        """Evaluates a mathematical expression given as a string."""
        try:
            return eval(expression) if expression else 0
        except Exception as e:
            print(f"Error evaluating expression '{expression}': {e}")
            return 0
    #PERSIST_DIRECTORY = './data'
    def convert_string_to_number(data):
        converted_dict = {}
        for key, value in data.items():
            if value == '':
                converted_dict[key] = value
                continue
            if isinstance(value, str):
                try:
                    float_val = float(value)
                    if float_val.is_integer():
                        converted_dict[key] = int(float_val)
                    else:
                        converted_dict[key] = float_val
                except ValueError:
                    converted_dict[key] = value
            else:
                converted_dict[key] = value
        return converted_dict

    if model_name == "llama":
        output_text = ''
        input_token = 0
        output_token = 0
        print('inference time;')
        type_key = {k: v for k, v in document_obj.items() if 'document_type' in k.lower() }
        type_key['reason'] = 'Provide the reason for the classification.'
        final_keys_to_extract = {}
        try:
            type_instruction = f"""You are a helpful and efficient QA assistant. Can you through the document context and classify the type of document. Respond with json {json.dumps(type_key)}. Output json:"""
            type_output = response_generation(type_instruction,output,1000)
            print('tuype',type_output)
            # type_output = type_output['result']
            instruction = '''You are a helpful and efficient QA assistant. Can you check whether its CGST,SGST or IGST tax method invoice. Respond with json {'CGST_SGST':True/False,'IGST':True/False}. Output json:'''
            md_output_text = response_generation(instruction,output,500)
            print('md_text',md_output_text)
            # md_output_text = md_output_text['result']
            del document_obj['Document_Type']
            if (md_output_text['CGST_SGST']):
                cgst_keys = {k: v for k, v in document_obj.items() if not 'igst' in k.lower()}
                instruction = '''You are a helpful and efficient QA assistant. Can you check whether its SGST or UTGST tax method invoice. Respond with json {'SGST':True/False,'UTGST':True/False}. Output json:'''
                md_output_text2 = response_generation(instruction,output,500)
                
                if(md_output_text2['SGST']):
                    filter_keys = {k: v for k, v in cgst_keys.items() if not 'utgst' in k.lower()}
                    final_keys_to_extract = filter_keys
                    #instruction_final = prompt_format+'\n Respond with json using context provided before\n'+json.dumps(filter_keys)+tax_percent_prompt+'\nOutput json:'
                else:
                    filter_keys = {k: v for k, v in cgst_keys.items() if not 'sgst' in k.lower()}
                    final_keys_to_extract = filter_keys
                    # instruction_final = prompt_format+'\n Respond with json using context provided before\n'+json.dumps(filter_keys)+tax_percent_prompt+'\nOutput json:'
            elif(md_output_text['IGST']):
                igst_keys = {k: v for k, v in document_obj.items() if not 'cgst' in k.lower() and not 'sgst' in k.lower() and not 'utgst' in k.lower()}
                final_keys_to_extract = igst_keys
                #instruction_final = prompt_format+'\n Respond with json using context provided before\n'+json.dumps(igst_keys)+tax_percent_prompt+'\nOutput json:'
            else:
                non_tax_keys = {k: v for k, v in document_obj.items() if not 'cgst' in k.lower() and not 'sgst' in k.lower() and not 'utgst' in k.lower() and not 'igst' in k.lower()}
                final_keys_to_extract = non_tax_keys
                #instruction_final = prompt_format+'\n Respond with json using context provided before\n'+json.dumps(non_tax_keys)+'\nOutput json:'
            parts_labour_keys = {k: v for k, v in final_keys_to_extract.items() if 'Parts' in k or 'Lab' in k or 'Total' in k or 'Amount' in k}
            header_keys =   {k: v for k, v in final_keys_to_extract.items() if not 'Parts' in k and not 'Lab' in k and not 'Total' in k and not 'Amount' in k}
            template_prompt = ''
            for i,prompt in enumerate(prompttemplate_data):
                temp_prompt = f'''
Template Sample {i+1} (Name- {prompt['template_name']}):
Input:
{prompt['input']}


'''
                template_prompt += temp_prompt
            content = f'''
Task: Convert the input invoice text into the json structure below. Classify which template sample's structure matches with the new input. Goal is not to match the full new input only a partial part of it. If not matched return matched_template_name as ''.
{template_prompt}

New Input:
{output}

Required Output Format:
{{"matched_template_name": ""}}

Result:
```json{{result}}```
'''
            res = response_generation_new(content,200)
            matched_template = None
            multi_output = False
            if ('matched_template_name' in res and res['matched_template_name']):
                matched_template = [temp for temp in prompttemplate_data if temp['template_name'] == res['matched_template_name']]
                if (len(matched_template)>0):
                    matched_template = matched_template[0]
                    if 'output2' in matched_template:
                        multi_output = True
                    field_content = f'''
    Task: Convert the input invoice text into the JSON structure below, using the examples for reference. IF A EXAMPLE MATCHES WITH NEW INPUT, FOLLOW THE SAME STRUCTURE. 
    {
    f"""Instruction:
    {matched_template['instruction']}""" if "instruction" in matched_template else ''
    }

    {create_temp_format(matched_template)}

    New Input:
    {output}

    {f"""Required Output Format:
    {json.dumps(parts_labour_keys,indent=2)}""" if not multi_output else ""}


    Provide reason for each claim in your response
    Result:
    {"```Text{{result}}```" if multi_output else "```json{{result}}```"}
    '''
                
            else:
                field_content = f'''
Task: Convert the input invoice text into the JSON structure below.

Input:
{output}

Required Output Format:
{parts_labour_keys}


Result:
```json{{result}}```
'''
            if multi_output:
                print('in multi_out')
                value_output = response_generation_text(field_content,800)
                field_content = f'''
Task: Convert the input invoice text into the JSON structure below, using the examples for reference. IF A EXAMPLE MATCHES WITH NEW INPUT, FOLLOW THE SAME STRUCTURE. 
{
   f"""Instruction:
{matched_template['instruction']}""" if "instruction" in matched_template else ''
}

{create_temp_format_2(matched_template)}

New Input:
{value_output}

Required Output Format:
{json.dumps(parts_labour_keys,indent=2)}


Result:
```json{{result}}```
'''
            
            
            value_output = response_generation_new(field_content,800)
            value_output = convert_string_to_number(value_output)
            field_content = f'''
Task: Convert the input invoice text into the JSON structure below.


Input:
{output}

Required Output Format:
{header_keys}


Result:
```json{{result}}```
'''
            
            
            for key, value in value_output.items():
                if key != "InvoiceTotalAmount":
                    formated_value = value.replace(',','') if isinstance(value,str) else value
                    updated_val = evaluate_expression(formated_value) if not isinstance(value,(float,int)) else formated_value
                    value_output[key] = updated_val
            
            
            main_output_text = response_generation_new(field_content,700)
            primary_output_text = main_output_text | value_output | type_output | res
            derived_output_text = {}
           
            output_text = {**primary_output_text,**derived_output_text}
            output_text = convert_string_to_number(output_text)
            output_text['model'] = 'qwen2.5-32b'
            input_token = len(output)
            output_token = len(json.dumps(primary_output_text))
        except Exception as e:
            print("---------------",document_obj)
            output_text_raw = f'{{"Invoice_Number":"","prediction_error":{e}}}'
            output_text = repair_json(output_text_raw)
            output_text = json.loads(output_text)
            output_text['model'] = 'qwen2.5-14b'
            print(f"respose================={output_text}")
            input_token = len((output))
            output_token = len((output_text_raw))

        
        model_result =json.dumps(output_text,default=str)
        print(f"final respose================={output_text}")
        

        if(config_value_json and 'mountpath' in config_value_json):
            file_name = file_name.replace(config_value_json['mountpath'], '/home/user/')
        '''else:
            file_name_new = file_name.replace('/home/anil/HDD/www/msme42-fs/','/home/user/')'''
        #print("=====================",file_name)
        df = pd.read_csv(file_name)
        prediction = output_text

        df['Property'] = 'undefined'

        
        for key in prediction:
            if isinstance(prediction[key],str):
                prediction_words = prediction[key].split()
                word_length = len(prediction_words)
                match = False
                prediction_value = prediction[key].lower()
                if (word_length==1):
                    threshold = 0.9
                else:
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
                            df.at[index_list[i], 'Property'] = key
                        break;
        import csv
        df.to_csv(file_name,quoting=csv.QUOTE_NONNUMERIC,index=None)
        from typing import Dict

        if not isinstance(output_text, Dict):
            return json.dumps({'status':400 , 'info':'Valid output not found'})

        from datetime import datetime
        output_text['documentTitle'] = documentType
        output_text['referenceNumber'] = ref_no
        output_text['createdAt'] = datetime.now()
        output_text['updatedAt'] = datetime.now()
        output_text['fileName'] = file_name
        output_text['orgId'] = org_id
        output_text['isTmp'] = False
        output_text['ocrConfidence'] = []
        #output_text['model'] = model_name
        torch.cuda.empty_cache()
        gc.collect()
        try:
            db.get_collection(documentType).insert_one(output_text)
        except Exception as e:
            print (e)
            outputData={'mlOutput':'Not inserted in db' , 'statusCode': '400'}
            # with open("file_"+timestamp+".json", "w") as f:
            #     json.dump(outputData, f)
            #     return str(1)

        outputData = {'mlOutput':model_result,'documentType':documentType,'statusCode':'200'}
        input_token_used = input_token
        complete_token_used = output_token
        total_token_used = input_token + output_token
        import datetime
        token_store_object = {
            "input_token_used": input_token_used,
            "output_token_used": complete_token_used,
            "total_token_used": total_token_used,
            "process": "GenAI",
            "collection_name": documentType,
            "subscriber_id": data['input']['mlInput']['subscriberId'],
            "org_id": data['input']['mlInput']['orgId'],
            "user_id": data['input']['userId'],
            "reference_number": ref_no,
            "created_time": datetime.datetime.utcnow()
        }
        try:
            db.get_collection('LLM_Tokens').insert_one(token_store_object)
        except Exception as e:
            print (e)

        gc.collect(generation=0)
        gc.collect(generation=1)
        gc.collect(generation=2)

        with open("file_"+timestamp+".json", "w") as f:
            json.dump(outputData, f)

        return outputData


#with open('file_event_1741575593.7683766.json','r') as f:
#    data = json.load(f)

#fieldDetection(data,str(time.time()))
# doctype, sub_doctype, fields = typeDetection(context)
# print(doctype, sub_doctype, fields)
if __name__=="__main__":
    print("\n\n\n\n[INFO] FILE TRIGGER ..", get_args()[0],"\t",get_args()[1], "\n\n")
    fieldDetection(json.load(open(get_args()[0], "r")), get_args()[1])
