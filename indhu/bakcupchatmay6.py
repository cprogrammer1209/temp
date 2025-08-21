##############################################################################################################################################################
import hashlib
import re
import json
import argparse
import time
import bson
import pymongo
from flask import Flask, jsonify, render_template, request,redirect, url_for,session, g
from functools import wraps
from pymongo import MongoClient
from json_repair import repair_json
import openai
from openai import OpenAI
import os
from flask_cors import CORS
import sys
import base64
import mysql.connector
import cx_Oracle
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
config={}
with open('config.json', 'r') as f:
    config = json.load(f)
app = Flask(__name__)
app.secret_key = "LeafmanZSecretKey"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
from bson.objectid import ObjectId
from bson import json_util
os.environ["OPENAI_API_KEY"] = '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'
# Set openai.api_key to the OPENAI environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]
########################################################################################################################################
from transformers import AutoTokenizer
from llama_index.callbacks import TokenCountingHandler
def get_tokens_and_count(string, tokenizer):
    tokens = tokenizer.encode(string)
    return  len(tokens)

#tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf")
from typing import List
from pydantic import BaseModel
class AggregateQuery(BaseModel):
    query: List[dict]

'''token_counter = TokenCountingHandler(
            tokenizer=tokenizer.encode
)'''
import datetime

class MongoJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)  # Convert ObjectId to string
        return super(MongoJSONEncoder, self).default(obj)

def using_dict_comprehension(keys):
    return {f'{key[0]}: {key[1]},' for key in keys}

###############################################################################################################################################################
def callopenai(new_chat_store):
    #client = OpenAI(api_key="sk-4e526b97029648f0a1cbac1624a00403", base_url="https://api.deepseek.com")
    print ('here')
    client = OpenAI()
    response_ai = client.chat.completions.create(
                model="gpt-4o-mini",
                #model="deepseek-chat",
                messages=new_chat_store,
                temperature=0.1,
                top_p=0.1
                )
    response = response_ai.choices[0].message.content
    print('out',response)
    # output = json.loads(response)
    usage = response_ai.usage
    # print(output)
    return response,usage

def complete_task( db, field_names, coll_name, prompt, chat_engine, mode, chat_store, input,context):
    mode = mode.lower()

    permission_filter = None
 
    print(f"calling the mode; ")
    print(context)
    permission = input['permission'] if 'permission' in input else 'sub'
    if (permission == 'org'):
        permission_filter = { "$match": {"orgId": ObjectId(input['orgId'])}}
    elif (permission == 'sub'):
        permission_filter = { "$match": {"subscriberId": ObjectId(input['subscriberId'])}}
    elif (permission == 'user'):
        permission_filter = { "$match": {"userId": ObjectId(input['userId'])}}
    elif (permission == 'dept'):
        permission_filter = { "$match": {"deptId": ObjectId(input['deptId'])}}
    print(f"1;;; ")

    supervisor = input['supervisor_name']
    employee_name = input['employee_names']
    username = input['username']
    this_user_tasks = db.get_collection("events").find({"projectName": "Collab Pro", "currentEventStatus.category": "Manual", "currentEventStatus.orchestratorStatus":"inProgress","currentEventStatus.statusName":"Assign","currentEventStatus.assignToList.0.assignedToId": ObjectId(input['userId'])},{"additionalInfoVar.Task":1, "additionalInfoVar.Task Description": 1, "_id": 1 })
    tasks_list = list(this_user_tasks)
    print(f"222;;; ")


    if mode == "online":
        # complete_query = f"""you are a smart assistant who understands human intentions through messages. Read this message: {prompt} and answer in one word. The word can either be 'completeTask' or 'fetchInfo'. If the message means the sender wants to complete his tasks then return 'completeTask' or return 'fetchInfo'. Think step by step. Response should just be one word."""
        complete_query = f"""you are a smart assistant who understands human intentions through messages. Read this task list: {tasks_list} and context: {context}. Return the id of that task whose task or task description matches the context best. If there is no context return the id of the first task. The response should just be the value of the most relevant id. Think step by step."""
        if(len(chat_store)>0):
                    # start_msg = chat_store[:1]
                    # recent_2_msgs = chat_store[-2:]
                    chat_store_final = []
                    chat_store_final.append({"role": "system", "content": complete_query})
                    print(chat_store_final)
        response_id,usage = callopenai(chat_store_final)

        # response = response_ai.choices[0].message.content
        #response_id = response_ai.choices[0].message.content
    print(f"333;;; ")
    
    filter_criteria = {"eventId" : ObjectId(response_id) ,"statusName":"Assign"}

    projection = {"assignToList": 1, "templateId": 1, "dueDate": 1, "eventStatusDesc": 1, "projectId": 1, "eventId": 1, "startDate": 1, "_id": 1}  # Include templateId, exclude _id

    # Find the latest document by sorting in descending order and getting the first one
    db = g.db
    personal_info = db.get_collection("users").find({"_id": ObjectId(input['userId'])},{"personalInfo": 1, "_id": 1})
    personal_info_details = {}
    for doc in personal_info:
        personal_info_details['temp'] = doc
        break
    print(f"555;;; ")
    
    latest_doc = db.get_collection("eventstatuses").find(filter_criteria,projection).sort("_id", -1)
    template = {}
    for doc in latest_doc:
        template['temp'] = doc
        break
    print(f"666;;; ")

    filter_2_criteria = {"_id": template['temp']['templateId']}
    
    project = {'additionalInfo': 1, "templateName": 1, "ruleId": 1, "_id": 0}

    template_details = db.get_collection("additionalinfos").find(filter_2_criteria,project)
    print(f"77;;; ")

    task_level_template_doc = db.get_collection("events").find({"_id": template['temp']['eventId']},{"templateId": 1, "variableList": 1, "additionalInfoVar": 1, "_id": 0})
    print(f"88;;; ")

    task_level_template = {}

    for doc in task_level_template_doc:
        task_level_template['temp'] = doc
        break
     
    task_level_template_details = db.get_collection("additionalinfos").find({"_id": task_level_template['temp']['templateId']},project)
    print(f"999;;; ")

    task_level_template_addinfo = {}

    for doc in task_level_template_details:
        task_level_template_addinfo = doc
        break

    task_level_template_values = [item["label"] for item in task_level_template_addinfo.get("additionalInfo", []) if item.get("required") == True]  
    task_level_template_all_values = [item["label"] for item in task_level_template_addinfo.get("additionalInfo", [])]

    additional_info = {}
    for doc in template_details:
        additional_info = doc
        break
    print(f"1000;;; ")
    
    final_values = [item["label"] for item in additional_info.get("additionalInfo", []) if item.get("required") == True]
    # final_values.extend(task_level_template_values)
    print(final_values)
    # task_details = {"templateId": template['temp']['templateId'], "dueDate": template['temp']['dueDate'], "eventStatusDesc": template['temp']['eventStatusDesc'],"projectId": template['temp']['projectId'],"addinfolabels": final_values, "_id": template['temp']['_id']}
    task_details = {"templateName": additional_info['templateName'], "bot_level_addinfo": additional_info['additionalInfo'],"ruleId":additional_info.get('ruleId') ,"personalInfo": personal_info_details['temp'], "startDate": template['temp']['startDate'],"assignToList": template['temp']['assignToList'],"dueDate": template['temp']['dueDate'],"templateId": template['temp']['templateId'],"eventStatusId": template['temp']['_id'],"eventId": template['temp']['eventId'], "variableList": task_level_template['temp']['variableList'],"additionalInfoVar": task_level_template['temp']['additionalInfoVar'], "taskLevelAddInfoVariables": task_level_template_all_values }
    
    
    response = {
    "completeTask": True,
    "message": final_values,
    "taskDetails": task_details,
    
    }
    print(response)

    return response

def find_objective(prompt, chat_engine, mode, chat_store, input):
    mode = mode.lower()
    response = ''

    permission_filter = None
 
    print(f"calling the mode find objective; ")

    permission = input['permission'] if 'permission' in input else 'sub'
    if (permission == 'org'):
        permission_filter = { "$match": {"orgId": ObjectId(input['orgId'])}}
    elif (permission == 'sub'):
        permission_filter = { "$match": {"subscriberId": ObjectId(input['subscriberId'])}}
    elif (permission == 'user'):
        permission_filter = { "$match": {"userId": ObjectId(input['userId'])}}
    elif (permission == 'dept'):
        permission_filter = { "$match": {"deptId": ObjectId(input['deptId'])}}

    supervisor = input['supervisor_name']
    employee_name = input['employee_names']
    username = input['username']
    client = OpenAI()
    print(f"1; ")

    if mode == "online":
        # complete_query = f"""you are a smart assistant who understands human intentions through messages. Read this message: {prompt} and answer in one word. The word can either be 'completeTask' or 'fetchInfo'. If the message means the sender wants to complete his tasks then return 'completeTask' or return 'fetchInfo'. Think step by step. Response should just be one word."""
        complete_query = f"""you are a smart assistant who understands human intentions through messages. Read this message: {prompt} and answer in one word. The word can either be 'completeTask' or 'fetchInfo'. If the message means the sender wants to complete his tasks then return 'completeTask' or return 'fetchInfo'. This value should be provided as the value of key. The name of the key should be 'objective'. Also if the message has information about which task the human wants to complete then provide it in the response as the value of another key called 'context'. Think step by step. Populate the output in the following json format: {{'output':{{'objective':'fetchInfo','context':'water coercion task'}}}}"""
        print(f"2; ")
        
        if(len(chat_store)>0):
                    # start_msg = chat_store[:1]
                    # recent_2_msgs = chat_store[-2:]
                    chat_store_final = []
                    chat_store_final.append({"role": "system", "content": complete_query})
                    print(chat_store_final)
        print(f"3; ")

        response,usage = callopenai(chat_store_final)
        response = repair_json(response)
        # response = response_ai.choices[0].message.content
        # print(f"""response inside function{response}""")
        print(f"4; ")

        response_json = json.loads(response)
        print(f"Response JSON: {response_json}")
        # response = str(response)
        
    return response_json, usage


import google.generativeai as genai

# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY='AIzaSyDFs31mlJSb4rfCv0vB4SxGv19mpK1sQuA'

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('models/gemini-2.0-flash')
from google.api_core import retry
my_retry = retry.Retry(
    initial=1.0,   # Initial delay in seconds
    maximum=10.0,  # Maximum delay in seconds
    multiplier=2.0, # Multiplier for exponential backoff
    deadline=60.0  # Maximum time to retry (in seconds)
)
from tavily import TavilyClient
tavily_client = TavilyClient(api_key="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")
def callgemini(text,question,lang='en'):
    print('here')
    from datetime import date
    response = tavily_client.search(question)
    print('Respponse')
    res = ''
    for i,news in enumerate(response['results']):
        res += f"Link:{news['url']}\nTitle: {news['title']}\nContent:{news['content']}\n"
    prompt = f"""Answer this question {question}. You can use this content if necessary information about the question is available. Content: {text}. Today's date is {str(date.today())}. Provide the answer with reference link used for it. Provide result in html which will be appended to a existing html file."""
    if g.news_id:
        print('using ind new id as sourc')
        response = model.generate_content(prompt)
    else:
        response = model.generate_content(f"""You are an intelligent query responder. The user is a government official. If question are asked about suggestions and recommendations make sure to categorise it like individual topics like External Security, health, internal security interventions, Border Areas, etc and also make sure responses are curated based on his role. 
Answer the question {question}. These are some references: {res}. Provide the response with facts and numbers included as per the question. 
Avoid generic answers. Responses should be like a list of checklist points in a concise way. 
Provide result in english html where links if present will open in a new tab which will be appended to a existing html file.
""")
    response_text = response.text
    # format_response = model.generate_content(f"Translate if any text in the provided content in other language to english and return in html. content: {response_text}")
    # response_text = format_response.text
    res_match = re.search(r"```html\s*(.*?)\s*```", response_text, re.DOTALL)
    if res_match:
        response_text = res_match.group(1)
    return response_text,response.usage_metadata

def extract_keyvalues(text,question,language):
   
    new_chat_store = [
            {
                "role":"system",
                "content": "You are a master of logical thinking. You carefully analyze the premises step by step, take detailed notes and draw intermediate conclusions based on which you can find the final answer to any question."
            },
            {
                "role":"user",
                "content": f"""Today's date is {str(datetime.date.today())}From the provided content {text}, answer this question {question}. Provide the answer with reference link used for it. Provide result in html which will be added in html page."""
            }
        ]
    response,usage = callopenai(new_chat_store)
    # res_match = re.search(r"```html\s*(.*?)\s*```", response, re.DOTALL)
    # if res_match:
    #     response = res_match.group(1)
    return response,usage

def convert_date_fields(pipeline_dict):
    import datetime
    if isinstance(pipeline_dict, dict):
        for key, value in list(pipeline_dict.items()):  # Use list() to avoid RuntimeError (dict size change)
            if isinstance(value, dict) and "$date" in value:
                # Convert "$date" string to Python datetime object
                pipeline_dict[key] = datetime.datetime.fromisoformat(value["$date"].replace("Z", "+00:00"))
            else:
                # Recursively process nested dictionaries or lists
                convert_date_fields(value)

    elif isinstance(pipeline_dict, list):
        for item in pipeline_dict:
            convert_date_fields(item)

    return pipeline_dict
from datetime import datetime

def convert_dates(obj):
    if isinstance(obj, dict):
        if "$date" in obj and isinstance(obj["$date"], str):
            # Convert $date string to datetime object
            return datetime.fromisoformat(obj["$date"].replace("Z", "+00:00"))
        else:
            return {k: convert_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates(item) for item in obj]
    else:
        return obj
def transform_regex_fields(pipeline):
    final = []
    for stage in pipeline:
        if '$match' in stage:
            transformed = {'$match': {}}
            expr_conditions = []

            for key, value in stage['$match'].items():
                if isinstance(value, dict) and "$regex" in value:
                    raw_pattern = value["$regex"]
                    # Normalize only the case, preserve spaces in the pattern
                    normalized_pattern = raw_pattern.lower()
                    options = value.get("$options", "")

                    # Prepare the transformed condition
                    condition = {
                        "$regexMatch": {
                            "input": {
                                "$replaceAll": {
                                    "input": {"$toLower": f"${key}"},
                                    "find": " ",
                                    "replacement": ""
                                }
                            },
                            "regex": normalized_pattern.replace(" ", ""),  # Remove spaces only from the input processing, not pattern
                            "options": options.replace("i", "")  # Remove 'i' since input is lowercased
                        }
                    }
                    expr_conditions.append(condition)
                else:
                    transformed['$match'][key] = value

            if expr_conditions:
                if len(expr_conditions) == 1:
                    transformed['$match']["$expr"] = expr_conditions[0]
                else:
                    transformed['$match']["$expr"] = {"$and": expr_conditions}

            final.append(transformed)
        else:
            final.append(stage)
    return final

def match_stages(pipeline):
    # Filter out $match stages
    if not '$match' in pipeline[0]:
        return pipeline
    filtered_pipeline = [stage for stage in pipeline if '$match'  in stage and '$regex' in json.dumps(stage['$match'])]
    # If no $match stages were present, return original
    if len(filtered_pipeline) == 0:
        return pipeline
    return filtered_pipeline
    
