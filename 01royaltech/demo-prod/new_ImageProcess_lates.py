# import cv2
# import random

import os
import gc
import cv2
os.environ["PYTHONHTTPSVERIFY"] = "0"
# Disable GPU Usage
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import time

import gc

gc.enable()
gc.set_debug(gc.DEBUG_SAVEALL)
gc.set_threshold(50, 5, 5)


from flask_cors import CORS
from flask import Flask, request
import subprocess
import requests
import json
import re
# import shutil
import os
#import torch
# import yaml
import json
# import ssl
from Document_Preprocess import Image_Preprocess
# from paddleocr import PaddleOCR

config = {}
with open("config.json", "r") as f:
    config = json.load(f)
print("config file loaded on start")
print(config["filepath"])
app = Flask(__name__)

cors = CORS(app)

pub_path = config["uploadFilePath"]
pub_url = config["pub_url"]
#model_weights = config['model_weights_path']
# import pymongo


import cv2
import multiprocessing as mp
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from typing import List, Dict, Any, Optional

\

@app.route(config["apiURL"] + "DocumentPreprocess_ocri", methods=["POST"])
def DocumentPreprocess_ocri():
    ############## Main ################

    ### Send ackn
    data = request.json
    if not data.get('input', {}).get('return'):
        got_input = {
        "projectId": data["projectId"],
        "botId": data["botId"],
        "eventId": data["input"]["eventId"],
        "iterationId": data["iterationId"],
        }
        head = {"authorization": data["token"], "content-type": "application/json"}
        response = requests.request(
        "POST", config["acknowledgeURL"], verify=False, json=got_input, headers=head
    )
        print("acknowledge api status --- ", response.status_code)

    ### Start
    print("Input---Data-------->>>>", data["input"])

    timestamp = str(time.time())
    '''with open("file_event_" + timestamp + ".json", "w") as f:
        json.dump(data, f)
    start_time = time.time()
    f_ = re.sub(
        "b'|\\\\n'",
        "",
        str(
            subprocess.check_output(
                "/home/user/anaconda3/envs/custom_genai/bin/python Document_Preprocess.py -i "
                + "file_event_"
                + timestamp
                + ".json"
                + " -t "
                + timestamp,
                shell=True,
            )
        ),
    )
    end_time =time.time()
    print('Exec time',end_time-start_time)
    # print(f_)
    '''
    
    endArray=[]
    Processed_Image_path = "output.png"

    print("input is------" ,data['input']['InputArray'])
    if type(data['input']['InputArray']) is str:
        print(">>>>> input is string >>>>>")
        # Testing purposes
       #data['input']['InputArray'] = [{'imageFilePath': re.sub(r"\d{1}\.png$", str(random.randint(0,4))+".png", data['input']['InputArray'])  }]
        #data['input']['InputArray'] = [{'imageFilePath': re.sub(r"\d{1}\.jpg$", str(random.randint(0,4))+".jpg", data['input']['InputArray'])  }]

    page_no = 0
    for index in range(len(data['input']['InputArray'])):
        for key in data['input']['InputArray'][index]:
            if key == 'imageFilePath':
               
                print("       [INFO] starting process for -           ", data['input']['InputArray'][index]['imageFilePath'], "          " )

                INPUT_IMAGE = cv2.imread(data['input']['InputArray'][index]['imageFilePath'])
                if page_no == 0:
                    output_image_path = data['input']['InputArray'][index]['imageFilePath']
                page_no = page_no + 1

                Image_Preprocess(data['input']['InputArray'][index]['imageFilePath'],data['input']['InputArray'][index]['imageFilePath'],str(data['input']['text_allignment_check']),str(data['input']['preprocess_image']),str(data['input']['deskew_correction']),str(data['input']['stretching_document']),str(data['input']['ml_denoise_document']),str(data['input']['white_text_on_gray_check']))

                ImageArary={}
                ImageArary={"imageFilePath":data['input']['InputArray'][index]['imageFilePath']}
                endArray.append(ImageArary)

                Processed_Image_path = output_image_path
                OUTPUT_IMAGE = cv2.imread(Processed_Image_path)
                height, width, channels = OUTPUT_IMAGE.shape
                INPUT_IMAGE = cv2.resize(INPUT_IMAGE, (width, height))
    outputData = {
        "outputArray": endArray,
       
        "statusCode": "200",
    }
    del INPUT_IMAGE
    del OUTPUT_IMAGE
    del ImageArary
    gc.collect()
    print("output---Data-------->>>>", outputData)
    if data.get('input', {}).get('return'):
        return json.dumps(outputData)
    taskData = {
        "projectId": data["projectId"],
        "botId": data["botId"],
        "eventId": data["input"]["eventId"],
        "status": "Complete",
        "outputParameters": outputData,
        "iterationId": data["iterationId"],
    }
    head = {"authorization": data["token"], "content-type": "application/json"}
    print("requestURL-----------------", config["requestURL"])
    response = requests.request(
        "POST", config["requestURL"], verify=False, json=taskData, headers=head
    )

    # os.system("rm " + os.getcwd() + "/file_event_" + timestamp + ".json")
    # os.system("rm " + os.getcwd() + "/file_" + timestamp + ".json")

    gc.collect(generation=0)
    gc.collect(generation=1)
    gc.collect(generation=2)

    return json.dumps(request.json)

#Image Quality Check
#########################




if __name__ == "__main__":
    app.run("127.0.0.1", 5022)