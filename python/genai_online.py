import json
import openai
from openai import OpenAI
import os
import math
import pymongo
import pandas as pd
import google.generativeai as genai
from json_repair import repair_json

os.environ["OPENAI_API_KEY"] = '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'
os.environ["DEEPSEEK_API_KEY"] = 'sk-a3ddb45eaf01401899f10084e88f8077'
openai.api_key = os.environ["OPENAI_API_KEY"]
client = OpenAI() 

GOOGLE_API_KEY='AIzaSyCba_YtqSiq5jNu4ySEsm-koKpe8DyuslU'
genai.configure(api_key=GOOGLE_API_KEY)
from difflib import SequenceMatcher
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#model = genai.GenerativeModel('gemini-1.5-pro-latest')
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

def fieldDetection(data,timestamp):
    combineLines = data['input']['combineLines']
    documentType = data['input']['mlInput']['documentType']
    model_name = data['input']['ai_model_name']
    config_value_json = data['input']['config_value_json']
    eventId = data['input']['eventId']
    ref_no = data['input']['refNo']
    file_name = data['input']['mlInput']['filePath']
    
    print("3222222          ",documentType)    

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
    context = ''
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
            context = document_type_data['context']


    def Average(lst): 
        return sum(lst) / len(lst) 
    output = ''
    avg_height = []
    for page in combineLines:
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
            if context != '':
                header_chat_format.insert(1,{"role": "system", "content": context})
            openai.api_key = os.environ["OPENAI_API_KEY"]
            openai.api_base = "https://api.openai.com/v1" 
            print ('Header query', header_chat_format)
            header_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=header_chat_format,
                temperature=0.1,
                top_p=0.1)
            
            response_content = header_response.choices[0].message.content
            print (response_content)
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
                for page in page_output[0:len(page_output)-1]:
                    table_chat_format = [
                        {"role": "system", "content": prompt_format+'\n'+json.dumps(table_obj)},
                        {"role": "user", "content": page}
                    ]
                    table_response = client.chat.completions.create(
                        model="gpt-4o-mini",
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
            openai.api_key = os.environ["DEEPSEEK_API_KEY"]
            openai.api_base = "https://api.deepseek.com/v1" 
            if context != '':
                header_chat_format.insert(1,{"role": "system", "content": context})
            print ('Header query', header_chat_format)
            header_response = client.chat.completions.create(
                model="deepseek-chat",
                messages=header_chat_format,
                temperature=0.1,
                top_p=0.1)
            
            response_content = header_response.choices[0].message.content
            print (response_content)
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
                for page in page_output[0:len(page_output)-1]:
                    table_chat_format = [
                        {"role": "system", "content": prompt_format+'\n'+json.dumps(table_obj)},
                        {"role": "user", "content": page}
                    ]
                    table_response = client.chat.completions.create(
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
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        if document_obj:
            content = prompt_format+'\n'+json.dumps(document_obj)+'\n\n'+output
            response = model.generate_content(content)
            invoice_obj = repair_json(response.text)
            invoice_obj = json.loads(invoice_obj)
            invoice_obj['invoiceItems']= []
            invoice_obj['multiTable'] = []
            if table_obj:
                page_output = output.split('\n---PAGE END---')
                for page in page_output[0:len(page_output)-1]:
                    table_chat_format = prompt_format+'\n'+json.dumps(table_obj)+'\n\n'+page
                    table_res = model.generate_content(table_chat_format)
                    table_content = repair_json(table_res.text)
                    table_content = json.loads(table_content)
                    for table in table_content:
                        if (table in table_result):
                            table_result[table].extend(table_content[table])
                        else:
                            table_result[table] = []
                            table_result[table].extend(table_content[table])

    if (table_result):
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
        print ('hello   ',fileUploadHistories)
        invoice_obj['filePath'] = fileUploadHistories['filePath']
        invoice_obj['file_name'] = fileUploadHistories['fileName']
    except Exception as e:
        print ("errror ",e)

    

    try:
        db.get_collection(documentType).insert_one(invoice_obj)
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
    try:
        db.get_collection('LLM_Tokens').insert_one(token_details)
    except Exception as e:
        print (e)

    outputData = {'mlOutput':'Done','data':invoice_obj,'statusCode':'200'}
    with open("file_"+timestamp+".json", "w") as f:
        json.dump(outputData, f)
    return outputData


if __name__=="__main__":
    print("\n\n\n\n[INFO] FILE TRIGGER ..", get_args()[0],"\t",get_args()[1], "\n\n")
    fieldDetection(json.load(open(get_args()[0], "r")), get_args()[1])