def create_query_retrieve_data( db, field_names, coll_name, prompt, chat_engine, mode, chat_store, input):


    try:

        # Fetching data from the database using model query.
        # client = MongoClient(db_url)
        # db = client[database]

        # Collection name taken as Coll name
        print ('db',db, 'coll_name', coll_name)
        collection = db[coll_name]
        # collection_info = collection.find_one()
        # collection_keys = collection_info.keys()

        schema_name = coll_name
        coll_name = using_dict_comprehension(field_names)  # I assume this function is defined elsewhere
        hide_keys = input['hide_keys']
        project_keys = input['project_keys']
        #print("Collection Metadata for '{}' in database '{}'".format(schema_name, coll_name))

        mode = mode.lower()

        permission_filter = None
        # query = prompt
        # header_tile = f"""Given the following table schema:{coll_name}"""
        # footer_tile = """Generate complete aggregate pipeline MongoDB query in output.
        #                     Only respond with mongo query in a valid JSON format without code block syntax around it."""
        # complete_query = f"""Write a MongoDB Aggregation pipeline.
        #     Use the following as mongoDB collection schema to write the query: {coll_name} Using the collection {schema_name}. {prompt}.
        #     Projection should exclude _id.
        # Only respond with mongo query in a valid JSON format without code block syntax around it."""

        print(f"calling the mode; ")

        permission = input['permission'] if 'permission' in input else 'sub'
        if (permission == 'org'):
            permission_filter = { "$match": {"orgId": ObjectId(input['orgId'])}}
        elif (permission == 'sub'):
            permission_filter = { "$match": {"subscriberId": ObjectId(input['subscriberId'])}}
        elif (permission == 'user'):
            permission_filter = { "$match": {"userId": ObjectId(input['userId'])}}
        elif (permission == 'dept'):
            permission_filter = { "$match": {"deptId": ObjectId(input['deptId'])}}

        print("permision filter ",permission_filter)
        supervisor = input['supervisor_name']
        employee_name = input['employee_names']
        username = input['username']
        if mode == "offline":

            # print(f"LLAMA {mode} Model is generating the query for you...")
            # response = chat_engine.chat(complete_query)

            try:
                query = prompt
                # header_tile = f"""Given the following table schema:{coll_name}"""
                # footer_tile = """I want only complete aggregate MongoDB query in output, don't give me extra content. Match queries must be case insensitive and handle partial or complete match and exclude _id in output."""
                # complete_query = header_tile + query + footer_tile
                complete_query = f"""Write a MongoDB Aggregation pipeline.
Use the following as mongoDB collection schema to write the query: {coll_name}
{'Use the following use cases and scenerios of the above schema : ' + input['attachmentExplanation'] if  "isAttachExplanation" in input and  input['isAttachExplanation']==True else ''}
Using the collection {schema_name}. {prompt.upper()}.
Projection should exclude _id.
Match queries must use $regex if field is string no need to use ^,$ , include case insensitive flag and exclude _id in output. If using $regex dont enclose it in /expression/
Only respond with mongo aggregation query in a valid array JSON format without code block syntax around it and each pipeline should be closed within object and quotes around each stage type. No explanation."""

                print(f"using this prompt we are fetching the results ----{complete_query} ")
                # print(f"LLAMA {mode} Model is generating the query for you...")
                # response = query_engine.query(complete_query)  # Assuming query_engine is defined elsewhere

                print(f"LLAMA {mode} Model is generating the query for you...")
                print("()()()()()()()()( ",complete_query)
                response = chat_engine.chat(complete_query)
                mongo_query = str(response)
                print('Mongo query', mongo_query)
                # Extracting the query from the response from models.
                regex_pattern = r'```(.*?)```'
                match = re.findall(regex_pattern, mongo_query, flags=re.S)
                final_query = None
                if (match):
                    final_query = match[0]
                else:
                    regex_pattern = r'\[MONGO\](.*?)\[\/MONGO\]'
                    matches = re.findall(regex_pattern, mongo_query, flags=re.S)
                    if (matches):
                        final_query = matches[0]
                    else:
                        regex_pattern = r'\[{.*}\]'
                        matches = re.findall(regex_pattern, mongo_query, flags=re.S)
                        if (matches):
                            final_query = matches[0]

                query_text = repair_json(final_query)
                print(f"1.----------------{query_text}-------------------")

                #conveting it into json format .
                python_object = json.loads(query_text)
                print(f"2.---------------{python_object}---------------")
                print(type(python_object))

                # Fetching data from the database using the model query.
                result_cursor = collection.aggregate(python_object)

                print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<{result_cursor}")
                final_result = list(result_cursor)
                return final_result,None, None
            except ValueError as e:
                print(f"There are some error is causing in offine Model---- {e}")
                return [], None, None


        else:

            try:
                if schema_name == 'News':
                    user_data = list(db['users'].find({"_id":ObjectId(input['userId'])}))
                    language = 'en'
                    if len(user_data) > 0:
                        language = user_data[0]['language']
                    
                    print(f'Calling chat for news collection using language',language)
                    if g.news_id:
                        final_result = list(collection.find({'_id':ObjectId(g.news_id)},{'_id':0,'createdAt':0,'orgId':0,'subscriberId':0}))
                    else:
                        final_result = list(collection.find({},{'_id':0,'createdAt':0,'orgId':0,'subscriberId':0}))
                    content = ''
                    for i,item in enumerate(final_result):
                        if 'Summary' in item and 'Link' in item and 'Title' in item: 
                            content += f"New Article No.{i}:\nLink:{item['Link']}\nTitle:{item['Title']}\nCategory:{item['Category']}\nContent:{item['Summary']}"

                    response,token_info = callgemini(content,prompt,language)
                    print('Resp',response)
                    return response,token_info,response

                additional_context = ''
                import datetime

                x = str(datetime.date.today())
                print('start time',x,)
                day_name = datetime.date.today().strftime("%A")
                if (supervisor == 'admin'):
                    additional_context = f'In this context, the user name is {username}.'
                    # and the role of user is the admin of an organisation.'
                    #The employees under the user include {employee_name}'
                else:
                    additional_context = f'In this context, the user name is {username}\n'
                    # and the role of user is the employee of an organisation.'
                    #The manager of the user is {supervisor}'
#                                    In this context, the user name is {username}. Use this username in match conditions only if me/my is mentioned in query requirement.
                print('checkoing the multi document ', "isMultiCollection" in input  and  input.get("isMultiCollection") is True ,' hello ', type(input['attachmentExplanation']))
                user_query = f"""Write a MongoDB Aggregation pipeline query.
Use the following as mongoDB collection schema to write the query: {coll_name}
{'Use the following use cases and scenerios of the above schema : ' + input['attachmentExplanation'] if  "isAttachExplanation" in input and  input['isAttachExplanation']==True  else ''}
Question:- {prompt}.
{'''You are an expert in mongodb aggregation creation. 
Check the user question whether the output aggregation pipeline can be generated with the above mongodb schema itself.
If it is required,  use the following additional mongoDb schema details to get deatils from other collections using lookup. 
While using lookup, the result  will be in dictionary or object. in project, give it as a seperate field. make sure you used dollar($) while giviting it as a seperate field. 
Dont give it in object.  
(sometimes the above db schema will also be attahed here, if it is there, ignore that and use the other schemas): ''' + 
str(input['multiTables']) if  "isMultiCollection" in input  and  "multiTables" in input  and input.get("isMultiCollection") is True else ''}
 """
                additional_info = f"""Additional Context: {additional_context} 
For any questions related to date, remember today's date is {x} and it falls on {day_name} of the current week . A week always starts with Monday ends with Sunday.      
Strict Rules and Regulations:
Its very critical to not use additional context like user match or date for generic query.
For direct date match use regular expression.
Its very critical to not add unnecassary match conditions if not prompted.
Its very critical Match queries must use $regex if field is type string, include case insensitive flag. 
Projection must exclude _id.
If using $regex dont enclose it in /expression/ and dont use ^ and $ in regex field.
Only respond with mongo aggregation query in a valid JSON list/array format without code block syntax around it and each pipeline should be closed within curly braces and quotes around each stage type. 
Always format response in this format. {{"pipeline":[]}}.
Its very critical, If the question is not related to schema respond empty."""
                print(f"LLAMA {mode} Model is generating the query for you...")
                # print('user query',user_query)
                # print('additional info',additional_info)
                
                client = OpenAI()

                import copy
                new_chat_store = None
                if(len(chat_store)>0):
                    start_msg = chat_store[:1]
                    recent_2_msgs = chat_store[-2:]
                    new_chat_store = start_msg
                else:
                    new_chat_store = copy.deepcopy(chat_store)
                # print('new_chat_stor',new_chat_store)
                rules = f"Your task to generate a mongodb query based on the following user query or quetion {prompt}"
                chat_store.append({"role": "user", "content": user_query})
                new_chat_store.append({"role": "user", "content": user_query})
                new_chat_store.append({"role": "user", "content": additional_info})
                new_chat_store.append({"role": "user", "content": rules})

                #yuvarj shankar logic for wockhardt
                import datetime
                query = ''
                if input['previousCollection'] == 'workhardt':
                    new_chat_store = []

                    user_query = f"""

                    context : 
                    A Pharamaceutical company is a company that develops, produces, and markets drugs or medications. The company is involved in the interaction(THey refer interaction as activity) with the doctors thorugh employee (sales representative).
                    Each doctor will have a separate employee(sales representative) who will be responsible for the interaction with the doctor.
                    The employee(sales representative) will connect with the doctor and will have the interaction with the doctor to boost the productity of the company.
                    In that interaction, the employee(sales representative) will discuss about the product and brand of wockhardt and also discuss about the competitor product brand details and value.
                    The interaction(activty) which i already held between the doctor and employee will be stored in the RCPA table,
                    and the further or future activity deatis on which date and call type will be stored in 'reporting' table
                    
                    There will be three collections in the database.
                    1) DML : This table or collection will have the data of the doctors related details like unique id, name, address, phone number, email id, on which day,time,place he will avvailable to interact with the employee etc.
                    2) reporting : This table or collection will have the data of the future or furhter actity date and call type between the doctors and employee(sales representative) like activity date, activity type, activity mode will be present.
                    3) RCPA : this table or collection will have the details of the already done or held interaction summary between the doctors and employee(sales representative) in detail like what product is discussed, what is the feedback from the doctor, etc.  
                    All three schema will have the doctor name and employee name.
                    
                    The some scenrios are like this:
                    1) DML : With DML table, the user may ask for the doctor details like doctor name, doctor id, doctor address, doctor phone number, doctor email id, on which day, time, place he available etc.
                    2) reporting : With reporting table, the user may ask for future meeting  details like activity date, activity type, activity mode. IF any future activity related detaill like date and calltype, what is the count of future meetings with doctor or how many meetings scheduled, then use reporting table
                    3) RCPA : With RCPA table, the user may ask for the already done or held interaction summary between the doctors and employee(sales representative) of specific activity date or dates in detail like what product is discussed, what is the feedback from the doctor.
                    and also THe RCPA table will have the doctor's  wockhard product quanity, products invovled in the prescribtion(rxn) and monetary value and aslo have the doctor's competitor  qunantity, rxn(prescribtion) and the monetary valueetc. 
                    How many times i connected with this specific doctor or how many meetings already held with this doctor like or this type of question, RCPA table needs to be used
                    the rxn will decide the doctors performance like if it is low, then the doctors performace is low and if it is high, then the doctors performace is high.
                    
                    And all the field values will be in string except date fields like activity date and upat will be in date datatype.

                    Check the attached schema for the above tables and their details.
                    Remember that i'm using pyton  to execute the aggregation pipeline.

                    Write a MongoDB Aggregation pipeline query.

                    Use the following as mongoDB collection to write the query: '{schema_name}'
                    Dont use it from other schemas fields. use other schema fields only in when lookup is used. in that also make user respective schema fields is being used.
                    
                    You are an expert in mongodb aggregation pipeline creation. 
                    Check the user question to create the aggregation from this collection itself. Current CollectionName: {coll_name}.
                    Check the user question whether the output aggregation pipeline can be generated with the above mongodb schema itself. 
                    Most of the cases the output canbe generated with single collection itself. If required, use lookup with other collection schema to write the query.
                    The some scenrios are the RCPA and reporting table will not have the doctors mobile number and email id and available calldays, call time, in that case only use lookup to get the doctors details with doctoruid
                    use the following additional mongoDb schema details to create the aggregation pipeline, if required, use the other collection schemas to create the aggregation pipeline using lookup.(THe above mongodb schema field will be duplicated below, ignore it)
                    Make sure, it is critical to use only the respective schema fields


                    {str([table for table in input['multiTables'] if table['tableName'] != coll_name]) }
                    """

                    additional_info = f"""Additional Context: {additional_context} 
                    For any questions related to date, remember today's date is {x} and it falls on {day_name} of the current week . A week always starts with Monday ends with Sunday.      
                    Strict Rules and Regulations:
                    
                    Its very critical to not use additional context like user match or date for generic query.
                    Date field will be in date datatype.
                    Its very critical to not add unnecassary match conditions if not prompted.
                    Its very critical Match queries must use $regex if field is type string, include case insensitive flag. 
                    Projection must exclude _id.
                    Projection must include the match field mandatorily.
                    Check the user question whether the output aggregation pipeline can be generated with the above mongodb schema itself. Dont add additional pipelines if not required.
                    If using $regex dont enclose it in /expression/ and dont use ^ and $ in regex field.
                    if lookup is used, the value will be in array, unwind it , then the field wil be in object format,  then in projection, create a new field according to the object fields and assign them.
                    For example :rcpaDetails is the lookup field and the object is like this,
                      rcpaDetails : {{"product" : "xxx",'brand':"yyy"}},
                    Then in projection, crate like this,
                    {{"product":"$rcpaDetails.product", "brand":"$rcpaDetails.brand"}}
                    PCPM = Total Sales (₹) in a Month / Number of Field Force (MRs) in the Team
                    In Projection, all the field value must be in string format(said only for object type of fields, if the field value is in object or dict, then only need to do this).so dont give it in object format. unwind it and then assign the field value in projection like above.
                    If lookup is not used dont do these things.
                    means all the date fields are already in date field only, so dont use for exisitng date field.
                    use when the date is need to use from llm like the user may ask for a spefic range and any particular range, in that time.  Use the following date as example, {{'$date': '2025-01-01T00:00:00.000Z'}}. DOnt use any other format.
                    Make sure, it is critical to use the respective schema fields.
                    Cycle is determined using (Apr-Jun 2025) + joining date
                    Since i told all the field datatypes is in string expect date, need to parse to double datatype for some fields like when it is used in $sum and doing other math functions like adding, subracting, multiply.
                    parse to double when it required. whenever the group aggregation is used ans operators like $sum is used. it is critical to parse into double and then add
                    Dont need to format any date value and give as it as in projection like updt': ---'$dateToString': 'format': '%Y-%m-%d %H:%M %p', 'date': '$updt'---, dont do this, give as it as.
                    While searching with name, in regex, dont use the Dr. dr prefix
                    Only respond with mongo aggregation query in a valid JSON list/array format without code block syntax around it and each pipeline should be closed within curly braces and quotes around each stage type. 
                    Always format response in this format. {{"pipeline":[],"collection_name_to_execute":""}}."""
                   
                    rules = f"Your task to generate a valid mongodb query based on the following user query or question: {prompt} and return the output in proper json using this format {{'pipeline':[]}}. {additional_context}. If its generic question return pipeline as empty list otherwise add atleast project stage. I need to run the query and later use llm to summarize so make sure all the necessary fields are in project."

                    # new_chat_store.append({"role": "user", "content": user_query})
                    # new_chat_store.append({"role": "user", "content": additional_info})
                    # new_chat_store.append({"role": "user", "content": rules})
                    print('new_chat_store  12345')

                    query = f'Task: {rules}\n\n{user_query}\n\n{additional_info}\n\n'
                    # print (query)

                # print('Chat_history', new_chat_store)
                # query = f'User Query: {user_query},\n Additional Information: {additional_info},\n Rules: {rules}'
                if not query:
                    response_ai = client.chat.completions.create(
                    # #response_ai = client.completions.create(
                        model="gpt-4o-mini",
                        #model="davinci-002",
                        #model="gpt-3.5-turbo-instruct",
                        response_format={ "type": "json_object" },
                        messages=new_chat_store,
                        temperature=0,
                        top_p=0.1
                        )
                    response = response_ai.choices[0].message.content
                    print ('Res==----------->,',response)
                    token_info = response_ai.usage
                    final_query =  response
                    query_text = repair_json(final_query)
                    print(f"1.----------------{query_text}-------------------")

                    #conveting it into json format .
                    python_object = json.loads(query_text)
                else:
                    model = genai.GenerativeModel('models/gemini-2.5-flash-preview-04-17')
                    response_ai = model.generate_content(query,generation_config={"temperature":0})
                    response = response_ai.text
                    query = format_json_llm(response)
                    # print ('Res==----------->,',query)
                    token_info = response_ai.usage_metadata
                    #final_query =  repair_json(query)
                    print ('New query==----------->,',query)
                    python_object = query
                    if 'collection_name_to_execute' in query:
                        schema_name = query['collection_name_to_execute']

                
                #repair the json format .
                
                if 'pipeline' in python_object and len(python_object['pipeline'])==0 and  not query:
                    return [],token_info,response
                elif 'pipeline' in python_object and len(python_object['pipeline'])==0 and  query:
                    print('Generic question')
                    prompt_final = f' Answer this question: {prompt} in a generic way. Provide the answer in a html code.'
                    # print(prompt)
                    response_final = model.generate_content(prompt_final)
                    result = format_html_llm(response_final.text)
                    return result, response_final.usage_metadata,response_final.text
                elif 'pipeline' in python_object and len(python_object['pipeline'])!=0 and  query:
                    old_pipeline = python_object['pipeline']
                    new_pipeline = match_stages(python_object['pipeline'])
                    python_object['pipeline'] = new_pipeline
                

                if permission_filter:
                    python_object['pipeline'].insert(0,permission_filter)
                    python_object['pipeline'].append({"$project": hide_keys})
                
                try:
                    if 'isAccessBased' in input and input['isAccessBased'] == True:
                        import requests
                        import jwt
                        token = input['headers']['Authorization'].split(' ')[1]
                        payload = jwt.decode(token, options={"verify_signature": False})
                        print("payload+_+_+_+_+_+_+_  ",payload,"     ",type(payload),'   ',payload['userId'])
                        #payload = json.loads(payload)
                        origin = input['headers']['Origin']
                        if "https://staging.aiqod.com:843" in origin:
                            # url = "http://127.0.0.1:7894/adhigam-api/website/combineLines"
                            url = "http://172.168.1.19:7894/gibots-api/user/type"
                            print(url)
                        else:
                            url = f"{origin}/gibots-api/user/type"
                            print("no")
                            
                        
                        print("url++++++++++++++",url)
                        jsonData = {"isAdmin": False, "type": "employee"}
                        headers = input.get('headers', {})

                        res_access = requests.post(url, headers=headers, json=jsonData)
                        res_access = res_access.json()
                        #print(" Response Content:", res_access)
                        userIds = []
                        if res_access['status'] == 0 and 'data' in res_access and len(res_access['data'])!=0:                            
                            userIds = list(map(lambda x: ObjectId(x['_id']), res_access['data']))
                        userIds.append(ObjectId(payload['userId']))
                        print("usersIDS ++ ++ + ++ + +  ",userIds)
                        user_permission_filter = { "$match": {"userId": {"$in": userIds}}}
                        if user_permission_filter and len(user_permission_filter)!=0:
                            python_object['pipeline'].insert(0,user_permission_filter)   
                except Exception as e:
                    print("Error in fetching user type",e)

                
                print(f"2.---------------{python_object['pipeline']}---------------{type(python_object['pipeline'])} --------  {schema_name}")
                # Fetching data from the database using the model query.
                if query:
                    myclient = pymongo.MongoClient('mongodb+srv://Yuvaraj:68DcFTTBrWCieCm@cluster0.uvgfy.mongodb.net/')
                    db = myclient['Test']
                    q_final = convert_date_fields(python_object['pipeline'])
                    q_final = transform_regex_fields(q_final)
                    print(q_final)

                    result_cursor = db.get_collection(schema_name).aggregate(q_final)
                    final_result = list(result_cursor)
                    if(len(final_result)>=100 or '$sum' in response):
                        q_final = convert_date_fields(old_pipeline)
                        q_final = transform_regex_fields(q_final)
                        print("lots of result, executing old query")
                        result_cursor = db.get_collection(schema_name).aggregate(q_final)
                        final_result = list(result_cursor)
                else:
                    result_cursor = db.get_collection(schema_name).aggregate(python_object['pipeline'])
                    final_result = list(result_cursor)

                # print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<{result_cursor}")
                
                print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<{len(final_result)}")
                

                if(len(final_result) == 0 and not query):
                    return [], token_info, response
                elif(len(final_result) == 0 and query):
                    prompt_final = f' Answer this question: {prompt} in a generic way. Provide the answer in a html code.'
                        # print(prompt)
                    response_final = model.generate_content(prompt_final)
                    result = format_html_llm(response_final.text)
                    return result, response_final.usage_metadata,response_final.text
                else:
                    format_output = []
                    for res in final_result:
                        format_obj = {}
                        for key in res:
                            if key in project_keys:
                                format_obj[project_keys[key]] = res[key]
                            elif key != '_id':
                                format_obj[key] = res[key]
                        format_output.append(format_obj)
                    final_result = format_output
                    if (len(final_result)<100 and query):
                        prompt_final = f'{additional_context}. Using this reference table data, {final_result}. {"Data Explanation:"+input["attachmentExplanation"] if "attachmentExplanation" in input else ""} Answer this question: {prompt}. Provide the answer in a html code using table with proper borders/paragraph tags with styling depending on the question.'
                        # print(prompt)
                        response_final = model.generate_content(prompt_final)
                        result = format_html_llm(response_final.text)
                        return result, response_final.usage_metadata,response_final.text
                    elif(final_result and query):
                        prompt_final = f'{additional_context}. Using this reference table data, {final_result[0:50]}. {"Data Explanation:"+input["attachmentExplanation"] if "attachmentExplanation" in input else ""} Answer this question: {prompt}. Provide the answer in a html code using table with proper borders/paragraph tags with styling depending on the question.'
                        # print(prompt)
                        response_final = model.generate_content(prompt_final)
                        result = format_html_llm(response_final.text)
                        return result, response_final.usage_metadata,response_final.text

                '''else:
                    for res in final_result:
                        if '_id' in res:
                            del res['_id']
            '''
                return final_result,token_info,response

            except ValueError as e:
                print(f"There are some error is causing in online Model---- {e}")
                return [], token_info, response

    except ValueError as ve:
        return [], None, None


        #     print(f"OpenAI {mode} Model is generating the query for you...")
        #     client = OpenAI()
        #     response_ai = client.chat.completions.create(
        #         model="gpt-3.5-turbo",
        #         messages=[
        #             {"role": "system", "content": complete_query}
        #         ]
        #     )
        #     response = response_ai.choices[0].message.content

        # final_query = str(response)
        # print ('Query',final_query)
        # # Extracting the query from the response from models.
        # #regex_pattern = r'(?s)\((.*?)\)'
        # #match = re.findall(regex_pattern, mongo_query)
        # #final_query = match[0]
        # #final_query = '['+final_query+']'
        # query_text = repair_json(final_query)  # Assuming repair_json is defined elsewhere
        # print(f"1.----------------{query_text}-------------------")
        # python_object = json.loads(query_text)
        # print(f"2.---------------{python_object}---------------")
        # print(type(python_object))

        # # Fetching data from the database using the model query.
        # result_cursor = collection.aggregate(python_object)

        # print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<{result_cursor}")
        # final_result = list(result_cursor)
        # if(len(final_result) == 0):
        #     return None

        # return final_result
    # except ValueError as ve:
    #     return None

    # return final_result


