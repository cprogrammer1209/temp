
import os
import gc
import time
import json
# import pymongo
import requests
import tracemalloc
import uuid
from paddleocr import PaddleOCR
# import cairo
import cv2
import psutil
process = psutil.Process(os.getpid())

from flask_cors import CORS
from flask import Flask, request, jsonify

config={}
with open('config.json', 'r') as f:
    config = json.load(f)

# db connecton set as global
# myclient = pymongo.MongoClient(config['dbConnection'])
# db = myclient[config['db']]

pub_path = config['uploadFilePath']
pub_url = config['pub_url']
tessdata_path = config['tessdata_path']
env_path = config['env_path']

os.environ['OMP_THREAD_LIMIT'] = '1'
os.environ['TESSDATA_PREFIX'] = tessdata_path

app = Flask(__name__)
cors = CORS(app)

if config['gpu'] == "yes":
    cuda = True
else:
    cuda = False
    os.environ['CUDA_VISIBLE_DEVICES']='0'

import re
import random
import subprocess


#######################################################################################################################################################
# Bot API code
@app.route('/gibots-ocr/tesseract_ocr_wbw', methods=['POST'])
def tesseract_ocr():
    T_ = time.time()
    print('\n'+'-'*25+'memory `1 -->', (process.memory_info().rss)/1048576, '\n')
    data = request.json
    print(f"input_data------------{data}")
    # data['input']['ImagesPath_Array'][-1]['imageFilePath'] = re.sub(r"\d{1}\.jpg$", str(random.randint(0,4))+".jpg", data['input']['ImagesPath_Array'][-1]['imageFilePath'])

    print("[INFO] running process on -> ", data['input']
          ['ImagesPath_Array'][-1]['imageFilePath'])
    input = data['input']
    if not data.get('input', {}).get('return'):
        got_input = {'projectId': data['projectId'], 'botId': data['botId'],
                 'eventId': input['eventId'], 'iterationId': data['iterationId']}
        head = {'authorization': data['token'], 'content-type': "application/json"}

    # try:
    #     response = requests.request("POST", config['acknowledgeURL'],verify=False, json=got_input, headers=head)
    #     print("\nacknowledge api status --- ",response.status_code)
    # except:
    #     print("acknowledge url not found. Bot may not become yellow in frontend. but API got hit. cheers!!!\n\n")

    timestamp = str(time.time())

    with open("file_event_"+timestamp+".json", "w") as f:
        json.dump(data, f)

    # str(data['input']['ImagesPath_Array'][-1]['imageFilePath'])
    f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
        "/newdata/anaconda3/envs/aiqod-dev-tesserect/bin/python pytesseract_run_ocr.py -i " + "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True)))

    print(f_,config)

    outputData = json.load(open("file_"+timestamp+".json", "r"))

    os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
    os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")
    if data.get('input', {}).get('return'):
        if data.get('input',{}).get('json_respond'):
            if outputData.get('ocr_output',None):
                json_savepath = '/data/backend-script/aiqod-dev-jobs/javaJsonFolder'
                with open(json_savepath+'/ocr_output_'+data['input']['eventId']+'.json','w') as file:
                    file.write(json.dumps(outputData.get('ocr_output')))
                outputData['ocr_output'] = json_savepath+'/ocr_output_'+input['eventId']+'.json'+'/isLocal'

        return jsonify(outputData)
    # import cv2
    # import random
    # i1 = cv2.imread(data['input']['ImagesPath_Array'][-1]['imageFilePath'])
    # for idx, d in enumerate(outputData["ocr_output"][-1]["sortedWords"]):
    #     if idx == len(outputData["ocr_output"][-1]["sortedWords"])-1:
    #         continue
    #     cv2.rectangle(i1, (d["leftX"], d["topY"]), (d["rightX"], d["bottomY"]), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)

    # cv2.imwrite("coords_test.png", i1)

    input = data['input']
    taskData = {'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'],
                'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId']}
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request(
        "POST", config['requestURL'], verify=False, json=taskData, headers=head)
    gc.collect(generation=0)
    gc.collect(generation=1)
    gc.collect(generation=2)

    print("-"*100)
    print('\nmemory `6 -->', (process.memory_info().rss)/1048576, '\n')
    print("[INFO] \t Total Time ", T_-time.time())

    return jsonify(outputData)


###############################################################################################################################################################################################

@app.route('/gibots-ocr/translation_with_Emboss',methods=["POST"])
def transaltion_emboss():
    T_ = time.time()
    print('\n'+'-'*25+'memory `1 -->',(process.memory_info().rss)/1048576, '\n')
    data=request.json
    # data['input']['ImagesPath_Array'][-1]['imageFilePath'] = re.sub(r"\d{1}\.jpg$", str(random.randint(0,4))+".jpg", data['input']['ImagesPath_Array'][-1]['imageFilePath'])

    print("[INFO] running process on -> ", data['ocr_output'][0]['obj']['filePath'])
    input=data['input']
    got_input = {'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'],'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}

    # try:
    #     response = requests.request("POST", config['acknowledgeURL'],verify=False, json=got_input, headers=head)
    #     print("\nacknowledge api status --- ",response.status_code)
    # except:
    #     print("acknowledge url not found. Bot may not become yellow in frontend. but API got hit. cheers!!!\n\n")

    timestamp = str(time.time())

    with open("file_"+timestamp+".json", "w") as f:
        json.dump(data, f)

    # str(data['input']['ImagesPath_Array'][-1]['imageFilePath'])
    f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
        "/newdata/anaconda3/bin/python translate_emboss.py -i "+ "file_"+timestamp+".json" + " -t " + timestamp, shell=True)))

    print(f_)

    output_data = json.load(open("file_trans_"+timestamp+".json", "r"))

    os.system("rm "+os.getcwd()+"/file_trans_"+timestamp+".json")
    os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")

    # import cv2
    # import random
    # i1 = cv2.imread(data['input']['ImagesPath_Array'][-1]['imageFilePath'])
    # for idx, d in enumerate(outputData["ocr_output"][-1]["sortedWords"]):
    #     if idx == len(outputData["ocr_output"][-1]["sortedWords"])-1:
    #         continue
    #     cv2.rectangle(i1, (d["leftX"], d["topY"]), (d["rightX"], d["bottomY"]), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)

    # cv2.imwrite("coords_test.png", i1)


    input=data['input']
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': output_data, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    gc.collect(generation=0)
    gc.collect(generation=1)
    gc.collect(generation=2)

    print("-"*100)
    print('\nmemory `6 -->',(process.memory_info().rss)/1048576, '\n')
    print("[INFO] \t Total Time ", T_-time.time())

    return jsonify(output_data)