# @app.before_request
# def before_request():
#     # Log current process ID
#     print("Process ID:", os.getpid())
# import psutil
# @app.after_request
# def after_request(response):
#     # Get CPU and RAM usage
#     cpu_percent = psutil.cpu_percent()
#     ram = psutil.virtual_memory()
#     print (ram)
#     ram_usage = psutil.virtual_memory().used / (1024 ** 3)  # Convert to GB
#     # Log CPU and RAM usage
#     print("CPU Usage:", cpu_percent, "%")
#     print("RAM Usage:", ram_usage, "GB")
#     return response

def check_token_limit(limit, userid, user_token_from_db):
    if (len(user_token_from_db)>0):
        previous_input_token = 0
        previous_output_token = 0
        for document in user_token_from_db:
            previous_input_token += document['input_token_used']
            previous_output_token += document['output_token_used']
        input_cost_used = (previous_input_token/1000000)*0.5
        output_cost_used = (previous_output_token/1000000)*1.5
        threshold = 0.005 #to prevent generating large output
        total_cost = input_cost_used + output_cost_used + threshold
        print ('total cost', total_cost)
        if (total_cost>limit):
            return False
        else:
            return True
    else:
        return False

# Middleware function to check user authentication
def limitcheck_middleware_old(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import datetime

        x = datetime.datetime.now()
        print('start time',x,)
        input = request.json['input']
        limit_in_rupees = input['llm_api_limit']
        limit_in_dollars = limit_in_rupees/83 #83 for cost of dollars
        print ('Limit of user in dollars',limit_in_dollars)
        mode = input['mode']
        user_id = input['userId']
        subscriber_id = input['subscriberId']
        user_name = input['user']
        supervisor = input['supervisor']
        collection_name =  input['collN'] if 'collN' in input else None
        origin = request.headers['Origin']
        g.news_id = input['news_id'] if 'news_id' in input else ''
        if 'https://debug.aiqod.com:643/' in origin:
            uri = config['debugDbLink'] #"mongodb://gibotsdev:gibotsdev112233@server.gibots.com:2700/msmemaster"
            db_name = config['debugDb']
        elif 'https://staging.aiqod.com:843' in origin:
            uri = config['stageDbLink']
            db_name = config['stageDb']
        elif 'https://dev.aiqod.com:843' in origin:
            uri = config['devDbLink']
            db_name = config['devDb']
        elif 'https://demo.aiqod.com:3443' in origin:
            uri = config['demoDbLink']
            db_name = config['demoDb']
        else:
            uri = config['stageDbLink']
            db_name = config['stageDb']
        print(f"-------------{uri}----{db_name}")
        myclient = pymongo.MongoClient(uri)
        db = myclient[db_name]
        user_token_from_db = list(db.get_collection('LLM_Tokens').find({'subscriber_id': subscriber_id, 'mode': mode, 'collection': collection_name}))
        supervisor_name = ''
        employee_names = []
        subscriber = db.get_collection('subscribers').find_one({'_id':ObjectId(subscriber_id)})
        if 'defaultChatCollection' in subscriber and input['collN'] == 'Collab Pro' and subscriber['defaultChatCollection']:
            print('change to default collection')
            input['collN'] = subscriber['defaultChatCollection']
            print("Default collection",input['collN'])
            
        if (supervisor != 'admin'):
            supervisor_list = db.get_collection('users').find({"_id": ObjectId(supervisor)})
            for user in supervisor_list:
                supervisor_name = user['personalInfo']['name']
        else:
            employee_list = db.get_collection('users').find({'supervisor': ObjectId(user_id)})
            supervisor_name = supervisor
            for user in employee_list:
                if(user['personalInfo']['name']):
                    employee_names.append(user['personalInfo']['name'])
        print(employee_names)
        employee_names = ",".join(str(name) for name in employee_names)
        if(len(user_token_from_db)!=0):
            if not limit_in_dollars or not check_token_limit(limit_in_dollars, user_id, user_token_from_db):
                return json.dumps({'type':'str','response':'Chat Limit exceeded. Please purchase Chat Limit Addon package to continue using chatbot.' , 'response_type': 'limit_exceeded'})
        g.db = db
        g.uri = uri
        g.db_name = db_name
        g.user_token_from_db = user_token_from_db
        g.user_name = user_name
        g.supervisor_name = supervisor_name
        g.employee_names = employee_names
        return func(*args, **kwargs)
    return wrapper

from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)  # Convert Decimal to float
        return super(DecimalEncoder, self).default(obj)
import mysql.connector
from mysql.connector import Error

# import paramiko



def update_summary(query: str, response: str,result=None) -> str:
    prompt = f"""
    Update the conversation summary with this new interaction.
    Provide a comprehensive summary.
    Keep the extracted fields as it is. Dont pluralize or change spellings.
    Current summary: {g.summary}
    New query: {query}
    New response: {f'{response}.Product found. Ensure that you save the stock quantity available and price of product, matched product:{json.dumps(result)}'if result else response}
    Updated summary:
    """
    
    response = model.generate_content(prompt, request_options={'retry': my_retry})
    return response.text

def run_mysql_query(query, params=None):
    try:
                # SSH connection details
        ssh_host = "150.230.232.245"  # Your public IP
        ssh_port = 22
        ssh_username = "ubuntu"
        # ssh_pkey = "/home/ubuntu/new_ssd/publicfolder/liberty-fs/Ubuntu_Bastion1.key"
        ssh_pkey = "/home/user/Downloads/Ubuntu_Bastion1.key"
        import paramiko
        import json


        # MySQL connection details from the \status command
        mysql_host = "172.16.3.192"
        mysql_port = 3306
        mysql_username = "Aiqod"
        mysql_password = "A!q0DmyTVS25"  # Your password
        database_name = 'myTVSPartsmart'
        # Create SSH client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print("Connecting to SSH...")
        client.connect(hostname=ssh_host, port=ssh_port, username=ssh_username, key_filename=ssh_pkey)
        print("Connected to SSH")
        client.get_transport().set_keepalive(600) 
        remote_query_file = "/tmp/temp_query.sql"
        print("Creating temporary SQL file...")
        
        # Write the query to the file
        stdin, stdout, stderr = client.exec_command(f"cat > {remote_query_file}")
        stdin.write(query)
        stdin.flush()
        stdin.channel.shutdown_write()
        client.exec_command
        # Execute the query from the file
        print("Executing query...")
        cmd = f"mysqlsh --result-format=json/array --host={mysql_host} --port={mysql_port} --user={mysql_username} --password={mysql_password} --schema={database_name} --sql --file={remote_query_file} "
        stdin, stdout, stderr = client.exec_command(cmd)
        
        output = stdout.read().decode()
        stderr_output = stderr.read().decode()
        
        # Check for errors
        if stderr_output and not stderr_output.strip().startswith("WARNING: Using a password"):
            print(f"Error: {stderr_output}")
        
        client.exec_command(f"rm {remote_query_file}")
        print("Temporary file cleaned up")
        # Process the result
        if output:
            try:
                # Try to parse JSON
                result = json.loads(output)
                print("Query result:")
                print(len(result))
                return result
            except json.JSONDecodeError:
                print("Raw output (could not parse as JSON):")
                print(type(output))
        else:
            print("No output received")
        
        # Clean up the temporary file
        return []
        
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return []
    

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
    
def format_html_llm(text):
    regex_pattern = r'```html(.*?)```'
    match = re.findall(regex_pattern,text, flags=re.S)

    
    if match:       
        return match[0]
    else:
        return text

def format_sql_llm(text):
    regex_pattern = r'```sql(.*?)```'
    match = re.findall(regex_pattern,text, flags=re.S)

    
    if match:       
        return match[0]
    else:
        return None
       

def build_mongo_query_new(entities, optional_entities, collection):
    myclient = pymongo.MongoClient('mongodb+srv://Yuvaraj:68DcFTTBrWCieCm@cluster0.uvgfy.mongodb.net/')
    db = myclient['Test']
    def generate_query_prompt(fields):
        entities = fields
        return f"""
Convert these automotive part search parameters into a MongoDB Atlas Search query using this exact format:

[
  {{
    "$search": {{
      "index": "default",
      "compound": {{
        "must": [
          // Fuzzy text matches for vehicle details
          {{
            "text": {{
              "query": "MakeValue",
              "path": "Make",
              "fuzzy": {{"maxEdits": 2}}
            }}
          }},
          // Add more must clauses as needed
        ],
        "filter": [
          // Exact matches for categorical fields
          {{
            "text": {{
              "query": "YearValue",
              "path": "Year"
            }}
          }}
          // Add more filters as needed
        ]
      }}
    }}
  }}
]

### Entities to Convert:
{json.dumps(entities, indent=2)}

### Rules:
1. Prioritize fields in order: Make > Model > Varient > Components > Year > Fuel Type
2. Apply fuzzy search (maxEdits=2) to: Make, Model, Varient, Components, Fuel Type
3. Use exact matches for: Year
4. Include all provided entities
5. Maintain the exact JSON structure shown

### Example Input:
{{"Make": "Toyota", "Model": "Camry", "Year": "2020", "Fuel Type": "Petrol"}}

### Example Output:
[
  {{
    "$search": {{
      "index": "default",
      "compound": {{
        "must": [
          {{
            "text": {{
              "query": "Toyota",
              "path": "Make",
              "fuzzy": {{"maxEdits": 2}}
            }}
          }},
          {{
            "text": {{
              "query": "Camry",
              "path": "Model",
              "fuzzy": {{"maxEdits": 2}}
            }}
          }},
          {{
            "text": {{
              "query": "Petrol",
              "path": "Fuel Type",
              "fuzzy": {{"maxEdits": 2}}
            }}
          }}
        ],
        "filter": [
          {{
            "text": {{
              "query": "2020",
              "path": "Year"
            }}
          }},
          
        ]
      }}
    }}
  }}
]

### Current Entities:
{json.dumps(entities, indent=2)}

Generate ONLY the JSON array between ||:
||
"""
    def format_response(results,entity,addn=''):
        if not results:
            return "No products matched your search"
        
        format_prompt = f"""
Generate a clean HTML response for a chat interface using this product data provided below:


### Requirements:
1. No forms/input tags (chat interaction only)
2. Structure product info clearly with line breaks
3. Display stock availability prominently
4. Ask for quantity via natural language instruction
5. Use only these HTML tags: <b>, <br>, <div>
{addn}
### Example Output:
<div>
<b>Found Matching Part:</b><br>
- All Product Details
- Unit price
- Stock Available: 6 units<br><br>

<b>📦 How many units would you like?</b><br>
</div>

### User requirement:
{json.dumps(entity, indent=2)}

### Current Product Data:
{json.dumps(results, indent=2, cls=DecimalEncoder)}
Based on user requirement pick the most matching product
Generate ONLY the HTML response:
"""

        response = model.generate_content(format_prompt, request_options={'retry': my_retry})
        print(response.text)
        return format_html_llm(response.text)

    def execute_query(fields):
        # Generate query
        prompt = generate_query_prompt(fields)
        response = model.generate_content(prompt, request_options={'retry': my_retry})
        query = format_json_llm(response.text)
        print('Query',query)
        
        if not query:
            return None
            
        # Add projection and execute
        full_query = query + [{'$project': {'_id': 0}}]
        return list(db.get_collection(collection).aggregate(full_query))

    # Main execution flow
    all_entities = {**entities, **optional_entities}
    
    # Try search with all entities first
    results = execute_query(all_entities)
    print('Res',results)
    if results:
        response = format_response(results,all_entities)
        return response, results, ''

    # Fallback to required entities only
    if optional_entities:
        results = execute_query(entities)
        if results:
            response = format_response(results,entities,'The result is an alternate brand. So inform the user about the alternate brand whether its okay and ask about quantity needed.')
            return response,results,'alternate'
        
    return "No products matched your search",[],''

def build_sql_query_new(entities, optional_entities, collection):
   
    def generate_query_prompt(fields):
        entities = fields
        return f"""
Convert automotive search parameters into SQL WHERE conditions and append to this fixed query:

SELECT DISTINCT 
    G1.ID, G1.Line_Code, G1.Product_Number, G1.Item_Creation_Date, 
    G1.Product_Description,G1.Sales_Multiple, G1.Mrp_price, G1.List_price,
    G1.HSN_Code, G1.GST_Rate, G1.Brand_Name, G1.Aggregate, G1.Sub_Aggregate, 
    G1.Components,G2.Vehicle_ID, G3.Vehicle_Segment, 
    G3.Vehicle_Make,G3.Vehicle_Model, G3.Vehicle_Sub_Model, G3.Vehicle_Fuel_Type, 
    G3.Vehicle_FromYear, G3.Vehicle_ToYear,
    SUM(G4.AVAILABLE_TO_RESERVE) AS Total_Available,
    AVG(G4.COST_PRICE) AS Avg_Cost_Price,
    G4.BusinessName
FROM GB_ItemMaster AS G1
RIGHT JOIN GB_Vehicle_Mapping AS G2 
    ON G1.Product_Number = G2.Product_Number
LEFT JOIN GB_VehicleMaster AS G3 
    ON G2.Vehicle_ID = G3.Vehicle_ID
INNER JOIN InventoryData AS G4 
    ON G1.Product_Number = G4.ITEM_NUMBER
WHERE
{{conditions}}  <!-- Add generated conditions here -->


### Rules:
1. Field Mapping:
   - Vehicle_Make → G3.`Vehicle_Make`
   - Vehicle_Model → G3.`Vehicle_Model`
   - Vehicle_Sub_Model → G3.`Vehicle_Sub_Model`
   - Components → G1.`Components`
   - Vehicle_Fuel_Type → G3.`Vehicle_Fuel_Type`
   - Vehicle_Year → (G3.`Vehicle_FromYear` AND G3.`Vehicle_ToYear`)
   - Product_Number → G1.Product_Number
   and so on

2. Matching Logic:
   - Fuzzy Fields (LIKE + SOUNDEX):
     - Vehicle_Make, Vehicle_Model, Vehicle_Sub_Model, Components, Vehicle_Fuel_Type
   - Year Range:
     - Input year must be BETWEEN Vehicle_FromYear AND Vehicle_ToYear
   - Always add BusinessName equal to Oracle in conditions
     

3. Format Requirements:
   - Use table aliases (G1/G3) for all column references
   - Combine fuzzy methods with OR in parentheses
   - Maintain existing join structure
   - Make sure all entity value are used in filter

### Parameters:
{json.dumps(entities, indent=2)}

### Example Input:
{{"Vehicle_Make": "Toyota", "Vehicle_Model": "Camry", "Vehicle_Fuel_Type": "Gasoline"}}

### Example Output:
```sql
WHERE
    (G4.BusinessName = 'Oracle') 
    AND (G3.`Vehicle_Make` LIKE '%Toyota%'
     OR SOUNDEX(G3.`Vehicle_Make`) = SOUNDEX('Toyota'))

    AND (G3.`Vehicle_Model` LIKE '%Camry%'
         OR SOUNDEX(G3.`Vehicle_Model`) = SOUNDEX('Camry'))

    AND (G3.`Vehicle_Fuel_Type` LIKE '%Gasoline%'
         OR SOUNDEX(G3.`Vehicle_Fuel_Type`) = SOUNDEX('Gasoline'))
    /* Year Range check */
    AND (G3.`Vehicle_FromYear` <= 2015 AND G3.`Vehicle_ToYear` >= 2015)
```
Generate ONLY the WHERE clause and ORDER BY in sql.
"""
    
    def generate_query_prompt_initial(fields):
        entities = fields
        return f"""
Convert automotive search parameters into SQL WHERE conditions and append to this fixed query:

SELECT DISTINCT 
    G1.ID, G1.Line_Code, G1.Product_Number, G1.Item_Creation_Date, 
    G1.Product_Description,G1.Sales_Multiple, G1.Mrp_price, G1.List_price,
    G1.HSN_Code, G1.GST_Rate, G1.Brand_Name, G1.Aggregate, G1.Sub_Aggregate, 
    G1.Components,G2.Vehicle_ID, G3.Vehicle_Segment, 
    G3.Vehicle_Make,G3.Vehicle_Model, G3.Vehicle_Sub_Model, G3.Vehicle_Fuel_Type, 
    G3.Vehicle_FromYear, G3.Vehicle_ToYear,
    SUM(G4.AVAILABLE_TO_RESERVE) AS Total_Available,
    AVG(G4.COST_PRICE) AS Avg_Cost_Price,
    G4.BusinessName
FROM GB_ItemMaster AS G1
RIGHT JOIN GB_Vehicle_Mapping AS G2 
    ON G1.Product_Number = G2.Product_Number
LEFT JOIN GB_VehicleMaster AS G3 
    ON G2.Vehicle_ID = G3.Vehicle_ID
INNER JOIN InventoryData AS G4 
    ON G1.Product_Number = G4.ITEM_NUMBER
WHERE
{{conditions}}  <!-- Add generated conditions here -->


### Rules:
1. Field Mapping:
   - Vehicle_Make → G3.`Vehicle_Make`
   - Vehicle_Model → G3.`Vehicle_Model`
   - Vehicle_Sub_Model → G3.`Vehicle_Sub_Model`
   - Components → G1.`Components`
   - Vehicle_Fuel_Type → G3.`Vehicle_Fuel_Type`
   - Vehicle_Year → (G3.`Vehicle_FromYear` AND G3.`Vehicle_ToYear`)
   - Product_Number → G1.Product_Number
   and so on

2. Matching Logic:
   - Fuzzy Fields (LIKE + SOUNDEX):
     - Vehicle_Make, Vehicle_Model, Vehicle_Sub_Model, Components, Vehicle_Fuel_Type
   - Year Range:
     - Input year must be BETWEEN Vehicle_FromYear AND Vehicle_ToYear
   - Always add BusinessName equal to Oracle in conditions
     

3. Format Requirements:
   - Use table aliases (G1/G3) for all column references
   - Combine fuzzy methods with OR in parentheses
   - Maintain existing join structure
   - Make sure all entity value are used in filter

### Parameters:
{json.dumps(entities, indent=2)}

### Example Input:
{{"Vehicle_Make": "Toyota", "Vehicle_Model": "Camry", "Vehicle_Fuel_Type": "Gasoline"}}

### Example Output:
```sql
WHERE
    (G4.BusinessName = 'Oracle') 
    AND (G3.`Vehicle_Make` LIKE '%Toyota%')

    AND (G3.`Vehicle_Model` LIKE '%Camry%')

    AND (G3.`Vehicle_Fuel_Type` LIKE '%Gasoline%')
    /* Year Range check */
    AND (G3.`Vehicle_FromYear` <= 2015 AND G3.`Vehicle_ToYear` >= 2015)
```
Generate ONLY the WHERE clause and ORDER BY in sql.
"""
    
    def format_response(results,entity,addn=''):
        if not results:
            return "No products matched your search"
        
        format_prompt = f"""
Generate a clean HTML response for a chat interface using this product data provided below:


### Requirements:
1. No forms/input tags (chat interaction only)
2. Structure product info clearly with line breaks
3. Display stock availability prominently
4. Ask for quantity via natural language instruction
5. Use only these HTML tags: <b>, <br>, <div>
{addn}
### Example Output:
<div>
<b>Found Matching Part:</b><br>
- All Product Details
- Unit price
- Stock Available: 6 units<br><br>

<b>📦 How many units would you like?</b><br>
</div>

### User requirement:
{json.dumps(entity, indent=2)}

### Current Product Data:
{json.dumps(results, indent=2)}
Based on user requirement pick the most matching product
Generate ONLY the HTML response:
"""

        response = model.generate_content(format_prompt, request_options={'retry': my_retry})
        print(response.text)
        return format_html_llm(response.text)


    def execute_query(fields):
        # Generate query
        prompt = generate_query_prompt(fields)
        prompt_initial = generate_query_prompt_initial(fields)
        response = model.generate_content(prompt, request_options={'retry': my_retry})
        response_initial = model.generate_content(prompt_initial, request_options={'retry': my_retry})
        query_initial = format_sql_llm(response_initial.text)
        query = format_sql_llm(response.text)
        print('Query',query)
        final_query = f"""SELECT DISTINCT 
    G1.ID, G1.Line_Code, G1.Product_Number, G1.Item_Creation_Date, 
    G1.Product_Description,G1.Sales_Multiple, G1.Mrp_price, G1.List_price,
    G1.HSN_Code, G1.GST_Rate, G1.Brand_Name, G1.Aggregate, G1.Sub_Aggregate, 
    G1.Components,G2.Vehicle_ID, G3.Vehicle_Segment, 
    G3.Vehicle_Make,G3.Vehicle_Model, G3.Vehicle_Sub_Model, G3.Vehicle_Fuel_Type, 
    G3.Vehicle_FromYear, G3.Vehicle_ToYear,
    SUM(G4.AVAILABLE_TO_RESERVE) AS Total_Available,
    AVG(G4.COST_PRICE) AS Avg_Cost_Price,
    G4.BusinessName
FROM GB_ItemMaster AS G1
RIGHT JOIN GB_Vehicle_Mapping AS G2 
    ON G1.Product_Number = G2.Product_Number
LEFT JOIN GB_VehicleMaster AS G3 
    ON G2.Vehicle_ID = G3.Vehicle_ID
INNER JOIN InventoryData AS G4 
    ON G1.Product_Number = G4.ITEM_NUMBER
{query}
GROUP BY 
    G1.ID, G1.Line_Code, G1.Product_Number, G1.Item_Creation_Date, 
    G1.Product_Description, G1.Sales_Multiple, G1.Mrp_price, G1.List_price,
    G1.HSN_Code, G1.GST_Rate, G1.Brand_Name, G1.Aggregate, 
    G1.Sub_Aggregate, G1.Components, G2.Vehicle_ID, G3.Vehicle_Segment, 
    G3.Vehicle_Make, G3.Vehicle_Model, G3.Vehicle_Sub_Model, 
    G3.Vehicle_Fuel_Type, G3.Vehicle_FromYear, G3.Vehicle_ToYear, 
    G4.BusinessName;"""
        final_query_initial  =f"""SELECT DISTINCT 
    G1.ID, G1.Line_Code, G1.Product_Number, G1.Item_Creation_Date, 
    G1.Product_Description,G1.Sales_Multiple, G1.Mrp_price, G1.List_price,
    G1.HSN_Code, G1.GST_Rate, G1.Brand_Name, G1.Aggregate, G1.Sub_Aggregate, 
    G1.Components,G2.Vehicle_ID, G3.Vehicle_Segment, 
    G3.Vehicle_Make,G3.Vehicle_Model, G3.Vehicle_Sub_Model, G3.Vehicle_Fuel_Type, 
    G3.Vehicle_FromYear, G3.Vehicle_ToYear,
    SUM(G4.AVAILABLE_TO_RESERVE) AS Total_Available,
    AVG(G4.COST_PRICE) AS Avg_Cost_Price,
    G4.BusinessName
FROM GB_ItemMaster AS G1
RIGHT JOIN GB_Vehicle_Mapping AS G2 
    ON G1.Product_Number = G2.Product_Number
LEFT JOIN GB_VehicleMaster AS G3 
    ON G2.Vehicle_ID = G3.Vehicle_ID
INNER JOIN InventoryData AS G4 
    ON G1.Product_Number = G4.ITEM_NUMBER
{query_initial}
GROUP BY 
    G1.ID, G1.Line_Code, G1.Product_Number, G1.Item_Creation_Date, 
    G1.Product_Description, G1.Sales_Multiple, G1.Mrp_price, G1.List_price,
    G1.HSN_Code, G1.GST_Rate, G1.Brand_Name, G1.Aggregate, 
    G1.Sub_Aggregate, G1.Components, G2.Vehicle_ID, G3.Vehicle_Segment, 
    G3.Vehicle_Make, G3.Vehicle_Model, G3.Vehicle_Sub_Model, 
    G3.Vehicle_Fuel_Type, G3.Vehicle_FromYear, G3.Vehicle_ToYear, 
    G4.BusinessName;"""
        if not query and not query_initial:
            return None
        result_initial = run_mysql_query(final_query_initial)
        if result_initial and len(result_initial)>0:
            return result_initial
        return run_mysql_query(final_query)

    # Main execution flow
    all_entities = {**entities, **optional_entities}
    print(all_entities)
    # Try search with all entities first
    results = execute_query(all_entities)
    print('Res',results)
    if results and len(results) > 1:
        return 'Multi products',results,''
    elif results:
        response = format_response(results,all_entities)
        return response, results, ''

    # Fallback to required entities only
    # if optional_entities:
    #     results = execute_query(entities)
    #     if results:
    #         response = format_response(results,entities,'The result is an alternate brand. So inform the user about the alternate brand whether its okay and ask about quantity needed.')
    #         return response,results,'alternate'
        
    return "No products matched your search",[],''