################################################################################### For Royal Tech  ################################################################################
from pytesseract_run_ocr_new import tesseract_ocr_wbw_parallel
#######################################################################################################################################################
# Bot API code
@app.route('/gibots-ocr/tesseract_ocr_wbw_new', methods=['POST'])
def tesseract_ocr_new():
    T_ = time.time()
    print('\n'+'-'*25+'memory `1 -->', (process.memory_info().rss)/1048576, '\n')
    data = request.json
    print(f"input_data------------{data}")
    # data['input']['ImagesPath_Array'][-1]['imageFilePath'] = re.sub(r"\d{1}\.jpg$", str(random.randint(0,4))+".jpg", data['input']['ImagesPath_Array'][-1]['imageFilePath'])

    print("[INFO] running process on -> ", data['input']
          ['ImagesPath_Array'][-1]['imageFilePath'])
    input = data['input']
    if not 'return' in input:
        got_input = {'projectId': data['projectId'], 'botId': data['botId'],
                 'eventId': input['eventId'], 'iterationId': data['iterationId']}
        head = {'authorization': data['token'], 'content-type': "application/json"}

    # try:
    #     response = requests.request("POST", config['acknowledgeURL'],verify=False, json=got_input, headers=head)
    #     print("\nacknowledge api status --- ",response.status_code)
    # except:
    #     print("acknowledge url not found. Bot may not become yellow in frontend. but API got hit. cheers!!!\n\n")

    timestamp = str(time.time())

    if len(data['input']['ImagesPath_Array'])>3:
        with open("file_event_"+timestamp+".json", "w") as f:
            json.dump(data, f)
        
        # str(data['input']['ImagesPath_Array'][-1]['imageFilePath'])
        
        """f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
            "/home/user/anaconda3/envs/demo-tessrect/bin/python pytesseract_run_ocr.py -i " + "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True)))

        print(f_)"""
        #env_path = "/home/user/anaconda3/envs/demo-tessrect/bin/python"
        #timestamp = "your_timestamp_here"  # Replace with actual timestamp

        # Construct the command
        command = f"{env_path} pytesseract_run_ocr_new.py -i file_event_{timestamp}.json -t {timestamp}"

        try:
            # Execute the command
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            # Decode and clean up the output
            f_ = re.sub(r"b'|\\n'|\\n", "", output.decode("utf-8"))
            print(f_)
        except subprocess.CalledProcessError as e:
            print(f"Error executing command: {e}")
            print(f"Command output: {e.output.decode('utf-8')}")

        outputData = json.load(open("file_"+timestamp+".json", "r"))

        os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
        os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")
    else:
        outputData = tesseract_ocr_wbw_parallel(data,timestamp,max_workers=2)
        os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
        gc.collect()
    # import cv2
    # import random
    # i1 = cv2.imread(data['input']['ImagesPath_Array'][-1]['imageFilePath'])
    # for idx, d in enumerate(outputData["ocr_output"][-1]["sortedWords"]):
    #     if idx == len(outputData["ocr_output"][-1]["sortedWords"])-1:
    #         continue
    #     cv2.rectangle(i1, (d["leftX"], d["topY"]), (d["rightX"], d["bottomY"]), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 2)

    # cv2.imwrite("coords_test.png", i1)

    #input = data['input']
    if data.get('input', {}).get('return'):
        if data.get('input',{}).get('json_respond'):
            if outputData.get('ocr_output',None):
                id = str(uuid.uuid4())
                json_savepath = '/data/backend-script/aiqod-dev-jobs/javaJsonFolder'
                with open(json_savepath+'/ocr_output_'+id+'.json','w') as file:
                    file.write(json.dumps(outputData.get('ocr_output')))
                outputData['ocr_output'] = json_savepath+'/ocr_output_'+id+'.json'+'/isLocal'

        return jsonify(outputData)

    taskData = {'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'],
                'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId']}
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request(
        "POST", config['requestURL'], verify=False, json=taskData, headers=head)
    gc.collect(generation=0)
    gc.collect(generation=1)
    gc.collect(generation=2)

    print("-"*100)
    print('\nmemory `6 -->', (process.memory_info().rss)/1048576, '\n')
    print("[INFO] \t Total Time ", T_-time.time())

    return jsonify(outputData)


#################################################################################################################################
###################################################################################################################################################################

if __name__=='__main__':
    app.run('0.0.0.0',config["ocr_port"])