def build_mongo_query_options_new(entities, project_entities, collection):
    myclient = pymongo.MongoClient('mongodb+srv://Yuvaraj:68DcFTTBrWCieCm@cluster0.uvgfy.mongodb.net/')
    db = myclient['Test']
    def generate_query_prompt(fields,project_fields):
        entities = fields
        return f"""
Convert these automotive part search parameters into a MongoDB Atlas Search query using this exact format:

[
  {{
    "$search": {{
      "index": "default",
      "compound": {{
        "must": [
          // Fuzzy text matches for vehicle details
          {{
            "text": {{
              "query": "MakeValue",
              "path": "Make",
              "fuzzy": {{"maxEdits": 2}}
            }}
          }},
          // Add more must clauses as needed
        ],
        "filter": [
          // Exact matches for categorical fields
          {{
            "text": {{
              "query": "YearValue",
              "path": "Year"
            }}
          }}
          // Add more filters as needed
        ]
      }}
    }}
  }},
  {{
    "$project": {project_fields}
  }}
]

### Entities to Convert:
{json.dumps(entities, indent=2)}

### Rules:
1. Prioritize fields in order: Make > Model > Varient > Components > Year > Fuel Type
2. Apply fuzzy search (maxEdits=2) to: Make, Model, Varient, Components, Fuel Type
3. Use exact matches for: Year
4. Include all provided entities
5. Maintain the exact JSON structure shown

### Example Input:
{{"Make": "Toyota", "Model": "Camry", "Year": "2020", "Fuel Type": "Petrol"}}

### Example Output:
[
  {{
    "$search": {{
      "index": "default",
      "compound": {{
        "must": [
          {{
            "text": {{
              "query": "Toyota",
              "path": "Make",
              "fuzzy": {{"maxEdits": 2}}
            }}
          }},
          {{
            "text": {{
              "query": "Camry",
              "path": "Model",
              "fuzzy": {{"maxEdits": 2}}
            }}
          }},
          {{
            "text": {{
              "query": "Petrol",
              "path": "Fuel Type",
              "fuzzy": {{"maxEdits": 2}}
            }}
          }}
        ],
        "filter": [
          {{
            "text": {{
              "query": "2020",
              "path": "Year"
            }}
          }},
          
        ]
      }}
    }}
  }},
   {{
    "$project": {{
    	"Varient": 1
    }}
  }}
]

### Current Entities:
{json.dumps(entities, indent=2)}

Generate ONLY the JSON array between ||:
||
"""
    

    def execute_query(fields,project_entities):
        # Generate query
        prompt = generate_query_prompt(fields,project_entities)
        response = model.generate_content(prompt, request_options={'retry': my_retry})
        query = format_json_llm(response.text)
        
        if not query:
            return None
            
        # Add projection and execute
        full_query = query+ [{'$project': {'_id': 0}}]
        print(full_query)
        return list(db.get_collection(collection).aggregate(full_query))

    # Main execution flow
   
    # Try search with all entities first
    results = execute_query(entities,project_entities)
    if results:
        return results


def build_sql_query_options_new(entities, project_entities, collection,summary):
    def generate_query_prompt(fields):
        entities = fields
        return f"""
Convert automotive search parameters into SQL WHERE conditions and append to this fixed query:

SELECT DISTINCT 
    G1.ID, G1.Line_Code, G1.Product_Number, G1.Item_Creation_Date, 
    G1.Product_Description,G1.Sales_Multiple, G1.Mrp_price, G1.List_price,
    G1.HSN_Code, G1.GST_Rate, G1.Brand_Name, G1.Aggregate, G1.Sub_Aggregate, 
    G1.Components,G2.Vehicle_ID, G3.Vehicle_Segment, 
    G3.Vehicle_Make,G3.Vehicle_Model, G3.Vehicle_Sub_Model, G3.Vehicle_Fuel_Type, 
    G3.Vehicle_FromYear, G3.Vehicle_ToYear,
    SUM(G4.AVAILABLE_TO_RESERVE) AS Total_Available,
    AVG(G4.COST_PRICE) AS Avg_Cost_Price,
    G4.BusinessName
FROM GB_ItemMaster AS G1
RIGHT JOIN GB_Vehicle_Mapping AS G2 
    ON G1.Product_Number = G2.Product_Number
LEFT JOIN GB_VehicleMaster AS G3 
    ON G2.Vehicle_ID = G3.Vehicle_ID
INNER JOIN InventoryData AS G4 
    ON G1.Product_Number = G4.ITEM_NUMBER
WHERE
{{conditions}}  <!-- Add generated conditions here -->


### Rules:
1. Field Mapping:
   - Vehicle_Make → G3.`Vehicle_Make`
   - Vehicle_Model → G3.`Vehicle_Model`
   - Vehicle_Sub_Model → G3.`Vehicle_Sub_Model`
   - Components → G1.`Components`
   - Vehicle_Fuel_Type → G3.`Vehicle_Fuel_Type`
   - Vehicle_Year → (G3.`Vehicle_FromYear` AND G3.`Vehicle_ToYear`)
   - Product_Number → G1.Product_Number
   and so on

2. Matching Logic:
   - Fuzzy Fields (LIKE + SOUNDEX):
     - Vehicle_Make, Vehicle_Model, Vehicle_Sub_Model, Components, Vehicle_Fuel_Type
   - Year Range:
     - Input year must be BETWEEN Vehicle_FromYear AND Vehicle_ToYear
   - Always add BusinessName equal to Oracle in conditions
   - Make sure all entity value are used in filter
     

3. Format Requirements:
   - Use table aliases (G1/G3) for all column references
   - Combine fuzzy methods with OR in parentheses
   - Maintain existing join structure

4. Overall Summary of transaction with user till now:
    - {g.summary}

### Parameters:
{json.dumps(entities, indent=2)}

### Example Input:
{{"Vehicle_Make": "Toyota", "Vehicle_Model": "Camry", "Vehicle_Fuel_Type": "Gasoline"}}

### Example Output:
```sql
WHERE
    (G4.BusinessName = 'Oracle') 
    AND (G3.`Vehicle_Make` LIKE '%Toyota%'
    OR SOUNDEX(G3.`Vehicle_Make`) = SOUNDEX('Toyota'))

    AND (G3.`Vehicle_Model` LIKE '%Camry%'
         OR SOUNDEX(G3.`Vehicle_Model`) = SOUNDEX('Camry'))

    AND (G3.`Vehicle_Fuel_Type` LIKE '%Gasoline%'
         OR SOUNDEX(G3.`Vehicle_Fuel_Type`) = SOUNDEX('Gasoline'))
    /* Year Range check */
    AND (G3.`Vehicle_FromYear` <= 2015 AND G3.`Vehicle_ToYear` >= 2015)
```
Generate ONLY the WHERE clause and ORDER BY in sql.
"""
    
    def generate_query_prompt_initial(fields):
        entities = fields
        return f"""
Convert automotive search parameters into SQL WHERE conditions and append to this fixed query:

SELECT DISTINCT 
    G1.ID, G1.Line_Code, G1.Product_Number, G1.Item_Creation_Date, 
    G1.Product_Description,G1.Sales_Multiple, G1.Mrp_price, G1.List_price,
    G1.HSN_Code, G1.GST_Rate, G1.Brand_Name, G1.Aggregate, G1.Sub_Aggregate, 
    G1.Components,G2.Vehicle_ID, G3.Vehicle_Segment, 
    G3.Vehicle_Make,G3.Vehicle_Model, G3.Vehicle_Sub_Model, G3.Vehicle_Fuel_Type, 
    G3.Vehicle_FromYear, G3.Vehicle_ToYear,
    SUM(G4.AVAILABLE_TO_RESERVE) AS Total_Available,
    AVG(G4.COST_PRICE) AS Avg_Cost_Price,
    G4.BusinessName
FROM GB_ItemMaster AS G1
RIGHT JOIN GB_Vehicle_Mapping AS G2 
    ON G1.Product_Number = G2.Product_Number
LEFT JOIN GB_VehicleMaster AS G3 
    ON G2.Vehicle_ID = G3.Vehicle_ID
INNER JOIN InventoryData AS G4 
    ON G1.Product_Number = G4.ITEM_NUMBER
WHERE
{{conditions}}  <!-- Add generated conditions here -->


### Rules:
1. Field Mapping:
   - Vehicle_Make → G3.`Vehicle_Make`
   - Vehicle_Model → G3.`Vehicle_Model`
   - Vehicle_Sub_Model → G3.`Vehicle_Sub_Model`
   - Components → G1.`Components`
   - Vehicle_Fuel_Type → G3.`Vehicle_Fuel_Type`
   - Vehicle_Year → (G3.`Vehicle_FromYear` AND G3.`Vehicle_ToYear`)
   - Product_Number → G1.Product_Number
   and so on

2. Matching Logic:
   - Fuzzy Fields (LIKE):
     - Vehicle_Make, Vehicle_Model, Vehicle_Sub_Model, Components, Vehicle_Fuel_Type
   - Year Range:
     - Input year must be BETWEEN Vehicle_FromYear AND Vehicle_ToYear
   - Always add BusinessName equal to Oracle in conditions
   - Make sure all entity value are used in filter
     

3. Format Requirements:
   - Use table aliases (G1/G3) for all column references
   - Combine fuzzy methods with OR in parentheses
   - Maintain existing join structure

4. Overall Summary of transaction with user till now:
    - {g.summary}

### Parameters:
{json.dumps(entities, indent=2)}
### Additional Information:
{g.summary}

### Example Input:
{{"Vehicle_Make": "Toyota", "Vehicle_Model": "Camry", "Vehicle_Fuel_Type": "Gasoline"}}

### Example Output:
```sql
WHERE
    (G4.BusinessName = 'Oracle') 
    AND (G3.`Vehicle_Make` LIKE '%Toyota%')

    AND (G3.`Vehicle_Model` LIKE '%Camry%')

    AND (G3.`Vehicle_Fuel_Type` LIKE '%Gasoline%')
    /* Year Range check */
    AND (G3.`Vehicle_FromYear` <= 2015 AND G3.`Vehicle_ToYear` >= 2015)
```
Generate ONLY the WHERE clause and ORDER BY in sql.
"""
    

    def execute_query(fields):
        # Generate query
        prompt = generate_query_prompt(fields)
        prompt_initial = generate_query_prompt_initial(fields)
        
        response_initial = model.generate_content(prompt_initial, request_options={'retry': my_retry})

        query_initial = format_sql_llm(response_initial.text)
        response = model.generate_content(prompt, request_options={'retry': my_retry})
        query = format_sql_llm(response.text)
        if not query and not query_initial:
            return None
        final_query = f"""SELECT DISTINCT 
    G1.ID, G1.Line_Code, G1.Product_Number, G1.Item_Creation_Date, 
    G1.Product_Description,G1.Sales_Multiple, G1.Mrp_price, G1.List_price,
    G1.HSN_Code, G1.GST_Rate, G1.Brand_Name, G1.Aggregate, G1.Sub_Aggregate, 
    G1.Components,G2.Vehicle_ID, G3.Vehicle_Segment, 
    G3.Vehicle_Make,G3.Vehicle_Model, G3.Vehicle_Sub_Model, G3.Vehicle_Fuel_Type, 
    G3.Vehicle_FromYear, G3.Vehicle_ToYear,
    G4.AVAILABLE_TO_RESERVE,
    G4.COST_PRICE,
    G4.BusinessName
FROM GB_ItemMaster AS G1
RIGHT JOIN GB_Vehicle_Mapping AS G2 
    ON G1.Product_Number = G2.Product_Number
LEFT JOIN GB_VehicleMaster AS G3 
    ON G2.Vehicle_ID = G3.Vehicle_ID
INNER JOIN InventoryData AS G4
    ON G1.Product_Number = G4.ITEM_NUMBER

"""
        result_initial = run_mysql_query(final_query+' '+query_initial)
        if result_initial and len(result_initial)>0:
            return result_initial
        print('here')
        
        return run_mysql_query(final_query+' '+query)
    
    def format_response(results,entity,addn=''):
        if not results:
            return "No products matched your search"
        
        format_prompt = f"""
Generate a clean HTML response for a chat interface using this product data provided below:


### Requirements:
1. No forms/input tags (chat interaction only)
2. Structure product info clearly with line breaks
3. Display stock availability prominently
4. Ask for quantity via natural language instruction
5. Use only these HTML tags: <b>, <br>, <div>
{addn}
### Example Output:
<div>
<b>Found Matching Part:</b><br>
- All Product Details
- Unit price
- Stock Available: 6 units<br><br>

<b>📦 How many units would you like?</b><br>
</div>

### User requirement:
{json.dumps(entity, indent=2)}

### Current Product Data:
{json.dumps(results, indent=2)}
Based on user requirement pick the most matching product
Generate ONLY the HTML response:
"""

        response = model.generate_content(format_prompt, request_options={'retry': my_retry})
        print(response.text)
        return format_html_llm(response.text)


    def get_next_entity_and_values(results, project_entities):
        summary = {}
        
        for entity in project_entities:
            if entity == 'Vehicle_Year':
                all_years = set()
                for res in results:
                    all_years.update(range(int(res['Vehicle_FromYear']), int(res['Vehicle_ToYear']) + 1))

                unique_values = sorted(all_years)
            else:
                unique_values = set(item[entity] for item in results if entity in item)
            if len(unique_values) > 1:
                return entity, summary, unique_values
            else:
                summary[entity] = list(unique_values)[0]
        
        return None, summary, []
    # Main execution flow
   
    # Try search with all entities first
    results = execute_query(entities)
    if results:
        if (len(results) == 1):
            response = format_response(results,entities)
            summary = update_summary('',response+'P.S: No need to fill any missing mandatory fields as product was found with existing entities')
            return response, summary, 'Product Found', ''
        
        entity, summary_values, unique_values = get_next_entity_and_values(results,project_entities)
        print('Entity',entity)
        print('Summary',summary_values)
        if(summary_values):
            summary = update_summary(g.question,f'Save these entity values in summary, {json.dumps(summary_values,indent=2)}')
        if not entity:
            return summary_values, summary, 'all', ''
        seen = set()
        unique_data = []
        if entity != 'Vehicle_Year':
            results = [{entity:item[entity]} for item in results]
            for d in results:
                # Convert dictionary to a frozenset of key-value tuples for hashing
                frozen = frozenset(d.items())
                if frozen not in seen:
                    seen.add(frozen)
                    unique_data.append(d)
        else:
            unique_data = unique_values
        
        return unique_data, summary,'entity', entity
    else:
        return [],summary,'Product unavailable',''


def saveOrderDetails(doc,fields):
    doc = {**doc,**fields}
    user_info = {'Order_Status':'Pending','user_id': g.input['userId'],'subscriber_id': g.input['subscriberId'],'session_id':g.session_id,'org_id': g.input['orgId'],'user_info':g.userInfo}
    final = {**doc,**user_info}
    try:
        result = g.db.get_collection('TVS_Order_Details').insert_one(final)
        inserted_id = result.inserted_id
        print("Inserted ID:", inserted_id)
        return inserted_id
    except Exception as e:
        print('Error while saving',e)

def predictflow(details):
    prompt = f"""
Based on this context {details} classify which should be the appropriate flow for next step.

1. Create_Order:
    - ONLY IF THE CUSTOMER EXPLICITLY MENTIONS THE DESIRED QUANTITY.
    - Only if user required quantity and product is found from history.
    - If all information is available in the conversation summary and user provides the quantity then verify if the quantity required is available in stock available if yes then create the order.
    - Create order details based on history and populate Order_Details and Order_Title and add in additional_info and return in this output format {{'Next_Flow':'Create_Order','Additional_info':{{'Order_Details':[{{'Brand_Name':'','Product_Number':'','Product_Description':'','Quantity':'','Price_Per_Unit':'','Total_Price':''}}],'Order_Title':''}}}}
2. Product_Search:
    - If all mandatory information is available and Missing_Mandatory_Fields is empty then next flow is to find the matching product
    - Return output in this format {{'Next_Flow':'Product_Search','Additional_info':'Details of product to seacth'}}
3. Product_Unavailable
    - If the user doesnt want alternate brand or stock availability for a product is 0 then mark Product_Unavailable key as yes.
    - Return output in this format {{'Next_Flow':'Product_Unavailable','Additional_info':'Detail of the product which is unavailable'}}
4. Stock_Quantity_Unavailable
    - when user requested quantity is less than stock available for a product.
    - Return output in this format {{'Next_Flow': 'Stock_Quantity_Unavailable','Additional_info': {{'Stock_Details':'Provide information about how much stock is requested vs available'}}}}
5. Missing_Fields:
    - When product is not found in details and Stock_Quantity_Requested is empty and mandatory fields are missing and populate output in this json {{'Next_Flow':'Missing_Fields','Additional_info':'Provide which mandatory field is missing.'}}
6. Stock_Quantity_Required:
    - When all necessary information is available, need to ask for stock desired by the user.
Instruction:
-If more than one flow matches, select it by order of it.
-Provide the reason for flow match in json.
-Return the output as json only
"""
    print(prompt)
    response = model.generate_content(prompt, request_options={'retry': my_retry})
    print('next flow',response.text)
    return format_json_llm(response.text)

def get_product_option(result):
    products_option = []
    for prod in result:
        products_option.append(f"\nBrand Name: {prod['Brand_Name']}\nProduct Number: {prod['Product_Number']}\nProduct Description: {prod['Product_Description']}\nStock Available: {prod['Total_Available']}\nPrice: {prod['Avg_Cost_Price']}")
    return products_option



def query_from_datasource(data,question,collection):
    try:
        print('intelligent query handler')
        question = str(question)
        primaryKeys = ','.join(data['primaryKeys'])
        secondaryKeys = ','.join(data['secondaryKeys'])
        # header_prompt = data['headerPrompt']
        # if g.summary:
        #     if is_topic_shift(question):
        #         g.summary = ''
        prompt = f"""
Extract automotive part search parameters from this query as JSON.


Mandatory Fields: {primaryKeys}.
Optional Fields: {secondaryKeys}.


**Current Context**:
- Previous Conversation: {g.summary}
- User Query: "{question}"



Rules to follow:
- First, determine if the current query introduces a new part search (different Make, different Model, different Component) that diverges from previous conversation.
- If the user query introduces a different vehicle OR different part than the previous summary, treat it as a NEW request and IGNORE the conversation summary.
- If the user query is a continuation of the previous conversation, include entity fields from the conversation summary in Extracted_Mandatory_Fields.
- Use exactly the same spelling/capitalization in Mandatory Fields as provided in primaryKeys.
- Extract all information explicitly mentioned in the current user query and dont pluralise.
- POPULATE FIELDS ONLY EXPLICITLY MENTIONED BY THE USER.
- For Optional_Fields, only include fields explicitly provided by the user. Do not include fields with None values.

Spelling Correction:
- Maintain brand-model relationships (e.g., "ato" → "Alto" when with Maruti)
- Auto-correct common misspellings using this reference:
    Brands: {{'Toyota', 'Maruti', 'Hyundai', ...}}
    Models: {{'Alto', 'Innova', 'Creta', ...}}
- Only correct when confidence >90% based on brand-model relationships
- Preserve exact capitalization of official names (e.g., "Toyota" not "toyta")



Populate the output in this python json format:
{{
  'Is this a continuation?': 'Yes/No',
  'Extracted_Mandatory_Fields': {{}}, 
  'Missing_Mandatory_Fields': [], 
  'question': '', 
  'Optional_Fields': {{}}, 
  'Stock_Quantity_Requested': ''
}}

Add all missing mandatory fields to the Missing_Mandatory_Fields list and ask user about this missing information.

"""
        print (prompt)
        
        response = model.generate_content(prompt,generation_config={
        "temperature":0.1}, request_options={'retry': my_retry})
        
        regex_pattern = r'```json(.*?)```'
        match = re.findall(regex_pattern, response.text, flags=re.S)
        if match:
            repaired_json = repair_json(match[0])
            response_out = json.loads(repaired_json)
            if response_out['Is this a continuation?'] == 'No':
                g.summary = ''
            response_out['Extracted_Mandatory_Fields'] = {k: v for k, v in response_out['Extracted_Mandatory_Fields'].items() if v not in [None, "None"]}
            g.question = question
            summary = update_summary(question,f'Store the Extracted_Mandatory_Fields as it is. Response: {json.dumps(repaired_json,indent=2)}')
            
            initial_response_details = '\nUser response: '+question+'\nModel response: '+response.text+'\n'+summary
            flow = predictflow(initial_response_details)
           
            print('Res',response_out)
            print('Summary',summary)
            count_of_token = response.usage_metadata.total_token_count
            if not g.summary or response_out['Is this a continuation?'] == 'No':
                add_info = {'Status':'New Enquiry'}
                g.add_info = {**add_info,**response_out['Extracted_Mandatory_Fields']}
            prod_search = None
            if(flow['Next_Flow']=='Missing_Fields'):
                if(len(response_out['Missing_Mandatory_Fields'])>0):
                    print('Missing only choice field')
                    optionField_set = set(data['optionKeys'])
                    Missing_set = set(response_out['Missing_Mandatory_Fields'])

                    common_elements = optionField_set.intersection(Missing_set)
                    common_elements_list = list(common_elements)
                    if (len(common_elements_list)>0):
                        result,summary,type,entity = build_sql_query_options_new(response_out['Extracted_Mandatory_Fields'],common_elements_list,collection,summary)
                        if (result and type == 'entity'):
                            question = f'Provide value for {entity} using these options.'
                            # if(len(common_elements_list) == 1):
                            
                            if (entity == 'Vehicle_Year'):
                                result = sorted(result, reverse=True)[:10]
                            else:
                                result = [doc[entity] for doc in result]
                            options = {'options':result}
                            return question,summary,count_of_token,options
                        elif(type=='all'): #found all the mandatory fiels
                            prod_search = True
                        elif(type=='Product Found'):
                            print('Result found using existing fields')
                            return result,summary,count_of_token,None
                        elif(type=='Product unavailable'):
                            print('Product not found')
                            additional_info = {'Status':'Product Unavailable'}
                            g.add_info = {**additional_info,**response_out['Extracted_Mandatory_Fields']}
                            summary = update_summary(summary,'Product Unavailable')
                            return 'No products found',summary,count_of_token,{'button':'Raise a ticket'}
                    if not prod_search:
                        return response_out['question'],summary,count_of_token,None
            elif(flow['Next_Flow']=='Stock_Quantity_Unavailable'):
                additional_info = {'Status':'Quantity Unavailable'}
                g.add_info = {**additional_info,**response_out['Extracted_Mandatory_Fields']}
                return flow['Additional_info']['Stock_Details'],summary,count_of_token,{'button':'Raise a ticket'}
            elif(flow['Next_Flow']=='Create_Order'):
                print('Order creating scenarion')

                additional_info = {'Status':'Order','Order_Status':'pending approval'}
                order_details = {'Order_Details':flow['Additional_info']['Order_Details']}
                g.add_info = {**additional_info,**order_details,**response_out['Extracted_Mandatory_Fields']}
                id = saveOrderDetails(order_details,response_out['Extracted_Mandatory_Fields'])
                return flow['Additional_info']['Order_Title'],summary,count_of_token,{'button':'Create Order','orderId':id}
            elif(flow['Next_Flow']=='Product_Unavailable'):
                additional_info = {'Status':'Product Unavailable'}
                g.add_info = {**additional_info,**response_out['Extracted_Mandatory_Fields']}
                return 'No products found',summary,count_of_token,{'button':'Raise a ticket'}
            if(flow['Next_Flow']=='Product_Search' or flow['Next_Flow'] =='Stock_Quantity_Required' or prod_search):
                print('Finding app product')
                response, result, type = build_sql_query_new(response_out['Extracted_Mandatory_Fields'],response_out['Optional_Fields'],collection)
                if('Multi products' in response):
                    options = get_product_option(result)
                    options_dict = {"options":options}
                    summary = update_summary(summary,f'Multiple products were found from search. Customer will provide the Product Number from these options. Once customer selects product next flow is to ask for desired quantity.{ json.dumps(options,indent=2)}')
                    return 'Select the product you want to buy using these options.',summary,count_of_token,options_dict
                elif('No products' in response):
                    additional_info = {'Status':'Product Unavailable'}
                    g.add_info = {**additional_info,**response_out['Extracted_Mandatory_Fields']}
                    summary = update_summary(summary,'Product Unavailable')
                    return 'No products found',summary,count_of_token,{'button':'Raise a ticket'}
                elif type and type == 'alternate':
                    additional_info = {'Status':'Alternate product'}
                    g.add_info = {**additional_info,**response_out['Extracted_Mandatory_Fields'],**response_out['Optional_Fields']}
                    summary = update_summary(question,response)
                    print(result)
                else:
                    summary = update_summary(question,response,result)
                return response,summary,count_of_token,None
    except Exception as e:
        print(e)






def generate_session_id():
    user_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', '')
    if 'userInfo' in request.json:
        data = request.json['userInfo']
        name = data.get("name", "")  # Default to empty string if key is missing
        email = data.get("email", "")
        mobile = data.get("mobile", "")
        session_string = f'{user_ip}{user_agent}{name}{email}{mobile}'
    else:
        session_string = f'{user_ip}{user_agent}'
    return hashlib.sha256(session_string.encode()).hexdigest()




def limitcheck_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        import datetime

        x = datetime.datetime.now()
        g.start_time = time.time()
        session_id = generate_session_id()
        print('start time',x,'session id',session_id)

        input = request.json['input']
        collection_name =  input['collN'] if 'collN' in input else None #"Invoice_Document_GENAI"
        context_switch = False
        if 'contextSwitch' in request.json:
            context_switch = request.json['contextSwitch']
            print('Switch context',context_switch)
        
        origin = request.headers['Origin']
        userId = input['userId']
        uri = config['stageDbLink']
        db_name = config['stageDb']

        myclient = pymongo.MongoClient(uri)
        db = myclient[db_name]
        previous_total_token = 0
        api_call_count = 0
        type = ''
        g.userInfo = {}
        if 'userInfo' in request.json:
            type = 'chatplugin'
            g.userInfo = request.json['userInfo']
        else:
            type = 'website'

        user_token_from_db = list(db.get_collection('LLM_Tokens').find({'userId': userId,'collection': collection_name}))
        if (len(user_token_from_db)>0):
            for document in user_token_from_db:
                previous_total_token = document['total_token_used']
                api_call_count = document['api_call_count']

        user_history_list = list(db.get_collection('SmartChatHistory').find({'session_id':session_id,'type':type,'current': True,'collection': collection_name}))
        user_history = None
        summary = ''
        if (len(user_history_list)>0):
            for document in user_history_list:
                user_history = document['history']
                summary = document['Summary']
        if context_switch:
            summary = ''
        g.location = request.json['location'] if 'location' in request.json else ''    
        g.session_id = session_id             
        g.db = db
        g.uri = uri
        g.user_history = user_history
        g.type = type
        g.db_name = db_name
        g.summary = summary
        g.collection = collection_name
        g.user_token_from_db = user_token_from_db
        g.previous_total_token = previous_total_token
        g.api_call_count = api_call_count
        g.input = input
        return func(*args, **kwargs)
    return wrapper


def addentry_middleware(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        #if isinstance(response, Response) and response.is_json:
        response_data = json.loads(response)
        print (response_data)
        db = g.db
        previous_total_token = g.previous_total_token
        api_call_count = g.api_call_count
        collection = g.collection

        import datetime
        session_id = g.session_id
        question = g.input['prompt']

        answer = str(response_data['response'])
        total = time.time()-g.start_time
        api_history = {
            'question': question,
            'answer': answer,
            'executed_time': datetime.datetime.utcnow(),
            'time_taken': total,
            'token_size': response_data['count'],
            'add_info': g.add_info if hasattr(g,'add_info') else ''
        }
        summary = response_data['summary'] if 'summary' in response_data else ''
        location = g.location
        if summary:
            if response_data['type'] == 'button':
                summary = ''
        chatbot_history = db.get_collection('SmartChatHistory').find_one({'user_id': g.input['userId'],'session_id':session_id,'type':g.type,'current': True,'collection':collection})
        
        if not chatbot_history or (chatbot_history and len(bson.BSON.encode(chatbot_history)) >= 16 * 1024 * 1024): 
            if chatbot_history and (len(bson.BSON.encode(chatbot_history)) >= 16 * 1024 * 1024):
                db.get_collection('SmartChatHistory').update_one({"_id":chatbot_history['_id']},{"current": False})     
            new_chat_history = {'user_id': g.input['userId'],'subscriber_id': g.input['subscriberId'],'session_id':session_id,'org_id': g.input['orgId'],'collection': collection, 'current': True, 
                                'Summary': summary,'location':location,   'api_count':1,'type': g.type, 'history': [api_history]}
            db.get_collection('SmartChatHistory').insert_one(new_chat_history)
        else:
            db.get_collection('SmartChatHistory').update_one({'user_id': g.input['userId'],'session_id':session_id,'type':g.type,'current': True,'collection':collection},{
                            "$push": {
                                'history': api_history
                            },
                            "$inc": {
                                'api_count': 1
                            },
                            "$set": {
                                "Summary": summary,
                                "location":location
                            }
                        })




        token_data = {
            'total_token_used': previous_total_token + int(response_data['count']),
            'api_call_count': api_call_count + 1,
            'process': 'smart_chat',
            'collection': g.collection,
            'subscriber_id': g.input['subscriberId'],
            'org_id': g.input['orgId'],
            'user_id': g.input['userId'],
            'mode': g.input['mode'],
            "created_time": datetime.datetime.utcnow(),
        }

        db.get_collection('LLM_Tokens').update_one({'userId': g.input['userId'],'mode': g.input['mode']}, {"$set": token_data}, upsert=True)
        return json.dumps(response_data, default=str)
    return wrapper

def getMultiCollectionName(collectionNames,db,input):
    print('inside getMultiCollectionName')
    tableMetaData = list(db.get_collection("tablemetadatas").find({'tableName': {"$in":collectionNames}, 'chat': True}))
    print('tableMetaData length   ',len(tableMetaData))
    tableToFind = []
    print('tableToFind   ',tableToFind)
    attachmentExplanation = []
    if tableMetaData:
        for table in tableMetaData:
            if table.get('isAttachExplanation') is True and "attachmentExplanation" in table:
                print( 'inside isAttachExplanation')
                tableDic={}
                tableDic['tableName'] = table['tableName']
                tableDic['explanation'] = table['attachmentExplanation']
                attachmentExplanation.append({'TableName': table['tableName'],'FieldDescription':table['attachmentExplanation']})
                tableDic['fields']=[]
                for fields in table['fields']:
                        if 'description' in fields and fields['description']:
                            tableDic['fields'].append((fields['dbName'], fields['description']))
                tableToFind.append(tableDic)
                print( 'inside isAttachExplanation11')
    
    print( 'inside isAttachExplanation111')
    if len(tableToFind) == 0:
        return None
    userQuery = input['prompt']
    input['multiTables'] = tableToFind

    prompt =f'''
    You are an expert AI assistant specialized in document classification. Given a document and a list of predefined document types with their descriptions, your task is to accurately identify the correct document type.

    Instructions:
    Analyze the given user query to understand its content, purpose, and structure.
    Compare the user query with the provided document type descriptions and determine which one it best matches.
    Select only one document type that most accurately represents the given uer query.
    All the three collections will have doctor name and employee name. 
    The user may ask questions like what is the doctor's mobile number, email id, doctor region and doctor unique id and on which date, day, time doctor available for the activity  and more personal doctor related details. This table or schema is all about doctor related details only. then it is  DML.

    if it is wockhard rxn, performance or productivity of the doctors, precribtion values, last visit summary, last activty, last interaction, product and brand details and This table will tell about the interaction activity which is already held or done with the employee(sales representative) and doctor.  This table will have the details like the activity date, what product and brand is discussed,how many wockhardt product and how many competitor product is prescribed and all will have. Quantity means no of wockhard products involved or sold to the patients. Rxn means no of prescribtions are with wockhardt product. Value means how much money generate by that doctor. Like wise compquanity, comprxn, compvalue will tell about the competitor performance. The user may ask questions like what is the last interaction between the employee and doctors, then we have to give brand, product, activity date, doctor name, employee name.Here interaction also means activity, inputs, discussion, summary and similar words. And the next type of questions will be based on the wockhardt quantity, rxn, value. These three will tell about the doctors performance with wockhardt. If any doctor’s performance related questions is being asked then it is related with rxn field. If the user asked about the total money generated with the wockhardt and competitor product then it with value and compvalue field. If the user asked with wochhardt product quantity related details then ir with quantity field like wise same for compquanity. THe user may ask like how many time i connected with doctor  or specific doctor, as i told this table will maintain the already done or held details, this table will have to use.then it is  RCPA table.

    if it is related future meeting deatils  like activity date and activity calltype ,how many calls with doctor on specific date or particalur date range means 'reporting' and also . This table will tell about the further activity details like activity date, activity call type. As i told this table or schema will tell only about the future or further activity related details like activity date, activity call type. The user may ask questions related to further activity dates and call type with the doctor. THe user may ask like how many times will i have to connect with the specific doctor. as i told this table will maintain the future or further activity details, this table will have to use for future related connection details. means reporting table only.
    Reporting table will have the employee name doctor name, future meeting activity date and call type. it doesn't have any what is going to discuss and all.
    so determine accordingly.
    Do not generate multiple classifications or create new types; strictly choose from the given list.
    If the question is related to doctor classification/segment use DML
    HQ, Ex HQ, Outstation are related to DML townType.
    Provide a brief justification for your choice based on the document’s characteristics and the given descriptions.

    Input Format:
    user query: {userQuery}

    Document Types & Descriptions:
    {attachmentExplanation}
    …

    Output Format:
    Always format response in this format. {{"document_type":"","reason":""}}.
    '''
    # print('prompt   ',prompt)   
    # reqDocumentType,usage = callopenai([{"role":"system","content":prompt}])
    # reqDocumentType = json.loads(reqDocumentType)
    response = model.generate_content(prompt)
    reqDocumentType = format_json_llm(response.text)
    
    print('reqDocumentType    type', type(reqDocumentType)) 
    # print('reqDocumentType   ', reqDocumentType['document_type']) 

    return reqDocumentType['document_type'] if reqDocumentType and 'document_type' in reqDocumentType else input['previousCollection']
@app.route('/chatbot/chat',methods=['GET', 'POST'])
@limitcheck_middleware_old

def chatbot():
    # sem.acquire()


    from llama_index import SummaryIndex
    from MongoReader import SimpleMongoReader

    #from llama_index.readers import SimpleMongoReader

    from llama_index.storage.chat_store import SimpleChatStore
    from llama_index.memory import ChatMemoryBuffer
    import json

    print('using this smart chat',request.headers['Origin'])
    
    try:
        data=request.json
        print(f"data-----------{data}")
        input =data['input']
        collection_name =  input['collN'] if 'collN' in input else None #"Invoice_Document_GENAI"
        uri = g.uri
        db_name = g.db_name
        #uri = config['dbConnection']
        print (uri, db_name)
        query_dict = input['query'] if 'query' in input else {}
        field_names = []
        prompt = input['prompt']
        #db_name = config['db']
        options = config['options']
        userId = input['userId']
        input['username'] = g.user_name
        input['supervisor_name'] = g.supervisor_name
        input['employee_names'] = g.employee_names
        input['headers'] = request.headers
        # myclient = pymongo.MongoClient(uri)
        # db = myclient[db_name]
        db = g.db
        mode = input['mode']
        exception_message = {'type':'str',
                'status':1,
                'response': """We're sorry, but the requested data could not be found.
                Please try again with different criteria or provide additional details to help us locate the information you're looking for. If the issue persists, feel free to reach out to our support team for further assistance.
                Thank you for your understanding.""",
                'response_type': 'output'}


        if not collection_name:
            # classified_collection = typeDetection(prompt, options, llm)
            # if not classified_collection:
            #     return json.dumps({'type':'arr','response':options,'response_type':'options'})
            # elif classified_collection == 'Others':
            #     return json.dumps({'type':'arr','response':options,'response_type':'options'})
            # else:
            #     collection_name = classified_collection
            return json.dumps(exception_message)
        input['previousCollection'] = ''
        try:
            if collection_name:
                table_metadata = None
                for y in db.get_collection("tablemetadatas").find({'tableName': collection_name, 'chat': True}):
                    table_metadata = y

                if table_metadata.get('isMultiCollection') is True:
                    print('inside isMultiCollection')

                    if 'multiCollection' in table_metadata:
                        collectionNames = table_metadata['multiCollection'].split(",")
                        print('collectionNames   ',collectionNames)
                        input['isMultiCollection'] = True
                        input['previousCollection'] = collection_name
                        collection_name = getMultiCollectionName(collectionNames,db,input)
                        print("length of the multi collection name",len(input['multiTables']))
                        # multiTables = getMultiCollectionName(collectionNames,db,input)
                        # input['multiTables'] = multiTables
                    
                    else:
                        raise("MultiCollection is True but multiCollection is not present in tablemetadata")
                        


        except Exception as e:
            print('Error in getting collection name',e)
            return json.dumps(exception_message)


        print ('Classified collection name', collection_name)
        if (collection_name in config['copilot']):
            collection_name = config['copilot'][collection_name]
        field_keys = []
        hide_keys = {'subscriberId': 0,'orgId': 0,'creatorId':0,'userId':0}
        project_keys = {}
        input['isAccessBased'] = False
        input['isAttachExplanation'] = False
        input['attachmentExplanation'] = False
        if collection_name:
            table_metadata = None
            for y in db.get_collection("tablemetadatas").find({'tableName': collection_name, 'chat': True}):
                table_metadata = y
                print('helllo  ',y)

            if table_metadata:
                for fields in table_metadata['fields']:
                    if 'description' in fields and fields['description']:
                        field_keys.append((fields['dbName'], fields['description']))
                        project_keys[fields['dbName']] = fields['uiName']
                    else:
                        hide_keys[fields['dbName']] = 0
                
            if table_metadata.get('isAccessBased') is True:
                print('inside isAccessBased')
                input['isAccessBased'] = True
                input['tableMetaData'] = table_metadata

            if table_metadata.get('isAttachExplanation') is True:
                print('inside isAttachExplanation' )
                input['isAttachExplanation'] = True
                input['attachmentExplanation'] = table_metadata['attachmentExplanation']
        input['tableMetaData'] = {}
        print("input ",input['tableMetaData'],' isaccessbased   ',   input['isAccessBased'] )
        print("input ",input['isAttachExplanation'],' attachmentExplanation   ',   input['attachmentExplanation'] )
        input['hide_keys'] = hide_keys
        input['project_keys'] = project_keys
        if (len(field_keys) == 0):
            print ('Inside retre...')
            return json.dumps(exception_message)

        count_of_tokens = 0
        if (mode!='online'):
            reader = SimpleMongoReader(uri=uri)
            documents = reader.load_data(
                db_name, collection_name, field_names,separator=' ', query_dict=query_dict, metadata_names=field_names
            )

            for doc in documents:
                text = doc.get_content()
                meta = doc.get_metadata_str()
                individual_doc_count = get_tokens_and_count(text+' '+meta,tokenizer)
                count_of_tokens += individual_doc_count

        previous_input_token = 0
        previous_output_token = 0
        previous_total_token = 0
        api_call_count = 0

        user_token_from_db = g.user_token_from_db #list(db.get_collection('LLM_Tokens').find({'userId': userId, 'mode': mode}))
        if (len(user_token_from_db)>0):
            for document in user_token_from_db:
                previous_input_token = document['input_token_used']
                previous_output_token = document['output_token_used']
                previous_total_token = document['total_token_used']
                api_call_count = document['api_call_count']

        user_chat_from_db = list(db.get_collection('SmartChatHistory').find({'userId': userId, 'mode': mode}))
        chat_store = None
        chat_memory = None
        if(mode == 'offline'):
            if (len(user_chat_from_db)>0):
                user_chat_history = None
                for chat in user_chat_from_db:
                    user_chat_history = chat['history']
                with open('persist.json', "w") as f:
                    f.write(json.dumps(user_chat_history))
                chat_store = SimpleChatStore.from_persist_path(
                    persist_path="persist.json"
                )
            else:
                chat_store = SimpleChatStore()

            chat_memory = ChatMemoryBuffer.from_defaults(
                token_limit=5000,
                chat_store=chat_store,
                chat_store_key=userId,
            )
        elif(mode == 'online'):
            print ('Inside retre')
            if(len(user_chat_from_db)>0):
                for chat in user_chat_from_db:
                    chat_store = chat['history']
            else:
                chat_store = [
                    {"role": "system", "content": "I'm going to ask to generate a MongoDB aggregation pipeline. Use mongoQuery to parse this data."}
                ]

        #count_of_tokens < 4000
        type = None
        response = None
        print ('Count of tokens for the data', count_of_tokens, collection_name)

        token = None
        response_ai = None
        chat_engine = None
        if (collection_name == 'Others'):
            print("checking 1")
            from llama_index.chat_engine import SimpleChatEngine
            type = 'context'
            chat_engine = SimpleChatEngine.from_defaults(memory=chat_memory,service_context=service_context)
            response = chat_engine.chat(prompt)
        elif (count_of_tokens < 1000 and mode == 'offline'):
            print("checking 2")
            from llama_index.chat_engine import SimpleChatEngine
            type = 'context'
            index = SummaryIndex.from_documents(documents,service_context=service_context)
            chat_engine = index.as_chat_engine(
                chat_mode="context",
                memory=chat_memory,
                system_prompt=(
                    "You are a chatbot, able to have normal interactions, as well as talk"
                ),
                verbose=False
            )
            #query_engine = index.as_query_engine()
            response = chat_engine.chat(prompt)
        else:
            print("checking 3")
            type = 'query'
            # try:
            #     chat_history = chat_store.store[userId]
            # except:
            #     chat_history = []
            #chat_engine = SimpleChatEngine.from_defaults(chat_history=chat_history)
            if(collection_name == "Collab Pro"):

                response_of_find_objective, token = find_objective(prompt, {}, mode, chat_store,input)
                objective = response_of_find_objective["output"]["objective"]
                context = response_of_find_objective["output"]["context"]
                print(objective)
                if(objective != 'completeTask'):
                    result, token, response_ai = create_query_retrieve_data(db, field_keys, collection_name, prompt, {}, mode, chat_store,input)
                else:
                    print('calling complete task')
                    result = complete_task(db, field_keys, collection_name, prompt, {}, mode, chat_store,input,context)
            else:
                result, token, response_ai = create_query_retrieve_data(db, field_keys, collection_name, prompt, {}, mode, chat_store,input)
            if (result and len(result)>0):
                response = result
            else:
                response = []
            #call db query method
        #outputData['Execution_time'] = "{:.6f}".format(execution_time)


        if (mode == 'online' and hasattr(token, 'prompt_tokens')):
            print("checking 4")
            current_inp_token = token.prompt_tokens
            current_out_token = token.completion_tokens
            current_tot_token = token.total_tokens

            assistant_response = {
                'role': 'assistant',
                'content': response_ai
            }
            chat_store.append(assistant_response)
            db_obj = {
                'userId': userId,
                'history': chat_store,
                'mode': mode
            }
            db.get_collection('SmartChatHistory').update_one({'userId': userId,'mode': mode}, {"$set": db_obj}, upsert=True)
        elif (mode == 'online' and hasattr(token, 'prompt_token_count')):
            print("checking 5")
            current_inp_token = token.prompt_token_count
            current_out_token = token.candidates_token_count
            current_tot_token = token.total_token_count

            assistant_response = {
                'role': 'assistant',
                'content': response_ai
            }
            chat_store.append(assistant_response)
            db_obj = {
                'userId': userId,
                'history': chat_store,
                'mode': mode,
                'model': 'gemini'
            }
            db.get_collection('SmartChatHistory').update_one({'userId': userId,'mode': mode}, {"$set": db_obj}, upsert=True)
        else:
            print("checking 6")
            updated_history = chat_store.json()
            #print (token_counter)
            tokenizer = AutoTokenizer.from_pretrained("NousResearch/Llama-2-7b-chat-hf")
            token_counter = TokenCountingHandler(
            tokenizer=tokenizer.encode
            )

            current_inp_token = token_counter.prompt_llm_token_count
            current_out_token = token_counter.completion_llm_token_count
            current_tot_token = token_counter.total_llm_token_count
            db_obj = {
                'userId': userId,
                'history': updated_history,
                'mode': mode
            }
            db.get_collection('SmartChatHistory').update_one({'userId': userId,'mode': mode}, {"$set": db_obj}, upsert=True)

        import datetime
        token_data = {
            'input_token_used': previous_input_token + current_inp_token,
            'output_token_used': previous_output_token + current_out_token,
            'total_token_used': previous_total_token + current_tot_token,
            'api_call_count': api_call_count + 1,
            'process': 'smart_chat',
            'subscriber_id': input['subscriberId'],
            'org_id': input['orgId'],
            'user_id': input['userId'],
            'mode': mode,
            "created_time": datetime.datetime.utcnow()
        }
        db.get_collection('LLM_Tokens').update_one({'userId': userId,'mode': mode, 'collection': collection_name}, {"$set": token_data}, upsert=True)
        # print (response)
        outputData = None
        if (type == 'context'):
            outputData={'type':'str','status':1,'response':str(response) , 'response_type': 'output'}
        else :
            if (len(response) == 0):
                outputData={'type':'str','status':1,'response':"No data found for the query. Please try again with different criteria or provide additional details to help us locate the information you're looking for.", 'response_type': 'output'}
            elif(isinstance(response,dict) and response):
                outputData={'type':'str','response':response , 'response_type': 'output'}
            elif (isinstance(response,str) and len(response)>0):
                outputData={'type':'str','status':0,'response':response , 'response_type': 'output'}
            else:
                outputData={'type':'arr','status':0,'response':response , 'response_type': 'output'}
        x = datetime.datetime.now()
        print('end time',x)
        return json.dumps(outputData, default=str)

    except Exception as e:
        # sem.release()
        print('this is an ERROR message', e)
        return json.dumps({'type':'str','status':1,
                'response': """We're sorry, but the requested data could not be found.
                Please try again with different criteria or provide additional details to help us locate the information you're looking for. If the issue persists, feel free to reach out to our support team for further assistance.
                Thank you for your understanding.""",
                'response_type': 'output'})

@app.route('/chatbot/findColl',methods=['GET', 'POST'])
@limitcheck_middleware
def findColl():
    # sem.acquire()


    from llama_index import SummaryIndex
    from MongoReader import SimpleMongoReader

    #from llama_index.readers import SimpleMongoReader

    from llama_index.storage.chat_store import SimpleChatStore
    from llama_index.memory import ChatMemoryBuffer
    import json

    print('using this smart chat',request.headers['Origin'])
    print('execuu1111......')
    try:
        data=request.json
        print('execuu22222......')
        print(f"data-----------{data}")
        db = g.db
        categoryDetail=db.get_collection('chatGenieCategory').find({'Category':data['input']['collN'],'subscriberId':ObjectId(data['input']['subscriberId'])})
        categoryDetail_list = list(categoryDetail)
        print('execuu3333......')
        # collections_info={}
        # for document in categoryDetail:
        #     collections_info[document['Category']]=document['Description']
        # collections_description = '\n'.join([f"{name}: {description}" for name, description in collections_info.items()])
    
        # prompt = f"""
        # You are an assistant that helps identify the appropriate MongoDB collection for a given question based on collection descriptions.

        # **Collections and Descriptions:**
        # {collections_description}

        # **Question:** "{data['input']['prompt']}"

        # Please identify the most relevant collection for this question and return a json object key as collection name and value as description..
        # """
        # print(prompt,'......')
        # new_chat=[]
        # new_chat.append({"role": "user", "content": prompt})
        # client = OpenAI()
        # response_ai = client.chat.completions.create(
        #         #response_ai = client.completions.create(
        #             model="gpt-4o-mini",
        #             #model="davinci-002",
        #             #model="gpt-3.5-turbo-instruct",
        #             response_format={ "type": "json_object" },
        #             messages=new_chat,
        #             temperature=0,
        #             top_p=0.1
        #             )

        # response = response_ai.choices[0].message.content
        # response=json.loads(response)
        # print ('Res==----------->,',response)
        # for key, value in response.items():
        # # Create a new dictionary with 'collection' and 'description' keys
        #     new_dict = {
        #     'collection': key,
        #     'description': value
        #     }
        # projection = {
        #     'Category': 1,  # Include this field in the result
        #     'Description': 1,  # Include this field in the result
        #     'type': 1,
        #     'Collection':1  # Include this field in the result
        # }
        # document = db.get_collection('Data Store').find_one({'Category': new_dict["collection"],'Description': new_dict["description"],'subscriberId':ObjectId(data['input']['subscriberId'])},projection=projection)
        # return json.dumps(document, cls=MongoJSONEncoder)
        print(categoryDetail_list,'......')
        return json_util.dumps(categoryDetail_list)
    except Exception as e:
        # sem.release()
        print('this is an ERROR message', e)
        return json.dumps({'type':'str',
                'response': """We're sorry, but the requested data could not be found.
                Please try again with different criteria or provide additional details to help us locate the information you're looking for. If the issue persists, feel free to reach out to our support team for further assistance.
                Thank you for your understanding.""",
                'response_type': 'output'})

@app.route('/chatbot/dataSource',methods=['GET', 'POST'])
@limitcheck_middleware
@addentry_middleware
def dataSource():
    # sem.acquire()


    from llama_index import SummaryIndex
    from MongoReader import SimpleMongoReader

    #from llama_index.readers import SimpleMongoReader

    from llama_index.storage.chat_store import SimpleChatStore
    from llama_index.memory import ChatMemoryBuffer
    import json

    print('using this smart chat',request.headers['Origin'])

    try:
        data=request.json
        print('execuu22222......')
        print(f"data-----------{data}")
        db = g.db
        collection = data['input']['collN']
        categoryDetail=db.get_collection('Data Sources').find({'Category':collection,'subscriberId':ObjectId(data['input']['subscriberId']),"isDeleted":False})
        categoryDetail_list = list(categoryDetail)
        categoryDetail=db.get_collection('Database Details').find({'Database Name':categoryDetail_list[0]['Database Name'],"isDeleted":False})
        databaseDetail=list(categoryDetail)
        db_type = databaseDetail[0]['Database Type']
        tablemetadata = list(db.get_collection('tablemetadatas').find({'tableName':collection}))
        if (len(tablemetadata)>0 and 'primaryKeys' in tablemetadata[0]):
            response, summary, count, info = query_from_datasource(tablemetadata[0],data['input']['prompt'],collection)
            print(info)
            if info and 'options' in info:
                outputData={'type':'choice','response':response, 'response_type': 'select', 'count':count, 'options': info['options'], 'summary':summary}
            elif info and 'button' in info:
                outputData={'type':'button','response':response, 'response_type': 'click','button_name':info['button'], 'count':count, 'summary':summary, 'info': info}
            else:
                outputData={'type':'str','response':response, 'response_type': 'output', 'count':count, 'summary':summary}
            return json.dumps(outputData,default=str)
        if db_type == 'MongoDB':
            new_chat_store = [
                {'role': 'system', 'content': "I'm going to ask to generate a MongoDB aggregation pipeline. Use mongoQuery to parse this data."
	            }
            ]
            prompt=data['input']['prompt']
            coll_name = {entry['Field Name']: entry['Field Description'] for entry in categoryDetail_list}
            user_query=f"""Write a MongoDB Aggregation pipeline query.
            Use the following as mongoDB collection schema to write the query: {coll_name}
            Question:- {prompt}. """
            additional_info = f"""      
        Strict Rules and Regulations:
        Its very critical to not use additional context like user match or date for generic query.
        For direct date match use regular expression.
        Its very critical to not add unnecassary match conditions if not prompted.
        Its very critical Match queries must use $regex if field is type string, include case insensitive flag. 
        Projection must exclude _id.
        If using $regex dont enclose it in /expression/ and dont use ^ and $ in regex field.
        Only respond with mongo aggregation query in a valid JSON list/array format without code block syntax around it and each pipeline should be closed within curly braces and quotes around each stage type. 
        Always format response in this format. {{"pipeline":[]}}.
        Its very critical, If the question is not related to schema respond empty."""
            rules = f"Your task to generate a mongodb query only if query- {prompt}. is related to schema not any general statements.Exclude _id field"
            new_chat_store.append({"role": "user", "content": user_query})
            new_chat_store.append({"role": "user", "content": additional_info})
            new_chat_store.append({"role": "user", "content": rules})
            print('Chat_history', new_chat_store)
            client = OpenAI()
            response_ai = client.chat.completions.create(
                #response_ai = client.completions.create(
                    model="gpt-4o",
                    #model="davinci-002",
                    #model="gpt-3.5-turbo-instruct",
                    response_format={ "type": "json_object" },
                    messages=new_chat_store,
                    temperature=0,
                    top_p=0.1
                    )

            response = response_ai.choices[0].message.content
            print ('Res==----------->,',response)
            token_info = response_ai.usage
            final_query =  response
        #repair the json format .
            query_text = repair_json(final_query)
            print(f"1.----------------{query_text}-------------------")
            python_object = json.loads(final_query)
            if python_object and 'pipeline' in python_object and len(python_object['pipeline']) == 0:
                return json.dumps({'type':'str',
                'response': """We're sorry, but the requested data could not be found.
                Please try again with different criteria or provide additional details to help us locate the information you're looking for. If the issue persists, feel free to reach out to our support team for further assistance.
                Thank you for your understanding.""",
                'response_type': 'output'})
                # Ensure _id is excluded in the projection stage
            for stage in python_object["pipeline"]:
                if "$project" in stage:
                    if "_id" not in stage["$project"]:
                        stage["$project"]["_id"] = 0

                # Connect to MongoDB and execute the query
            passw = base64.b64decode(databaseDetail[0]['Password']).decode('utf-8')
            uri = f"mongodb://{databaseDetail[0]['User Name']}:{passw}@{databaseDetail[0]['Host']}:{databaseDetail[0]['Port']}/{databaseDetail[0]['Database Name']}"
            client = MongoClient(uri)
            db1 = client[databaseDetail[0]['Database Name']]
            result_cursor = db1.get_collection(categoryDetail_list[0]['Collection']).aggregate(python_object['pipeline'])
        elif db_type in ['MySQL', 'Oracle']:
            new_chat_store = [{'role': 'system', 'content': "I'm going to ask to generate a database query. Use the schema to create the appropriate query."}]
            prompt=data['input']['prompt']
            coll_name = {entry['Field Name']: entry['Field Description'] for entry in categoryDetail_list}
            user_query = f"""Write an SQL query (for {db_type}) using the following schema: {coll_name} Question: {prompt}. """
            additional_info = f"""For SQL queries, ensure to use proper syntax for SELECT statements. The query should include only necessary fields and use WHERE conditions relevant to the schema provided."""
            rules = f"Your task is to generate a SQL query (for {db_type}) based on the schema and the question provided. Ensure the query follows correct SQL syntax and uses WHERE conditions appropriately.My database Name is {databaseDetail[0]['Database Name']} and my table name is {categoryDetail_list[0]['Collection']}"
            new_chat_store.append({"role": "user", "content": user_query})
            new_chat_store.append({"role": "user", "content": additional_info})
            new_chat_store.append({"role": "user", "content": rules})
            print('Chat_history', new_chat_store)
            client = OpenAI()
            response_ai = client.chat.completions.create(
            model="gpt-4",  # Ensure to use the correct model
            messages=new_chat_store,
            temperature=0,
            top_p=0.1
            )
        
            response = response_ai.choices[0].message.content
            print(f"AI Response: {response}")
            token_info = response_ai.usage

        # Repair and format the query text
            final_query = repair_json(response)
            print(f"Formatted Query: {final_query}")

                #conveting it into json format .
        if db_type == 'MySQL':
            try:
                # MySQL query handling
                query = final_query.strip()
                print(f"MySQL Query: {query}",databaseDetail[0])
                passw = base64.b64decode(databaseDetail[0]['Password']).decode('utf-8')
                conn = mysql.connector.connect(
                    host=databaseDetail[0]['Host'],
                    user=databaseDetail[0]['User Name'],
                    password=passw,
                    database=databaseDetail[0]['Database Name']
                )
                cursor = conn.cursor(dictionary=True)
                cursor.execute(query)
                result = cursor.fetchall()
                print('.........',result)
                conn.close()

            except Exception as e:
                print(f"MySQL Error: {e}")
                result = []

        final_result = list(result_cursor)
        print(f"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<{final_result}")
        result=final_result
        response_ai=response
        if (result and len(result)>0):
            response = result
        else:
            response = []
        if (len(response) == 0):
            outputData={'type':'str','response':"No data found for the query. Please try again with different criteria or provide additional details to help us locate the information you're looking for.", 'response_type': 'output'}
        else:
            outputData={'type':'arr','response':response , 'response_type': 'output'}
        return json.dumps(outputData, default=str)
    except Exception as e:
        # sem.release()
        print('this is an ERROR message', e)
        return json.dumps({'type':'str',
                'response': """We're sorry, but the requested data could not be found.
                Please try again with different criteria or provide additional details to help us locate the information you're looking for. If the issue persists, feel free to reach out to our support team for further assistance.
                Thank you for your understanding.""",
                'response_type': 'output','count':0})


@app.route('/chatbot/updateStatus',methods=['POST'])
def update_order_status():
    """Update the status of a document in TVS_Order_Details collection."""
    uri = config['stageDbLink']
    db_name = config['stageDb']
    myclient = pymongo.MongoClient(uri)
    db = myclient[db_name]
    collection = db.get_collection("TVS_Order_Details")
    
    try:
        # Get JSON data from request
        data = request.json
        print(data)
        order_id = data.get("_id")
        new_status = data.get("status",'Approved')
        print('id',order_id)
        # Validate input
        if not order_id or not new_status:
            return jsonify({"error": "Missing _id or status"}), 400

        # Convert _id to ObjectId
        try:
            order_id = ObjectId(order_id)
        except Exception:
            return jsonify({"error": "Invalid _id format"}), 400

        # Update document
        result = collection.update_one({"_id": order_id}, {"$set": {"Order_Status": new_status}})

        if result.matched_count == 0:
            return jsonify({"error": "No document found with given _id"}), 404

        return jsonify({"message": f"Order {order_id} updated to status: {new_status}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=3000,
                        help="Port to run the UI on. Defaults to 5111.")
    parser.add_argument("--host", type=str, default="0.0.0.0",
                        help="Host to run the UI on. Defaults to 127.0.0.1. "
                             "Set to 0.0.0.0 to make the UI externally "
                             "accessible from other devices.")
    args = parser.parse_args()
    # with app.app_context():
    #     load_model()

    app.run(debug=False, host=args.host, port=args.port, processes=1)




