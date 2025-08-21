import math
import shutil, sys 
import traceback
                                                                                                                                                   

#from werkzeug import secure_filename
from datetime import datetime
import datetime
import threading
from Naked.toolshed.shell import execute_js, muterun_js
import os
from moviepy.editor import *
#from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
import cv2
import sys
import cx_Oracle
from PIL import Image
import subprocess
import json
from flask import *
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib as plt
import pymongo
import sklearn
import urllib.request
#from sklearn.externals import joblib
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import StandardScaler
import sklearn
import joblib
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, log_loss
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from tawazun_training_api import fieldTrainingTawazunApi
from PIL import Image
import pytesseract
import pandas as pd
import io
import argparse
import cv2
import os
import glob
import numpy as np
from pytesseract import Output
import json
import re
from datetime import datetime
#import dlib
from scipy.spatial import distance as dist
from imutils import face_utils
import argparse
import imutils
#import speech_recognition as sr
from fuzzywuzzy import fuzz
import gc 
import re
import nltk
#nltk.download('stopwords')
#nltk.download('wordnet')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from BotsIOWrite import writeBotOutput
import os, requests, json
#import ultralytics
scaler = StandardScaler()


from multiprocessing import Semaphore
semaphore = Semaphore(10)
semaphore_jsw = Semaphore(1)


import time
import random
from bs4 import BeautifulSoup
import requests
config={}
with open('config.json', 'r') as f:
    config = json.load(f)
print ("config file loaded on start")
print (config['ty'])
#command='read white black << (convert Cheque1_CR_1545122627558_7.png -format "%[fx:mean*w*h] %[fx:(1-mean)*w*h]" info:)'
#subprocess.call([command],shell=True)
#print(os.environ['white'])
#print(os.environ['black'])
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER']=config['uploadFilePath']
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
@app.route('/gibots-pyapi/aj',methods = ['POST'])
def hello_world():
    greetOut = ['hey there!', 'hi!', 'hi there!', 'hey!']
    bot = random.choice(greetOut)
    print("hiiiiiiii")
    resp={"similarity":90,"orignal_image":"http://scan-dev.gibots.com","cheque_image":"http://scan-dev.gibots.com"}
    return render_template('signature.html', resp=resp)
    
    
    



from splitter import split_files
@app.route('/gibots-pyapi/split_documents',methods = ['POST'])
def split_documents():
    data = request.json
    t1 = time.perf_counter()
    import pprint
    pprint.pprint(data)
    timestamp = str(time.time())
    with open("file_event_"+timestamp+".json", "w") as f:
        json.dump(data, f)

    f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
    "/home/ubuntu/anaconda3/bin/python splitter_new.py -i "+ "file_event_"+timestamp+".json" + " -t "+ timestamp, shell=True)))

    #print(f_)

    final_output = json.load(open("file_"+timestamp+".json", "r"))
    receivedInput=data['input']
    #final_output = split_files(receivedInput)

    outputData = final_output
    outputData['statusCode'] = '200'
    print("\n[INFO] output data : \n")
    pprint.pprint(outputData)
    t2 = time.perf_counter()
    print('time taken      ---------------',t2-t1)
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "https://rpa.gibots.com/gibots-orch/orchestrator/botsiowrite", json=taskData, headers=head, verify=False)
    os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")
    os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
    return json.dumps({"result":final_output})

from omega_prediction_api import omega_prediction
@app.route('/gibots-pyapi/omega',methods = ['POST'])
def omega():
    data = request.json
    receivedInput=data['input']
    print("\n[INFO] input data : \n")
    import pprint
    pprint.pprint(data)

    result = omega_prediction(data['input'])
    outputData = json.loads(result)
    outputData['statusCode'] = '200'
    print("\n[INFO] output data : \n")
    print(outputData)

    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "https://rpa.gibots.com/gibots-orch/orchestrator/botsiowrite", json=taskData, headers=head, verify=False)

    return json.dumps({"result":result})
    #return result

    #return json.dumps(result)

    # final_output = omega_prediction(data)
    # print("\n[INFO] output data : \n")
    # pprint.pprint(final_output)

    # outputData={'output':final_output, 'statusCode': '200'}

    # taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    # head = {'authorization': data['token'], 'content-type': "application/json"}
    # response = requests.request("POST", "https://rpa.gibots.com/gibots-orch/orchestrator/botsiowrite", json=taskData, headers=head, verify=False)

    # return json.dumps({"result":final_output})


def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])
    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    # return the eye aspect ratio
    return ear


def imouth_aspect_ratio(mouth):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(mouth[1], mouth[7])
    B = dist.euclidean(mouth[2], mouth[6])
    C = dist.euclidean(mouth[3], mouth[5])

    
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    D = dist.euclidean(mouth[0], mouth[4])
    # compute the eye aspect ratio
    mar = (A + B + C) / (3.0 * C)
    # return the eye aspect ratio
    return mar

def omouth_aspect_ratio(mouth):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(mouth[1], mouth[19])
    B = dist.euclidean(mouth[2], mouth[18])
    C = dist.euclidean(mouth[3], mouth[17])
    D = dist.euclidean(mouth[4], mouth[16])
    E = dist.euclidean(mouth[5], mouth[15])
    F = dist.euclidean(mouth[6], mouth[14])
    G = dist.euclidean(mouth[7], mouth[13])
    H = dist.euclidean(mouth[8], mouth[12])
    I = dist.euclidean(mouth[9], mouth[11])



    
    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    J = dist.euclidean(mouth[0], mouth[19])
    # compute the eye aspect ratio
    mar = (A + B + C + D + E + F + G + H + I) / (9.0 * J)
    # return the eye aspect ratio
    return mar



def compare_signature(sig1,sig2):
    return sig1+sig2;

def write_file(data,filename):
    print (filename)
    with open(filename, 'wb') as f:
        f.write(data)
def allowed_file(filename):
    print ('inside allowed extension function')
    print (filename)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/gibots-pyapi/countExcelRows', methods=['POST'])
def countExcelRows():
    print('Calling /gibots-pyapi/countExcelRows API')
    try:
        data = request.json
        if not data or 'filePath' not in data:
            return jsonify({"status": "error", "message": "Missing 'filePath' in request body"}), 400

        excel_file_path = data['filePath']
        print(f"Received request to count rows for: {excel_file_path}")

        if not os.path.exists(excel_file_path):
            return jsonify({"status": "error", "message": f"File not found at path: {excel_file_path}"}), 404

        try:
            # Load the Excel file to inspect its sheets without loading all data yet
            # We use a custom engine to get sheet names
            xls = pd.ExcelFile(excel_file_path, engine='openpyxl')
            sheet_names = xls.sheet_names
            print(f"Sheets found in Excel: {sheet_names}")

            target_sheet_name = None
            for sheet_name in sheet_names:
                if sheet_name != 'DropdownValues':
                    target_sheet_name = sheet_name
                    break # Found the first valid sheet, let's use it

            if not target_sheet_name:
                return jsonify({"status": "error", "message": "No valid sheet found in Excel file (all sheets were 'DropdownValues' or file has no other sheets)."}), 400

            print(f"Counting rows for sheet: {target_sheet_name}")
            # Read only the target sheet into a pandas DataFrame
            df = pd.read_excel(excel_file_path, sheet_name=target_sheet_name, engine='openpyxl')
            row_count = len(df)

            return jsonify({"status": "success", "filePath": excel_file_path, "rowCount": row_count, "sheetName": target_sheet_name}), 200

        except pd.errors.EmptyDataError:
            return jsonify({"status": "success", "filePath": excel_file_path, "rowCount": 0, "sheetName": target_sheet_name or "N/A", "message": "Excel file is empty or the selected sheet is empty"}), 200
        except Exception as e:
            # Catch general pandas or file reading errors
            return jsonify({"status": "error", "message": f"Failed to read Excel file or count rows: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": f"Invalid request payload: {str(e)}"}), 400

@app.route('/gibots-pyapi/uploader', methods = ['GET', 'POST'])
def upload_file():
   print ('account number')
   print (time.time())
   if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
                resp={"error_message":"File not found in the request"};
                return render_template('signature_fail.html', resp=resp)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
             resp={"error_message":"No file selected"};
             return render_template('signature_fail.html', resp=resp)
        if file and allowed_file(file.filename):
            filename = os.path.splitext(secure_filename(file.filename))[0]+'_'+str(int(round(time.time() * 1000)))+'.'+os.path.splitext(file.filename)[1]
            millis = int(round(time.time() * 1000))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            acc_number=request.args.get('accno')
            #print request.args.get('accno')
            orignalFilename=filename.split('.')[0];
            #print '-----Orignal File Name=='+orignalFilename
            orignalFullPath=config['uploadFilePath']+filename
            extension=os.path.splitext(file.filename)[1]
            croppath=config['uploadFilePath']+orignalFilename+'_crop'+extension
            orignalsig=config['uploadFilePath']+orignalFilename+'_orignal'+extension
            masterfile=config['uploadFilePath']+orignalFilename+'_file'
            im = Image.open(orignalFullPath)
            width, height = im.size
            lx=config['lx']*width
            ty=config['ty']*height
            Wbox=config['Wbox']*width
            Hbox=config['Hbox']*height
            command='sh ' + config['scriptPath']+' '+orignalFullPath+' '+croppath+' '+str(width)+' '+str(height)+' '+str(lx)+' '+str(ty)+' '+str(Wbox)+' '+str(Hbox);
            subprocess.call([command],shell=True)
            con = cx_Oracle.connect(config['oracleConnectionString'])
            cur = con.cursor()
            named_params={'acc_number':acc_number}
            cur.execute('select * from imagelist where acc_number= :acc_number',named_params)
            row_count=cur.fetchall()
            #print len(row_count)
            if len(row_count) > 0:
                for result in row_count:
                    #print "inside for writing result Ajjjjj"
                    #print result
                    write_file(result[0].read(),orignalsig)
                cur.close()
                con.close()
                print ("Image From DataBase"+orignalsig)
                print ("Image On the Cheque"+croppath)
                masterFileCommand='sh '+config['scriptPathCrop']+' '+orignalsig+' '+orignalsig;
                subprocess.call([masterFileCommand],shell=True)
                f=open(orignalsig+'_hough_lines.mvg',"r")
                contents=f.readlines();
                print ("Contents From SVG FILE")
                print (contents)
                linecount=0
                orignalwidth=0
                orignalheight=0
                horizontalLine=[]
                verticalLine=[]
                lines=[]
                splitWord=[]
                obj={}
                #Below code is to parse the master file
                for contentline in contents:
                    #print contentline
                    #Below condition is to skip the first line from master file
                    if linecount==0:
                        #print "inside"
                        linecount=linecount+1
                        continue
                    #this is to get height and width from the orignal image
                    if linecount==1:
                        splitWord=contentline.split(' ')
                        orignalwidth=float(splitWord[3])
                        orignalheight=float(splitWord[4])
                        linecount=linecount+1
                        print ('orignal width height from SVG file')
                        print (orignalwidth)
                        print (orignalheight)
                        #This logic is to add default top horizonalt line
                        obj["x1"]=0
                        obj["y1"]=0
                        obj["x2"]=orignalwidth
                        obj["y2"]=0
                        horizontalLine.append(obj)
                        #This logic is to add default left vertical line
                        obj={}
                        obj["x1"]=0
                        obj["y1"]=0
                        obj["x2"]=0
                        obj["y2"]=orignalheight
                        verticalLine.append(obj)
                        print ("object appended")
                        continue
                    #below logic is to parse the 'line 0,62.2169 603,72.7423  # 166' string to get x1,y1 x2,y2
                    print (linecount)
                    splitWord=contentline.split(' ',2)
                    firstsplit=splitWord[1].split(',')
                    obj={}
                    print (obj)
                    obj["x1"]=float(firstsplit[0])
                    obj["y1"]=float(firstsplit[1])
                    secondsplit=splitWord[2].split(',')
                    obj["x2"]=float(secondsplit[0])
                    thirdsplit=secondsplit[1].split('#')
                    obj["y2"]=float(thirdsplit[0].lstrip())
                    lines.append(obj)
                    if obj["x1"]==0.0 and obj["x2"]==orignalwidth:
                        #This logic is to remove unwanted diagonal lines present in the image
                        hslope=(abs(obj["y1"]-obj["y2"])/orignalwidth)*100
                        print ("hslope")
                        print (hslope)
                        if hslope <= 5:
                            horizontalLine.append(obj)
                    if obj["y1"]==0.0 and obj["y2"]==orignalheight:
                        #this logic is to remove unwanted diagonal lines present in the image
                        vslope=(abs(obj["x1"]-obj["x2"])/orignalheight)
                        print ("vslope")
                        print (vslope)
                        if vslope <= 5:
                            verticalLine.append(obj)
                    linecount=linecount+1
                #This logic is to add default bottom horizontal line
                obj={}
                obj["x1"]=0
                obj["y1"]=orignalheight
                obj["x2"]=orignalwidth
                obj["y2"]=orignalheight
                horizontalLine.append(obj)
                obj={}
                #This logic is to add default right vertical line
                obj["x1"]=orignalwidth
                obj["y1"]=0
                obj["x2"]=orignalwidth
                obj["y2"]=orignalheight
                verticalLine.append(obj)
                box=[]
                print ("Horizontal Line")
                print (horizontalLine)
                print ("Vertical Line")
                print (verticalLine)
                if len(horizontalLine)<=3 and len(verticalLine)<=3:
                        cropboxes=[]
                        grayscalecommand='sh '+config['scriptPathOrignal']+' '+orignalsig+' '+orignalsig
                        #print "-----Grayscalecommaaan-------"+grayscalecommand
                        subprocess.call([grayscalecommand],shell=True)
                        sys.path.append(os.path.abspath(config['signatureLibPath']))
                        from sigcompare import compare
                        print ("Single signature Found")
                        sim=compare(orignalsig,croppath)
                        os.chdir(config['homeDir'])
                        content = request.get_json()
                        simper = sim * 100
                        resp={"account_number":acc_number,"similarity":round(simper,2),"orignal_image":config["url"]+orignalFilename+'_orignal'+extension ,"cheque_image":config["url"]+orignalFilename+'_crop'+extension,"index":"per0"}
                        cropboxes.append(resp)
                else:
                    for i in range(len(horizontalLine)-1):
                        for j in range(len(verticalLine)-1):
                            obj={}
                            obj["left"]=max(verticalLine[j]["x1"],verticalLine[j]["x2"])
                            obj["right"]=min(verticalLine[j+1]["x1"],verticalLine[j+1]["x2"])
                            obj["top"]=max(horizontalLine[i]["y1"],horizontalLine[i]["y2"])
                            obj["bottom"]=min(horizontalLine[i+1]["y1"],horizontalLine[i+1]["y2"])
                            obj["width"]=abs(obj["right"]-obj["left"])
                            obj["height"]=abs(obj["top"]-obj["bottom"])
                            obj["area"]=obj["width"]*obj["height"]
                            box.append(obj)
                    #this logic is used to find box with the maximum area to eliminate unwanted boxes
                    print ("Final BOX")
                    print (box)
                    maxareaobject = max(box, key=lambda ev: ev['area'])
                    print ("Maximum Area of Box in the Orignal Image")
                    print (maxareaobject)
                    maxarea=maxareaobject["area"]
                    print (maxarea)
                    cropboxes=[]
                    matchindex=0
                    for i in range(len(box)):
                        criteria=(box[i]["area"]/maxarea)*100
                        #print box[i]
                        #print "criteria"+str(criteria)
                        box[i]["criteria"]=criteria
                        if criteria>=50:
                            #This to crop the box from orignal image
                            orignal_crop_sig=config['uploadFilePath']+orignalFilename+'_'+str(i)+'.png'
                            print ('Orignal Crop BOX PATH')
                            print (orignal_crop_sig)
                            cropBoxCommand='convert '+orignalsig+' -crop '+str(box[i]["width"])+'x'+str(box[i]["height"])+'+'+str(box[i]["left"])+'+'+str(box[i]['top'])+' +repage '+orignal_crop_sig
                            #print '________cropBoxCommand----'+str(i)
                            #print cropBoxCommand
                            subprocess.call([cropBoxCommand],shell=True)
                            grayscalecommand='sh '+config['scriptPathOrignal']+' '+orignal_crop_sig+' '+orignal_crop_sig
                            #print "-----Grayscalecommaaan-------"+grayscalecommand
                            subprocess.call([grayscalecommand],shell=True)
                            sys.path.append(os.path.abspath(config['signatureLibPath']))
                            from sigcompare import compare
                            sim=compare(orignal_crop_sig,croppath)
                            os.chdir(config['homeDir'])
                            content = request.get_json()
                            simper = sim * 100
                            # print "Matching % for box"+str(i)+'------'+str(simper)
                            box[i]["similarity"]=round(simper,2)
                            box[i]["orignal_image"]=config["url"]+orignalFilename+'_'+str(i)+'.png'
                            box[i]["cheque_image"]=config["url"]+orignalFilename+'_crop'+extension
                            box[i]["acc_number"]=acc_number
                            box[i]["index"]="per"+str(matchindex)
                            matchindex=matchindex+1
                            cropboxes.append(box[i])
                    print ('-----------------CROP BOXES WITH URL')
                    print(cropboxes)
                    print (len(cropboxes))
                return render_template('signature_success.html', cropboxes=cropboxes)
            else:
                resp={"error_message":"Account number does not exist"};
                return render_template('signature_fail.html', resp=resp)
                #return jsonify({"info":'Account number does not exist'})
        else:
                resp={"error_message":"Invalid File Format"};
                return render_template('signature_fail.html', resp=resp)
                #return jsonify({"status":1,"info":"Invalid File Format"})
   else:
                 resp={"error_message":"Not a valid request format"};
                 return render_template('signature_fail.html', resp=resp)
                 #return ({"status":1,"info":"Not a valid"})

def fetch_data(data):
    print (data)
    input = data['input']
    projectId = data['projectId']
    botId = data['botId']

    sourceName = input['sourceName']
    idName = input['idName']
    className = input['className']
    eventId = input['eventId']
    page = requests.get(sourceName)
    soup = BeautifulSoup(page.content, 'html.parser')
    idA = soup.find(id=idName)
    classData = idA.find_all(class_=className)
    finalData = []
    token = data['token']
    if sourceName == 'https://economictimes.indiatimes.com/topic/MSME' or sourceName == 'https://economictimes.indiatimes.com/industry/cons-products/garments-/-textiles':
        for sample in classData:
            n1 = sample.find('h3')
            if (n1 == None):
                n1 = li.find('h2')
            n1 = n1.get_text()
            n2 = sample.find('p').get_text()
            newsData = n1 +' - '+ n2
            publishDate = sample.find('time').get_text()
            link = 'https://economictimes.indiatimes.com'+sample.find('a').get('href')
            news = {'data': newsData, 'link': link}
            singleData = { 'news': news, 'publishDate': publishDate, 'source': sourceName }
            finalData.append(singleData)
        #print finalData[0]['news']
        outputData = { 'crawledData': finalData, 'statusCode': '200' }
        taskData = { 'projectId': projectId, 'botId': botId, 'eventId': eventId, 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': token, 'content-type': "application/json"}
        response = requests.request("POST", "http://rpa-preprod.gibots.com/gibots-api/orchestrator/botsiowrite", json=taskData, headers=head)
        print (response.text)

    if sourceName == 'https://bidplus.gem.gov.in/servicelists' or sourceName == 'https://bidplus.gem.gov.in/bidlists':
        tenderData = []
        for item in classData:
            l = item.find_all("div")
            bidNo = l[0].find('p').get_text()
            lnk = 'https://bidplus.gem.gov.in'+l[0].find('a').get('href')
            iQ = l[2].find_all('span')
            item = iQ[0].get_text()
            quant = iQ[1].get_text()
            add = l[4].find_all('p')
            addr = add[1].get_text()
            addr = ' '.join(addr.split())
            sed = l[6].find_all('span')
            stDt = sed[0].get_text()
            enDt = sed[1].get_text()
            sampleData = {'Tender_Id': bidNo, 'ItemName': item, 'Quantityrequired': quant, 'DepartmentAddress': addr, 'StartDate': stDt, 'EndDate': enDt, 'source': sourceName, 'Summary': bidNo, 'link': lnk}
            tenderData.append(sampleData)
        #print tenderData[0]['DepartmentAddress']
        outputData = { 'crawledData': tenderData, 'statusCode': '200' }
        taskData = { 'projectId': projectId, 'botId': botId, 'eventId': eventId, 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': token, 'content-type': "application/json"}
        response = requests.request("POST", "http://rpa-preprod.gibots.com/gibots-api/orchestrator/botsiowrite", json=taskData, headers=head)
        print (response.text)

    if sourceName == 'https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata/byYzJWc1pXTjBBMTNoMVNXNW1iM0p0WVhScGIyNGdWR1ZqYUc1dmJHOW5lU0FvU1ZRcEExM2gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMQ==' or sourceName == 'https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata/byYzJWc1pXTjBBMTNoMVNXNW1iM0p0WVhScGIyNGdWR1ZqYUc1dmJHOW5lUzlVWld4bFkyOXRBMTNoMWNIVmliR2x6YUdWa1gyUmhkR1U9QTEzaDE=' or sourceName == 'https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata/byYzJWc1pXTjBBMTNoMVNWUWdMU0JCYkd3PUExM2gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMQ==' or sourceName == 'https://eprocure.gov.in/cppp/latestactivetendersnew/cpppdata/byYzJWc1pXTjBBMTNoMVNWUWdMU0JCYkd3PUExM2gxY0hWaWJHbHphR1ZrWDJSaGRHVT1BMTNoMQ==':
        eprocureData = []
        idData = idA.find_all('tr')
        for i in range(1, len(idData)):
            row = idData[i].find_all('td')
            epDt = row[1].get_text()
            enDt = row[3].get_text()
            tId = row[4].get_text()
            summ = row[4].get_text()
            org = row[5].get_text()
            fD = {"EndDate": enDt, "e_publishedDate": epDt, "Summary": summ, "Tender_Id": tId, "OrganisationName": org, "source": 'Eprocure.gov.in', 'link': sourceName}
            eprocureData.append(fD)
        #print eprocureData
        outputData = { 'crawledData': eprocureData, 'statusCode': '200' }
        taskData = { 'projectId': projectId, 'botId': botId, 'eventId': eventId, 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': token, 'content-type': "application/json"}
        response = requests.request("POST", "http://rpa-preprod.gibots.com/gibots-api/orchestrator/botsiowrite", json=taskData, headers=head)
        print (response.text)

@app.route('/gibots-pyapi/websiteCrawler', methods = ['POST'])
def websiteCrawlFunction():
    fetch_data(request.json)
    #print request.json
    return json.dumps(request.json)

@app.route('/gibots-pyapi/scanning', methods = ['POST'])
def scanning():
    from sklearn.externals import joblib
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import HashingVectorizer
    data=request.json
    filePath=data['filePath']
    print ('FIle PAth ==='+filePath)
    df=pd.read_csv(filePath)
    millis = int(round(time.time() * 1000))
    result=str(millis)+'_'+'prediction.csv'
    print (result)
    lines = []
    for i in df['Name']:
        lines.append(i)
    lines[0]
    import re
    import nltk
    nltk.download('stopwords')
    nltk.download('wordnet')
    from nltk.corpus import stopwords
    corpus = []
    for i in range(0, 10000):
        try:
            review = re.sub('[^a-zA-Z0-9]', ' ', lines[i])
            review = review.lower()
            review = review.split(" ")
            from nltk.stem import WordNetLemmatizer
            lem = WordNetLemmatizer()
            review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
            review = ' '.join(review)
            corpus.append(review)
        except IndexError:
            break
    vectorizer = joblib.load('./vectorizer.pkl')
    x = vectorizer.fit_transform(corpus)
    x = pd.DataFrame(x.toarray(), columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    df1 = pd.concat([df.drop(['Name','TextOnePositionLeftText','TextOnePositionOnTop','OnePositionOnTop','TextOnePositionLeft'],axis=1), x], axis=1)
    loaded_model = joblib.load('./invoicemodel.pkl')
    y_pred = loaded_model.predict(df1)
    mapping = {0: 'invReceiverName', 1: 'invTotal', 2: 'invNum', 3: 'undefined', 4: 'sgst', 5: 'cgst', 6: 'invTotalTax', 7: 'gstin', 8: 'igst', 9: 'invDt', 10: 'invoiceDueDate', 11: 'invSupplierName', 12: 'invSupplierGstin'}
    propseries = pd.Series(y_pred,name='Property')
    finalprop = propseries.map(mapping)
    newdata = pd.concat([df, finalprop], axis=1)
    millis = int(round(time.time() * 1000))
    path=config['uploadFilePath']+result
    print (path)
    newdata.to_csv(path)
    #finaldata=y_pred.tolist()
    return json.dumps({"result":path})

@app.route('/gibots-pyapi/scanning_allsec', methods = ['POST'])
def scanning_allsec():
    from sklearn.externals import joblib
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import HashingVectorizer
    data=request.json
    filePath=data['filePath']
    print ('FIle PAth ==='+filePath)
    df=pd.read_csv(filePath)
    millis = int(round(time.time() * 1000))
    result=str(millis)+'_'+'prediction.csv'
    print (result)
    lines = []
    for i in df['Name']:
        lines.append(i)
    lines[0]
    import re
    import nltk
    nltk.download('stopwords')
    nltk.download('wordnet')
    from nltk.corpus import stopwords
    corpus = []
    for i in range(0, 10000):
        try:
            review = re.sub('[^a-zA-Z0-9]', ' ', lines[i])
            review = review.lower()
            review = review.split(" ")
            from nltk.stem import WordNetLemmatizer
            lem = WordNetLemmatizer()
            review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
            review = ' '.join(review)
            corpus.append(review)
        except IndexError:
            break
    vectorizer = joblib.load('./vectorizerALLSEC.pkl')
    x = vectorizer.fit_transform(corpus)
    x = pd.DataFrame(x.toarray(), columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    df1 = pd.concat([df.drop(['Name','TextOnePositionLeftText','TextOnePositionOnTop','OnePositionOnTop','TextOnePositionLeft'],axis=1), x], axis=1)
    loaded_model = joblib.load('./invoicemodelALLSEC.pkl')
    y_pred = loaded_model.predict(df1)
    mapping = {0:'undefined', 1:'inSupplierName', 2:'invDt', 3:'invTotal'}
    propseries = pd.Series(y_pred,name='Property')
    finalprop = propseries.map(mapping)
    newdata = pd.concat([df, finalprop], axis=1)
    millis = int(round(time.time() * 1000))
    path=config['uploadFilePath']+result
    print (path)
    newdata.to_csv(path)
    #finaldata=y_pred.tolist()
    return json.dumps({"result":path})

@app.route('/gibots-pyapi/scanning_lonar', methods = ['POST'])
def scanning_lonar():
    from sklearn.externals import joblib
    import pandas as pd
    import numpy as np
    from sklearn.feature_extraction.text import HashingVectorizer
    data=request.json
    filePath=data['filePath']
    print ('FIle PAth ==='+filePath)
    df=pd.read_csv(filePath)
    millis = int(round(time.time() * 1000))
    result=str(millis)+'_'+'prediction.csv'
    print (result)
    lines = []
    for i in df['Name']:
        lines.append(i)
    lines[0]
    import re
    import nltk
    nltk.download('stopwords')
    nltk.download('wordnet')
    from nltk.corpus import stopwords
    corpus = []
    for i in range(0, 10000):
        try:
            review = re.sub('[^a-zA-Z0-9]', ' ', lines[i])
            review = review.lower()
            review = review.split(" ")
            from nltk.stem import WordNetLemmatizer
            lem = WordNetLemmatizer()
            review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
            review = ' '.join(review)
            corpus.append(review)
        except IndexError:
            break
    vectorizer = joblib.load('./vectorizerlonar.pkl')
    x = vectorizer.fit_transform(corpus)
    x = pd.DataFrame(x.toarray(), columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
    df1=df.drop(['Name','TextOnePositionLeftText','TextOnePositionOnTop','OnePositionOnTop','TextOnePositionLeft', 'RightMargin', 'LeftMargin','TopMargin','BottomMargin','RightMarginRelative','LeftMarginRelative','TopMarginRelative','BottomMarginRelative','PageHeight','PageWidth'],axis=1)
    loaded_model = joblib.load('./invoicemodellonar.pkl')
    y_pred = loaded_model.predict(df1)
    mapping = {0:'undefined', 1:'empId', 2:'interCode', 3:'bankAcNo', 4:'lastName', 5:'middleName' ,6:'firstName',7:'insured4lakh',8:'place', 9:'date', 10:'applicantFirstName', 11:'applicantLastName', 12:'initialAmt', 13:'monthlyFrequency', 14:'debitAccNo', 15:'witness1', 16:'witnessAddress11', 17:'witnessAddress12', 18:'witness2', 19:'witnessAddress21', 20:'monthlyAmt', 21:'witnessAddress22', 22:'witnessDate', 23:'applicationNo', 24:'branchNo', 25:'mobileNo', 26:'nomineeFirstName', 27:'nomineeLastName', 28:'nomineeAge'}
    propseries = pd.Series(y_pred,name='Property')
    finalprop = propseries.map(mapping)
    newdata = pd.concat([df, finalprop], axis=1)
    class_probabilities = loaded_model.predict_proba(df1)
    predProba=[]
    for i in class_probabilities:
        i.sort()
        predProba.append(i[::-1][0])
    predseries = pd.Series(predProba,name='confidence')
    print(predseries)
    newdata = pd.concat([newdata, predseries], axis=1)
    millis = int(round(time.time() * 1000))
    path=config['uploadFilePath']+result
    print (path)
    newdata.to_csv(path)
    #finaldata=y_pred.tolist()
    return json.dumps({"result":path})

@app.route('/gibots-pyapi/clustering', methods = ['POST'])
def clustering():
    from sklearn.externals import joblib
    import pandas as pd
    import numpy as np
    import cv2 as cv
    data=request.json
    receivedInput=data['input']
    filePath=receivedInput['filePath']
    print ('FIle PAth ==='+filePath)
    im=cv.imread(filePath)
    im = cv.resize(im, (800, 800))
    im = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
    im = im.flatten()
    df = pd.DataFrame(im)
    df = df.T
    millis = int(round(time.time() * 1000))
    result=str(millis)+'_'+'prediction.csv'
    print (result)
    loaded_model = joblib.load('./cluster.pkl')
    y_pred = loaded_model.predict(df)
    mapping = {'1':'toll', '2':'invoice'}
    propseries = pd.Series(y_pred,name='Property')
    finalprop = propseries.map(mapping)
    print(finalprop[0])
    outputData={'output':finalprop[0], 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "https://rpa.gibots.com/gibots-api/orchestrator/botsiowrite", json=taskData, headers=head, verify=False)
    return json.dumps(request.json) 


@app.route('/gibots-pyapi/medicalcomprehend', methods = ['POST'])
def comprehend():
    data=request.json
    receivedInput=data['input']
    import boto3
    import json

    client = boto3.client(service_name='comprehendmedical', region_name='us-east-1')
    result = client.detect_entities(Text= receivedInput['input'])
    entities = result['Entities']
    dict={}
    list=[]

    for entity in entities:
        keys = ['Category', 'Attributes', 'Text', 'Type']
        dict ={x:entity[x] for x in keys if x in entity}
        list.append(dict)

    list1=[]
    for a in list:
        keys = ['Category', 'Text', 'Type']
        dict ={x.lower():a[x].lower() for x in keys if x in a}
        if ('Attributes') in a:
            for x in a['Attributes']:
                dict[x['Type'].lower()]=x['Text']
        list1.append(dict)
    outputData={'output':list1, 'statusCode': '200'}
    #print outputData
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com:1443/gibots-api/orchestrator/botsiowrite", json=taskData, headers=head)
    #print response.text
    return json.dumps(request.json)

@app.route('/gibots-pyapi/readPDF', methods = ['POST'])
def readPDFFunction():
    import textract
    data = request.json
    print (data)
    input = data['input']
    projectId = data['projectId']
    botId = data['botId']
    token = data['token']
    eventId = input['eventId']
    inputFile = input['inputFile']
    text = textract.process(inputFile)
    outputData = { 'extractedData': text, 'statusCode': '200' }
    taskData = { 'projectId': projectId, 'botId': botId, 'eventId': eventId, 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': token, 'content-type': "application/json"}
    response = requests.request("POST", "https://rpa.gibots.com/gibots-api/orchestrator/botsiowrite", json=taskData, headers=head)
    print (response.text)
    return json.dumps(request.json)


@app.route('/gibots-pyapi/fieldTraining',methods=['GET', 'POST'])
def fieldTrainer():
    data=request.json
    print(data)
    try:
    	filePath=data['filePath']
    except Exception as e:
        print("Please upload valid File",e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    try:
        modelType=data['modelType']    
    except:
        print("Model type invalid")
        return json.dumps({'status':400 , 'info':'Model type invalid'})
    try:
        documentType=data['documentType']    
    except:
        print('Document type invalid')
        return json.dumps({'status':400 , 'info':'Document type invalid'})
    try:
        orgId=data['orgId']
    except:
        print('Invalid organization')
        return json.dumps({'status':400 , 'info':'Invalid organization'})
    try:
        df=pd.read_csv(filePath)
    except Exception as e:
        print('Please upload valid File',e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
 
    lines=[]
    linesTop=[]
    linesBot=[]
    linesLeft=[]
    linesRight=[]
    textPatterns=[]
    
    for i in df.columns:
        if "Name" in i:
            df[i]=df[i].fillna('null')
        else:
            df[i]=df[i].fillna(0)
    
    for i in df['Name']:
        lines.append(str(i))
    for i in df['TOP_Name']:
        linesTop.append(str(i))
    for i in df['BOTTOM_Name']:
        linesBot.append(str(i))
    for i in df['LEFT_Name']:
        linesLeft.append(str(i))
    for i in df['RIGHT_Name']:
        linesRight.append(str(i))
    for i in df['TextPatterns']:
        textPatterns.append(str(i)) 
        
    newLines=[]
    newLinesTop=[]
    newLinesBot=[]
    newLinesLeft=[]
    newLinesRight=[]
    newTextPatterns=[]
    corpus = set()
    for i in range(0,len(lines)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLines.append(review)
    
    for i in range(0,len(linesTop)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLinesTop.append(review)
    
    for i in range(0,len(linesBot)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLinesBot.append(review)
    
    for i in range(0,len(linesLeft)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLinesLeft.append(review)
    
    for i in range(0,len(linesRight)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLinesRight.append(review)
        
    for i in range(0,len(textPatterns)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newTextPatterns.append(review)
    
    myclient = pymongo.MongoClient(config['dbConnection'])
    db = myclient[config['db']]
    version=0

    try:
        for y in db.get_collection("modeldatas").find():
            if y['modelType']==modelType and y['documentType']==documentType and y['orgId']==orgId:
                version=y['versionNumber']
        newVersion=version+1
        oldFileName=modelType+orgId+documentType+str(version)+".pkl"


    except IndexError  as e:
        print('Valid training file not found',e)
        return json.dumps({'status':400 , 'info':'Valid training file not found'})
    from gensim.models import FastText
        
    
    vectorizer = FastText(list(corpus), size=20, window=5, min_count=5, workers=4,sg=1)
    x=[]
    for i in newLines:
        x.append(vectorizer[i])
    xTop=[]
    for i in newLinesTop:
        xTop.append(vectorizer[i])
    xBot=[]
    for i in newLinesBot:
        xBot.append(vectorizer[i])
    xLeft=[]
    for i in newLinesLeft:
        xLeft.append(vectorizer[i])
    xRight=[]
    for i in newLinesRight:
        xRight.append(vectorizer[i])
    xTextPatterns=[]
    for i in newLinesRight:
        xTextPatterns.append(vectorizer[i])
        
    try:
        newdata=pd.DataFrame(df, columns=df.columns.drop(['Name','fileName','PageHeight','TextPatterns','PageWidth','TOP_PageHeight','TOP_PageWidth','BOTTOM_PageHeight','BOTTOM_PageWidth','LEFT_PageHeight','LEFT_PageWidth','RIGHT_PageHeight','RIGHT_PageWidth','TOP_Name','BOTTOM_Name','LEFT_Name','RIGHT_Name','leftX','rightX','topY', 'bottomY','LEFT_leftX','LEFT_rightX','LEFT_topY', 'LEFT_bottomY','RIGHT_leftX','RIGHT_rightX','RIGHT_topY', 'RIGHT_bottomY','TOP_leftX','TOP_rightX','TOP_topY', 'TOP_bottomY','BOTTOM_leftX','BOTTOM_rightX','BOTTOM_topY', 'BOTTOM_bottomY', 'PageWidth', 'PageHeight']))
    except Exception as e:
        print('Valid columns not found',e)
        #return json.dumps({'status':400 , 'info':'Valid columns not found'})
        
    x=pd.DataFrame(x,columns=[str(x) for x in range(1,21)])
    xTop=pd.DataFrame(xTop,columns=["top"+str(x) for x in range(1,21)])
    xBot=pd.DataFrame(xBot,columns=["bot"+str(x) for x in range(1,21)])
    xLeft=pd.DataFrame(xLeft,columns=["left"+str(x) for x in range(1,21)])
    xRight=pd.DataFrame(xRight,columns=["right"+str(x) for x in range(1,21)])
    xPatterns=pd.DataFrame(xTextPatterns,columns=["pattern"+str(x) for x in range(1,21)])
    
    newdata1=pd.concat([newdata, x, xTop, xBot, xLeft, xRight, xPatterns], axis=1)
    
    for i in newdata1.columns:
        if "Name" in i:
            newdata1[i]=newdata1[i].fillna('null')
        else:
            newdata1[i]=newdata1[i].fillna(0)  
    
    #classifiers = [RandomForestClassifier(n_estimators=1000), SVC(kernel="rbf", C=0.025, probability=True),DecisionTreeClassifier(),AdaBoostClassifier(),GradientBoostingClassifier(), GaussianNB(),LinearDiscriminantAnalysis(),XGBClassifier()]
    
    classifiers = [RandomForestClassifier(n_estimators=1000)]
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(newdata1.drop(['property'],axis=1), newdata1['property'], test_size=0.2, random_state=101)
    print(X_train.info())
    
    f1scores={}
    accuracies={}

    for clf in classifiers:
        clf.fit(X_train, y_train)
        name = clf.__class__.__name__
        print("="*30)
        print(name)

        print('****Results****')
        train_predictions = clf.predict(X_test)
        acc = accuracy_score(y_test, train_predictions)
        print("Accuracy: {:.2%}".format(acc))
        
        f1score=sklearn.metrics.f1_score(y_test,train_predictions, average="macro")
        print("F1 Score: {:.4}".format(f1score))
        
        print("="*30)
    
    for clf in classifiers:
        clf.fit(newdata1.drop(['property'],axis=1), newdata1['property'])
        name = clf.__class__.__name__
        print("="*30)
        print(name)

        print('****Results****')
        train_predictions = clf.predict(newdata1.drop(['property'],axis=1))
        acc = accuracy_score(newdata1['property'], train_predictions)
        print("Accuracy: {:.2%}".format(acc))
        accuracies[name]=acc
        
        f1score=sklearn.metrics.f1_score(newdata1['property'],train_predictions, average="macro")
        print("F1 Score: {:.4}".format(f1score))
        f1scores[name]=f1score
        
        print("="*30)
    
    f1scores={k: v for k, v in sorted(f1scores.items(), key=lambda item: item[1])}
    classifierName=list(f1scores.keys())[-1]
    f1score=f1scores[classifierName]
    method_name = classifierName
    print('classfierName----',classifierName) 
    #possibles = globals()
    #.copy()
    #possibles.update(locals())
    #classifier = possibles.get(method_name)
    classifier=eval(classifierName)(n_estimators=1000)
    classifier.fit(newdata1.drop(['property'],axis=1), newdata1['property'])
    
    fileName=modelType+orgId+documentType+str(newVersion)+".pkl"
    joblib.dump(vectorizer, ("vectorizer"+fileName), compress=True, protocol=2)  
    joblib.dump(classifier, (fileName), compress=True ,protocol=2)
    
    y_pred = classifier.predict(newdata1.drop(['property'],axis=1))
    from sklearn.metrics import confusion_matrix
    print(confusion_matrix(newdata1['property'],y_pred))
    import time
    predseries = pd.Series(y_pred,name='Property')
    result = pd.concat([df, predseries], axis=1)
    result.to_csv(df['fileName'][0][:-4]+".csv")
    timestamp = int(time.time())
    print("timestamp =", timestamp)
    print(y_train)
    print(fileName)
    x=db.get_collection("modeldatas").insert({'versionNumber': newVersion,'accuracies':accuracies, 'f1scores':f1scores, 'timeStamp' :timestamp, 'subscriberId':data['subscriberId'], 'modelType':modelType, 'fileName':fileName, 'orgId':orgId, 'documentType':documentType, 'fileList':'null', 'f1score':f1score, 'status':'trained'})
    print(x)
    return jsonify({'status':'true', 'info':'Model trained Successfully'})



@app.route('/gibots-pyapi/fieldDetection',methods=['GET', 'POST'])
def fieldDetector():
    data=request.json
    print(data)
    try:
        filePath=data['filePath']
        print(filePath)
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    try:
        modelType=data['modelType']    
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Model type invalid'})
    try:
        documentType=data['documentType']    
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Document type invalid'})
    try:
        orgId=data['orgId']
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Invalid organization'})
    try:
        df=pd.read_csv(filePath)
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    
    lines=[]
    linesTop=[]
    linesBot=[]
    linesLeft=[]
    linesRight=[]
    textPatterns=[]

    for i in df.columns:
        if "Name" in i:
            df[i]=df[i].fillna('null')
        else:
            df[i]=df[i].fillna(0)

    for i in df['Name']:
        lines.append(str(i))
    for i in df['TOP_Name']:
        linesTop.append(str(i))
    for i in df['BOTTOM_Name']:
        linesBot.append(str(i))
    for i in df['LEFT_Name']:
        linesLeft.append(str(i))
    for i in df['RIGHT_Name']:
        linesRight.append(str(i))
            
    newLines=[]
    newLinesTop=[]
    newLinesBot=[]
    newLinesLeft=[]
    newLinesRight=[]
    newTextPatterns=[]

    corpus = set()
    for i in range(0,len(lines)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLines.append(review)
    
    for i in range(0,len(linesTop)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLinesTop.append(review)
    
    for i in range(0,len(linesBot)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLinesBot.append(review)
    
    for i in range(0,len(linesLeft)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLinesLeft.append(review)
    
    for i in range(0,len(linesRight)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newLinesRight.append(review)
        
    for i in range(0,len(textPatterns)):
        review = re.sub('[^a-zA-Z0-9]', ' ',str(lines[i]))
        review = review.lower()
        review = review.split(" ")
        from nltk.stem import WordNetLemmatizer
        lem = WordNetLemmatizer()
        review = [lem.lemmatize(word) for word in review if not word in set(stopwords.words('english'))]
        review = ' '.join(review)
        corpus.add(review)
        newTextPatterns.append(review)

    myclient = pymongo.MongoClient(config['dbConnection'])
    db = myclient[config['db']]
    version=1

    try:
        for y in db.get_collection("modeldatas").find():
            if y['modelType']==modelType and y['documentType']==documentType and y['orgId']==orgId and  y['status']=='inProduction':
                version=y['versionNumber']
        fileName=modelType+orgId+documentType+str(version)+".pkl"
        print(fileName)
        loaded_model=joblib.load(fileName)
    except Exception as e:
        print('Valid training file not found',e)

        return json.dumps({'status':400 , 'info':'Valid training file not found'})
    
    vectorizer=joblib.load("vectorizer"+fileName)
    
    x=[]
    for i in newLines:
        x.append(vectorizer[i])
    xTop=[]
    for i in newLinesTop:
        xTop.append(vectorizer[i])
    xBot=[]
    for i in newLinesBot:
        xBot.append(vectorizer[i])
    xLeft=[]
    for i in newLinesLeft:
        xLeft.append(vectorizer[i])
    xRight=[]
    for i in newLinesRight:
        xRight.append(vectorizer[i])
    xTextPatterns=[]
    for i in newLinesRight:
        xTextPatterns.append(vectorizer[i])
    
    
    try:
        newdata=pd.DataFrame(df, columns=df.columns.drop(['Name','fileName','PageHeight','TextPatterns','PageWidth','TOP_PageHeight','TOP_PageWidth','BOTTOM_PageHeight','BOTTOM_PageWidth','LEFT_PageHeight','LEFT_PageWidth','RIGHT_PageHeight','RIGHT_PageWidth','TOP_Name','BOTTOM_Name','LEFT_Name','RIGHT_Name','leftX','rightX','topY', 'bottomY','LEFT_leftX','LEFT_rightX','LEFT_topY', 'LEFT_bottomY','RIGHT_leftX','RIGHT_rightX','RIGHT_topY', 'RIGHT_bottomY','TOP_leftX','TOP_rightX','TOP_topY', 'TOP_bottomY','BOTTOM_leftX','BOTTOM_rightX','BOTTOM_topY', 'BOTTOM_bottomY', 'PageWidth', 'PageHeight']))
    except Exception as e:
        print('Valid columns not found',e)
        return json.dumps({'status':400 , 'info':'Valid columns not found'})
        
    x=pd.DataFrame(x,columns=[str(x) for x in range(1,21)])
    xTop=pd.DataFrame(xTop,columns=["top"+str(x) for x in range(1,21)])
    xBot=pd.DataFrame(xBot,columns=["bot"+str(x) for x in range(1,21)])
    xLeft=pd.DataFrame(xLeft,columns=["left"+str(x) for x in range(1,21)])
    xRight=pd.DataFrame(xRight,columns=["right"+str(x) for x in range(1,21)])
    xPatterns=pd.DataFrame(xTextPatterns,columns=["pattern"+str(x) for x in range(1,21)])


    newdata1=pd.concat([newdata, x, xTop, xBot, xLeft, xRight, xPatterns], axis=1)
  
    y_pred = loaded_model.predict(newdata1)
    try:
        propseries = pd.Series(y_pred,name='Property')
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Property column not made'})
    print(propseries)
    newdata = pd.concat([df, propseries], axis=1)
    class_probabilities = loaded_model.predict_proba(newdata1)
    predProba=[]
    for i in class_probabilities:
        i.sort()
        predProba.append(i[::-1][0])
    predseries = pd.Series(predProba,name='confidence')
    print(predseries)
    newdata = pd.concat([newdata, predseries], axis=1)
    
    for i in range(0,len(newdata['Name'])):
        if '"' in newdata['Name'][i]:
           newdata['Name'][i]= newdata['Name'][i].replace('"', '')
           print("replacing quotes")

    millis = int(round(time.time() * 1000))
    result=str(millis)+'_'+'prediction.csv'
    path=config['uploadFilePath']+result
    #path="/var/www/scan/"+result
    print (path)
    newdata.to_csv(path)
    #finaldata=y_pred.tolist()
    return json.dumps({"result":path})

@app.route('/gibots-pyapi/clusterTraining',methods=['GET', 'POST'])
def clusterTrainer():
    import cv2 as cv
    import urllib.request
    inputData=request.json
    #fileList=inputData['fileList']
    print(inputData)
    try:
    	filePath=data['filePath']
    except:
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    try:
        documentType=data['documentType']    
    except:
        return json.dumps({'status':400 , 'info':'Document type not found'})
    try:
        orgId=data['orgId']
    except:
        return json.dumps({'status':400 , 'info':'Invalid organization'})
    #subscriberId=inputData['subscriberId']
    result=pd.DataFrame(columns=[x for x in range(1,640000)])
    print(result.info())
    for i in filePath:
        print(i)
        #resp = urllib.request.urlopen(i)
        #image = np.asarray(bytearray(resp.read()), dtype="uint8")
        #im = cv.imdecode(image, cv.IMREAD_COLOR)
        try:
            im=cv.imread(i)
        except:    
            return json.dumps({'status':400 , 'info':'Invalid imapicklege'})
        im = cv.resize(im, (800, 800))
        im = cv.cvtColor(im,cv.COLOR_BGR2GRAY)
        im =im.flatten()
        df1=pd.DataFrame(im)
        df1=df1.T
        df2=pd.DataFrame(data=pd.Series(documentType),columns=['property'])
        result1 = pd.concat([df1, df2], axis=1, join_axes=[df1.index])
        result = pd.concat([result, result1],ignore_index=True)
    myclient = pymongo.MongoClient(config['dbConnection'])
    db = myclient[config['db']]
    version=0
    try:
        for y in db.get_collection("modeldatas").find():
            if y['modelType']=='clusterModel' and y['orgId']==orgId:
                version=y['versionNumber']
        newVersion=version+1
        oldFileName="clusteringModel"+orgId+str(version)+".pkl"
    except:
        return json.dumps({'status':400 , 'info':'Invalid db'})        
    try:
        classifier=joblib.load(oldFileName)
    except:
        classifier=RandomForestClassifier(n_estimators=1000)
    classifier.fit(result.drop(['property'],axis=1), result['property'])
    fileName="clusteringModel"+orgId+str(newVersion)+".pkl"
    joblib.dump(classifier, (fileName), compress=True ,protocol=2)
    from datetime import datetime

    # current date and time
    now = datetime.now()

    timestamp = datetime.timestamp(now)
    print("timestamp =", timestamp)

    x=db.get_collection("modeldatas").insert({'versionNumber': newVersion, 'timeStamp':timestamp, 'modelType':'clusterModel', 'fileName':fileName, 'orgId':orgId, 'fileList':'null', 'status':'trained'})
    print(x)
    return jsonify({'status':'true', 'info':'Model trained Successfully'})

@app.route('/gibots-pyapi/tableTraining',methods=['GET', 'POST'])
def tableTraining():
    inputData=request.json
    filePath=inputData['filePath']
    orgId=inputData['orgId']
    documentType=inputData['documentType']
    subscriberId=inputData['subscriberId']

    import luminoth
    import pymongo
    import subprocess
    import os

    root_dir = os.getcwd()
    file_list = [ 'train.csv']
    image_source_dir = os.path.join(root_dir, 'data/train/')
    orig_image_dir = os.path.join(root_dir, 'data/images/')
    data_root = os.path.join(root_dir, 'data')
    tf_dir = os.path.join(root_dir, 'tfdata2')
    for file in file_list:
        print (file)
        image_target_dir = os.path.join(data_root, file.split(".")[0])

        # read list of image files to process from file
        image_list = pd.read_csv(os.path.join(data_root, file), header=None)[0]
        image_list.pop(0)

        print("Start preprocessing images")
        print (image_list)
        for image in image_list:
            # open image file
            print(image)
            img = cv2.imread(orig_image_dir+image)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # perform transformations on image
            b = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=5)
            g = cv2.distanceTransform(img, distanceType=cv2.DIST_L1, maskSize=5)
            r = cv2.distanceTransform(img, distanceType=cv2.DIST_C, maskSize=5)

            # merge the transformed channels back to an image
            transformed_image = cv2.merge((b, g, r))
            target_file = os.path.join(image_target_dir, image)
            print("Writing target file {}".format(target_file))
            cv2.imwrite(target_file, transformed_image)


    myclient = pymongo.MongoClient(config['dbConnection'])
    db = myclient[config['db']]
    version=0
    for y in db.get_collection("modeldatas").find():
        if y['status']=='inProduction' and y['modelType']=='tableModel' and y['documentType']==documentType and y['orgId']==orgId:
            version=y['versionNumber']

    move_folder=os.path.join(root_dir, 'data/data', 'tableData'+version)

    subprocess.call(["sudo","mv", orig_image_dir, "-t", move_folder , "`ls|grep", "image`"])
    subprocess.call(["sudo","rm", image_source_dir+"*"])


    newVersion= version+1
    subprocess.call(["lumi", "dataset", "transform", "--type", "csv", "--data-dir", data_root,"/", "--output-dir", tf_dir,"/", "--split", "train", "--split", "val"])

    subprocess.call(["lumi", "train", "-c", "config.yml"])

    subprocess.call(["lumi","checkpoint","create","config.yml","-e","name:",name,"-e","alias:","table"+str(newVersion)])
    from datetime import datetime

    # current date and time
    now = datetime.now()

    timestamp = datetime.timestamp(now)
    print("timestamp =", timestamp)

    x=db.get_collection("modeldatas").insert({'versionNumber': newVersion, 'timeStamp':timestamp, 'subscriberId':subscriberId, 'modelType':'tableModel', 'fileName':fileName, 'orgId':orgId, 'documentType':documentType, 'fileList':'null', 'status':'trained'})
    print(x)
    return jsonify({'status':'true', 'info':'Model trained Successfully'})

@app.route('/gibots-pyapi/columnTraining',methods=['GET', 'POST'])
def columnTraining():
    inputData=request.json
    filePath=inputData['filePath']
    orgId=inputData['orgId']
    subscriberId=inputData['subscriberId']
    import luminoth
    import pymongo
    import subprocess
    import os

    root_dir = os.getcwd()
    file_list = [ 'train.csv']
    image_source_dir = os.path.join(root_dir, 'data/train/')
    orig_image_dir = os.path.join(root_dir, 'data/images/')
    data_root = os.path.join(root_dir, 'data')
    tf_dir = os.path.join(root_dir, 'tfdata2')


    for file in file_list:
        print (file)
        image_target_dir = os.path.join(data_root, file.split(".")[0])

        # read list of image files to process from file
        image_list = pd.read_csv(os.path.join(data_root, file), header=None)[0]
        image_list.pop(0)

        print("Start preprocessing images")
        print (image_list)
        for image in image_list:
            # open image file
            print(image)
            img = cv2.imread(orig_image_dir+image)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # perform transformations on image
            b = cv2.distanceTransform(img, distanceType=cv2.DIST_L2, maskSize=5)
            g = cv2.distanceTransform(img, distanceType=cv2.DIST_L1, maskSize=5)
            r = cv2.distanceTransform(img, distanceType=cv2.DIST_C, maskSize=5)

            # merge the transformed channels back to an image
            transformed_image = cv2.merge((b, g, r))
            target_file = os.path.join(image_target_dir, image)
            print("Writing target file {}".format(target_file))
            cv2.imwrite(target_file, transformed_image)


    myclient = pymongo.MongoClient(config['dbConnection'])
    db = myclient[config['db']]
    version=0
    for y in db.get_collection("modeldatas").find():
        if y['Status']=='inProduction' and y['modelType']=='columnModel' and y['documentType']==documentType and y['orgId']==orgId:
            version=y['versionNumber']
    
    move_folder=os.path.join(root_dir, 'data/data', 'tableData'+version)

    subprocess.call(["sudo","mv", orig_image_dir, "-t", move_folder , "`ls|grep", "image`"])
    subprocess.call(["sudo","rm", image_source_dir+"*"])


    newVersion=version+1
    subprocess.call(["lumi", "dataset", "transform", "--type", "csv", "--data-dir", data_root,"/", "--output-dir", tf_dir,"/", "--split", "train", "--split", "val"])

    subprocess.call(["lumi", "train", "-c", "config.yml"])

    subprocess.call(["lumi","checkpoint","create","config.yml","-e","name:",name,"-e","alias:","column"+str(newVersion)])

    from datetime import datetime

    # current date and time
    now = datetime.now()

    timestamp = datetime.timestamp(now)
    print("timestamp =", timestamp)

    x=db.get_collection("modeldatas").insert({'versionNumber': newVersion, 'timeStamp':timestamp, 'subscriberId':subscriberId, 'modelType':'columnModel', 'fileName':fileName, 'orgId':orgId, 'documentType':documentType, 'fileList':'null', 'status':'trained'})
    print(x)
    return jsonify({'status':'true', 'info':'Model trained Successfully'})

@app.route('/gibots-pyapi/clusterDetection',methods=['GET', 'POST'])
def clusterDetector():
    import cv2 as cv
    data=request.json
    receivedInput=data['input']
    print(receivedInput) 
    try:
        filePath=receivedInput['filePath']
    except:
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    try:
        orgId=receivedInput['orgId']
    except:
        return json.dumps({'status':400 , 'info':'Org ID invalid'})
    #resp = urllib.request.urlopen(filePath)
    #image = np.asarray(bytearray(resp.read()), dtype="uint8")
    #im1 = cv.imdecode(image, cv.IMREAD_COLOR)
    im1 = cv.imread(filePath)
    im1 = cv.resize(im1, (800, 800))
    im1 = cv.cvtColor(im1,cv.COLOR_BGR2GRAY)
    im1=im1.flatten()
    df1=pd.DataFrame(im1)
    df1=df1.T
    myclient = pymongo.MongoClient(config['dbConnection'])
    db = myclient[config['db']]
    version=0
    try:
        for y in db.get_collection("modeldatas").find():
            if y['status']=='inProduction' and y['modelType']==modelType and y['documentType']==documentType and y['orgId']==orgId:
                version=y['versionNumber']
        fileName="clusteringModel"+orgId+documentType+str(version)+".pkl"
        model=joblib.load(fileName)
    except:
         return json.dumps({'status':400 , 'info':'Valid training file not found'})   
    y_pred=model.predict(df1)
    print(y_pred[0])
    outputData={'documentType':y_pred[0], 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com:1443/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)

@app.route('/gibots-pyapi/tableDetection',methods=['GET', 'POST'])
def tableDetector():
    data=request.json
    filePath=data['filePath']
    from luminoth import Detector, read_image, vis_objects
    detector = Detector(checkpoint='table')
    image = read_image(filePath)
    objects = detector.predict(image)
    for prediction in objects:   
        if prediction['prob'] > .80:
            a=[int(i) for i in prediction['bbox']]
            prediction['bbox']=a
            left=a[0]
            top=a[1]
            right=a[2]
            bottom=a[3]
            cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 4)
            cv2.imwrite(filePath, image)
    
    
    print(objects)
    print("Object Drawn")
    output={"filePath":filePath,"points":objects}
    return output

@app.route('/gibots-pyapi/columnDetection',methods=['GET', 'POST'])
def columnDetector():
    data=request.json
    filePath=data['filePath']
    import cv2
    import os
    from luminoth import Detector, read_image, vis_objects
    detector = Detector(checkpoint='column')
    image = read_image(filePath)
    objects = detector.predict(image)
    for prediction in objects:   
        if prediction['prob'] > .80:
            a=[int(i) for i in prediction['bbox']]
            prediction['bbox']=a
            left=a[0]
            top=a[1]
            right=a[2]
            bottom=a[3]
            cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 4)
            cv2.imwrite(filePath, image)
    
    
    print(objects)
    print("Object Drawn")
    output={"filePath":filePath,"points":objects}
    return output

@app.route('/gibots-pyapi/modelUpdate',methods=['GET', 'POST'])
@cross_origin()
def modelUpdater():
    data=request.json
    try:
        version=data['versionNumber']
    except:
         return json.dumps({'status':400 , 'info':'Valid version number not found'})       
    try:
        modelType=data['modelType']
    except:
        return json.dumps({'status':400 , 'info':'Valid model type not found'})    
    try:
        documentType=data['documentType']
    except:
         return json.dumps({'status':400 , 'info':'Valid document type not found'})    
    try:
        orgId=data['orgId']
    except:
         return json.dumps({'status':400 , 'info':'orgId is invalid'})
    try:     
        subscriberId=data['subscriberId']
    except:
         return json.dumps({'status':400 , 'info':'subscriberId not found'})    
    myclient = pymongo.MongoClient(config['dbConnection'])
    db = myclient[config['db']]
    x=db.get_collection("modeldatas").find_one_and_update({ "orgId": orgId, "subscriberId":subscriberId, "modelType": modelType, "status": "inProduction", "documentType": documentType},{ "$set":{"status":"retired"}}, new=True)
    y=db.get_collection("modeldatas").find_one_and_update({ "orgId": orgId, "subscriberId":subscriberId, "modelType": modelType, "versionNumber":version, "documentType": documentType},{ "$set":{"status":"inProduction"}}, new=True)
    print(x)
    print(y)
    if y['status']=='inProduction':
        return jsonify({'status':'true', 'info':'Model Updated Successfully'})
    else:
        return jsonify({'status':'false', 'info':'Error updating model'})

@app.route('/gibots-pyapi/tagMarking',methods=['GET', 'POST'])
def MarkingTags():
    import cv2 as cv
    import img2pdf
    data=request.json
    filePath=data['filePath']
    lines=data['lines']
    coOrdinates=[{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}]
    j=0
    l=0
    try:
        for i in range(1,len(lines)):
            if (i>=l):
                if (lines[i]['Property']!='undefined'):
                    coOrdinates[j]['Property']=lines[i]['Property']
                    coOrdinates[j]['leftX']=lines[i]['leftX']
                    coOrdinates[j]['topY']=lines[i]['topY']
                    print("i=",i)
                    if coOrdinates[j]['Property']!=lines[i]['Property']:
                        coOrdinates[j]['Property']=lines[i]['Property']
                        coOrdinates[j]['leftX']=lines[i]['leftX']
                        coOrdinates[j]['topY']=lines[i]['topY']
                    elif lines[i]['Property']==coOrdinates[j]['Property']:
                        for k in range(i,len(lines)+1):
                            if lines[k]['Property']!=lines[i]['Property']:
                                coOrdinates[j]['rightX']=lines[k-1]['rightX']
                                coOrdinates[j]['bottomY']=lines[k-1]['bottomY']
                                l=k
                                print("k=",k)
                                break
                else:
                    continue
                print("J=",j)
                j=j+1

    except IndexError:
        coOrdinates[j]['rightX']=lines[k-1]['rightX']
        coOrdinates[j]['bottomY']=lines[k-1]['bottomY']

    img=cv.imread(filePath)
    try:
        for x in coOrdinates:
            print(x)
            cv.rectangle(img,(int(x['leftX'])-10,int(x['topY'])-10),(int(x['rightX'])+10,int(x['bottomY'])+10),(255,0,0),2)
    except KeyError:
        try:
            print("Writing Image")
            cv.imwrite(filePath,img)
            print("Image"+filePath)
        except:
            print("An exception was thrown")

    # png to pdf converter
    #  with open(imagePath,"wb") as f:
    #     f.write(img2pdf.convert(imagePath, dpi=300)
    return (jsonify({"imagePath":filePath}))

@app.route('/gibots-pyapi/dewaPredict',methods=['GET', 'POST'])
@cross_origin()
def dewaPredictor():
    data=request.json
    receivedInput=data['input']
    print(receivedInput) 
    input=receivedInput['input']
    dataArray=input.split("\n")
    
    result=[]
    for i in range(1, len(dataArray)):
        if 'OTP' in dataArray[i] or 'TP' in dataArray[i]:
            result.append(dataArray[i]+" "+dataArray[i+1]+" "+dataArray[i+2])
    output=[]

    for i in range(1,len(result)):
        tempDict={}
        tempDict["label"]="Tag"+" "+str(i)
        tempDict["type"]= "text"
        tempDict["field"]="Tag"+" "+str(i)
        tempDict["isDMSKey"]= False
        tempDict["value"]=result[i]
        tempDict["Tag"+" "+str(i)]= result[i]
        output.append(tempDict)
    count={
            "label": "Trench Pit Count",
            "type": "text",
            "field": "Trench Pit Count",
            "isDMSKey": False,
            "value": len(output),
            "Trench Pit Count": len(output)
          }
    output.append(count)

    outputData={'output':output, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)

@app.route('/gibots-pyapi/pdfTableExtract',methods=['GET', 'POST'])
@cross_origin()
def dewaPrpdfTableExtractor():
    data=request.json
    receivedInput=data['input']
    path=receivedInput['inputPdfPath']
    import pdfplumber
    import json
    import sys

    print('------',path)

    ruleObj = [{
        "Cable size":2.5,
        "Load kW":15
    },{
        "Cable size":4,
        "Load kW":20
    },{
        "Cable size":6,
        "Load kW":30
    },{
        "Cable size":10,
        "Load kW":40
    },{
        "Cable size":16,
        "Load kW":50
    },{
        "Cable size":25,
        "Load kW":60
    },{
        "Cable size":25,
        "Load kW":80
    },{
        "Cable size":50,
        "Load kW":100
    },{
        "Cable size":70,
        "Load kW":125
    },{
        "Cable size":65,
        "Load kW":160
    },{
        "Cable size":120,
        "Load kW":180
    },{
        "Cable size":150,
        "Load kW":200
    },{
        "Cable size":185,
        "Load kW":250
    },{
        "Cable size":240,
        "Load kW":300
    },{
        "Cable size":300,
        "Load kW":350
    },{
        "Cable size":400,
        "Load kW":400
    }]


    ruleObjIncomer = [
        {
        "Incomer/MCCB":60,
        "Load kW":30
        },
        {
        "Incomer/MCCB":100,
        "Load kW":50
        },
        {
        "Incomer/MCCB":125,
        "Load kW":60
        },
        {
        "Incomer/MCCB":160,
        "Load kW":80
        },
        {
        "Incomer/MCCB":200,
        "Load kW":100
        },
        {
        "Incomer/MCCB":300,
        "Load kW":150
        },
        {
        "Incomer/MCCB":400,
        "Load kW":200
        }
    ]

    # pages = [2,3,4,5,6,10,11,12,13]
    pages = [2,3,4,5,6]


    import re

    regex = r"(\d*)MM2"
    finalArr = []
    with pdfplumber.open(path) as pdf:
        for page in pages:
            # print('**********************Table',page-1,'*******************************************') 
            first_page = pdf.pages[page-1]
            table1 = first_page.extract_table()
            # print (table1)
            subHeaders = table1[2]
            subHeaders[0]=table1[1][0]         
            finalSubHeaders= []
            for subHeader in subHeaders:
                if type(subHeader) == str:
                    finalSubHeaders.append(subHeader.replace("\n", " "));
                else:
                    finalSubHeaders.append(subHeader)   
            # print(finalSubHeaders)
            finalSubHeaders.append('ValidCable')
            finalSubHeaders.append('MCCBValid')
            finalSubHeaders.append('phaseBalance')
            finalSubHeaders.append('Aggregation')

            obj = {'ValidCable':'','MCCBValid':'','phaseBalance':'','Aggreagation':''}
            tableFinal1=[]
            for i in range(len(table1)):
                if table1[i][0] =='MDB CONNECTED TO :  DEWA LV DB/ TRANSF MDB \nCONNECTED TO : DEWA ……….':
                    print('--------------break')
                    break 
                if table1[i][0] =='MDB CONNECTED TO :  DEWA LV DB/ TRANSF\nMDB CONNECTED TO : MDB ……….':
                    print('--------------break')
                    break      
                if i >2:
                    row = table1[i]
                    for j in range(len(row)):
                        if row[j] ==None:
                            row[j]=''                   
                        obj[finalSubHeaders[j]]=row[j]
                    tableFinal1.append(obj)  
                    obj = {'ValidCable':'','MCCBValid':'','phaseBalance':'','Aggreagation':''}

        

            # print(tableFinal1)
            outGoingBPH = 0.0
            outGoingYPH = 0.0
            outGoingRPH = 0.0
            IncomerRPH = 0.0
            IncomerYPH = 0.0
            IncomerBPH = 0.0
            for row in tableFinal1: 
                # print(row)
                loadAvg=0.0
                RPH=0.0
                YPH=0.0
                BPH=0.0
                deviation=0.0
                if ('R  - P  H KW' in row and row['R  - P  H KW']) and row['R  - P  H KW']:
                    row['R-PH KW'] = row['R  - P  H KW']
                    del(row['R  - P  H KW'])
                if ('R-PH KW' in row and row['R-PH KW']) and ('Y-PH KW' in row and row['Y-PH KW']) and ('B-PH KW' in row and row['B-PH KW']):
                    loadAvg = (float(row['R-PH KW'])+float(row['Y-PH KW'])+float(row['B-PH KW']))/3
                    # print('loadAvg------')
                    outGoingRPH= outGoingRPH + float(row['R-PH KW'])
                    outGoinYPH= outGoingYPH + float(row['Y-PH KW'])
                    outGoingBPH= outGoingBPH + float(row['B-PH KW'])

                    RPH = (float(row['R-PH KW'])/loadAvg)*100
                    if RPH<100:
                        RPH=100-RPH
                    if RPH>100:  
                        RPH=RPH-100  
                    YPH = (float(row['Y-PH KW'])/loadAvg)*100
                    if YPH<100:
                        YPH=100-YPH
                    if YPH>100:  
                        YPH=YPH-100 
                    BPH = (float(row['B-PH KW'])/loadAvg)*100
                    if BPH<100:
                        BPH=100-BPH
                    if BPH>100:  
                        BPH=BPH-100 
                    if RPH > 5 or YPH > 5 or BPH > 5:      
                        row['phaseBalance']='invalid'
                    else:
                        row['phaseBalance']='valid'
                        # print('--------------RPH--',RPH)
        
                if (('1c sq mm' in row and row['1c sq mm']) or ('1c              sq mm' in row and row['1c              sq mm'])) and row['TOTAL    KW']:
                    if '1c              sq mm' in row and row['1c              sq mm']:
                        ECC_SIZE = row['1c              sq mm']
                        row['1c sq mm'] = row['1c              sq mm']
                        del row['1c              sq mm']
                    else:
                        ECC_SIZE = row['1c sq mm']        
                    matches = re.finditer(regex, ECC_SIZE, re.MULTILINE)
                    for matchNum, match in enumerate(matches, start=1):
                        for groupNum in range(0, len(match.groups())):
                            groupNum = groupNum + 1
                            ECC_SIZE = match.group(groupNum)
                    if ECC_SIZE:
                        # print(ECC_SIZE) 
                        for rule in ruleObj:
                            if float(row['TOTAL    KW'])<rule['Load kW']:
                                if  int(ECC_SIZE) <= rule['Cable size'] :
                                    row['ValidCable'] = "valid"
                                else:
                                    row['ValidCable'] = "invalid"
                                # print(ECC_SIZE,' ',row)     
                                break

                if row['CITCUIT / FEEDER   DB NO.'] =='INCOMER':
                    if ('R  - P  H KW' in row and row['R  - P  H KW']) and row['R  - P  H KW']:
                        row['R-PH KW'] = row['R  - P  H KW']
                        del(row['R  - P  H KW'])
                    if ('R-PH KW' in row and row['R-PH KW']) and ('Y-PH KW' in row and row['Y-PH KW']) and ('B-PH KW' in row and row['B-PH KW']):
                         IncomerRPH = float(row['R-PH KW'])
                         IncomerYPH = float(row['Y-PH KW'])
                         IncomerBPH = float(row['B-PH KW'])

                if row['CITCUIT / FEEDER   DB NO.'] =='INCOMER' and row['MCCB']:
                    SIZE = row['MCCB'].split('A') 
                    # print(SIZE[0])
                    for rule in ruleObjIncomer:  
                        if float(row['TOTAL    KW'])<rule['Load kW']:
                            if  int(SIZE[0]) <= rule['Incomer/MCCB']:
                                row['MCCBValid'] = "valid"
                            else:
                                row['MCCBValid'] = "invalid"    
                            break    
                            # print(SIZE,' ',row)     
            print('--------------RPH--',IncomerRPH,'--------------RPH--',outGoingRPH,)
            print('--------------YPH--',IncomerYPH,'--------------YPH--',outGoingYPH,)   
            print('--------------BPH--',IncomerBPH,'--------------BPH--',outGoingBPH,)
            # print(tableFinal1)
            # finalObj['table'+str(page-1)]=tableFinal1
            finalArr.append(tableFinal1)
            outputData={'statusCode': '200'}
            for i in range(0, len(finalArr)):
                outputData['table'+str(i+1)]=finalArr[i]
    print("\n\n\n\n\n\n\n")    
    print(json.dumps(outputData))
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)
          
@app.route('/gibots-pyapi/getToken',methods=['GET', 'POST'])
def get_auth_token():
    inputData=request.json
    user=inputData['user']
    password=inputData['password']
    def generate_auth_token(user,password,id=100,expiration = 86400):
        myclient = pymongo.MongoClient(config['dbConnection'])
        db = myclient[config['db']]
        for y in db.get_collection("userinfo").find({},{"user": user, "password": password }):
            if y['user']==user and y['password']==password:
                s = Serializer(config['SECRET_KEY'], expires_in = expiration)
                return s.dumps({ 'id': id })
        return None

    token = generate_auth_token(user,password)
    print (token)
    if token==None:
        return json.dumps({'token':"", 'status':400 , 'info':'username or password is invalid'})
    else:
        return json.dumps({ 'token': token.decode('ascii'), 'status':200 })
#2
@app.route('/gibots-pyapi/ocr',methods=['GET', 'POST'])
def ocReader():
    #os.environ['OMP_THREAD_LIMIT'] = '2'
    
    inputData=request.json
    print(request.headers)
    try:
    	token=request.headers['authorization']
    except:
        return json.dumps({'status':400 , 'info':'Please send authorization token'})
    try:
        img_data=inputData['image']
    except:
        return json.dumps({'status':400 , 'info':'Please send image base64 string'})
    img_data=str.encode(img_data)

    s = Serializer(config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return json.dumps({'status':400 , 'info':'Valid token, but expired'})
    except BadSignature:
        return json.dumps({'status':400 , 'info':'Invalid token'})

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file

    #langs = ['5x5_Dots_FT_500', 'dotOCRDData1', 'Dotrice_FT_500', 'DotMatrix_FT_500','DisplayDots_FT_500', 'LCDDot_FT_500', 'Orario_FT_500', 'Transit_FT_500','eng'] 
    langs= ['eng']
    import base64
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    im_name=str(request.remote_addr)+"_"+str(current_time)+".png"
    try:
    	with open(im_name, "wb") as fh:
    		fh.write(base64.decodebytes(img_data))
    except:
        json.dumps({'status':400 , 'info':'Invalid base64 string. Please send a valid base64 string. You can convert any image to a base64 string using online converters.'})

    print('\n')
    OCR_outputs = set()
    OCR_map = {}
    scores = []
    avg_confidences = []
    for i in range(len(langs)):
        print("We are entering command")
        data = pytesseract.image_to_data(Image.open(im_name), lang = langs[i], config='--psm 6 --oem 1', 
                output_type=Output.DICT)
        #print("data-------",data)
        textString = pytesseract.image_to_string(Image.open(im_name), lang = langs[i], config='--psm 6 --oem 1')
        text = data['text']
        print(text)
        confidences = []
        numChars = []
        
        for j in range(len(text)):
            if int(data['conf'][j]) > -1:
                confidences.append(int(data['conf'][j]))
                numChars.append(len(text[j]))

        if confidences != []:
            avg_confidences.append(np.average(confidences, weights=numChars))
        else:
            avg_confidences.append(0)
        if textString not in OCR_outputs:
            OCR_outputs.add(textString)
            OCR_map[textString] = [i]
            scores.append(avg_confidences[i])
        else:
            scoreSum = avg_confidences[i]
            for j in OCR_map[textString]:
                scoreSum = scoreSum + avg_confidences[j]
            for j in OCR_map[textString]:
                scores[j] = scoreSum
            OCR_map[textString].append(i)
            scores.append(scoreSum)
    best = scores.index(max(scores))
    text = pytesseract.image_to_string(Image.open(im_name), lang = langs[best], config='--psm 6 --oem 1')
    data = pytesseract.image_to_data(Image.open(im_name), lang = langs[best], config='--psm 6 --oem 1', 
                output_type=Output.DICT)
    cData = []            
    for j in range(len(data['text'])):
            if int(data['conf'][j]) > -1:
                obj = {
                    "leftX":data['left'][j],
                    "topY":data['top'][j],
                    "rightX":data['left'][j]+data['width'][j],
                    "bottomY":data['top'][j]+data['height'][j],
                    "text":data['text'][j],
                    "confidence":data['conf'][j]
                }

                cData.append(obj)
    strData = json.dumps(data)
    cDataParse = json.dumps(cData)
 
    f = open(str(request.remote_addr)+"_"+str(current_time)+".txt", "w")
    f.write(text)
    f.write('\n')
    f.write(strData)
    f.write('\n')
    f.write(cDataParse)
    
    
    return json.dumps({'text':text, 'CData':cData})

@app.route('/gibots-pyapi/pan1',methods=['GET', 'POST'])
def panIdentification():
    import re
    from flask import request
    data=request.json
    receivedInput=data['input']
    panString=receivedInput['input']
    print(panString)
    result = re.sub(r"INCOME TAX DEPARTMENT","",panString, flags = re.I)
    result1 = re.sub(r"GOVT. OF INDIA","", result, flags = re.I)
    result2 = re.sub(r"आयकर विभाग","", result1, flags = re.I)
 #   resu = re.sub(r"GOVT OF IND", result2, flags = re.I)

    result3 = re.sub(r"भारत सरकार","",result2)

    
    c=[]
    e=[]
    output=[]
    p=re.findall('([A-Z]+)', result3)
    c.append(p[0:3])
    for i in c:
        name=((' '.join(i)))
#        print("Name:",name)
    e.append(p[3:6])
    for t in e:
        Fname=((' '.join(t)))
#        print("Father's Name:",Fname)
    Date = re.findall(r'(\d+/\d+/\d+)',result3)
#    print("DOB :",Date[0])
    panNo=("[A-Z]{5}[0-9]{4}[A-Z]{1}");
    PanNo = re.findall(panNo,result3)
#    print("PanNo:",PanNo[0])
    
    tempDict={}
    tempDict["Name"]=name
    tempDict["Father's Name"]= Fname
    tempDict["DOB"]=Date[0]
    tempDict["PanNo"]= PanNo[0] 
    output.append(tempDict)
    print(output)
    finalOut=[]
    obj={}
    for key,value in tempDict.items():
        obj={}
        obj['label']=key
        obj['value']=value
        obj["type"]= "text"
        obj["isDMSKey"]= False
        finalOut.append(obj)
#    print(finalOut)
        
        
        
    
    outputData={'output':finalOut, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)
    
@app.route('/gibots-pyapi/riskDetection1',methods=['GET', 'POST'])
def riskDetector1():
    import pandas as pd
    import numpy as np
    import pymongo
    import json
    from sklearn import preprocessing
    from sklearn.externals import joblib
    from xgboost import XGBClassifier
    print("555")
    data=request.json
    print(data)
    try:
        receivedInput=data['input']
        input=receivedInput['input']
        df=pd.DataFrame(input, columns=['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges', 'familyHistory', 'medicalHistory', 'claimsPerYear', 'totalClaimAmount'])
    except:
        return json.dumps({'status':400 , 'info':'Invalid JSON'})

    try:
        df['sex'] = df['sex'].astype('category').cat.codes
        df['smoker'] = df['smoker'].astype('category').cat.codes
        df['region'] = df['region'].astype('category').cat.codes
    except:
        return json.dumps({'status':400 , 'info':'Unable to find columns in given data'})        

    x = df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    dataset=pd.DataFrame(data=x_scaled,columns=df.columns)

    try:
        classifier=joblib.load('insuranceModel.pkl')
    except:
        return json.dumps({'status':400 , 'info':'Unable to find trained model'})

    y_pred = classifier.predict(dataset)
    class_probabilities = classifier.predict_proba()
    output=[]
    for i in class_probabilities:
        i.sort()
        output.append(i[::-1][0]*100)
    
    df2=pd.DataFrame(data=y_pred, columns=['riskLevel'])
    df3=pd.DataFrame(data=output, columns=['predictionAccuracy'])

    df['riskLevel']=df2['riskLevel']
    df['predictionAccuracy']=df3['predictionAccuracy']

    result = {}
    for index, row in dataset.iterrows():
        result[index] = dict(row)

    outputData={'output':jsonify(result), 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)


@app.route('/gibots-pyapi/riskDetection',methods=['GET', 'POST'])
def riskDetector():
    import pandas as pd
    import numpy as np
    import pymongo
    import json
    from sklearn import preprocessing
    from sklearn.externals import joblib
    from xgboost import XGBClassifier

    data=request.json
    print(data)
    
    receivedInput=data['input']
    age=[receivedInput['age']]
    print("The length of the string  is :",len(age)) 
    sex=[receivedInput['sex']]
    bmi=[receivedInput['bmi']]
    children=[receivedInput['children']]
    
    smoker=[receivedInput['smoker']]
    print("The length of the smoker  is :",len(smoker))
    region=[receivedInput['region']]
    familyHistory=[receivedInput['familyHistory']]
    medicalHistory=[receivedInput['medicalHistory']]
    if familyHistory == ['Yes']:
	     familyHistory = 9
    elif familyHistory == ['No']:
	        familyHistory = 0
    if medicalHistory == ['Yes']:
             medicalHistory = 9
    elif medicalHistory == ['No']:
             medicalHistory = 0
             print("i am print",familyHistory)
    print("i am print",familyHistory)
    print("i am medicalHistory",medicalHistory)
    df=pd.DataFrame(age,columns=['age'])
    df['sex']=sex
    df['bmi']=bmi
    df['children']=children
    df['smoker']=smoker
    df['region']=region
    df['familyHistory']=familyHistory
    df['medicalHistory']=medicalHistory
 
    sample=pd.read_csv("insurance.csv")
    riskLevel= sample['riskLevel']
    sample.drop('riskLevel',axis=1,inplace=True)
    df=pd.concat([sample,df],axis=0)
    df['sex'] = df['sex'].astype('category').cat.codes
    df['smoker'] = df['smoker'].astype('category').cat.codes
    df['region'] = df['region'].astype('category').cat.codes

    x =df.values
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x)
    dataset=pd.DataFrame(data=x_scaled,columns=df.columns)

    X_test=dataset[::-1][0:1]
    dataset.drop(index=1338,axis=0,inplace=True)
 
    classifier = XGBClassifier()
    classifier.fit(dataset, riskLevel)

    y_pred = classifier.predict(X_test)
    riskLevel=y_pred[0]
    class_probabilities = classifier.predict_proba(X_test)
    for i in class_probabilities:
        i.sort()
        riskProbability=i[::-1][0]*100
    print("RISK LEVEL-----"+riskLevel)
    outputData={'riskProbability':riskProbability,'riskLevel':riskLevel, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)



@app.route('/gibots-pyapi/pan2',methods=['GET', 'POST'])
def PanIdentification1():
    data=request.json
    receivedInput=data['input']['input']
    import re
    print(receivedInput)
    result = re.sub(r"INCOME TAX DEPARTMENT","", receivedInput, flags = re.I)
    result1 = re.sub(r"GOVT. OF INDIA","", result, flags = re.I)
    result2 = re.sub(r"आयकर विभाग","", result1, flags = re.I)
    result3 = re.sub(r"भारत सरकार","", result2)
    result4 = re.sub(r"नाम /NAME","", result3)
    result5 = re.sub(r"HTTP/FATHER'S NAME","", result4)
    result6 = re.sub(r"T FERT/PERMANENT ACCOUNT NUMBER","", result5)
    result7 = re.sub(r"जन्म तीथि / DATE OF BIRTH","", result6)
    result8 = re.sub(r"हस्ताक्षर / SIGNATURE","", result7)
    result9 = re.sub(r"आयकर आयुक्त (कंप्यूटर प्रचालन), बेंगलूर\n(Commissioner of Income Tax Computer Operations), Bonga\n","", result8)
    result10 = re.sub(r"जन्म की तारीख /Date of Birth","", result9)
    result11 = re.sub(r"नाम /Name","", result10)
    result12 = re.sub(r"हस्ताक्षर / Signature","", result11)
    result13 = re.sub(r"पिता का नाम /Father's Name","", result12)
    result14 = re.sub(r"। स्थायी लेखा संख्या कार्ड","", result13)
    result15 = re.sub(r"Permanent Account Number Card","", result14)
    result16 = re.sub(r" GOVT. OF IND","", result15)
    result17 = re.sub(r"सत्यमेव जयते"," ",result16)
    #print(result15)
    c=[]
    obj={}
    output=[]
    try:
        panNo=("([A-Za-z]+[\d@]+[\w@]*|[\d@]+[A-Za-z]+[\w@]*)");
        PanNo = re.findall(panNo,result17)
        print(PanNo[0])
    except:
        print("Error")
        return json.dumps({'status':400 , 'info':'Please Enter the Good Picture'})
    try:
        date=re.findall("((0?[13578]|10|12)(-|\/)((0[0-9])|([12])([0-9]?)|(3[01]?))(-|\/)((\d{4})|(\d{2}))|(0?[2469]|11)(-|\/)((0[0-9])|([12])([0-9]?)|(3[0]?))(-|\/)((\d{4}|\d{2})))",result17)
        Date=(date[0][0])
        print(Date)
    except:
        print("Please Enter the Good Picture")
        return json.dumps({'status':400 , 'info':'Please Enter the Good Picture'})
    
    p1=re.findall('([A-Z0-9]+)', result17)
    if re.match("([A-Za-z]+[\d@]+[\w@]*|[\d@]+[A-Za-z]+[\w@]*)",p1[0]) != None:
        p1.remove(p1[0])
    c.append(p1[0:3])
    #print(c)
    for Name in c:
        name=(' '.join(Name))
        print(name)
    l=[]
    l.append(p1[3:6])
    for fname in l:
        Fname=(' '.join(fname))
        print(Fname)
    tempDict={}
    tempDict["Name"]=name
    tempDict["Father's Name"]= Fname
    tempDict["DOB"]=Date
    tempDict["PanNo"]= PanNo[0]
    output.append(tempDict)
    print(output)
    finalOut=[]
    obj={}
    for key,value in tempDict.items():
        obj={}
        obj['label']=key
        obj['value']=value
        obj["type"]= "text"
        obj["isDMSKey"]= False
        finalOut.append(obj)
    print(finalOut)


    outputData={'output':finalOut, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': data['input']['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)


@app.route('/gibots-pyapi/tan',methods=['GET', 'POST'])
def panPredictionn():
    import re
    data=request.json
    receivedInput=data['input']['input']
    inputList=receivedInput.split("\n")
    panNumber=""
    name=""
    fatherName=""
    dob=""
    
    #print(inputList)
    for i in range(0,len(inputList)):
        if "PERMANENT ACCOUNT NUMBER" in inputList[i] or "Permanent Account Number" in inputList[i]:
            panNumber=inputList[i+1]
        if "NAME" in inputList[i] or "Name" in inputList[i]:
            if "FATHER" in inputList[i]:
                fatherName=inputList[i+1]+" "+inputList[i+2]
            elif "Father" in inputList[i]:
                fatherName=inputList[i+1]
            else:
                name=inputList[i+1]
        if "DATE OF BIRTH" in inputList[i] or "Date of Birth" in inputList[i]:
            dob=inputList[i+1]
            if dob[0:1].isdigit():
                continue
            else:
                dob=inputList[i+3]
    
    
    if name=="":
        for i in range(0,len(inputList)):
            if "INCOME TAX DEPARTMENT" in inputList[i]:
                name=inputList[i+1]
            if "GOVT. OF INDIA" in inputList[i]:
                if "INCOME TAX DEPARTMENT" in inputList[i]:
                    fatherName=inputList[i+2]
                    dob=inputList[i+3]
                else:
                    if name[0:1]!='भ':
                        if name!='GOVT. OF INDIA':
                            fatherName=inputList[i+1]
                            dob=inputList[i+2]
                            if fatherName[0:1]=='स':
                                fatherName=inputList[i+2]
                                dob=inputList[i+3]
                        else:
                            name=inputList[i+1]
                            fatherName=inputList[i+2]
                            dob=inputList[i+3]
                    else:
                        name=inputList[i+1]
                        fatherName=inputList[i+2]
                        dob=inputList[i+3]
            
    print(panNumber +"\n"+ name + "\n"+ fatherName + "\n" + dob)
    print(dob)
    if(dob[0].isnumeric()):
        print(dob[0])
    else:
        dob=re.findall("((0?[13578]|10|12)(-|\/)((0[0-9])|([12])([0-9]?)|(3[01]?))(-|\/)((\d{4})|(\d{2}))|(0?[2469]|11)(-|\/)((0[0-9])|([12])([0-9]?)|(3[0]?))(-|\/)((\d{4}|\d{2})))",receivedInput)
        dob=(dob[0][0])
    output=[]
    tempDict={}
    tempDict["Name"]=name
    tempDict["Father's Name"]= fatherName
    tempDict["DOB"]=dob
    tempDict["PanNo"]= panNumber
    output.append(tempDict)   
    finalOut=[]
    obj={}
    for key,value in tempDict.items():
        obj={}
        obj['label']=key
        obj['value']=value
        obj["type"]= "text"
        obj["isDMSKey"]= False
        finalOut.append(obj)
    print(finalOut)

    outputData={'output':finalOut, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': data['input']['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)
        

@app.route('/gibots-pyapi/pan',methods=['GET', 'POST'])
def panPrediction():
    
    data=request.json
    
    receivedInput=data['input']['input']
    
    inputList=receivedInput.split("\n")
    panNumber=""
    name=""
    fatherName=""
    dob=""

    for i in range(0,len(inputList)):
        if "PERMANENT ACCOUNT NUMBER" in inputList[i] or "Permanent Account Number" in inputList[i]:
            panNumber=inputList[i+1]
        if "NAME" in inputList[i] or "Name" in inputList[i]:
            if "FATHER" in inputList[i]:
                fatherName=inputList[i+1]+" "+inputList[i+2]
            elif "Father" in inputList[i]:
                fatherName=inputList[i+1]
            else:
                name=inputList[i+1]
        if "DATE OF BIRTH" in inputList[i] or "Date of Birth" in inputList[i]:
            dob=inputList[i+1]
            if dob[0:1].isdigit():
                continue
            else:
                dob=inputList[i+3]

    for i in inputList:
        try:
            i.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            inputList.remove(i)

    print(inputList)

    if name=="":
        for i in range(0,len(inputList)):
            if "INCOME TAX DEPARTMENT" in inputList[i]:
                name=inputList[i+1]
                fatherName=inputList[i+2]
                dob=inputList[i+3]
                
            if "GOVT. OF INDIA" in inputList[i]:
                if "INCOME TAX DEPARTMENT" in inputList[i]:
                
                    fatherName=inputList[i+2]
                    dob=inputList[i+3]
                else:
                    if name!='GOVT. OF INDIA':
                        fatherName=inputList[i+1]
                        dob=inputList[i+2]
                    else:
                            name=inputList[i+1]
                            fatherName=inputList[i+2]
                            dob=inputList[i+3]
                if fatherName[0:1].isdigit():
                    fatherName=inputList[i-1]
                    dob=inputList[i+1]

    print(panNumber +"\n"+ name + "\n"+ fatherName + "\n" + dob)
    output=[]
    tempDict={}
    tempDict["Name"]=name
    tempDict["Father's Name"]= fatherName
    tempDict["DOB"]=dob
    tempDict["PanNo"]= panNumber
    output.append(tempDict)   
    finalOut=[]
    obj={}
    for key,value in tempDict.items():
        obj={}
        obj['label']=key
        obj['value']=value
        obj["type"]= "text"
        obj["isDMSKey"]= False
        finalOut.append(obj)
    print(finalOut)
    outputData={'output':finalOut, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': data['input']['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)
#1
@app.route('/gibots-pyapi/getToken1',methods=['GET', 'POST'])
def get_auth_token1():
    inputData=request.json
    user=inputData['user']
    password=inputData['password']
    def generate_auth_token(user,password,id=100,expiration = 86400):
        myclient = pymongo.MongoClient(config['dbConnection'])
        db = myclient[config['db']]
        for y in db.get_collection("userinfo").find({},{"user": user, "password": password }):
            if y['user']==user and y['password']==password:
                s = Serializer(config['SECRET_KEY'], expires_in = expiration)
                return s.dumps({ 'id': id })
        return None

    token = generate_auth_token(user,password)
    print (token)
    if token==None:
        return json.dumps({'token':"", 'status':400 , 'info':'username or password is invalid'})
    else:
        return json.dumps({ 'token': token.decode('ascii'), 'status':200 })

@app.route('/gibots-pyapi/ocr1',methods=['GET', 'POST'])
def OCReader1():

    from PIL import Image
    import pytesseract
    import pandas as pd
    import io
    import argparse
    import cv2
    import os
    import glob
    import numpy as np
    from pytesseract import Output
    import json
    import re
    from datetime import datetime

    inputData=request.json
    print(request.headers)
    try:
        token=request.headers['authorization']
    except:
        return json.dumps({'status':400 , 'info':'Please send authorization token'})
    try:
        img_data=inputData['image']
    except:
        return json.dumps({'status':400 , 'info':'Please send image base64 string'})
    img_data=str.encode(img_data)

    s = Serializer(config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return json.dumps({'status':400 , 'info':'Valid token, but expired'})
    except BadSignature:
        return json.dumps({'status':400 , 'info':'Invalid token'})

    # load the image as a PIL/Pillow image, apply OCR, and then delete
    # the temporary file

    #langs = ['5x5_Dots_FT_500', 'dotOCRDData1', 'Dotrice_FT_500', 'DotMatrix_FT_500','DisplayDots_FT_500', 'LCDDot_FT_500', 'Orario_FT_500', 'Transit_FT_500','eng'] 
    langs= ['eng']
    import base64
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    im_name=str(request.remote_addr)+"_"+str(current_time)+".png"
    try:
        with open(im_name, "wb") as fh:
                fh.write(base64.decodebytes(img_data))
    except:
        json.dumps({'status':400 , 'info':'Invalid base64 string. Please send a valid base64 string. You can convert any image to a base64 string using online converters.'})

    print('\n')
    OCR_outputs = set()
    OCR_map = {}
    scores = []
    avg_confidences = []
    for i in range(len(langs)):
        data = pytesseract.image_to_data(Image.open(im_name), lang = langs[i], config='--psm 6 --oem 1',
                output_type=Output.DICT)
        #print("data-------",data)
        textString = pytesseract.image_to_string(Image.open(im_name), lang = langs[i], config='--psm 6 --oem 1')
        text = data['text']
        print(text)
        confidences = []
        numChars = []

        for j in range(len(text)):
            if int(data['conf'][j]) > -1:
                confidences.append(int(data['conf'][j]))
                numChars.append(len(text[j]))	

        if confidences != []:
            avg_confidences.append(np.average(confidences, weights=numChars))
        else:
            avg_confidences.append(0)
        if textString not in OCR_outputs:
            OCR_outputs.add(textString)
            OCR_map[textString] = [i]
            scores.append(avg_confidences[i])
        else:
            scoreSum = avg_confidences[i]
            for j in OCR_map[textString]:
                scoreSum = scoreSum + avg_confidences[j]
            for j in OCR_map[textString]:
                scores[j] = scoreSum
            OCR_map[textString].append(i)
            scores.append(scoreSum)
    best = scores.index(max(scores))
    text = pytesseract.image_to_string(Image.open(im_name), lang = langs[best], config='--psm 6 --oem 1')
    data = pytesseract.image_to_data(Image.open(im_name), lang = langs[best], config='--psm 6 --oem 1',
                output_type=Output.DICT)
    cData = []
    for j in range(len(data['text'])):
            if int(data['conf'][j]) > -1:
                obj = {
                    "leftX":data['left'][j],
                    "topY":data['top'][j],
                    "rightX":data['left'][j]+data['width'][j],
                    "bottomY":data['top'][j]+data['height'][j],
                    "text":data['text'][j],
                    "confidence":data['conf'][j]
                }

                cData.append(obj)
    strData = json.dumps(data)
    cDataParse = json.dumps(cData)

    f = open(str(request.remote_addr)+"_"+str(current_time)+".txt", "w")
    f.write(text)
    f.write('\n')
    f.write(strData)
    f.write('\n')
    f.write(cDataParse)
    return json.dumps({'text':text, 'CData':cData})


@app.route('/gibots-pyapi/face',methods=['GET','POST'])
def faceDetection():
    import json
    data=request.json
    receivedInput=data['input']
    input=receivedInput['image']
    print(input);
    print(os.path.basename(input))
    #input = request.json['receivedInput']['input']
    #import face_recognition
    import cv2
    from matplotlib import pyplot as plt
    import sys
    image1 = cv2.imread(input)
    rgb1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    font = cv2.FONT_HERSHEY_SIMPLEX
    boxes1 = face_recognition.face_locations(rgb1,model="hog")
    fig, (ax1) = plt.subplots(ncols=1, figsize=(10, 10))

    if len(boxes1) >= 2:

                    encodings1 = face_recognition.face_encodings(rgb1, boxes1)
                    matches = face_recognition.compare_faces(encodings1,encodings1[1],0.625)
                    rgb1=cv2.rectangle (rgb1, (boxes1[0][3],boxes1[0][0]),(boxes1[0][1],boxes1[0][2]),(0,0,255), 4)
                    rgb1=cv2.rectangle (rgb1, (boxes1[1][3],boxes1[1][0]),(boxes1[1][1],boxes1[1][2]),(0,0,255), 4)
                    print (matches[0])
                    if matches[0]:
                                    fig.suptitle('Matched', fontsize=24)
                                    cv2.putText(rgb1, 'Matched', (100,100), font, 2, (0,255,0), 3, cv2.LINE_AA)

                    else:
                                    fig.suptitle('Not Matched', fontsize=24)
                                    cv2.putText(rgb1, 'Not Matched', (100,100), font, 2, (255,0,0), 3, cv2.LINE_AA)

    else:      

                    fig.suptitle('Not enough faces detected', fontsize=24)

                    rgb1 = cv2.rectangle (rgb1, (boxes1[0][3],boxes1[0][0]),(boxes1[0][1],boxes1[0][2]),(0,0,255), 4)

                    cv2.putText(rgb1, 'Not enough faces detected', (100,100), font, 2, (255,0,0), 3, cv2.LINE_AA)

    cv2.imwrite ('/var/www/file-server/rpa/'+"output_"+os.path.basename(input), cv2.cvtColor(rgb1, cv2.COLOR_BGR2RGB))    
    
    print("https://rpa-fs.gibots.com/rpa/"+"output_"+os.path.basename(input))

    outputData={"outputImg":"https://rpa-fs.gibots.com/rpa/"+"output_"+os.path.basename(input),'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)



def vconcat_resize_min (im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(im.shape[0] * w_min / im.shape[1])),interpolation=interpolation)
                      for im in im_list]
    return cv2.vconcat(im_list_resize)



@app.route('/gibots-pyapi/facepassport',methods=['GET','POST'])
def faceDetectionPassport():
        import json
        import face_recognition
        import cv2
        from matplotlib import pyplot as plt
        import sys
        data=request.json
        receivedInput=data['input']
        orignalImage=receivedInput['orignalImage']
        passportImage=receivedInput['image']
        print("orignalImage"+orignalImage);
        print("passportImage"+passportImage);
        print(os.path.basename(orignalImage))

        font = cv2.FONT_HERSHEY_SIMPLEX
        fig, (ax1) = plt.subplots(ncols=1, figsize=(10, 10))

        image1 = cv2.imread(orignalImage)
        rgb1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

        image2 = cv2.imread(passportImage)
        rgb2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)


        boxes1 = face_recognition.face_locations(rgb1,model="hog")
        encodings1 = face_recognition.face_encodings(rgb1, boxes1)


        boxes2 = face_recognition.face_locations(rgb2,model="hog")
        encodings2 = face_recognition.face_encodings(rgb2, boxes2)

        if len(boxes1) != 0:
                rgb1 = cv2.rectangle (rgb1, (boxes1[0][3],boxes1[0][0]),(boxes1[0][1],boxes1[0][2]),(0,0,255), 4)
        if len(boxes2) != 0:
                rgb2 = cv2.rectangle (rgb2, (boxes2[0][3],boxes2[0][0]),(boxes2[0][1],boxes2[0][2]),(0,0,255), 4)

        vccat = vconcat_resize_min([rgb1, rgb2])

        width = vccat.shape[0]
        font_size = 1
        print (width)
        if width > 400:
                font_size = 2
        if width > 600:
                font_size = 3
        if width > 800:
                font_size = 4

        match_size = 125*font_size/2
        mismatch_size =  195*font_size/2
        passResult = 'true'

        if len(boxes1) != 0 and len(boxes2) != 0:
                matches = face_recognition.compare_faces(encodings1,encodings2[0],0.525)
                print (matches[0])
                if matches[0]:
                                fig.suptitle('Matched', fontsize=24)
                                cv2.putText(vccat, 'Matched', (int(vccat.shape[1]/2-match_size), int(vccat.shape[0]/2-150)), font, font_size, (0,255,0), font_size, cv2.LINE_AA)
                                passResult = 'true'
                else:
                        fig.suptitle('Not Matched', fontsize=24)
                        cv2.putText(vccat, 'Not Matched',  (int(vccat.shape[1]/2-mismatch_size),int(vccat.shape[0]/2-150)), font, font_size, (255,0,0), font_size, cv2.LINE_AA)
                        passResult = 'false'
        else:
                fig.suptitle('Not enough faces detected', fontsize=24)
                cv2.putText(rgb1, 'Not enough faces detected',  (int(vccat.shape[1]/2-300),int(vccat.shape[0]/2-150)), font, font_size, (255,0,0), font_size, cv2.LINE_AA)
                passResult = 'false'
        cv2.imwrite ('/var/www/file-server/rpa/'+"outputpass_"+os.path.basename(orignalImage), cv2.cvtColor(vccat, cv2.COLOR_BGR2RGB))
        #print('/var/www/file-server/rpa/'+"output_"+os.path.basename(input));
        ax1.imshow(vccat)
        plt.show()

        outputData={"outputImg":"https://rpa-fs.gibots.com/rpa/"+"outputpass_"+os.path.basename(orignalImage),"passResult":passResult,'statusCode': '200'};print(outputData)

        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
        print(response)
        return json.dumps(request.json)






def getDate(data):
    from datetime import date
    r = date(int(data[0]),int(data[1]),int(data[2]))
    return r

@app.route('/gibots-pyapi/datecompare',methods=['GET','POST'])
def dateCompare():
    import json
    import re
    from datetime import date
    import datetime
    data = request.json
    receivedInput = data['input']
    today = str(date.today())
    splitDate = today.split('-')
    b = getDate(splitDate)
    a = receivedInput['billDate']
    threshHold = receivedInput['threshHold']
    a = re.sub("[\s-]", "", a)
    print(a)
    dd = a[0:2]
    mm = a[2:4]
    yy = a[4:8]
    d = getDate([yy, mm, dd])
    c = (b-d).days
    valid = 'true'
    if c >= int(threshHold):
        valid = 'false'
    else:
        valid = 'true'
    outputData = {"valid": valid, "days": c, 'statusCode': '200'}
    print(outputData)
    taskData = {'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'],
                'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId']}
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request(
        "POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite", verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)


@app.route('/gibots-pyapi/blink',methods=['GET', 'POST'])
def blinking():
    data=request.json
    print(data)
    receivedInput=data['input']
    print(receivedInput['videoPath'])
    cap = cv2.VideoCapture(receivedInput['videoPath'])
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")

    EYE_AR_THRESH = 0.20
    EYE_AR_CONSEC_FRAMES = 2

    MOUTH_AR_THRESH = 1.05
    MOUTH_AR_CONSEC_FRAMES = 3


    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0
    MCOUNTER = 0
    MTOTAL = 0


    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")


    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    (imStart, imEnd) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]



    i=0
    while(cap.isOpened()):
    # Capture frame-by-frame
        ret, frame = cap.read()
        if i==2:
            cv2.imwrite('/var/www/'+str(i)+'.jpg',frame)
            i+=1
        if ret != True:
            print("Exiting...")
            break
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0) 
        for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                mouth = shape[mStart:mEnd]
                iMouth = shape[imStart:imEnd]

                
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                
                oMar = omouth_aspect_ratio(mouth)
                iMar = imouth_aspect_ratio(iMouth)
                
                print( oMar ,iMar)
                
                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0
                
                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                mouthHull = cv2.convexHull(mouth)
                iMouthHull = cv2.convexHull(iMouth)

            
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)
                cv2.drawContours(frame, [mouthHull], -1, (0, 0, 255), 1)
                cv2.drawContours(frame, [iMouthHull], -1, (0, 0, 255), 1)
            
                if ear < EYE_AR_THRESH:
                    COUNTER += 1
                else:
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        TOTAL += 1
                    COUNTER = 0
                    
                if oMar > MOUTH_AR_THRESH:
                    MCOUNTER += 1
                else:
                    if MCOUNTER >= MOUTH_AR_CONSEC_FRAMES:
                        MTOTAL += 1
                    MCOUNTER = 0
                    
                    
                cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                cv2.putText(frame, "Talking: {}".format(MTOTAL), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "I-MAR: {:.2f}".format(iMar), (150, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "O-MAR: {:.2f}".format(oMar), (300, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                print(MTOTAL)

                
    cap.release()

    if TOTAL>5 or MTOTAL>5:
        status=("True")
    else:
        status=("False")

    print(status)
    outputData={'output':status, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)










import re
@app.route('/gibots-pyapi/DubaiResidentCard',methods=['GET', 'POST'])
def residentCard():

    data=request.json
    receivedInput=data['input']['input']
    inputList=receivedInput.split("\n")

                
    for i in range(0,len(inputList)):

        if "Name" in inputList[i] or "Name" in inputList[i]:
            Nme=inputList[i]
            Name=Nme.split(" ")
            Name11=(Name[1:])
            Name1=' '.join(Name11)
            
      

        if "ID Number" in inputList[i] or "ID" in inputList[i]:
            ID=inputList[i+1]
            print("ID",ID)
    nat=[]
    for ii in inputList:
        
        nat.append(ii)
    n=(nat[-2:])
    Nationality=" ".join(n)
  
    if "Nationality:" in Nationality:
        print("inside if ")
        Nationality=Nationality.replace('Nationality:', '')
       

    output=[]
    tempDict={}
    tempDict["Name"]=Name1
    tempDict["ID Number"]= ID
    tempDict["Nationality"]=Nationality

    output.append(tempDict)
    # print(output)
    finalOut=[]
    obj={}
    for key,value in tempDict.items():
        obj={}
        obj['label']=key
        obj['value']=value
        obj["type"]= "text"
        obj["isDMSKey"]= False
        finalOut.append(obj)
    print("FinalOut",finalOut)
   
    outputData={'output':finalOut, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': data['input']['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)

#speechRecog()

@app.route('/gibots-pyapi/speechRecog',methods=['GET', 'POST'])
def speechRecog():
    data=request.json
    receivedInput=data['input']
    print(receivedInput['videoPath'])
    command='ffmpeg -i '+receivedInput['videoPath']+' -strict experimental '+'/var/www/video.mp4'
    subprocess.call([command],shell=True)
    baseName = receivedInput['videoPath'].split('/')
    print(baseName)
    print(len(baseName)) 
    fileName = baseName[len(baseName)-1].split('.')[0]
    print(fileName)
    receivedInput['videoPath'] = '/var/www/video.mp4'
    print(receivedInput['videoPath'])
    #cap = cv2.VideoCapture('/var/www/7073_17-03-2020_1584447657721.mp4')
    cap = cv2.VideoCapture(receivedInput['videoPath'])
    if (cap.isOpened()== False): 
        print("Error opening video stream or file")

    EYE_AR_THRESH = 0.20
    EYE_AR_CONSEC_FRAMES = 2

    MOUTH_AR_THRESH = 1.05
    MOUTH_AR_CONSEC_FRAMES = 3


    # initialize the frame counters and the total number of blinks
    COUNTER = 0
    TOTAL = 0
    MCOUNTER = 0
    MTOTAL = 0


    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")


    # grab the indexes of the facial landmarks for the left and
    # right eye, respectively
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    (imStart, imEnd) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]



    i=0
    snapshotPath=''
    while(cap.isOpened()):
    # Capture frame-by-frame
        i+=1
        ret, frame = cap.read()
        if i==4:
            cv2.imwrite('/var/www/'+fileName+'_'+str(i)+'.png',frame)
            snapshotPath='/var/www/'+fileName+'_'+str(i)+'.png'
            break
        if ret != True:
            print("Exiting...")
            break
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 0) 
        for rect in rects:
                # determine the facial landmarks for the face region, then
                # convert the facial landmark (x, y)-coordinates to a NumPy
                # array
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                mouth = shape[mStart:mEnd]
                iMouth = shape[imStart:imEnd]

                
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)
                
                oMar = omouth_aspect_ratio(mouth)
                iMar = imouth_aspect_ratio(iMouth)
                
                print( oMar ,iMar)
                
                # average the eye aspect ratio together for both eyes
                ear = (leftEAR + rightEAR) / 2.0
                
                # compute the convex hull for the left and right eye, then
                # visualize each of the eyes
                leftEyeHull = cv2.convexHull(leftEye)
                rightEyeHull = cv2.convexHull(rightEye)
                mouthHull = cv2.convexHull(mouth)
                iMouthHull = cv2.convexHull(iMouth)

            
                cv2.drawContours(frame, [leftEyeHull], -1, (0, 0, 255), 1)
                cv2.drawContours(frame, [rightEyeHull], -1, (0, 0, 255), 1)
                cv2.drawContours(frame, [mouthHull], -1, (0, 0, 255), 1)
                cv2.drawContours(frame, [iMouthHull], -1, (0, 0, 255), 1)
            
                if ear < EYE_AR_THRESH:
                    COUNTER += 1
                else:
                    if COUNTER >= EYE_AR_CONSEC_FRAMES:
                        TOTAL += 1
                    COUNTER = 0
                    
                if oMar > MOUTH_AR_THRESH:
                    MCOUNTER += 1
                else:
                    if MCOUNTER >= MOUTH_AR_CONSEC_FRAMES:
                        MTOTAL += 1
                    MCOUNTER = 0
                    
                    
                cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                   
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                cv2.putText(frame, "Talking: {}".format(MTOTAL), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "I-MAR: {:.2f}".format(iMar), (150, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "O-MAR: {:.2f}".format(oMar), (300, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    cap.release()
    if TOTAL>2 or MTOTAL>2:
        status1=("The video is Live as there are "+str(TOTAL) +"Blinks ")
        blinkStatus=("True")
    else:
        status1=("The video is recorded as there are"+str(TOTAL)+"Blinks")
        blinkStatus=("False")

    print(status1)
    video = VideoFileClip(receivedInput['videoPath'])
    audio = video.audio
    audioo=audio.write_audiofile("/var/www/Nishant.wav")
    AUDIO_FILE =  "/var/www/Nishant.wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file
      
        
    try:
        audiospeech=(r.recognize_google(audio))
       
        speech=("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        print(speech)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    
    validationText=receivedInput['text']
    print(validationText)
    Ratio = fuzz.ratio(validationText.lower(),audiospeech.lower())
    received=receivedInput['Threshold']
    receivedThreshold=int(received)
    if Ratio > receivedThreshold:
        status=("True")
    else:
        status=("False")
    print(status)
    print(status1)
    outputData={'output':status,'snapshotPath':snapshotPath,'blinkStatus':blinkStatus,'voiceString':audiospeech.lower(),'statusCode': '200'}
    print(outputData)
    command='sudo rm /var/www/video.mp4'
    subprocess.call([command],shell=True)
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': receivedInput['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print(response)
    return json.dumps(request.json)
@app.route('/gibots-pyapi/imageFile',methods=['GET', 'POST'])
def imageFile():
    data=request.json

    input= data["input"]
    fileName=input["EnterFilePath"]
    receivedInput=input["OutputPath"]
    img1=cv2.imread(fileName)
    img2=cv2.imread(fileName)

#    input= data["EnterFilePath"]
#    receivedInput=data["OutputPath"]
#    img1=cv2.imread(input)
#    img2=cv2.imread(input)
    hsv = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV)
    inputName=input["EnterSystem"]
    millis = int(round(time.time() * 1000))
    name1=str(millis)+".png"
    print(name1)
    millis2 = int(round(time.time() * 1001))
    name2=str(millis2)+".png"
    print(name2)
    if inputName=='Drainage':
        print("drain-------------------")
        light_colour = (115, 125, 125)
        dark_colour = (125, 255, 255)
        mask = cv2.inRange(hsv, light_colour, dark_colour)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        dilate = cv2.dilate(mask, kernel, iterations=3)
        edge = cv2.Canny(dilate, 100,200)
        edgeD = cv2.dilate(edge, kernel, iterations=3)
        img1[dilate == 255] = [0, 0, 255]
        img2[edge == 255] = [255, 0, 0]
     
        cv2.imwrite(receivedInput+name1,img1)  # replaced color with Blue
        cv2.imwrite(receivedInput+name2,img2)# outline around the sewer/drain
    elif inputName=='Sewer':
        light_colour = (160, 125, 125)
        dark_colour = (190, 255, 255)
        mask = cv2.inRange(hsv, light_colour, dark_colour)
        print("sewer------------------------------------")
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        dilate = cv2.dilate(mask, kernel, iterations=3)
        edge = cv2.Canny(dilate, 100,200)
        edgeD = cv2.dilate(edge, kernel, iterations=3)
        img1[dilate == 255] = [0, 255, 0]
        img2[edge == 255] = [255, 0, 0]
        
        cv2.imwrite(receivedInput+name1,img1)  # replaced color with Blue
        cv2.imwrite(receivedInput+name2,img2) # outline around the sewer/drain


    outputData={'outputFilePath1':"https://rpa-fs.gibots.com/rpa/"+name1, 'outputFilePath2':"https://rpa-fs.gibots.com/rpa/"+name2,'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    print(head)
    response = requests.request("POST", "http://ocri.gibots.com/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    print (response.text)
    return json.dumps(request.json)

@app.route('/gibots-pyapi/faceAPI',methods=['GET', 'POST'])
def faceReader():
    inputData=request.json
    print(request.headers)
    try:
    	token=request.headers['authorization']
    except:
        return json.dumps({'status':400 , 'info':'Please send authorization token'})
    try:
        img_data=inputData['image']
    except:
        return json.dumps({'status':400 , 'info':'Please send image base64 string'})
    img_data=str.encode(img_data)

    s = Serializer(config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return json.dumps({'status':400 , 'info':'Valid token, but expired'})
    except BadSignature:
        return json.dumps({'status':400 , 'info':'Invalid token'})

    import base64
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    im_name=str(request.remote_addr)+"_"+str(current_time)+".png"
    try:
    	with open(im_name, "wb") as fh:
    		fh.write(base64.decodebytes(img_data))
    except:
        json.dumps({'status':400 , 'info':'Invalid base64 string. Please send a valid base64 string. You can convert any image to a base64 string using online converters.'})


    image1 = cv2.imread(im_name)
    rgb1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
    font = cv2.FONT_HERSHEY_SIMPLEX
    boxes1 = face_recognition.face_locations(rgb1,model="hog")
    fig, (ax1) = plt.subplots(ncols=1, figsize=(10, 10))

    if len(boxes1) >= 2:

                    encodings1 = face_recognition.face_encodings(rgb1, boxes1)
                    matches = face_recognition.compare_faces(encodings1,encodings1[1],0.625)
                    rgb1=cv2.rectangle (rgb1, (boxes1[0][3],boxes1[0][0]),(boxes1[0][1],boxes1[0][2]),(0,0,255), 4)
                    rgb1=cv2.rectangle (rgb1, (boxes1[1][3],boxes1[1][0]),(boxes1[1][1],boxes1[1][2]),(0,0,255), 4)
                    print (matches[0])
                    if matches[0]:
                                    fig.suptitle('Matched', fontsize=24)
                                    cv2.putText(rgb1, 'Matched', (100,100), font, 2, (0,255,0), 3, cv2.LINE_AA)

                    else:
                                    fig.suptitle('Not Matched', fontsize=24)
                                    cv2.putText(rgb1, 'Not Matched', (100,100), font, 2, (255,0,0), 3, cv2.LINE_AA)

    else:      

                    fig.suptitle('Not enough faces detected', fontsize=24)

                    rgb1 = cv2.rectangle (rgb1, (boxes1[0][3],boxes1[0][0]),(boxes1[0][1],boxes1[0][2]),(0,0,255), 4)

                    cv2.putText(rgb1, 'Not enough faces detected', (100,100), font, 2, (255,0,0), 3, cv2.LINE_AA)

    cv2.imwrite ('/var/www/file-server/rpa/'+"output_"+os.path.basename(input), cv2.cvtColor(rgb1, cv2.COLOR_BGR2RGB))    
    
    print("https://rpa-fs.gibots.com/rpa/"+"output_"+os.path.basename(input))

    outputData={"outputImg":"https://rpa-fs.gibots.com/rpa/"+"output_"+os.path.basename(input),'statusCode': '200'}

    return json.dumps(outputData)

@app.route('/gibots-pyapi/facepassportAPI',methods=['GET','POST'])
def faceDetectionPassportAPI():

    inputData=request.json
    print(request.headers)
    try:
    	token=request.headers['authorization']
    except:
        return json.dumps({'status':400 , 'info':'Please send authorization token'})
    try:
        passportImage=inputData['image']
        originalImage=inputData['originalImage']
    except:
        return json.dumps({'status':400 , 'info':'Please send image base64 string'})
    passportImage=str.encode(passportImage)
    originalImag=str.encode(originalImage)

    s = Serializer(config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return json.dumps({'status':400 , 'info':'Valid token, but expired'})
    except BadSignature:
        return json.dumps({'status':400 , 'info':'Invalid token'})

    import base64
    now = datetime.now()
    current_time = now.strftime("%H%M%S")
    orig=str(request.remote_addr)+"_"+str(current_time)+"originalImage.png"
    try:
    	with open(orig, "wb") as fh:
    		fh.write(base64.decodebytes(originalImage))
    except:
        json.dumps({'status':400 , 'info':'Invalid base64 string. Please send a valid base64 string. You can convert any image to a base64 string using online converters.'})
        
    passport=str(request.remote_addr)+"_"+str(current_time)+"passportImage.png"
    try:
    	with open(passport, "wb") as fh:
    		fh.write(base64.decodebytes(passportImage))
    except:
        json.dumps({'status':400 , 'info':'Invalid base64 string. Please send a valid base64 string. You can convert any image to a base64 string using online converters.'})

    print("orignalImage"+orig);
    print("passportImage"+passport);
    print(os.path.basename(orig))

    font = cv2.FONT_HERSHEY_SIMPLEX
    fig, (ax1) = plt.subplots(ncols=1, figsize=(10, 10))

    image1 = cv2.imread(orig)
    rgb1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

    image2 = cv2.imread(passport)
    rgb2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)


    boxes1 = face_recognition.face_locations(rgb1,model="hog")
    encodings1 = face_recognition.face_encodings(rgb1, boxes1)


    boxes2 = face_recognition.face_locations(rgb2,model="hog")
    encodings2 = face_recognition.face_encodings(rgb2, boxes2)

    if len(boxes1) != 0:
        rgb1 = cv2.rectangle (rgb1, (boxes1[0][3],boxes1[0][0]),(boxes1[0][1],boxes1[0][2]),(0,0,255), 4)
    if len(boxes2) != 0:
        rgb2 = cv2.rectangle (rgb2, (boxes2[0][3],boxes2[0][0]),(boxes2[0][1],boxes2[0][2]),(0,0,255), 4)

    vccat = vconcat_resize_min([rgb1, rgb2])

    width = vccat.shape[0]
    font_size = 1
    print (width)
    if width > 400:
        font_size = 2
    if width > 600:
        font_size = 3
    if width > 800:
        font_size = 4

    match_size = 125*font_size/2
    mismatch_size =  195*font_size/2
    passResult = 'true'

    if len(boxes1) != 0 and len(boxes2) != 0:
        matches = face_recognition.compare_faces(encodings1,encodings2[0],0.525)
        print (matches[0])
        if matches[0]:
            fig.suptitle('Matched', fontsize=24)
            cv2.putText(vccat, 'Matched', (int(vccat.shape[1]/2-match_size), int(vccat.shape[0]/2-150)), font, font_size, (0,255,0), font_size, cv2.LINE_AA)
            passResult = 'true'
        else:
            fig.suptitle('Not Matched', fontsize=24)
            cv2.putText(vccat, 'Not Matched',  (int(vccat.shape[1]/2-mismatch_size),int(vccat.shape[0]/2-150)), font, font_size, (255,0,0), font_size, cv2.LINE_AA)
            passResult = 'false'
    else:
        fig.suptitle('Not enough faces detected', fontsize=24)
        cv2.putText(rgb1, 'Not enough faces detected',  (int(vccat.shape[1]/2-300),int(vccat.shape[0]/2-150)), font, font_size, (255,0,0), font_size, cv2.LINE_AA)
        passResult = 'false'
    cv2.imwrite ('/var/www/file-server/rpa/'+"outputpass_"+os.path.basename(orignalImage), cv2.cvtColor(vccat, cv2.COLOR_BGR2RGB))
    #print('/var/www/file-server/rpa/'+"output_"+os.path.basename(input));
    ax1.imshow(vccat)
    plt.show()

    outputData={"outputImg":"https://rpa-fs.gibots.com/rpa/"+"outputpass_"+os.path.basename(orignalImage),"passResult":passResult,'statusCode': '200'};print(outputData)
    return json.dumps(outputData)

def modified_ed_id(x1,y1,w1,z1,x2,y2,w2,z2):
    wc1 = x1+(y1-x1)/2
    wc2 = x2+(y2-x2)/2
    hc1 = w1+(z1-w1)/2
    hc2 = w2+(z2-w2)/2
    print(wc1,wc2,hc1,hc2)
    dist1 = 1*((wc1-wc2)**2)+0.15*((np.abs((hc1-hc2)**2)))
    print('--------------------------')
    print(dist1)
    return dist1


def distance_calc_id(index,df):
    print(index)
    left,right,top,bottom = df[df['index'] == index][['leftX','rightX','topY','bottomY']].values[0]
    len_ver =  len(str(df[df['index'] == index]['Name'].values[0]))
    print(index,top,bottom,left,right)
    dfa = df[(df['topY'] > bottom-((bottom-top)/4))]
    print(dfa)
    if len(dfa) > 0:
        dfa['dist1'] = None
        dfa['dist1'] = dfa[['leftX','rightX','topY','bottomY']].apply(lambda x: modified_ed_id(x.topY,x.bottomY,x.rightX,x.leftX,top,bottom,right,left),axis=1,result_type="expand")
        print('#####################')
        print(dfa[['Name','dist1']])
        dfa = dfa[((dfa['leftX'] > left - (rightmost-leftmost)/4) & (dfa['rightX'] < right + (rightmost-leftmost)/4)) | ((dfa['leftX'] < left - ((right-left)/4)) & (dfa['rightX'] > right + ((right-left)/4)))]
        print(dfa)
        if len(dfa) > 0:
            dfa.sort_values(['dist1'],inplace=True)
            dfa.reset_index(inplace=True,drop=True)
            if len(str(dfa['Name'].iloc[0])) > 8:
                name = str(dfa['Name'].iloc[0])
                return dfa['index'].iloc[0],name
            else:
                dfa_name = dfa[dfa['bottomY'] < dfa['bottomY'].iloc[0] + ((bottom-top)/2)]
                dfa_name.sort_values(['leftX'],inplace=True)
                print(dfa_name)
                name = ' '.join(list(dfa_name['Name']))
                return dfa['index'].iloc[0],name
        else:
            print('Dead End Encountered!!')
            return None,None
    else:
        print('Dead End Encountered!!')
        return None,None

@app.route('/gibots-pyapi/passportI', methods = ['POST'])
def PassportI():
    print('****************ABC')
    data=request.json
    print('**Hello',data)
    js2=data['input']
    js1=js2['input']

    myclient = pymongo.MongoClient(config['dbConnection'])
    db = myclient[config['db']]
    print("**********************************",js1)
    
    try:
        line_no = []
        for no,sl in enumerate(js1):
            ls = len(sl)
            for i in range(ls):
                line_no.append(no)
            
            
        df = pd.DataFrame()
        for subl in js1:
            tdf = pd.DataFrame(subl)
            df = df.append(tdf)
            
        df['line_no'] = line_no
        df['Name'] = df['Name'].apply(lambda x: str(x).replace('«','<').replace('く','<').replace('>','<'))
        
        df.reset_index(inplace=True,drop=True)
        df['center'] = df['topY'] + ((df['bottomY'] - df['topY'] ) /2.0)
        sdf = df[df['Name'].str.contains('<')]
        deviation = np.mean(sdf['bottomY'] - sdf['topY'])/2.0
        sdf['center'] = sdf['topY'] + ((sdf['bottomY'] - sdf['topY'] ) /2.0)
        sdf.sort_values('topY',inplace=True)
        l1 = sdf[sdf['center'] < (sdf['center'].iloc[0] + deviation)]
        print("No Value found")
        l2 = sdf[~(sdf['center'] < (sdf['center'].iloc[0] + deviation))]
        print("value")
        
        leftmost, rightmost = np.min([np.min(l1['leftX']),np.min(l2['leftX'])]), np.max([np.max(l1['rightX']), np.max(l2['rightX'])])
        adj_pixel = (rightmost - leftmost) / 10

        l1_line = np.min(l1['line_no'])
        l2_line = np.min(l2['line_no'])

        add_l1 = df[(df['line_no'] == l1_line) & (df['rightX'] > leftmost-adj_pixel) & (df['leftX'] < rightmost+adj_pixel)]
        add_l2 = df[(df['line_no'] == l2_line) & (df['rightX'] > leftmost-adj_pixel) & (df['leftX'] < rightmost+adj_pixel)]

        l1 = l1.append(add_l1)
        l2 = l2.append(add_l2)
        l1.drop_duplicates(inplace=True)
        l2.drop_duplicates(inplace=True)

        l1.sort_values('leftX',inplace=True)
        l2.sort_values('leftX',inplace=True)
        cl1="Not Found/ OCR Error"
        cl1 = ''.join(list(l1['Name'])).replace(' ','')
        if len(cl1) > 6:
            if (cl1[:1] == 'P') & (cl1[2:4] == 'IN'):
                cl1 = cl1[:1]+'<'+cl1[2:4]+'D'+cl1[5:]
        cl2="Not Found/ OCR Error"
        cl2 = ''.join(list(l2['Name'])).replace(' ','')
        print("1st_Lines",cl1)
        print("2nd_Lines",cl2)
        surname=''
        Name=''
        cnt=0
        for_name=cl1[5:]
        Type="Not Found/ OCR Error"
        try:
            Type=cl1[0]
        except:
            print("Text is not on corrrect position")
        country_code="Not Found/ OCR Error"
        try:
            country_code=cl1[2:5]  
            print("11111111111111111111111",country_code)
        
        except:
            print("Text is not on corrrect position")

        Surname="Not Found/OCR Error"
        try:
            list1=for_name.split("<<")
            list2=list1[0]
            Surname=list2.replace('<'," ")
        except:
            print("OCR is not corerct")
        Name="Not Found/OCR Issue"
        try:
            list3=list1[1]
            Name=''.join(list3.replace("<"," "))
            Name=re.sub(r'[^a-zA-Z]', " ", Name)
        except:
            print("OCR is not corerct")
        passportNumber="Not Found/OCR Issue"
        Validity='Valid'
        PassportNo='Not Found/OCR Issue'
        try:
            passportNumber=cl2[0:9]
            check_number=cl2[9]
            print('check_number',check_number)
            PassportNo=passportNumber.replace('<'," ")
            passport_no = {}
            passport_no['A'] = 10
            passport_no['B'] = 11
            passport_no['C'] = 12
            passport_no['D'] = 13
            passport_no['E'] = 14
            passport_no['F'] = 15
            passport_no['G'] = 16
            passport_no['H'] = 17
            passport_no['I'] = 18
            passport_no['J'] = 19
            passport_no['K'] = 20
            passport_no['L'] = 21
            passport_no['M'] = 22
            passport_no['N'] = 23
            passport_no['O'] = 24
            passport_no['P'] = 25
            passport_no['Q'] = 26
            passport_no['R'] = 27
            passport_no['S'] = 28
            passport_no['T'] = 29
            passport_no['U'] = 30
            passport_no['V'] = 31
            passport_no['W'] = 32
            passport_no['X'] = 33
            passport_no['Y'] = 34
            passport_no['Z'] = 35
            passport_no['0'] = 0
            passport_no['1'] = 1
            passport_no['2'] = 2
            passport_no['3'] = 3
            passport_no['4'] = 4
            passport_no['5'] = 5
            passport_no['6'] = 6
            passport_no['7'] = 7
            passport_no['8'] = 8
            passport_no['9'] = 9
            passport_no['<'] = 0
            cal_check_number_values = (passport_no[passportNumber[0]]*7) + (passport_no[passportNumber[1]]*3)+(passport_no[passportNumber[2]]*1)+(passport_no[passportNumber[3]]*7)+(passport_no[passportNumber[4]]*3)+(passport_no[passportNumber[5]]*1)+(passport_no[passportNumber[6]]*7)+(passport_no[passportNumber[7]]*3)+(passport_no[passportNumber[8]]*1)
            cal_check_number = cal_check_number_values%10
            print('cal_check_number',cal_check_number)
            if cal_check_number==int(check_number) : 
                Validity = "Valid"
            else:
                Validity = "Not Valid"
            print(Validity)
        except:
            print("Text is not on corrrect position")    
        
        nationality="Not Found/OCR Issue"

        try:
            Nationality=cl2[10:13]
            from mrz.checker.td1 import get_country
            nationality=(get_country(Nationality))
            if nationality == "Arab Emirates":
                nationality="United Arab Emirates"
            elif nationality =="Morocco":
                nationality="Marocaine"
            elif nationality=="India":
                nationality="Indian"
            elif nationality=="Egypt":
                nationality="Egyptian"
        except:

            print("Text is not on corrrect position")
        BirthDate_c="Not Found/OCR Issue"
        try:
            BirthDate=cl2[13:19]

            BirthDate.replace('<'," ")
            BirthDateq=BirthDate[0:2]+'/'+BirthDate[2:4]+'/'+BirthDate[4:6]
            print(BirthDateq)
            Birthdate=BirthDate[0:2]
            if len(Birthdate)>1:
                print("true")
                if "o" in Birthdate:
                    c=Birthdate.replace('o',"0")
                    print(c)
                    if int(c)> 19:
                        Birthdate=("19"+c)
                    elif int(c)<= 19:
                        Birthdate=("20"+c)
                    print(Birthdate)
                elif "O" in Birthdate:
                    c=Birthdate.replace('o',"0")
                    print(c)
                    if int(c)> 19:
                        Birthdate=("19"+c)
                    elif int(c)<= 19:
                        Birthdate=("20"+c)
                    print(Birthdate)
                elif "B" in Birthdate:
                    c=Birthdate.replace('B',"8")
                    print(c)
                    if int(c)> 19:
                        Birthdate=("19"+c)
                    elif int(c)<= 19:
                        Birthdate=("20"+c)
                    print(Birthdate)
                else:
                    c=Birthdate
                    if int(c)> 19:
                        Birthdate=("19"+c)
                    elif int(c)<= 19:
                        Birthdate=("20"+c)
                    print(Birthdate)
            BirthDate_c=BirthDate[4:6]+'/'+BirthDate[2:4]+'/'+Birthdate

            
        except:
            print("Text is not on corrrect position")
        Gender="Not Found/OCR Issue"
        try:
            Gender=cl2[20]
        except:
            print("Text is not on corrrect position")
       
        ExpiryDate='Not Found/OCR Error'
        try:

            Expiry_Date=cl2[21:27]
            Expiry_Date.replace('<'," ")
            l=Expiry_Date.split('-',3)
            print('bbbbbbbbbbbbbbbbbbb',l)
            Expiry=Expiry_Date[0:2]+'/'+Expiry_Date[2:4]+'/'+Expiry_Date[4:6]
            print(Expiry)
            expiryDate=Expiry[0:2]
            if len(expiryDate)>1:
                print("true")
                if "o" in expiryDate: 
                    print("true0000")
                    m=expiryDate.replace('o',"0")
                    print(m)
                    if int(m)> 35:
                        print("19"+m)
                    elif int(m)<= 35:
                        print("20"+m)
                elif "O" in expiryDate:
                    print("false))))")
                    m=expiryDate.replace('O',"0")

                    if int(m)> 35:
                        expiryDate=("19"+m)
                    elif int(m)<= 35:
                        expiryDate=("20"+m)
                elif "B" in expiryDate:
                    m=expiryDate.replace('B',"8")
                    if int(m)> 35:
                        expiryDate=("19"+m)
                    elif int(m)<= 35:
                        expiryDate=("20"+m)

                else:
                    m=expiryDate
                    print("without alphabet")
                    if int(m)>35:
                        expiryDate=("19"+m)
                    elif int(m)<= 35:
                        expiryDate=("20"+m)
            else:
                print("OCR Error")
            ExpiryDate=Expiry_Date[4:6]+'/'+Expiry_Date[2:4]+'/'+expiryDate

            

        except:
            print("Text is not on corrrect position")

    except:
        print("Hellooo***Not Found/ OCR Error")
        date='Not Found/OCR Error'
        cl1='Not Found/OCR Error'
        cl2='Not Found/OCR Error'
        Type='Not Found/OCR Error'
        country_code='Not Found/OCR Error'
        Name='Not Found/OCR Error'
        Surname='Not Found/OCR Error'
        PassportNo='Not Found/OCR Error'
        nationality='Not Found/OCR Error'
        Date='Not Found/OCR Error'
        Gender='Not Found/OCR Error'
        BirthDate_c="Not Found/OCR Error"


    df.reset_index(inplace=True)
    print(df.head())

    def modified_ed(x1,y1,w1,z1,x2,y2,w2,z2):
        wc1 = x1+(y1-x1)/2
        wc2 = x2+(y2-x2)/2
        hc1 = w1+(z1-w1)/2
        hc2 = w2+(z2-w2)/2
        print(wc1,wc2,hc1,hc2)
        dist1 = 1*((wc1-wc2)**2)+(np.abs((hc1-hc2)**1))
        print('--------------------------')
        print(dist1)
        return dist1


    def distance_calc(index,df):
        print(index)
        left,right,top,bottom = df[df['index'] == index][['leftX','rightX','topY','bottomY']].values[0]
        len_ver =  len(str(df[df['index'] == index]['Name'].values[0]))
        print(index,top,bottom,left,right)
        dfa = df[(df['topY'] > bottom-((bottom-top)/4))]
        print(dfa)
        if len(dfa) > 0:
            dfa['dist1'] = None
            dfa['dist1'] = dfa[['leftX','rightX','topY','bottomY']].apply(lambda x: modified_ed(x.topY,x.bottomY,x.rightX,x.leftX,top,bottom,right,left),axis=1,result_type="expand")
            print('#####################')
            print(dfa[['Name','dist1']])
            dfa = dfa[((dfa['leftX'] > left - (rightmost-leftmost)/4) & (dfa['rightX'] < right + (rightmost-leftmost)/4)) | ((dfa['leftX'] < left - ((right-left)/4)) & (dfa['rightX'] > right + ((right-left)/4)))]
            print(dfa)
            if len(dfa) > 0:
                dfa.sort_values(['dist1'],inplace=True)
                dfa.reset_index(inplace=True,drop=True)
                if len(str(dfa['Name'].iloc[0])) > 8:
                    name = str(dfa['Name'].iloc[0])
                    return dfa['index'].iloc[0],name
                else:
                    dfa_name = dfa[dfa['bottomY'] < dfa['bottomY'].iloc[0] + ((bottom-top)/2)]
                    dfa_name.sort_values(['leftX'],inplace=True)
                    print(dfa_name)
                    name = ' '.join(list(dfa_name['Name']))
                    return dfa['index'].iloc[0],name
            else:
                print('Dead End Encountered!!')
                return None,None
        else:
            print('Dead End Encountered!!')
            return None,None

    fuzz_candidates = ' '.join(list(df['Name'])).replace('  ','').split(' ')

    fuzz_place = []
    fuzz_issue = []
    fuzz_date = []
    fuzz_issuing = []
    fuzz_authority = []
    fuzz_occupation = []
    for i in fuzz_candidates:
        Ratio = fuzz.ratio('place',i.lower())
        if Ratio > 75:
            fuzz_place.append(i)
        Ratio = fuzz.ratio('issue',i.lower())
        if Ratio > 75:
            fuzz_issue.append(i)
        Ratio = fuzz.ratio('date',i.lower())
        if Ratio > 70:
            fuzz_date.append(i)
        Ratio = fuzz.ratio('issuing',i.lower())
        if Ratio > 70:
            fuzz_issuing.append(i)
        Ratio = fuzz.ratio('authority',i.lower())
        if Ratio >= 70:
            fuzz_authority.append(i)
        Ratio = fuzz.ratio('occupation',i.lower())
        if Ratio > 80:
            fuzz_occupation.append(i)
    import re
    str_place = 'Place'
    str_issue = ['issue']
    str_date = 'Date'
    str_issuing = 'Issuing'
    str_authority = 'Authority'
    str_occupation = 'Occupation'

    if len(fuzz_place)>0:
        str_place = '|'.join(list(dict.fromkeys(fuzz_place)))
    if len(fuzz_issue)>0:
        str_issue = fuzz_issue
    if len(fuzz_date)>0:
        str_date = '|'.join(list(dict.fromkeys(fuzz_date)))
    if len(fuzz_issuing)>0:
        str_issuing = '|'.join(list(dict.fromkeys(fuzz_issuing)))
    if len(fuzz_authority)>0:
        str_authority = '|'.join(list(dict.fromkeys(fuzz_authority)))
    if len(fuzz_occupation)>0:
        str_occupation = '|'.join(list(dict.fromkeys(fuzz_occupation)))


    iadf = df[(df['Name'].str.contains(str_issuing))]
    if len(iadf) > 0:
        ia_index = iadf['index'].iloc[0]
        Issuing_Authority = distance_calc(ia_index,df)[1]
    else:
        Issuing_Authority = 'Not Found'
        
    audf = df[(df['Name'].str.contains(str_authority))]
    if (len(audf) > 0) & (Issuing_Authority == 'Not Found'):
        au_index = audf['index'].iloc[0]
        Issuing_Authority = distance_calc(au_index,df)[1]
    # else:
    #     Issuing_Authority = 'Not Found'
        
    occdf = df[(df['Name'].str.contains(str_occupation))]
    if len(occdf) > 0:
        occ_index = occdf['index'].iloc[0]
        Occupation = distance_calc(occ_index,df)[1]
    else:
        Occupation = 'Not Found'
        
    placedf = df[(df['Name'].str.contains(str_place))]
    if len(placedf) >= 2:
        place_birth_index = placedf['index'].iloc[0]
        place_issue_index = placedf['index'].iloc[1]
        
        birthplace = distance_calc(place_birth_index,df)[1]
        issueplace = distance_calc(place_issue_index,df)[1]
        
    elif len(placedf) == 1:
        place_birth_index = placedf['index'].iloc[0]
        birthplace = distance_calc(place_birth_index,df)[1]
        issueplace = "Not Found"

    else:
        issueplace = "Not Found"
        birthplace = "Not Found"
    issuedatedf = df[(df['Name'].str.contains(str_date))]
    issuedate="Not Found/OCR Error"


    def modified_ed_id(x1,y1,w1,z1,x2,y2,w2,z2):
        wc1 = x1+(y1-x1)/2
        wc2 = x2+(y2-x2)/2
        hc1 = w1+(z1-w1)/2
        hc2 = w2+(z2-w2)/2
        print(wc1,wc2,hc1,hc2)
        dist1 = 1*((wc1-wc2)**2)+0.15*((np.abs((hc1-hc2)**2)))
        print('--------------------------')
        print(dist1)
        return dist1


    def distance_calc_id(index,df):
        print(index)
        left,right,top,bottom = df[df['index'] == index][['leftX','rightX','topY','bottomY']].values[0]
        len_ver =  len(str(df[df['index'] == index]['Name'].values[0]))
        print(index,top,bottom,left,right)
        dfa = df[(df['topY'] > bottom-((bottom-top)/4))]
        print(dfa)
        if len(dfa) > 0:
            dfa['dist1'] = None
            dfa['dist1'] = dfa[['leftX','rightX','topY','bottomY']].apply(lambda x: modified_ed_id(x.topY,x.bottomY,x.rightX,x.leftX,top,bottom,right,left),axis=1,result_type="expand")
            print('#####################')
            print(dfa[['Name','dist1']])
            dfa = dfa[((dfa['leftX'] > left - (rightmost-leftmost)/4) & (dfa['rightX'] < right + (rightmost-leftmost)/4)) | ((dfa['leftX'] < left - ((right-left)/4)) & (dfa['rightX'] > right + ((right-left)/4)))]
            print(dfa)
            if len(dfa) > 0:
                dfa.sort_values(['dist1'],inplace=True)
                dfa.reset_index(inplace=True,drop=True)
                if len(str(dfa['Name'].iloc[0])) > 8:
                    name = str(dfa['Name'].iloc[0])
                    return dfa['index'].iloc[0],name
                else:
                    dfa_name = dfa[dfa['bottomY'] < dfa['bottomY'].iloc[0] + ((bottom-top)/2)]
                    dfa_name.sort_values(['leftX'],inplace=True)
                    print(dfa_name)
                    name = ' '.join(list(dfa_name['Name']))
                    return dfa['index'].iloc[0],name
            else:
                print('Dead End Encountered!!')
                return None,None
        else:
            print('Dead End Encountered!!')
            return None,None
    
    












    def count_digits(s):
        digits = sum(c.isdigit() for c in str(s))
        return digits

    for i in range(len(issuedatedf)):
        curretindex = issuedatedf['index'].iloc[i]
        search_text = ' '.join(list(df['Name'].iloc[curretindex:curretindex+3])).lower().replace(' ','')
        search_text2 = ' '.join(list(df['Name'].iloc[curretindex+1:curretindex+3])).lower().replace(' ','')
        
        if len(re.findall('[A-Za-z0-9]',search_text)) > 12:
            search_text = ' '.join(list(df['Name'].iloc[curretindex:curretindex+2])).lower().replace(' ','')
            search_text2 = ' '.join(list(df['Name'].iloc[curretindex+1:curretindex+2])).lower().replace(' ','')
            
        if len(re.findall('[A-Za-z0-9]',search_text)) > 12:
            search_text = ' '.join(list(df['Name'].iloc[curretindex:curretindex+1])).lower().replace(' ','')
            search_text2 = ' '.join(list(df['Name'].iloc[curretindex+1:curretindex+1])).lower().replace(' ','')
        print(curretindex)
        print(search_text)
        for issue_var in str_issue:
            if str(issue_var).lower() in str(search_text).lower():
                if 'date' not in search_text2:
                    issuedate = distance_calc_id(curretindex,df)[1]
                    print('issue date',issuedate)
                    fissuedate = issuedate.split(' ')[0]
                    j = 1
                    if len(issuedate)>6:
                        while (count_digits(fissuedate) < 5) and (j <= len(issuedate.split(' '))-1):
                            print('enetered')
                            fissuedate = fissuedate+' '+issuedate.split(' ')[j]
                            j+=1
                        issuedate = fissuedate
                        print(issuedate)
                        break
                    else:
                        issuedate = issuedate
                        break
                
        if issuedate != 'Not Found/OCR Error':
            break
    print("***********##********IssueDate*************##***",issuedate)
            
    birthplace = ' '.join([''.join(x for x in s if x.isalpha()) for s in birthplace.split(' ')]).strip()
   
    import re

    if len(re.findall('[A-Za-z0-9]',birthplace)) == 0:
        birthplace = ''
    if len(re.findall('[A-Za-z0-9]',issueplace)) == 0:
        issueplace = ''
    # if len(re.findall('[A-Za-z0-9]',Issuing_Authority)) == 0:
    #     Issuing_Authority = ''
    if len(re.findall('[A-Za-z0-9]',issuedate)) >= 12:
        issuedate = ''
    print("******123*************IssueDate*******123*********",issuedate)
    
    if issueplace=="Not Found" and ((country_code == "ARE") or (country_code =="PHL")):
        issueplace="Not Applicable"
    issueplace=re.sub(r'[^a-zA-Z]', " ", issueplace)

    from googletrans import Translator
    import time
    arabic_name='Not Found'
    arabic_place='Not Found'
    arabic_ia="Not Found"
    arabic_occ="Not Found"
    arebic_gender="Not Found"
    arabic_nationality="Not Found"
   
  
    #country_code=''

    if (country_code == 'ARE') or (country_code == 'JOR') or (country_code == 'EGY') or (country_code == 'MAR'):
        def modified_ed_araebic(x1,y1,w1,z1,x2,y2,w2,z2):
            wc1 = x1+(y1-x1)/2
            wc2 = x2+(y2-x2)/2
            hc1 = w1+(z1-w1)/2
            hc2 = w2+(z2-w2)/2
            print(wc1,wc2,hc1,hc2)
            dist1 = ((wc1-wc2)**2)+((hc1-hc2)**2)
            print('--------------------------')
            print(dist1)
            return dist1


        def distance_calc_arabic(index,df):
            print(index)
            left,right,top,bottom = df[df['index'] == index][['leftX','rightX','topY','bottomY']].values[0]
            print(index,top,bottom,left,right)
            dfa = df[(df['topY'] > bottom-((bottom-top)/2))]
            print(dfa)
            if len(dfa) > 0:
                dfa['dist1'] = None
                dfa['dist1'] = dfa[['leftX','rightX','topY','bottomY']].apply(lambda x: modified_ed_araebic(x.topY,x.bottomY,x.rightX,x.leftX,top,bottom,right,left),axis=1,result_type="expand")
                print(dfa)
                dfa.sort_values(['dist1'],inplace=True)
                dfa.reset_index(inplace=True,drop=True)
                if len(str(dfa['Name'].iloc[0])) > 4 :
                    name = str(dfa['Name'].iloc[0])
                    return dfa['index'].iloc[0],name
                else:
                    dfa_name = dfa[dfa['bottomY'] < dfa['bottomY'].iloc[0] + ((bottom-top)/2)]
                    dfa_name.sort_values(['leftX'],inplace=True)
                    print(dfa_name)
                    name = ' '.join(list(dfa_name['Name']))
                    return dfa['index'].iloc[0],name


        arabic_gender_dict = {'M':'ذكر',"F":'أنثى'}
        # print(arabic_name,arebic_gender,arabic_nationality,arabic_name,arabic_place,arabic_ia,arabic_occ)
        if (Gender == 'M') or (Gender == 'F'):
            arebic_gender = arabic_gender_dict[Gender]
        else:
            arebic_gender = 'OCR Issue'
        
        if country_code == 'ARE':
            arabic_nationality = 'الإمارات العربية المتحدة'
        if country_code == 'JOR':
            arabic_nationality = ''
        if country_code == 'MAR':
            arabic_nationality = ''
        if country_code == 'EGY':
            arabic_nationality = 'مصري' 
        
        
        translator = Translator()

        arabic_name = ''
        arabic_place = ''
        arabic_ia = ''
        arabic_occ = ''

        are_namedf = df[(df['Name'].str.contains('الاسم'))]
        if len(are_namedf) > 0:
            arabic_name_index = are_namedf['index'].iloc[0]
            arabic_name = distance_calc_arabic(arabic_name_index,df)[1]
        else:
            arabic_name = ''

        are_placedf = df[(df['Name'].str.contains('محل المیلاد'))]
        if len(are_placedf) > 0:
            arabic_place_index = are_placedf['index'].iloc[0]
            arabic_place = distance_calc_arabic(arabic_place_index,df)[1]
    #     else:
    #         if 'not ' in birthplace.lower():
    #             arabic_place = ''
    #         else:
    #             try:
    #                 arabic_place = translator.translate(birthplace,dest='ar').text
    #             except Exception as e:
    #                 print(e)
    #                 print('Waiting for API call !!')
    #                 time.sleep(3)
    #                 try:
    #                     arabic_place = translator.translate(birthplace,dest='ar').text
    #                 except:
    #                     pass
        
        if country_code != 'EGY':
            are_iadf = df[(df['Name'].str.contains('إصدار'))]
            if len(are_iadf) > 0:
                print('path right taken!!')
                arabic_ia_index = are_iadf['index'].iloc[0]
                arabic_ia = distance_calc_arabic(arabic_ia_index,df)[1]
    #         else:
    #             if 'not ' in Issuing_Authority.lower():
    #                 arabic_ia = ''
    #             else:
    #                 try:
    #                     arabic_ia = translator.translate(Issuing_Authority,dest='ar').text
    #                 except Exception as e:
    #                     print(e)
    #                     print('Waiting for API call !!')
    #                     time.sleep(3)
    #                     try:
    #                         arabic_ia = translator.translate(Issuing_Authority,dest='ar').text
    #                     except:
    #                         pass
        
    #     are_occdf = df[(df['Name'].str.contains('احتلال'))]
    #     if len(are_occdf) > 0:
    #         arabic_occ_index = are_occdf['index'].iloc[0]
    #         arabic_occ = distance_calc_arabic(arabic_occ_index,df)[1]
    #     else:
    #         if 'not ' in Occupation.lower():
    #             arabic_occ = ''
    #         else:
    #             try:
    #                 arabic_occ = translator.translate(Occupation,dest='ar').text
    #             except Exception as e:
    #                 print(e)
    #                 print('Waiting for API call !!')
    #                 time.sleep(3)
    #                 try:
    #                     arabic_occ = translator.translate(Occupation,dest='ar').text
    #                 except:
    #                     pass
                    
    #     print(arabic_name,arebic_gender,arabic_nationality,arabic_name,arabic_place,arabic_ia,arabic_occ)
        # print('Name ',arabic_name)
        # print('Gender ',arebic_gender)
        # print('Nationality ',arabic_nationality)
        # print('place ',arabic_place)
        # print('IA ',arabic_ia)
    import re

    if len(re.findall('[A-Za-z0-9]',birthplace)) == 0:
        birthplace = ''
    if len(re.findall('[A-Za-z0-9]',issueplace)) == 0:
        issueplace = ''
    if len(re.findall('[A-Za-z0-9]',Issuing_Authority)) == 0:
        Issuing_Authority = ''
    if len(re.findall('[A-Za-z0-9]',issuedate)) >= 12:
        issuedate = ''
    arabic_ia=re.sub(r'[a-zA-Z0-9]', " ",arabic_ia )
    arabic_name=re.sub(r'[a-zA-Z0-9]', " ",arabic_name )
    print("*******************IssueDate****************",issuedate)
    # issuedate=re.sub(r'[^0-9a-zA-Z]',' ', issuedate)
#   print('Occ ',arabic_occ)
    arabic_ia=re.sub(r'[a-zA-Z0-9]', " ",arabic_ia )
    arabic_name=re.sub(r'[a-zA-Z0-9]', " ",arabic_name )
    Issuing_Authority=re.sub(r'[^a-zA-Z0-9]',' ', Issuing_Authority)
    birthplace=re.sub(r'[^a-zA-Z]',' ', birthplace)
    issuedate=re.sub(r'[^0-9a-zA-Z/]',' ', issuedate)
    print('888888888typeee',type(issuedate))
    output=[]
    tempDict={}
    
    if (country_code == 'ARE') or (country_code == 'EGY') or (country_code=='MAR'):
        tempDict["Type"]= Type
        tempDict["Country Code"]=country_code
        tempDict["Passport No"]=PassportNo
        tempDict["Surname"]= Surname
        tempDict["Given Name"]=Name
        tempDict["Name (Arabic)"]=arabic_name
        tempDict["Nationality"]= nationality
        tempDict["Nationality (Arabic)"]=arabic_nationality
        tempDict["Gender"]= Gender
        tempDict["Gender (Arabic)"]=arebic_gender
        tempDict["Date of Birth"]=BirthDate_c
        tempDict["Place of Birth"]= birthplace
        tempDict["Place of Birth(Arabic)"]=arabic_place
        tempDict["Date of Issue"]= issuedate
        tempDict["Date of Expiry"]= ExpiryDate
        tempDict["Issuing Authority"]=Issuing_Authority
        tempDict["Issuing Authority (Arabic)"]=arabic_ia
        tempDict["Passport No. Check"]=Validity


    elif (country_code == 'JOR'):
        birth=datetime.strptime(BirthDate_c,'%d/%m/%Y').strftime('%d %b %Y')
        EP=datetime.strptime(ExpiryDate,'%d/%m/%Y').strftime('%d %b %Y')
        #JorDate=datetime.strptime(issuedate, '%d %b  %Y').strftime('%d/%m/%Y')
        tempDict["Type"]= Type
        tempDict["Country Code"]=country_code
        tempDict["Passport No"]=PassportNo
        tempDict["Surname"]= Surname
        tempDict["Given Name"]=Name
        tempDict["Name (Arabic)"]=arabic_name
        tempDict["Nationality"]= nationality
        tempDict["Nationality (Arabic)"]=arabic_nationality
        tempDict["Gender"]= Gender
        tempDict["Gender (Arabic)"]=arebic_gender
        tempDict["Date of Birth"]=birth
        tempDict["Place of Birth"]= birthplace
        tempDict["Place of Birth(Arabic)"]=arabic_place
        tempDict["Date of Issue"]=issuedate
        tempDict["Date of Expiry"]=EP
        tempDict["Issuing Authority"]=Issuing_Authority
        tempDict["Issuing Authority (Arabic)"]=arabic_ia
        tempDict["Passport No. Check"]=Validity
       
       


    elif (country_code == 'PHL'):
        birthD=datetime.strptime(BirthDate_c,'%d/%m/%Y').strftime('%d %b %Y')
        EPD=datetime.strptime(ExpiryDate,'%d/%m/%Y').strftime('%d %b %Y')

       # Date=datetime.strptime(issuedate, '%d %b  %Y').strftime('%d/%m/%Y')
        tempDict["Type"]= Type
        tempDict["Country Code"]=country_code
        tempDict["Passport No"]=PassportNo
        tempDict["Surname"]= Surname
        tempDict["Given Name"]=Name
        tempDict["Nationality"]= nationality
        tempDict["Gender"]= Gender
        tempDict["Date of Birth"]=birthD
        tempDict["Place of Birth"]= birthplace
        tempDict["Issuing Authority"]=Issuing_Authority
        tempDict["Date of Issue"]= issuedate
        tempDict["Date of Expiry"]= EPD
        tempDict["Passport No. Check"]=Validity
    else:
        tempDict["Type"]= Type
        tempDict["Country Code"]=country_code
        tempDict["Passport No"]=PassportNo
        tempDict["Surname"]= Surname
        tempDict["Given Name"]=Name
        tempDict["Nationality"]= nationality
        tempDict["Gender"]= Gender
        tempDict["Date of Birth"]=BirthDate_c
        tempDict["Place of Birth"]= birthplace
        tempDict["Place of Issue"]= issueplace
        tempDict["Date of Issue"]= issuedate
        tempDict["Date of Expiry"]= ExpiryDate
        tempDict["Passport No. Check"]=Validity

    print("FINAL OUT will be printed_----0-------")
    output.append(tempDict)
    finalOut=[]
    obj={}
    for key,value in tempDict.items():
        obj={}
        obj['label']=key
        obj['value']=value
        obj["type"]= "text"
        obj["isDMSKey"]= False
        finalOut.append(obj)
    #print(finalOut)
    x=db.get_collection('Passport').insert({'PassportType':Type,'Country' : country_code,'Surname' : Surname,'FirstName' : Name,'PassportNo' : PassportNo,'nationality' : nationality,'BirthDate' : BirthDate_c,'Gender' : Gender,'Expiry_Date' : ExpiryDate,
'birthplace' : birthplace,
'issueplace' : issueplace,
'issuedate' :issuedate,'Issuing Authority':Issuing_Authority,'Occupation':Occupation, 'documentType':'Passport', 'Validity':Validity
 })
    print("000000000",request.json,"9999999999999999")
    data=request.json
    js2= data["input"]
    js1 = js2["input"]
    print("******************",data['botId'])

    outputData={'output':finalOut, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': js2['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com:1443/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
   
    print(taskData)
    print(response)
    return json.dumps(request.json)


@app.route('/gibots-pyapi/pdfTable',methods = ['POST'])
def tableExtractor():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            resp={"error_message":"File not found in the request"}
            return(resp)

    file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
    if file.filename == '':
        resp={"error_message":"No file selected"};
        return(resp)
    filename = os.path.splitext(file.filename)[0]+'_'+str(int(round(time.time() * 1000)))+os.path.splitext(file.filename)[1]
    millis = int(round(time.time() * 1000))
    thread = threading.Thread(target=file.save(filename))
    response = muterun_js('table.js', filename)
    b=str(response.stderr)
    b=b.split("\\n")
    for i in range(0,15):
        if 'CLASS' in b[i]:
            class1=b[i].split(' ')[1]
    
    if class1=='31440X':
        for i in range(0,len(b)):
            if b[i]=='ASSEMBLIES ':
                del b[i+1:]
                break
    table1=[]
    table=" "
    for i in range(0,len(b)-1):
        if table=='start':
            table1.append(b[i])
        if b[i]== 'DN Schedule ':
            table='start'
        if b[i+1]== ' ':
            table='end'
    dnDict={}
    dnDict['DN']='Schedule'
    for i in range(0,len(table1)):
        table1[i]=table1[i].split(" ")
        if "." in table1[i][1]:
            dnDict[table1[i][0]]=table1[i][1]+"mm THK"
        else:
            dnDict[table1[i][0]]="SCH."+table1[i][1] 
    
    dnInchDict={"15":"1/2","20":"3/4","25":"1","40":"1 1/2","50":"2","80":"3" ,"100":"4","150":"6","200":"8","250":"10","300":"12","350":"14","400":"16","450":"18","500":"20","600":"24","750":"30","900":"36","1050":"42","1200":"48"}    
    
    pipClassIndex={"11440X":"150", "31440X":"300"}


    table2=[]
    table=" "
    for i in range(0,len(b)-1):
        if table=='start':
            table2.append(b[i])
        if b[i]== 'Code Explanation of characters ':
            table='start'
        if b[i+1]== ' ':
            table='end'
    
    codeDict={}
    codeDict['Code']='Explanation of Characters'
    for i in range(0,len(table2)):
        table2[i]=table2[i].split(" ")
        codeDict[table2[i][0]]=table2[i][1:-1]
    for key in codeDict.keys():
        if key != 'Code':
            codeDict[key]= (" ").join(codeDict[key])


    table3=[]
    RunSizeArray=[]
    table=" "
    for i in range(0,len(b)-1):
        if table=='start':
            table3.append(b[i])
        if b[i]== 'size ':
            table='start'
        if b[i+1]== ' ':
            table='end'
    for i in range(0,len(table3)):
        table3[i]=table3[i].split(" ")
    for j in range (0,len(table3[1])-2):
        sizeDict={}
        sizeDict["Branch Size"]=table3[0][j]
        for i in range(0,len(table3)):
            sizeDict[table3[i][0]]=table3[i][j+1]
        
        RunSizeArray.append(sizeDict)

    table4=[]
    table=" "
    for i in range(0,len(b)-1):
        if table=='start':
            table4.append(b[i])
        if b[i]== '(For full material description see relevant MESC buying description.)':
            table='start'
        if b[i+1]== 'PIPING COMPONENTS':
            table='end'
     
    table7=[]
    table=" "
    for i in range(0,len(b)-1):
        if table=='start':
            table7.append(b[i])
        if b[i]== 'BOLTING ':
            table='start'
        if b[i+1]== 'ASSEMBLIES ':
            table='end'

    pipesTable=[]
    table=" "
    for i in range(0,len(table4)):
        if table4[i]== 'Pipe ':
            table='start'
        if table4[i]== ' ':
            table='end'
        if table=='start':
            pipesTable.append(table4[i])
    pipesArray=[]
    for i in range(2,len(pipesTable)):
        pipesDict={}
        pipesTable[i]=pipesTable[i].split(" ")
        for j in range(0, len(pipesTable[i])):
            if pipesTable[i][j]== 'DN':
                pipesTable[i][1]=pipesTable[i][1:j]
                pipesTable[i][1]=" ".join(pipesTable[i][1])
                pipesTable[i][j+2]=pipesTable[i][j+2:-1]
                pipesTable[i][j+2]=" ".join(pipesTable[i][j+2])
                del pipesTable[i][j+3:-1]
                del pipesTable[i][2:j]
                pipesDict[pipesTable[i][0]]=pipesTable[i][1:-1]
                pipesArray.append(pipesDict)
                break
            elif pipesTable[i][j]== '---':
                break

        

    flangesTable=[]
    table=" "
    for i in range(0,len(table4)):
        if table4[i]== 'Flanges ':
            table='start'
        if table4[i]== ' ':
            table='end'
        if table=='start':
            flangesTable.append(table4[i])

    flangesArray=[]
    for i in range(2,len(flangesTable)):
        flangesDict={}
        flangesTable[i]=flangesTable[i].split(" ")
        for j in range(0, len(flangesTable[i])):
            if flangesTable[i][j]== 'DN':
                flangesTable[i][1]=flangesTable[i][1:j]
                flangesTable[i][1]=" ".join(flangesTable[i][1])
                flangesTable[i][j+2]=flangesTable[i][j+2:-1]
                flangesTable[i][j+2]=" ".join(flangesTable[i][j+2])
                del flangesTable[i][j+3:-1]
                del flangesTable[i][2:j]
                flangesDict[flangesTable[i][0]]=flangesTable[i][1:-1]
                flangesArray.append(flangesDict)
                break
            elif flangesTable[i][j]== '---':
                break

    fittingsTable=[]
    table=" "
    for i in range(0,len(table4)):
        if table4[i]== 'Fittings ':
            table='start'
        if table4[i]== ' ':
            table='end'
        if table=='start':
            fittingsTable.append(table4[i])

    fittingsArray=[]
    for i in range(2,len(fittingsTable)):
        fittingsDict={}
        fittingsTable[i]=fittingsTable[i].split(" ")
        for j in range(0, len(fittingsTable[i])):
            if fittingsTable[i][j]== 'DN':
                fittingsTable[i][1]=fittingsTable[i][1:j]
                fittingsTable[i][1]=" ".join(fittingsTable[i][1])
                fittingsTable[i][j+2]=fittingsTable[i][j+2:-1]
                fittingsTable[i][j+2]=" ".join(fittingsTable[i][j+2])
                del fittingsTable[i][j+3:-1]
                del fittingsTable[i][2:j]
                fittingsDict[fittingsTable[i][0]]=fittingsTable[i][1:-1]
                fittingsArray.append(fittingsDict)
                break
            elif fittingsTable[i][j]== '---':
                break



    reducingFittingsTable=[]
    table=" "
    for i in range(0,len(table4)):
        if table4[i]== 'Reducing fittings ':
            table='start'
        if table4[i]== ' ':
            table='end'
        if table=='start':
            reducingFittingsTable.append(table4[i])

    reducingFittingsArray=[]
    for i in range(2,len(reducingFittingsTable)):
        reducingFittingsDict={}
        reducingFittingsTable[i]=reducingFittingsTable[i].split(" ")
        for j in range(0, len(reducingFittingsTable[i])):
            if reducingFittingsTable[i][j]== 'DN':
                reducingFittingsTable[i][1]=reducingFittingsTable[i][1:j]
                reducingFittingsTable[i][1]=" ".join(reducingFittingsTable[i][1])
                reducingFittingsTable[i][j+2]=reducingFittingsTable[i][j+2:-1]
                reducingFittingsTable[i][j+2]=" ".join(reducingFittingsTable[i][j+2])
                del reducingFittingsTable[i][j+3:-1]
                del reducingFittingsTable[i][2:j]
                reducingFittingsDict[reducingFittingsTable[i][0]]=reducingFittingsTable[i][1:-1]
                reducingFittingsArray.append(reducingFittingsDict)
                break
            elif reducingFittingsTable[i][j]== '---':
                break

    valvesTable=[]
    table=" "
    for i in range(0,len(table4)):
        if table4[i]== 'Valves ':
            table='start'
        if table4[i]== ' ':
            table='end'
        if table=='start':
            valvesTable.append(table4[i])

    valvesArray=[]
    for i in range(2,len(valvesTable)):
        valvesDict={}
        valvesTable[i]=valvesTable[i].split(" ")
        if i % 2 != 0:
            valvesTable[i-1]=valvesTable[i-1][:-1]+valvesTable[i][3:-1]
            for j in range(0, len(valvesTable[i-1])):
                if valvesTable[i-1][j]== 'DN':
                    valvesTable[i-1][1]=valvesTable[i-1][1:j]
                    valvesTable[i-1][1]=" ".join(valvesTable[i-1][1])
                    valvesTable[i-1][j+2]=valvesTable[i-1][j+2:]
                    valvesTable[i-1][j+2]=" ".join(valvesTable[i-1][j+2])
                    del valvesTable[i-1][j+3:-1]
                    del valvesTable[i-1][2:j]
                    valvesDict[valvesTable[i-1][0]]=valvesTable[i-1][1:-1]
                    valvesArray.append(valvesDict)
                    break
                elif valvesTable[i][j]== '---':
                    break

    instrumentsTable=[]
    table=" "
    for i in range(0,len(table4)):
        if table4[i]== 'Instruments ':
            table='start'
        if table4[i]== ' ':
            table='end'
        if table=='start':
            instrumentsTable.append(table4[i])
    instrumentsArray=[]
    for i in range(2,len(instrumentsTable)):
        instrumentsDict={}
        instrumentsTable[i]=instrumentsTable[i].split(" ")
        for j in range(0, len(instrumentsTable[i])):
            if instrumentsTable[i][j]== 'DN':
                if '-' in instrumentsTable[i][j+1]:
                    instrumentsTable[i][1]=instrumentsTable[i][1:j]
                    instrumentsTable[i][1]=" ".join(instrumentsTable[i][1])
                    instrumentsTable[i][j+2]=instrumentsTable[i][j+2:-1]
                    instrumentsTable[i][j+2]=" ".join(instrumentsTable[i][j+2])
                    del instrumentsTable[i][j+3:-1]
                    del instrumentsTable[i][2:j]
                    instrumentsDict[instrumentsTable[i][0]]=instrumentsTable[i][1:-1]
                    instrumentsArray.append(instrumentsDict)
                    break
            elif instrumentsTable[i][j]== '---':
                break

    miscellaneousTable=[]
    table=" "
    for i in range(0,len(table4)):
        if table4[i]== 'Miscellaneous ':
            table='start'
        if table4[i]== ' ':
            table='end'
        if table=='start':
            miscellaneousTable.append(table4[i])

    miscellaneousArray=[]
    for i in range(2,len(miscellaneousTable)):
        miscellaneousDict={}
        miscellaneousTable[i]=miscellaneousTable[i].split(" ")
        if 'GK' in miscellaneousTable[i-1][0]:
            miscellaneousTable[i-1]=miscellaneousTable[i-1][:-1]+miscellaneousTable[i][3:-1]
            for j in range(0, len(miscellaneousTable[i-1])):
                if miscellaneousTable[i-1][j]== 'DN':
                    miscellaneousTable[i-1][1]=miscellaneousTable[i-1][1:j]
                    miscellaneousTable[i-1][1]=" ".join(miscellaneousTable[i-1][1])
                    miscellaneousTable[i-1][j+2]=miscellaneousTable[i-1][j+2:-1]
                    miscellaneousTable[i-1][j+2]=" ".join(miscellaneousTable[i-1][j+2])
                    del miscellaneousTable[i-1][j+3:-1]
                    del miscellaneousTable[i-1][2:j]
                    miscellaneousDict[miscellaneousTable[i-1][0]]=miscellaneousTable[i-1][1:-1]
                    break
                elif miscellaneousTable[i-1][j]== '---':
                    break

        else:
            for j in range(0, len(miscellaneousTable[i-1])):
                print(miscellaneousTable[i-1][j])
                if miscellaneousTable[i-1][j]== 'DN':
                    miscellaneousTable[i-1][1]=miscellaneousTable[i-1][1:j]
                    miscellaneousTable[i-1][1]=" ".join(miscellaneousTable[i-1][1])
                    miscellaneousTable[i-1][j+2]=miscellaneousTable[i-1][j+2:-1]
                    miscellaneousTable[i-1][j+2]=" ".join(miscellaneousTable[i-1][j+2])
                    del miscellaneousTable[i-1][j+3:-1]
                    del miscellaneousTable[i-1][2:j]
                    miscellaneousDict[miscellaneousTable[i-1][0]]=miscellaneousTable[i-1][1:-1]
                    break
                elif miscellaneousTable[i-1][j]== '---':
                    break

        if miscellaneousTable[i-1][0]==" " or miscellaneousTable[i-1][0]=="":
            continue
        else:        
            miscellaneousArray.append(miscellaneousDict)

    bolting1Table=[]
    table=" "
    for i in range(0,len(b)):
        if b[i]== 'Std boltset standard flg ':
            table='start'
        if b[i]== ' ':
            table='end'
        if table=='start':
            bolting1Table.append(b[i])


    bolting1Array=[]
    for i in range(1,len(bolting1Table)):
        bolting1Dict={}
        bolting1Table[i]=bolting1Table[i].split(" ")

        if bolting1Table[i][2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if bolting1Table[i][3]!= '':
                bolting1Table[i][2] = bolting1Table[i][2]+" "+bolting1Table[i][3]
                bolting1Table[i].pop(3)
            else:
                del bolting1Table[i][3:7]

        bolting1Table[i][3] = bolting1Table[i][3]+" "+bolting1Table[i][4]
        bolting1Table[i].pop(4)
        if i==1:
            bolting1Table[1][-3] = bolting1Table[1][-3]+" "+bolting1Table[1][-2]
            bolting1Table[1].pop(-2)
        else:
            bolting1Dict={}
            for j in range(0,len(bolting1Table[1])-1):
                bolting1Dict[bolting1Table[1][j]]=bolting1Table[i][j]
            bolting1Array.append(bolting1Dict)

    bolting2Table=[]
    table=" "
    for i in range(0,len(b)):
        if b[i]== 'Std boltset mrun flg ':
            table='start'
        if b[i]== ' ':
            table='end'
        if table=='start':
            bolting2Table.append(b[i])

    bolting2Array=[]
    for i in range(1,len(bolting2Table)):
        bolting2Dict={}
        bolting2Table[i]=bolting2Table[i].split(" ")

        if bolting2Table[i][2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if bolting2Table[i][3]!= '':
                bolting2Table[i][2] = bolting2Table[i][2]+" "+bolting2Table[i][3]
                bolting2Table[i].pop(3)
            else:
                del bolting2Table[i][3:7]

        bolting2Table[i][3] = bolting2Table[i][3]+" "+bolting2Table[i][4]
        bolting2Table[i].pop(4)
        if i==1:
            bolting2Table[1][-3] = bolting2Table[1][-3]+" "+bolting2Table[1][-2]
            bolting2Table[1].pop(-2)
        else:
            bolting2Dict={}
            for j in range(0,len(bolting2Table[1])-1):
                bolting2Dict[bolting2Table[1][j]]=bolting2Table[i][j]
            bolting2Array.append(bolting2Dict)

    bolting3Table=[]
    table=" "
    for i in range(0,len(b)):
        if b[i]== 'Std boltset orifice flg ':
            table='start'
        if b[i]== ' ':
            table='end'
        if table=='start':
            bolting3Table.append(b[i])

    bolting3Array=[]
    for i in range(1,len(bolting3Table)):
        bolting3Dict={}
        bolting3Table[i]=bolting3Table[i].split(" ")

        if bolting3Table[i][2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if bolting3Table[i][3]!= '':
                bolting3Table[i][2] = bolting3Table[i][2]+" "+bolting3Table[i][3]
                bolting3Table[i].pop(3)
            else:
                del bolting3Table[i][3:7]

        bolting3Table[i][3] = bolting3Table[i][3]+" "+bolting3Table[i][4]
        bolting3Table[i].pop(4)
        if i==1:
            bolting3Table[1][-3] = bolting3Table[1][-3]+" "+bolting3Table[1][-2]
            bolting3Table[1].pop(-2)
        else:
            bolting3Dict={}
            for j in range(0,len(bolting3Table[1])-1):
                bolting3Dict[bolting3Table[1][j]]=bolting3Table[i][j]
            bolting3Array.append(bolting3Dict)

        
    bolting4Table=[]
    table=" "
    for i in range(0,len(b)):
        if b[i]== 'Std boltset blind/spacer ':
            table='start'
        if b[i]== ' ':
            table='end'
        if table=='start':
            bolting4Table.append(b[i])

    bolting4Array=[]
    for i in range(1,len(bolting4Table)):
        bolting4Dict={}
        bolting4Table[i]=bolting4Table[i].split(" ")

        if bolting4Table[i][2] in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if bolting4Table[i][3]!= '':
                bolting4Table[i][2] = bolting4Table[i][2]+" "+bolting4Table[i][3]
                bolting4Table[i].pop(3)
            else:
                del bolting4Table[i][3:7]

        bolting4Table[i][3] = bolting4Table[i][3]+" "+bolting4Table[i][4]
        bolting4Table[i].pop(4)
        if i==1:
            bolting4Table[1][-3] = bolting4Table[1][-3]+" "+bolting4Table[1][-2]
            bolting4Table[1].pop(-2)
        else:
            bolting4Dict={}
            for j in range(0,len(bolting4Table[1])-1):
                bolting4Dict[bolting4Table[1][j]]=bolting4Table[i][j]
            bolting4Array.append(bolting4Dict)


    finalPipe=[]
    for i in pipesArray:
        for k in i.keys():
            for l in range(0,len(i[k])):
                if i[k][l]=='DN':
                    list=(i[k][l+1].split("-"))
            for j in dnDict.keys():
                if j != 'DN':
                    if int(j) >= int(list[0]) and int(j)<= int(list[1]):
                        pipes={}
                        pipes['Class']=class1
                        pipes['Code']=k
                        pipes['Code Desc']=i[k][0]
                        pipes['Size1']=dnInchDict[j]
                        pipes['Size2']='0'
                        pipes['Manu Std']='ASME B36.10'
                        pipes['Material']=i[k][-1]
                        pipes['Rating']=dnDict[j]
                        pipes['Size1unit']='"'
                        pipes['Size2unit']='"'
                        if '/' in pipes['Size1']:
                            if pipes['Size1'][1]!=' ':
                                deciSize=int(pipes['Size1'][0])/int(pipes['Size1'][2])
                            else:
                                deciSize=int(pipes['Size1'][0])+ (int(pipes['Size1'][2])/int(pipes['Size1'][4]))
                        else:
                            deciSize=pipes['Size1']
                        pipes['TotalCode']=class1+k+str(deciSize)+pipes['Size2']
                        pipes['Full Description']=pipes['Code Desc']+';;'+str(deciSize)+pipes['Size1unit']+';;'+pipes['Rating']+';;'+pipes['Material']+';;'+pipes['Manu Std']+';;'+'Class - '+pipes['Class']
                        finalPipe.append(pipes)

    finalFlange=[]
    for i in flangesArray:
        for k in i.keys():
            for l in range(0,len(i[k])):
                if i[k][l]=='DN':
                    list=(i[k][l+1].split("-"))
            for j in dnDict.keys():
                if j != 'DN':
                    if int(j) >= int(list[0]) and int(j)<= int(list[1]):
                        flanges={}
                        flanges['Class']=class1
                        flanges['Code']=k
                        flanges['Code Desc']=i[k][0]
                        flanges['Size1']=dnInchDict[j]
                        if '/' in flanges['Size1']:
                            if flanges['Size1'][1]!=' ':
                                deciSize=int(flanges['Size1'][0])/int(flanges['Size1'][2])
                            else:
                                deciSize=int(flanges['Size1'][0])+ (int(flanges['Size1'][2])/int(flanges['Size1'][4]))
                        else:
                            deciSize=flanges['Size1']
                        flanges['Size2']='0'
                        if flanges['Code Desc']=='Blind flange' or flanges['Code Desc']=='Weldneck flange':
                            if int(deciSize) > 24:
                                flanges['Manu Std']='ASME B16.47 Series A'
                            else:
                                flanges['Manu Std']='ASME B16.5'
                        else:
                            flanges['Manu Std']='ASME B16.48'
                        flanges['Material']=i[k][-1]
                        if class1=='31440X':
                            if 'Welding' in flanges['Code Desc']:
                                flanges['Rating']=pipClassIndex[class1]
                            else:
                                flanges['Rating']=pipClassIndex[class1]+'/'+dnDict[j]
                        else:
                            flanges['Rating']=''
                        flanges['Size1unit']='"'
                        flanges['Size2unit']='"'

                        flanges['TotalCode']=class1+k+str(deciSize)+flanges['Size2']
                        flanges['Full Description']=flanges['Code Desc']+';;'+str(deciSize)+flanges['Size1unit']+';;'+flanges['Rating']+';;'+flanges['Material']+';;'+flanges['Manu Std']+';;'+'Class - '+flanges['Class']
                        finalFlange.append(flanges)

    finalFitting=[]
    for i in fittingsArray:
        for k in i.keys():
            for l in range(0,len(i[k])):
                if i[k][l]=='DN':
                    list=(i[k][l+1].split("-"))
            for j in dnDict.keys():
                if j != 'DN':
                    if int(j) >= int(list[0]) and int(j)<= int(list[1]):
                        fittings={}
                        fittings['Class']=class1
                        fittings['Code']=k
                        fittings['Code Desc']=i[k][0]
                        fittings['Size1']=dnInchDict[j]
                        if fittings['Code']=='TEEB':
                            fittings['Size2']=dnInchDict[j]
                        else:
                            fittings['Size2']='0'
                        fittings['Manu Std']='ASME B16.9'
                        fittings['Material']=i[k][-1]
                        if fittings['Code']=='TEEB':
                            fittings['Rating']=dnDict[j]+'/'+dnDict[j]
                        else:
                            fittings['Rating']=dnDict[j]
                        fittings['Size1unit']='"'
                        fittings['Size2unit']='"'
                        if '/' in fittings['Size1']:
                            if fittings['Size1'][1]!=' ':
                                deciSize=int(fittings['Size1'][0])/int(fittings['Size1'][2])
                            else:
                                deciSize=int(fittings['Size1'][0])+ (int(fittings['Size1'][2])/int(fittings['Size1'][4]))
                        else:
                            deciSize=fittings['Size1']
                        fittings['TotalCode']=class1+k+str(deciSize)+fittings['Size2']
                        if fittings['Code']=='TEEB':
                            fittings['Full Description']=fittings['Code Desc']+';;'+str(deciSize)+fittings['Size1unit']+'x'+str(deciSize)+fittings['Size1unit']+';;'+fittings['Rating']+';;'+fittings['Material']+';;'+fittings['Manu Std']+';;'+'Class - '+fittings['Class']
                        else:
                            fittings['Full Description']=fittings['Code Desc']+';;'+str(deciSize)+fittings['Size1unit']+';;'+fittings['Rating']+';;'+fittings['Material']+';;'+fittings['Manu Std']+';;'+'Class - '+fittings['Class']
                        finalFitting.append(fittings)

        
    finalReducingFitting=[]
    for i in reducingFittingsArray:
        for k in i.keys():
            for l in range(0,len(i[k])):
                if i[k][l]=='DN':
                    list=(i[k][l+1].split("-"))
            for j in dnDict.keys():
                if j != 'DN':
                    if int(j) >= int(list[0]) and int(j)<= int(list[1]):
                        if 'Tee reducing' in i[k][0]:
                            CodeList=[]
                            for key in codeDict.keys():
                                if 'Reducing tee' in codeDict[key]:
                                    CodeList.append(key)
                        elif 'Branch fitting' in i[k][0]:
                            CodeList=[]
                            for key in codeDict.keys():
                                if 'Branch fitting' in codeDict[key]:
                                    CodeList.append(key)
                        elif 'Branch outlet bw' in i[k][0]:
                            CodeList=[]
                            for key in codeDict.keys():
                                if 'Branch outlet BW' in codeDict[key]:
                                    CodeList.append(key)
                        else:
                            CodeList=[]
                        sizeDict={}
                        for runSize in RunSizeArray[0].keys():
                            sizeList=[]
                            if runSize != 'Branch Size':
                                for code in CodeList:
                                    for obj in RunSizeArray:
                                        if obj[runSize]== code:
                                            sizeList.append(obj['Branch Size'])
                            if len(sizeList) >= 1:
                                sizeDict[runSize]=sizeList
        if len(sizeDict)>=1:
            for size in sizeDict:
                for coding in sizeDict[size]:
                    reducingFittings={}
                    reducingFittings['Class']=class1
                    reducingFittings['Code']=k
                    reducingFittings['Code Desc']=i[k][0]
                    reducingFittings['Size1']=dnInchDict[size]
                    reducingFittings['Size2']=dnInchDict[coding]
                    if 'Branch' in reducingFittings['Code Desc']:
                        reducingFittings['Manu Std']='MSS SP 97'
                    else:
                        reducingFittings['Manu Std']='ASME B16.9'
                    reducingFittings['Material']=i[k][-1]
                    reducingFittings['Rating']=dnDict[size]+'/'+dnDict[coding]
                    reducingFittings['Size1unit']='"'
                    reducingFittings['Size2unit']='"'
                    if '/' in reducingFittings['Size1']:
                        if reducingFittings['Size1'][1]!=' ':
                            deciSize1=int(reducingFittings['Size1'][0])/int(reducingFittings['Size1'][2])
                        else:
                            deciSize1=int(reducingFittings['Size1'][0])+ (int(reducingFittings['Size1'][2])/int(reducingFittings['Size1'][4]))
                    else:
                        deciSize1=reducingFittings['Size1']

                    if '/' in reducingFittings['Size2']:
                        if reducingFittings['Size2'][1]!=' ':
                            deciSize2=int(reducingFittings['Size2'][0])/int(reducingFittings['Size2'][2])
                        else:
                            deciSize2=int(reducingFittings['Size2'][0])+ (int(reducingFittings['Size2'][2])/int(reducingFittings['Size2'][4]))
                    else:
                        deciSize2=reducingFittings['Size2']
                    reducingFittings['TotalCode']=class1+k+str(deciSize1)+str(deciSize2)
                    reducingFittings['Full Description']=reducingFittings['Code Desc']+';;'+str(deciSize)+reducingFittings['Size1unit']+'x'+str(deciSize2)+reducingFittings['Size2unit']+';;'+reducingFittings['Rating']+';;'+reducingFittings['Material']+';;'+reducingFittings['Manu Std']+';;'+'Class - '+reducingFittings['Class']
                    finalReducingFitting.append(reducingFittings)           
                       
                        
    finalValve=[]
    for i in valvesArray:
        for k in i.keys():
            for l in range(0,len(i[k])):
                if i[k][l]=='DN':
                    list=(i[k][l+1].split("-"))
            for j in dnDict.keys():
                if j != 'DN':
                    if int(j) >= int(list[0]) and int(j)<= int(list[1]):
                        valves={}
                        valves['Class']=class1
                        valves['Code']=k
                        valves['Code Desc']=i[k][0]
                        valves['Size1']=dnInchDict[j]
                        valves['Size2']='0'
                        valves['Manu Std']=''
                        valves['Material']=i[k][-1]
                        valves['Rating']=dnDict[j]
                        valves['Size1unit']='"'
                        valves['Size2unit']='"'
                        if '/' in valves['Size1']:
                            if valves['Size1'][1]!=' ':
                                deciSize=int(valves['Size1'][0])/int(valves['Size1'][2])
                            else:
                                deciSize=int(valves['Size1'][0])+ (int(valves['Size1'][2])/int(valves['Size1'][4]))
                        else:
                            deciSize=valves['Size1']
                        valves['TotalCode']=class1+k+str(deciSize)+valves['Size2']
                        valves['Full Description']=valves['Code Desc']+';;'+str(deciSize)+valves['Size1unit']+';;'+valves['Rating']+';;'+valves['Material']+';;'+valves['Manu Std']+';;'+'Class - '+valves['Class']
                        finalValve.append(valves)
                        
    finalInstrument=[]
    for i in instrumentsArray:
        for k in i.keys():
            for l in range(0,len(i[k])):
                if i[k][l]=='DN':
                    list=(i[k][l+1].split("-"))
            for j in dnDict.keys():
                if j != 'DN':
                    if int(j) >= int(list[0]) and int(j)<= int(list[1]):
                        instruments={}
                        instruments['Class']=class1
                        instruments['Code']=k
                        instruments['Code Desc']=i[k][0]
                        instruments['Size1']=dnInchDict[j]
                        instruments['Size2']='0'
                        instruments['Manu Std']=''
                        instruments['Material']=i[k][-1]
                        instruments['Rating']=dnDict[j]
                        instruments['Size1unit']='"'
                        instruments['Size2unit']='"'
                        if '/' in instruments['Size1']:
                            if instruments['Size1'][1]!=' ':
                                deciSize=int(instruments['Size1'][0])/int(instruments['Size1'][2])
                            else:
                                deciSize=int(instruments['Size1'][0])+ (int(instruments['Size1'][2])/int(instruments['Size1'][4]))
                        else:
                            deciSize=instruments['Size1']
                        instruments['TotalCode']=class1+k+str(deciSize)+instruments['Size2']
                        instruments['Full Description']=instruments['Code Desc']+';;'+str(deciSize)+instruments['Size1unit']+';;'+instruments['Rating']+';;'+instruments['Material']+';;'+instruments['Manu Std']+';;'+'Class - '+instruments['Class']
                        finalInstrument.append(instruments)
                        
    finalMiscellaneous=[]
    for i in miscellaneousArray:
        for k in i.keys():
            for l in range(0,len(i[k])):
                if i[k][l]=='DN':
                    list=(i[k][l+1].split("-"))
            for j in dnDict.keys():
                if j != 'DN':
                    if int(j) >= int(list[0]) and int(j)<= int(list[1]):
                        miscellaneous={}
                        miscellaneous['Class']=class1
                        miscellaneous['Code']=k
                        miscellaneous['Code Desc']=i[k][0]
                        miscellaneous['Size1']=dnInchDict[j]
                        miscellaneous['Size2']='0'
                        if 'Gasket' in i[k][0]:
                            miscellaneous['Manu Std']='ASME B16.20'
                        else:
                            miscellaneous['Manu Std']=''
                        miscellaneous['Material']=i[k][-1]
                        miscellaneous['Rating']=dnDict[j]
                        miscellaneous['Size1unit']='"'
                        miscellaneous['Size2unit']='"'
                        if '/' in miscellaneous['Size1']:
                            if miscellaneous['Size1'][1]!=' ':
                                deciSize=int(miscellaneous['Size1'][0])/int(miscellaneous['Size1'][2])
                            else:
                                deciSize=int(miscellaneous['Size1'][0])+ (int(miscellaneous['Size1'][2])/int(miscellaneous['Size1'][4]))
                        else:
                            deciSize=miscellaneous['Size1']
                        miscellaneous['TotalCode']=class1+k+str(deciSize)+miscellaneous['Size2']
                        miscellaneous['Full Description']=miscellaneous['Code Desc']+';;'+str(deciSize)+miscellaneous['Size1unit']+';;'+miscellaneous['Rating']+';;'+miscellaneous['Material']+';;'+miscellaneous['Manu Std']+';;'+'Class - '+miscellaneous['Class']
                        finalMiscellaneous.append(miscellaneous)
                        
    finalBolting1=[]
    for i in bolting1Array:
        bolts1={}
        bolts1['Class']=class1
        bolts1['Code']='STBT'
        bolts1['Code Desc']='Stud Bolts with 2 heavy Hex nuts'
        bolts1['Size1']=i['inch']
        bolts1['Size2']=i['x mm'][2:]
        bolts1['Manu Std']='ASME 18.2.1 / 18.2.2'
        for j in pipesArray:
            for k in j.keys():
                for l in range(0,len(j[k])):
                    if j[k][l]=='DN':
                        list=(j[k][l+1].split("-"))
                        if int(list[0]) <= int(i['DN']) and int(list[1]) >= int(i['DN']):
                            bolts1['Material']=j[k][-1]
                            break
            break
        bolts1['Rating']=''
        bolts1['Size1unit']='"'
        bolts1['Size2unit']='mm'
        if '/' in bolts1['Size1']:
            if bolts1['Size1'][1]!=' ':
                deciSize=int(bolts1['Size1'][0])/int(bolts1['Size1'][2])
            else:
                deciSize=int(bolts1['Size1'][0])+ (int(bolts1['Size1'][2])/int(bolts1['Size1'][4]))
        else:
            deciSize=bolts1['Size1']
        bolts1['TotalCode']=class1+bolts1['Code']+str(deciSize)+bolts1['Size2']
        bolts1['Full Description']=bolts1['Code Desc']+';;'+str(deciSize)+bolts1['Size1unit']+';;'+bolts1['Rating']+';;'+bolts1['Material']+';;'+bolts1['Manu Std']+';;'+'Class - '+bolts1['Class']

        finalBolting1.append(bolts1)
        
    finalBolting2=[]
    for i in bolting2Array:
        bolts2={}
        bolts2['Class']=class1
        bolts2['Code']='STBT'
        bolts2['Code Desc']='Stud Bolts with 2 heavy Hex nuts'
        bolts2['Size1']=i['inch']
        bolts2['Size2']=i['x mm'][2:]
        bolts2['Manu Std']='ASME 18.2.1 / 18.2.2'
        for j in pipesArray:
            for k in j.keys():
                for l in range(0,len(j[k])):
                    if j[k][l]=='DN':
                        list=(j[k][l+1].split("-"))
                        if int(list[0]) <= int(i['DN']) and int(list[1]) >= int(i['DN']):
                            bolts2['Material']=j[k][-1]
                            break
            break
        bolts2['Rating']=''
        bolts2['Size1unit']='"'
        bolts2['Size2unit']='mm'
        if '/' in bolts2['Size1']:
            if bolts2['Size1'][1]!=' ':
                deciSize=int(bolts2['Size1'][0])/int(bolts2['Size1'][2])
            else:
                deciSize=int(bolts2['Size1'][0])+ (int(bolts2['Size1'][2])/int(bolts2['Size1'][4]))
        else:
            deciSize=bolts2['Size1']
        bolts2['TotalCode']=class1+bolts2['Code']+str(deciSize)+bolts2['Size2']
        bolts2['Full Description']=bolts2['Code Desc']+';;'+str(deciSize)+bolts2['Size1unit']+';;'+bolts2['Rating']+';;'+bolts2['Material']+';;'+bolts2['Manu Std']+';;'+'Class - '+bolts2['Class']

        finalBolting2.append(bolts2)
        
    finalBolting3=[]
    for i in bolting3Array:
        bolts3={}
        bolts3['Class']=class1
        bolts3['Code']='STBT'
        bolts3['Code Desc']='Stud Bolts with 2 heavy Hex nuts'
        bolts3['Size1']=i['inch']
        bolts3['Size2']=i['x mm'][2:]
        bolts3['Manu Std']='ASME 18.2.1 / 18.2.2'
        for j in pipesArray:
            for k in j.keys():
                for l in range(0,len(j[k])):
                    if j[k][l]=='DN':
                        list=(j[k][l+1].split("-"))
                        if int(list[0]) <= int(i['DN']) and int(list[1]) >= int(i['DN']):
                            bolts3['Material']=j[k][-1]
                            break
            break
        bolts3['Rating']=''
        bolts3['Size1unit']='"'
        bolts3['Size2unit']='mm'
        if '/' in bolts3['Size1']:
            if bolts3['Size1'][1]!=' ':
                deciSize=int(bolts3['Size1'][0])/int(bolts3['Size1'][2])
            else:
                deciSize=int(bolts3['Size1'][0])+ (int(bolts3['Size1'][2])/int(bolts3['Size1'][4]))
        else:
            deciSize=bolts3['Size1']
        bolts3['TotalCode']=class1+bolts3['Code']+str(deciSize)+bolts3['Size2']
        bolts3['Full Description']=bolts3['Code Desc']+';;'+str(deciSize)+bolts3['Size1unit']+';;'+bolts3['Rating']+';;'+bolts3['Material']+';;'+bolts3['Manu Std']+';;'+'Class - '+bolts3['Class']

        finalBolting3.append(bolts3)
        
    finalBolting4=[]
    for i in bolting4Array:
        bolts4={}
        bolts4['Class']=class1
        bolts4['Code']='STBT'
        bolts4['Code Desc']='Stud Bolts with 2 heavy Hex nuts'
        bolts4['Size1']=i['inch']
        bolts4['Size2']=i['x mm'][2:]
        bolts4['Manu Std']='ASME 18.2.1 / 18.2.2'
        for j in pipesArray:
            for k in j.keys():
                for l in range(0,len(j[k])):
                    if j[k][l]=='DN':
                        list=(j[k][l+1].split("-"))
                        if int(list[0]) <= int(i['DN']) and int(list[1]) >= int(i['DN']):
                            bolts4['Material']=j[k][-1]
                            break
            break
        bolts4['Rating']=''
        bolts4['Size1unit']='"'
        bolts4['Size2unit']='mm'
        if '/' in bolts4['Size1']:
            if bolts4['Size1'][1]!=' ':
                deciSize=int(bolts4['Size1'][0])/int(bolts4['Size1'][2])
            else:
                deciSize=int(bolts4['Size1'][0])+ (int(bolts4['Size1'][2])/int(bolts4['Size1'][4]))
        else:
            deciSize=bolts4['Size1']
        bolts4['TotalCode']=class1+bolts4['Code']+str(deciSize)+bolts4['Size2']
        bolts4['Full Description']=bolts4['Code Desc']+';;'+str(deciSize)+bolts4['Size1unit']+';;'+bolts4['Rating']+';;'+bolts4['Material']+';;'+bolts4['Manu Std']+';;'+'Class - '+bolts4['Class']

        finalBolting4.append(bolts4)
                

    dataFrame1=pd.DataFrame(finalPipe+finalFlange+finalFitting+finalReducingFitting+finalValve+finalInstrument+finalMiscellaneous+finalBolting1+finalBolting2+finalBolting3+finalBolting4)
    dataFrame1.to_csv('/var/www/cuda-fs/test.csv',index=False)

    #return json.dumps({'DNtable':DNDict, 'CodeTable':CodeDict, 'BranchSizeTable':BranchSizeDict, 'Pipes':pipeDict, 'Flanges':flangesDict, 'fittingsTable':fittingsDict, 'valvesTable':valvesDict, 'instruemntsTable':instrumentsDict, 'miscellaneousTable':miscellaneousDict, 'Std boltset standard flg':boltingDict1, 'Std boltset mrun flg':boltingDict2, 'Std boltset orifice flg':boltingDict3, 'Std boltset blind/spacer':boltingDict4})
    #return json.dumps({'DNtable':dnDict,'CodeTable':codeDict,'RunSizeTable':RunSizeArray, 'Pipes':pipeArray, 'Flanges':flangesArray, 'Fittings':fittingsArray, 'Valves':valvesArray, 'Instruments':instrumentsArray, 'Miscellaneous':miscellaneousArray,'Std boltset standard flg':bolting1Array, 'Std boltset mrun flg':bolting2Array, 'Std boltset orifice flg':bolting3Array, 'Std boltset blind/spacer':bolting4Array})
    return ('cuda-fs.gibots.com:1443/test.csv')


from matplotlib import pyplot as plt
#import dlib
from collections import Counter
from imutils import face_utils
#import face_recognition
from math import atan2,degrees

def AngleBtw2Points(pointA, pointB):
    changeInX = pointB[0] - pointA[0]
    changeInY = pointB[1] - pointA[1]
    return degrees(atan2(changeInY,changeInX)) #remove degrees if you want your answer in radians

def distance_selection(l1,l2):
    dist = np.sqrt((l1[0] - l2[0])**2 + (l1[1] - l2[1])**2)
    return dist

def rotate_image_pil(im, angle):
    im_rotate = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    return im_rotate

def rotate_image(mat, angle):
    
    height, width = mat.shape[:2] # image shape has 3 dimensions
    image_center = (width/2, height/2) # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    # rotation calculates the cos and sin, taking absolutes of those.
    abs_cos = abs(rotation_mat[0,0]) 
    abs_sin = abs(rotation_mat[0,1])

    # find the new width and height bounds
    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    # subtract old image center (bringing image back to origo) and adding the new image center coordinates
    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    # rotate image with the new bounds and translated rotation matrix
    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat


def rotate_to_face(img1,im):
    
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    print("[INFO] loading facial landmark predictor...")
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("/var/www/cuda-fs/shape_predictor_68_face_landmarks.dat")

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]


    rects = detector(gray, 0)
    org_rects = detector(gray, 0) 
    print('RECTANGLE:', len(rects))
#     print(rects[0])
    increment = 0;
    angle = 0;
#     cv2.rectangle(rgb,(1714, 1403) ,(1929, 1618),(136,255,122),5)
    
    while (len(rects) == 0 and increment <= 240):
        print('Entered')
        increment += 30;
        rgray = rotate_image(gray, increment)
        rects = detector(rgray, 0)
        print ('-----------------------------------',increment);
        print ('-----------------------------------R',rects)
    #---Modified---
    if len(rects) == 0:
        org_rects = ['No Face Found']

    if len(rects) >0 and increment != 0:    
        gray = rotate_image(gray, increment)
        #rgb1 = rotate_image(rgb1, increment)
        image1 = rotate_image(img1, increment)
        im1_pil = rotate_image_pil(im, increment)
        print("Rotate 1 ")
        print(increment)
    
    else:
        image1 = img1
        im1_pil = im

    return image1,im1_pil,org_rects


#### main program
#import pandas as pd
#import numpy as np
#import re
#import subprocess
#from flask import *
#from datetime import datetime
#app = Flask(__name__)
@app.route('/gibots-pyapi/ImagePreprocessing', methods = ['POST'])
def ImageProcessing():
    data=request.json
    input=data['input']
    imname=input['ImageInput']
    angle = 0;

    # imname = 'PP 270.jpg'
    image1 = cv2.imread(imname)
    f=os.path.splitext(imname)[0]
    v=f.split('/')[-1]
    s=os.path.splitext(imname)[1]
    print(s)
    fn_proc = "/var/www/cuda-fs/"+v + "_rotate_minrect"+s
    # ext = image1.split('.')[1]
    # fn_proc = "/var/www/cuda-fs/"+[-4] + "_rotate_minrect."+ext

    rgb = cv2.imread(imname)
    im = Image.open(imname)
    rgb,im1,org_rects = rotate_to_face(rgb,im)
    height, width, channels = rgb.shape 
    small = cv2.cvtColor(rgb, cv2.COLOR_BGR2GRAY)


    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)) #(3,3)
    grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)

    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1)) 
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)

    #Image.fromarray(connected).show()

    # using RETR_EXTERNAL instead of RETR_CCOMP
    contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    #For opencv 3+ comment the previous line and uncomment the following line
    #_, contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    mask = np.zeros(bw.shape, dtype=np.uint8)

    counter = 0
    sum_angle = 0 
    sum_angle2 = 0 
    rotate = 0
    angles = []
    print('-------------------------LEN CONTOUR',len(contours))


    for idx in range(len(contours)):
        area = cv2.contourArea(contours[idx])
        rect = cv2.minAreaRect(contours[idx])
        center, weight, angle = cv2.minAreaRect(contours[idx])
        box = np.int0(cv2.boxPoints(rect))
        print(area)
        #if area < (height*width)* 0.80 and 
        if area > 500:  
    #         print('entered')
            x, y, w, h = cv2.boundingRect(contours[idx])
            rect = cv2.minAreaRect(contours[idx])
            center, weight, angle = cv2.minAreaRect(contours[idx])
            box = np.int0(cv2.boxPoints(rect))
            
            angdf = pd.DataFrame(box).reset_index().sort_values([0,1])
            first_point = angdf['index'].iloc[0]
            third_point = angdf['index'].iloc[2]
            second_point = angdf['index'].iloc[1]

            angle = AngleBtw2Points(box[first_point],box[third_point]) 
            dist1 = distance_selection(box[first_point],box[second_point])
            dist2 = distance_selection(box[first_point],box[third_point])
            print('DISTANCE',dist2,dist1)
    #         cv2.drawContours(rgb, [box], 0, (255,0,0), 3)
            lx = min(box[0][0],box[1][0],box[2][0],box[3][0])
            rx = max(box[0][0],box[1][0],box[2][0],box[3][0])
            ty = min(box[0][1],box[1][1],box[2][1],box[3][1])
            by = max(box[0][1],box[1][1],box[2][1],box[3][1])

            w =  rx - lx #abs( box[2][0] - box[0][0])
            h =  by - ty #abs( box[3][1] - box[2][1]) 
    #         print(h,w,width,h/w,w/width)
            #print (w,h,h/w, w/width, h*w, (height*width),area/(height*width),((h/w) < 0.5 and w/width > .45 and h > 4 ),(area > (height*width)* 0.40))
            if ( h > 4 and dist2/dist1>10 ) :    # .7
                print('angle:',angle)
    #             cv2.drawContours(rgb, [box], 0, (36,255,12), 3)
    #             Image.fromarray(rgb).show()
                sum_angle +=angle 
                counter+=1
                angles.append(angle)
            else : 
                if (h*w) > (height*width)* 0.40:
                    sum_angle2 = angle


    print("8888888888",sum_angle,counter,sum_angle2)
    print(angles)

    median_angle = np.median(angles)
    mean_angle = np.mean(angles)

    if counter != 0:
        if (np.abs(mean_angle-median_angle)>0.30) & (counter >=4):
            rotate = median_angle
        else:
            rotate = mean_angle
    else :
        if sum_angle2 != 0:
            rotate = sum_angle2 

    rotate = np.round(rotate,2)
    # if rotate < -45:
    #     rotate +=90 
    #---Modified--- 
    print(org_rects,"************ORG_RECT**************")
    if ((rotate>1.25) or (rotate<-1.25)):
        rgb = rotate_image(rgb,rotate)
        im2 = rotate_image_pil(im1,rotate)
        im2.save(fn_proc)
    elif len(org_rects) == 0:
        im2 = im1
        cv2.imwrite(fn_proc, rgb)
    elif len(org_rects) > 0:
        print('################COPIED##########################')
        # importing shutil module  
        import shutil 
        # Source path 
        source = imname

        # Destination path 
        destination = fn_proc

        try: 
            shutil.copy2(source, destination) 
            print("File copied successfully.") 

        # If source and destination are same 
        except shutil.SameFileError: 
            print("Source and destination represents the same file.") 

        # If destination is a directory. 
        except IsADirectoryError: 
            print("Destination is a directory.") 

        # If there is any permission issue 
        except PermissionError: 
            print("Permission denied.") 
        # For other errors 
        except: 
            print("Error occurred while copying file.")
 

        
    #if rotate>1.25 or rotate<-1.25:
        #rgb = rotate_image(rgb,rotate)
        #im2 = rotate_image_pil(im1,rotate)
       # im2.save(fn_proc)
    #else:
        #im2=im1
        #cv2.imwrite(fn_proc, rgb)
    # Image.fromarray(rgb).show()
    #cv2.imwrite('Passport_Scan_Adjust/Output/'+fn_proc, rgb)
    #im2.save(fn_proc)
    print("Deskewd Image-----",fn_proc)

    outputData={'output':fn_proc, 'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com:1443/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    return json.dumps(request.json)




@app.route('/gibots-pyapi/Image_conversion', methods = ['POST'])
def Image_conversion():
    data=request.json    
    img=data['input']
    inputImage=img['Image']
    output=''
    print(inputImage,"--------**--------")
    if inputImage.endswith(".pdf"):
        print("Entered in IF Loop for converting PDF file")
        f=os.path.splitext(inputImage)[0]
        v=f.split('/')[-1]
        print(inputImage)
        output=("/var/www/cuda-fs/"+v+".png")
        cmd="sudo convert -units PixelsPerInch -density 150"+' '+inputImage+' '+'-alpha off -verbose'+' '+output
        # cmd="convert"+' '+inputImage+' '+output
        print(cmd)
        subprocess.call([cmd],shell=True)
    else:
        print("Didn't receive any PDF file..")
        output=inputImage
    outputData={'output':output, 'statusCode': '200'}
    print('output---Data-------->>>>',outputData)
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': img['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", "http://ocri.gibots.com:1443/gibots-api/orchestrator/botsiowrite",verify=False, json=taskData, headers=head)
    return json.dumps(request.json)



@app.route('/gibots-pyapi/tableBoundary',methods=['GET', 'POST'])
def table_boundary_detector():
    data=request.json
    print(data)
    try:
        filename=data['filename']
    except Exception as e:
        print("Please upload valid File",e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    try:
        checkpoint_file=data['modelCp']    
    except:
        print("Checkpoint Path invalid")
        return json.dumps({'status':400 , 'info':'Please upload valid Model Checkpoint'})
    try:
        config_file=data['config_file']    
    except:
        print('Config file invalid')
        return json.dumps({'status':400 , 'info':'Config file invalid'})
    try:
        table_output_folder=data['outpath']
    except:
        print('Output path invalid')
        return json.dumps({'status':400 , 'info':'Invalid output path'})
    try:
        thre_value=data['thre_value']
    except:
        print('Thresold value invalid')
        return json.dumps({'status':400 , 'info':'Invalid threshold'})
    
#     # Load model
#     filename = 'give exact file location'
#     checkpoint_file = 'epoch_36.pth'
#     config_file = 'CascadeTabNet/Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py'
#     table_output_folder = 'give output folder location'
#     thre_value = 'take from config file and change below'
    
    # input_folder = 'CascadeTabNet/Demo/Invoices/B/'
    
    out_file_detail = table_output_folder+filename[:-4]+'_TO.png'
    #model = init_detector(config_file, checkpoint_file, device='cuda:0')
    

    res_border = []
    res_bless = []
    import subprocess
    import os 
    subprocess.run('source activate test',shell=True)
    os.system('source activate test')
    from mmdet.apis import init_detector, inference_detector, show_result_pyplot, show_result
    import mmcv
    import subprocess
    import os
    os.system('source activate test')
    subprocess.run('source activate test',shell=True)    
    
    model = init_detector(config_file, checkpoint_file, device='cuda:0')
    print(filename)
    img = filename
    # Run Inference
    result = inference_detector(model, img)

    try:
        # Visualization results
        #show_result_pyplot(img, result,('Bordered', 'cell', 'Borderless'), score_thr=0.85)
        show_result(img,result,('Bordered', 'cell', 'Borderless'),score_thr=0.85,out_file=out_file_detail)


        ## for border
        for r in result[0][0]:
            if r[4]>.85:
                res_border.append(r[:4].astype(int))

        ## for borderless
        for r in result[0][2]:
            if r[4]>.85:
                res_bless.append(r[:4].astype(int))   

        ## for cells
        # for r in result[0][1]:
        #     if r[4]>.85:
        #         r[4] = r[4]*100
        #         res_cell.append(r.astype(int))

    except:
        pass
    os.system('source deactivate')
    subprocess.run('source deactivate',shell=True)
        
    return json.dumps({"result":out_file_detail,'border_co':res_border,'bless_co':res_bless})

@app.route('/gibots-pyapi/fieldDetectionTawazun',methods=['GET', 'POST'])
def fieldDetectorTawazun():
    data=request.json
    print(stop)
    from tawazun_prediction_api import fieldDetectionTawazunApi
    #from prediction_testing import fieldDetectionTawazunApi
    print(data)
    print('CALLING THIS API -----fieldDetectionTawazun')
    try:
        filePath=data['filePath']
        print(filePath)
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    try:
        modelType=data['modelType']    
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Model type invalid'})
    try:
        documentType=data['documentType']    
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Document type invalid'})
    try:
        orgId=data['orgId']
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Invalid organization'})
    try:
        df=pd.read_csv(filePath)
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    
    with semaphore:
        result=fieldDetectionTawazunApi(data)
        print('Final output from fieldDetectorTawazun api -----',result)

        return result


@app.route('/gibots-pyapi/genai_prediction_royal_tech',methods=['GET', 'POST'])
def genai_prediction():
    # sem.acquire()
    print('using this api mlPrediction')
    try:
        data=request.json
        try:
           print('before document type  ',data['input']['mlInput']['documentType'])
           #dynamic document insertion
           if (data['input']['isDynamic']!='false' and data['input']['dynamicDocType']):
              data['input']['mlInput']['documentType'] = data['input']['dynamicDocType']
           print('After document type  ',data['input']['mlInput']['documentType'])
        except Exception as e:
           print('Error ',e)
        print('After document type  ',data['input']['mlInput']['documentType'])
        print('Aaaa  ',data['input']['template_based'])

        input =data['input']
        mlInput = input['mlInput']
        combineLines = input['combineLines']
        ai_model_name = input['ai_model_name']
        ref_no = input['refNo']
        config_value = input['configValue'] #config values coming from bot input
        if config_value:
            print (config_value)
            config_value = config_value.replace("'", "\"")
            config_value_json = json.loads(config_value)
            data['input']['config_value_json'] = config_value_json
        if(type(combineLines) == str and combineLines.find('isLocal') != -1):
            file = combineLines.replace('/isLocal','')
            file_opn = open(file,'r')
            combineLines = json.load(file_opn)
            file_opn.close()
            data['input']['combineLines'] = combineLines
            print ('Loaded from json', len(combineLines))
        

        try:
            filePath=mlInput['filePath']
            print(filePath)
        except Exception as e:
            print(e)
            raise Exception('Please upload valid File')
        try:
            modelType=mlInput['modelType']
        except Exception as e:
            print(e)
            raise Exception('Model type invalid')
        try:
            documentType=mlInput['documentType']
        except Exception as e:
            print(e)
            raise Exception('Document type invalid')
        try:
            orgId=mlInput['orgId']
        except Exception as e:
            print(e)
            raise Exception('Invalid organization')

        timestamp = str(time.time())
        #from gen_ai_13b import fieldDetection

        '''with open("file_event_"+timestamp+".json", "w") as f:
            json.dump(data, f)'''
        print('------READY TO CALL LLAMA----   ',timestamp)
        
        #from genai_online import fieldDetection
        with open("file_event_"+timestamp+".json", "w") as f:
            json.dump(data, f)

        f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
             "/home/user/anaconda3/envs/genai-online/bin/python genai_online_royal.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True , universal_newlines=True)))
        print('FOUND SUBPROCESS DATA FROM TAWAZUN API----')
        print(f_)
        print('**'*50)

        outputData = json.load(open("file_"+timestamp+".json", "r"))
        #done by yuvraj shankar
        outputData['ml_input'] = data['input']['mlInput']
        print('  1   ')
        try:
           print('  2   ')
           if  outputData.get('data', {}).get('isRightDocument'):
               print ('inside try if ',outputData['data']['isRightDocument'])
               outputData['isRightDocument'] = outputData['data']['isRightDocument']
           else:
               print('  3   ')
               outputData['isRightDocument'] = 'false'
           print ('inside try  ',outputData['isRightDocument'])

        except Exception as e:
           print(e)
           outputData['isRightDocument'] = 'false'
           print ('inside else  ',outputData['data']['isRightDocument'])
        print('  5   ')
        #print('Final output from fieldDetectorTawazun api -----',result)
        os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
        #os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")
        #outputData = fieldDetection(data,timestamp)
        print('Final output from fieldDetectorTawazun api -----',outputData)

        #outputData = fieldDetection(data)
        #print('Final output from fieldDetectorTawazun api -----',outputData)
        end_time = time.time()

    # Calculate and print the execution time
        execution_time = end_time - float(timestamp)
        print(f"Execution time: {execution_time:.6f} seconds")
        #outputData['Execution_time'] = "{:.6f}".format(execution_time)
        #torch.cuda.empty_cache()
        #outputData={'mlOutput':'done' , 'statusCode': '200'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        #print('response ------------------->',taskData, config_value_json)

        if 'requestURL' in config_value_json:
            response = requests.request("POST", config_value_json['requestURL'], json=taskData, headers=head)
        else:
            response = requests.request("POST", config['requestURL'], json=taskData, headers=head)
        
        return json.dumps(outputData)

    except Exception as e:
        # sem.release()
        
        print('ERROR: error in GEN Ai !!!',traceback.format_exc())
        print(e)
        outputData={'output':str(e), 'statusCode': '202'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)

        return json.dumps(outputData)




@app.route('/gibots-pyapi/genai_prediction',methods=['GET', 'POST'])
def genai_prediction():
    # sem.acquire()
    print('using this api mlPrediction')
    try:
        data=request.json

        try:
           print('before document type  ',data['input']['mlInput']['documentType'])
           #dynamic document insertion
           if (data['input']['isDynamic']!='false' and data['input']['dynamicDocType']):
              data['input']['mlInput']['documentType'] = data['input']['dynamicDocType']
           print('After document type  ',data['input']['mlInput']['documentType'])
        except Exception as e:
           print('Error ',e)
        print('After document type  ',data['input']['mlInput']['documentType'])

        print("data input from the genai_prediction bot ---------------",data)
        input =data['input']
        mlInput = input['mlInput']
        combineLines = input['combineLines']
        ai_model_name = input['ai_model_name']
        ref_no = input['refNo']
        config_value = input['configValue'] #config values coming from bot input
        if config_value:
            print (config_value)
            config_value = config_value.replace("'", "\"")
            config_value_json = json.loads(config_value)
            data['input']['config_value_json'] = config_value_json
        if(type(combineLines) == str and combineLines.find('isLocal') != -1):
            if combineLines.startswith("../"):
                combineLines = "../" + combineLines
            file = combineLines.replace('/isLocal','')
            file_opn = open(file,'r')
            combineLines = json.load(file_opn)
            file_opn.close()
            data['input']['combineLines'] = combineLines
            print ('Loaded from json', len(combineLines))
       
        try:
            filePath=mlInput['filePath']
            print(filePath)
        except Exception as e:
            print(e)
            raise Exception('Please upload valid File')
        try:
            modelType=mlInput['modelType']
        except Exception as e:
            print(e)
            raise Exception('Model type invalid')
        try:
            documentType=mlInput['documentType']
        except Exception as e:
            print(e)
            raise Exception('Document type invalid')
        try:
            orgId=mlInput['orgId']
        except Exception as e:
            print(e)
            raise Exception('Invalid organization')

        timestamp = str(time.time())
        #from gen_ai_13b import fieldDetection

        print('------READY TO CALL openai----')
        
        #from genai_online import fieldDetection
        with open("file_event_"+timestamp+".json", "w") as f:
            json.dump(data, f)
            
        f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
            "/home/ubuntu/.conda/envs/Genai-online/bin/python genai_online.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True , universal_newlines=True)))
        
        print('FOUND SUBPROCESS DATA FROM TAWAZUN API----')
        print(f_)
        print('**'*50)
        
        outputData = json.load(open("file_"+timestamp+".json", "r"))
        try:
            outputData['fileObj'] = input['fileObj']
            outputData['tableRuleObj'] = input['tableRuleObj']
        except Exception as e:
            print('fileobj and tableruleobj not available')
        #done by yuvraj shankar
        outputData['ml_input'] = data['input']['mlInput']
        print('  1   ')
        try:
           print('  2   ')
           if  outputData.get('data', {}).get('isRightDocument'):
               print ('inside try if ',outputData['data']['isRightDocument'])
               outputData['isRightDocument'] = outputData['data']['isRightDocument']
           else:
               print('  3   ')
               outputData['isRightDocument'] = 'false'
           print ('inside try  ',outputData['isRightDocument'])

        except Exception as e:
           print(e)
           outputData['isRightDocument'] = 'false'
           print ('inside else  ',outputData['data']['isRightDocument'])
        print('  5   ')
        
        #print('Final output from fieldDetectorTawazun api -----',result)
        os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
        os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")
        #outputData = fieldDetection(data)
        print('Final output from fieldDetectorTawazun api -----',outputData)
        end_time = time.time()

    # Calculate and print the execution time
        execution_time = end_time - float(timestamp)
        print(f"Execution time: {execution_time:.6f} seconds")
        #outputData['Execution_time'] = "{:.6f}".format(execution_time)
        #torch.cuda.empty_cache()
        #outputData={'mlOutput':'done' , 'statusCode': '200'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        print('response ------------------->',taskData)

        if 'requestURL' in config_value_json:
            response = requests.request("POST", config_value_json['requestURL'], json=taskData, headers=head)
        else:
            response = requests.request("POST", config['requestURL'], json=taskData, headers=head)
        
        return json.dumps(outputData)

    except Exception as e:
        # sem.release()
        
        print('ERROR: error in GEN Ai !!!',traceback.format_exc())
        print(e)
        outputData={'output':str(e), 'statusCode': '202'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)

        return json.dumps(outputData)




#Gen AI + Temolate API
@app.route('/gibots-pyapi/templatePrediction',methods=['GET', 'POST'])
def templatePrediction():
    print('using this api mlPrediction')
    try:
        data=request.json
        from ml_prediction_api import fieldDetectionTawazunApi
        #from prediction_testing import fieldDetectionTawazunApi
        # print(data)
        input =data['input']
        mlInput = input['mlInput']
        print(input)
        #print(yes)
        try:
            filePath=mlInput['filePath']
            print(filePath)
        except Exception as e:
            print(e)
            raise Exception('Please upload valid File')
        try:
            modelType=mlInput['modelType']    
        except Exception as e:
            print(e)
            raise Exception('Model type invalid')
        try:
            documentType=mlInput['documentType']    
        except Exception as e:
            print(e)
            raise Exception('Document type invalid')
        try:
            orgId=mlInput['orgId']
        except Exception as e:
            print(e)
            raise Exception('Invalid organization')
        try:
            df=pd.read_csv(filePath)
        except Exception as e:
            print(e)
            raise Exception('Please upload valid File')
            
        #######################################################
        
        timestamp = str(time.time())

        with open("file_event_"+timestamp+".json", "w") as f:
            json.dump(data['input']['mlInput'], f)
            
        f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
            "/home/ubuntu/.conda/envs/python38/bin/python ml_prediction_api.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True , universal_newlines=True)))
        
        print('FOUND SUBPROCESS DATA FROM TAWAZUN API----')
        print(f_)
        print('**'*50)
        
        result = json.load(open("file_"+timestamp+".json", "r"))
        
        print('Final output from fieldDetectorTawazun api -----',result)
        os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
        os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")

        
        #result=fieldDetectionTawazunApi(mlInput)
        
        print('Final output from fieldDetectorTawazun api -----',result)
        outputData={'mlOutput':result ,'template_found': result['isTmp'], 'statusCode': '200'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        print(taskData)
        response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)

        return jsonify(outputData)

    except Exception as e:
        print(e)
        outputData={'output':str(e), 'statusCode': '202'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)

        return jsonify(outputData)




# @app.route('/gibots-pyapi/mlPrediction',methods=['GET', 'POST'])
# def mlPrediction():
#     print('using this api mlPrediction')
#     try:
#         data=request.json
#         from tawazun_prediction_api import fieldDetectionTawazunApi
#         #from prediction_testing import fieldDetectionTawazunApi
#         # print(data)
#         input =data['input']
#         mlInput = input['mlInput']
#         print(input)
#         #print(yes)
#         try:
#             filePath=mlInput['filePath']
#             print(filePath)
#         except Exception as e:
#             print(e)
#             raise Exception('Please upload valid File')
#         try:
#             modelType=mlInput['modelType']    
#         except Exception as e:
#             print(e)
#             raise Exception('Model type invalid')
#         try:
#             documentType=mlInput['documentType']    
#         except Exception as e:
#             print(e)
#             raise Exception('Document type invalid')
#         try:
#             orgId=mlInput['orgId']
#         except Exception as e:
#             print(e)
#             raise Exception('Invalid organization')
#         try:
#             df=pd.read_csv(filePath)
#         except Exception as e:
#             print(e)
#             raise Exception('Please upload valid File')
            
#         #######################################################
        
#         timestamp = str(time.time())

#         with open("file_event_"+timestamp+".json", "w") as f:
#             json.dump(data['input']['mlInput'], f)
            
#         f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
#             "/home/ubuntu/anaconda3/bin/python tawazun_prediction_api.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True , universal_newlines=True)))
        
#         print('FOUND SUBPROCESS DATA FROM TAWAZUN API----')
#         print(f_)
#         print('**'*50)
        
#         result = json.load(open("file_"+timestamp+".json", "r"))
        
#         print('Final output from fieldDetectorTawazun api -----',result)
#         os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
#         os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")

        
#         #result=fieldDetectionTawazunApi(mlInput)
        
#         print('Final output from fieldDetectorTawazun api -----',result)
#         outputData={'mlOutput':result , 'statusCode': '200'}
#         taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
#         head = {'authorization': data['token'], 'content-type': "application/json"}
#         print(taskData)
#         response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)

#         return jsonify(outputData)

#     except Exception as e:
#         print(e)
#         outputData={'output':str(e), 'statusCode': '202'}
#         taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
#         head = {'authorization': data['token'], 'content-type': "application/json"}
#         response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)

#         return jsonify(outputData)

@app.route('/gibots-pyapi/fieldTrainingTawazun',methods=['GET', 'POST'])
def fieldTrainerTawazun():
    data=request.json
    print(data)
    try:
        filePath=data['filePath']
        print(filePath)
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    try:
        modelType=data['modelType']
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Model type invalid'})
    try:
        documentType=data['documentType']
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Document type invalid'})
    try:
        orgId=data['orgId']
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Invalid organization'})
    try:
        df=pd.read_csv(filePath)
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    # ==> UNCOMMENT BELOW TO START TRAINING FROM FRONT-END
    # result=fieldTrainingTawazunApi(data)

    return jsonify({'status':'true', 'info':'Model trained Successfully'})

#######################################################################################################################################################################
#######################################################################################################################################################################



@app.route('/gibots-pyapi/'+'jsonToTxt', methods = ['POST'])
def jsontotext():
    data=request.json
    img=data['input']
    I_filepath=img['pdfName']
    O_filepath=img['JsonFilePath']
    pd.set_option('display.max_rows',500)
    df = pd.read_csv(O_filepath)
    df['text'].fillna('\n',inplace=True)
    df.rename(columns={'leftX':'left','topY':'top','pageNo':'page_num','pageWidth':'Page width','pageHeight':'Page height'},inplace=True)
    # df.head(500)
    # df[df['page_num'] == 4].head(500)
    # df['Filter_New_Line'] = df['text'].
    df['right'] = df['left'] + df['width']
    df['bottom'] = df['top'] + df['height']
    # df['box_type'] = df['width'] / df['height']
    # df.columns
    df['page_num'].sort_values().unique()
    final_text = ''
    full_df = pd.DataFrame()
    for page in df['page_num'].sort_values().unique():
        dft = df[df['page_num'] == page]
        # Extra Page Details Cleaning
        dftt = dft[(dft['text'] != '\n')]
        dftt = dftt[(dftt['text'] != ' ')]
        filter_df = dftt.groupby(['Page width','page_num', 'block_num', 'par_num', 'line_num'])['width'].sum().reset_index()
        filter_df['coverage'] = 100 * filter_df['width'] / filter_df['Page width']
        filter_df = filter_df[['page_num', 'block_num', 'par_num', 'line_num','coverage']]
        mdf =  pd.merge(dft,filter_df,on=['page_num', 'block_num', 'par_num', 'line_num'],how='left')
        mdf['coverage'].fillna(1000,inplace=True)
        # mdf[mdf['top'] < 0.15*mdf['Page height']]
        # mdf[mdf['bottom'] > 0.85*mdf['Page height']]
        mdf = mdf.loc[~((mdf['coverage'] < 45) & (mdf['bottom'] > 0.85*mdf['Page height'])) ]
        mdf = mdf.loc[~((mdf['coverage'] < 45) & (mdf['top'] < 0.15*mdf['Page height'])) ]
        mdf['text_nearby'] = mdf['text'].shift(-1)
        mdf['text'] = mdf['text'].astype(str)
        mdf['text_nearby'] = mdf['text_nearby'].astype(str)
        mdf['SS'] = mdf['text_nearby'].apply(lambda x: len(re.findall('\d\.\d',x)) )
        mdf.loc[(mdf['SS'] == 1) & (mdf['text'] == '\n'),'text'] = '\n \n'
        full_df = full_df.append(mdf)
        # Data Merging to get TXT of Contract
        sample_text = ' '.join(mdf['text'].astype(str)).replace(' \n \n ','CHANGELATER').replace(' \n ','').replace('CHANGELATER','\n').replace('\n ','\n')
        final_text = final_text+sample_text
    # full_df.groupby(['page_num','block_num','par_num'])['text'].apply(' '.join).reset_index()
    # print(' '.join(full_df['text'].astype(str)).replace(' \n \n ','CHANGELATER').replace(' \n ','').replace('CHANGELATER','\n').replace('\n ','\n'))
    # Additional OCR Correction !!
    final_text = final_text.replace(':','.')
    print(final_text)
    filenew=os.path.basename(I_filepath)
    print('Newfilename of Text generated from jsontxt',filenew)
    outputFile="/var/www/cuda-fs/"+filenew+".txt"
    with open(outputFile, "a") as file_object:
        # Append 'hello' at the end of file
        file_object.write(final_text)
    
    input=data['input']
    outputData={'outputFile': outputFile,'statusCode': '200'}
    print('output---Data---from jsonTxt----->>>>',outputData)
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    print('requestURL-----------------',config['requestURL'])
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    return json.dumps(request.json)






@app.route('/gibots-pyapi/pdfCutting', methods=['POST'])
def pdfCutting():
    #O_path='/home/gibots/'+
    data=request.json
    img=data['input']
    #folder_path=img['TextFilePath']
    pdf_path1 = img['pdfPath']
    print('pdf_path1--->',pdf_path1)
    #specialChar=[' ','(',')',';',':','*','&','%','+']
    pdf_path=''
    import os
    import ntpath
    dir_path='/'.join(pdf_path1.split('/')[:-1])
    print(dir_path)
    os.chdir(dir_path)
    print('path changed')
    oldname=os.path.basename(pdf_path1)
    newname=''.join(c for c in oldname if c.isalpha())
    os.rename(oldname,newname+'.pdf')
    pdf_newpath=dir_path+'/'+newname+'.pdf'
    #for i in range(0,len(specialChar)):
        #if specialChar[i] in pdf_path1:
         #   print('specialCha---->',specialChar[i])
        #    pdf_path=pdf_path.replace(specialChar[i],'')
       #     print('pdfnewName---',pdf_path)
      #  else:
     #       pdf_path1=pdf_path
    #print('new--->',pdf_path,'old--->',pdf_path1)
    from pdfrw import PdfReader, PdfWriter
    #pdf_path=os.rename(pdf_path1,pdf_path)

    pages = PdfReader(pdf_newpath).pages
    parts = [(1,6)]
    base_name=('.').join(os.path.basename(pdf_newpath).split('.')[:-1])+'_pages_'+str(parts[0][0])+'_'+str(parts[0][1])
    print(base_name)

    if ' ' in base_name:
        base_name=base_name.replace(' ','_')
    for part in parts:
        #out_path = 'var/www/cuda-fs/'+str(base_name)+'.pdf'
        #outdata = PdfWriter(out_path)
        outdata = PdfWriter('/var/www/cuda-fs/'+base_name+f'pages_{part[0]}_{part[1]}.pdf')
        outt='/var/www/cuda-fs/'+base_name+f'pages_{part[0]}_{part[1]}.pdf'
        #if ' ' in outt:

         #   outt=outt.replace(' ','_')
          #  print(outt)
        #else:
         #   outt=outt
        for pagenum in range(*part):
            outdata.addpage(pages[pagenum-1])
        outdata.write()
        #return path
        #outputFile = os.path.join(dest_path, 'version_segregation.xlsx')
    
    outputFile = outt
    input=data['input']
    outputData={'OutputFile': outputFile,'statusCode': '200'}
    print(outputData)
    # print('output---Data-------->>>>',outputData)
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    print('requestURL-----------------',config['requestURL'])
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    return json.dumps(request.json)

################################################################################################



@app.route('/gibots-pyapi/separateFilesVersion', methods=['POST'])
def separateFilesVersion():
    #folder_path='/home/user/Documents/NLP_Tata_comm/tata_text/test'
    #dest_path='/home/user/Documents/NLP_Tata_comm/tata_text/version_separation'
    
    data=request.json
    img=data['input']
    folder_path=img['TextFilePath']
    pdf_path = img['pdfPath']
    print('-----folderPath----',img)
    dest_path = os.path.join(config['uploadFilePath'], 'version_separated_files')

    template_type_list=[]
    filename_list=[]
    version_no_list=[]

    error_cnt=0

    try:
        df = pd.read_csv(folder_path, error_bad_lines=False, delimiter = "\t",names=['text'])
        status3=status2=status1=False

        Std_Nonstd = 'NoN_TATA'
        stamp_text = ' '.join(df['text'].astype(str))

        try:
            msa_version_text = df[df.text.str.startswith('Master Service Agreement',na=False)]['text'].values[0]
            regex1 = '\(v\d.\d'
            regex3 = '\(v\d'
            regex2 = 'version'
            version_no = re.search("|".join([regex1,regex2,regex3]),msa_version_text.lower()).group()[1:]
        except AttributeError as e:
            version_no = 'undefined'
            error_cnt+=1
            print(e)
        except IndexError as e:
            version_no = 'undefined'
            error_cnt+=1
            print(e) 


        standard_stamps_poss2 = [m1.start(0) for m1 in re.finditer('docu',stamp_text.lower())]
        for ind in standard_stamps_poss2:
            check_txt = stamp_text[ind:ind+50]
            if 'envelope' in check_txt.lower() and 'id' in check_txt.lower():
                status3=True
        standard_stamps_poss = [m.start(0) for m in re.finditer('msa',stamp_text.lower())]
        for ind in standard_stamps_poss:
	        check_txt = stamp_text[ind:ind+30]
	        if 'msa' in check_txt.lower() and 'reference' in check_txt.lower():
	            status1=True
        standard_stamps_poss2 = [m1.start(0) for m1 in re.finditer('master',stamp_text.lower())]
        for ind in standard_stamps_poss2:
	        check_txt = stamp_text[ind:ind+50]
	        if 'service' in check_txt.lower() and 'agreement' in check_txt.lower() and 'v' in check_txt.lower():
	            status2=True

        template_type= 'Non_Tata'        
        if status1==True and status2==True and status3 == True:
	        template_type='Tata'

    
        
    except IndexError as e:
        print(e)
        error_cnt+=1
    except :
        print('file couldnt run')
        
#    print(folder_path,'---',msa_version_text,'---',version_no)
#    print(f'Processed:{folder_path}')
    try:
    # make new directory for version numbers
        os.makedirs(os.path.join(dest_path,version_no),exist_ok=True)
        shutil.copy(pdf_path, os.path.join(dest_path,version_no))

    # version, template type for excel
        template_type_list.append(template_type)
        filename_list.append(folder_path)
        version_no_list.append(version_no)

    # print(f'Error in {error_cnt} files.')
        df_excel = pd.DataFrame({'filename':filename_list, 'template':template_type_list, 'version':version_no_list})
        df_excel.to_csv('/var/www/cuda-fs/version_segregation_imagePDF.xlsx',mode='a', index = False, header=None)
    
        outputFile='/var/www/cuda-fs/version_segregation_imagePDF.xlsx'
    #outputFile = os.path.join(dest_path, '/var/www/cuda-fs/version_segregation.xlsx')
        print(outputFile,'78787878777787')
    except:
        outputFile='NofileFound'
    input=data['input']
    outputData={'outputFile': outputFile,'statusCode': '200'}
    print('output---Data-------->>>>',outputData)

    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    print('requestURL-----------------',config['requestURL'])
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    return json.dumps(request.json)

@app.route('/gibots-pyapi/separateFilesVersion', methods=['POST'])
def nlp_tata_prediction():
    data=request.json
    img=data['input']
    txt_file_path=img['TextFilePath']
    #pdf_path = img['pdfPath']
    print('**NLP BOT:-- Folder:-',img)
    dest_path = os.path.join(config['uploadFilePath'], 'version_separated_files')


    target_names = ['Acceptance of Services', 'Agreement Term', 'Auto renew COF',
       'Cure Period Payment', 'Disputed Invoices', 'Effective Date',
       'Entity names', 'Interest rate', 'MSA Ref no', 'MSA Version no',
       'Payment Term', 'Supplier Remedies', 'Termination Notice',
       'undefined']

    # reload our model/tokenizer. Optional, only usable when in Python files instead of notebooks
    model_path = '/home/gibots/scanning/gibots-sftp-s3/tatacomm-model-test-para-5E'
    model = BertForSequenceClassification.from_pretrained(model_path, num_labels=len(target_names))#.to("cuda")
    tokenizer = BertTokenizerFast.from_pretrained(model_path)

    # max sequence length for each document/sentence sample
    max_length = 512

    # read txt file
    df = pd.read_csv(txt_file_path, sep='\n', header=None,names=['text'])

    list_clauses = df['text'].tolist()
    preds=[]
    probs=[]
    for clause in list_clauses:
        # prepare our text into tokenized sequence
        inputs = tokenizer(clause, padding=True, truncation=True, max_length=max_length, return_tensors="pt")#.to("cuda")
        # perform inference to our model
        outputs = model(**inputs)
        # get output probabilities by doing softmax
        prob = outputs[0].softmax(1)
        # append predisctions and probabilities
        probs.append(prob)
        preds.append(target_names[prob.argmax()])
#       print(prob.max(axis=1)[0].cpu().detach().numpy())
#       print([target_names[label] for label in probs.argmax(axis=1)])

    # convert into a list
    probability = [float(x.max().cpu().detach().numpy()) for x in probs]

    df['probability']=probability
    df['prediction']=preds

    # save predictions to an excel file
    df.to_csv(dest_path+os.sep+'sample_para_prediction.xlsx')

    input=data['input']
    outputData={'outputFile': outputFile,'statusCode': '200'}
    print('output---Data-------->>>>',outputData)

    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    print('*NLP BOT:- requestURL-----------------',config['requestURL'])
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    return json.dumps(request.json)
@app.route('/gibots-pyapi/augmentInvoiceApi',methods=['GET', 'POST'])
def augmentInvoiceApi():
    def make_listOflist(lst):
        return [[ele] for ele in lst]
    data=request.json
    input=data['input']
    print(f'Input to augmentInvoice function:-\n{input}')
    pixel_list = input['pixel_list']
    directions = input['directions']
    # convert string input into list: input = '[5,10]' output = ['5','10']
    pixel_list = pixel_list.split(',')
    got_input = {'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'],'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    #from augment_invoice_api import augment_invoice
    print(data)
    try:
        input = data['input']
        filePath = input['filePath']
        print(f'Path of CSV to be augmented: {filePath}')
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    #try:
    #    modelType=data['modelType']
    #except Exception as e:
    #    print(e)
    #    return json.dumps({'status':400 , 'info':'Model type invalid'})
    #try:
    #    documentType=data['documentType']
    #except Exception as e:
    #    print(e)
    #    return json.dumps({'status':400 , 'info':'Document type invalid'})
    #try:
    #    orgId=data['orgId']
    #except Exception as e:
    #    print(e)
    #    return json.dumps({'status':400 , 'info':'Invalid organization'})
    try:
        one_df=pd.read_csv(filePath)
        #df_origi=df.copy()
        print(f'Augment function read csv correctly---shape:{one_df.shape}')
        #=========REMOVE undefined property===============================
        one_df = one_df[one_df['property']!='undefined']
        print(f"shape after removing undefined:{one_df.shape}")
        one_df['Name'].fillna('NULL', inplace=True) #replace empty Name with NULL and remove them
        one_df = one_df[one_df['Name']!='NULL']
        #one_df.to_csv('/var/www/cuda-fs/RemoveNULLAugmentInvoiceFN.csv',index=False)
        print(f"after removing empty Name:{one_df.shape}")
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'}) 

    # print(selected_df['filePath'].unique())
    ocr_output=[]
    #one_df.to_csv('debuging_csv.csv',index=False)
    #print("checking for error int64")
    #print('before with  int64',one_df.select_dtypes('int64').columns)
    one_df[['index', 'topY', 'bottomY', 'pageNo', 'lineNumber', 'PageHeight','PageWidth', 'LineSize']] = one_df[['index', 'topY', 'bottomY', 'pageNo', 'lineNumber', 'PageHeight','PageWidth', 'LineSize']].astype('int32')
    #print('after without  int64',one_df.select_dtypes('int64').columns)

    for pixel_val in pixel_list:
        # make copies for augmented dataframes
        up_df = one_df.copy()
        down_df = one_df.copy()
        left_df = one_df.copy()
        right_df = one_df.copy()
        left_up= one_df.copy()
        left_down= one_df.copy()
        right_up= one_df.copy()
        right_down= one_df.copy()

        pixel_val = int(pixel_val)
        
        if directions=='four':
            up_df['topY'], up_df['bottomY'] = up_df['topY']- pixel_val, up_df['bottomY']-pixel_val
            down_df['topY'], down_df['bottomY'] = down_df['topY']+pixel_val, down_df['bottomY']+pixel_val
            left_df['leftX'], left_df['rightX'] = left_df['leftX']-pixel_val, left_df['rightX']-pixel_val
            right_df['leftX'], right_df['rightX'] = right_df['leftX']+pixel_val, right_df['rightX']+pixel_val
        
            list_augmented_df = [up_df, down_df, left_df, right_df]

        if directions=='diagonal':
            left_up['leftX'], left_up['rightX'], left_up['topY'], left_up['bottomY'] = left_up['leftX']-pixel_val, left_up['rightX']-pixel_val, left_up['topY']-pixel_val, left_up['bottomY']-pixel_val    
            left_down['leftX'], left_down['rightX'], left_down['topY'], left_down['bottomY'] = left_down['leftX']-pixel_val, left_down['rightX']-pixel_val, left_down['topY']+pixel_val, left_down['bottomY']+pixel_val
            right_up['leftX'], right_up['rightX'], right_up['topY'], right_up['bottomY'] = right_up['leftX']+pixel_val,right_up['rightX']+pixel_val, right_up['topY']-pixel_val,right_up['bottomY']-pixel_val
            right_down['leftX'], right_down['rightX'], right_down['topY'], right_down['bottomY'] = right_down['leftX']+pixel_val,right_down['rightX']+pixel_val, right_down['topY']+pixel_val,right_down['bottomY']+pixel_val
        
            list_augmented_df = [left_up, left_down, right_up, right_down]

        if directions=='eight':
            up_df['topY'], up_df['bottomY'] = up_df['topY']- pixel_val, up_df['bottomY']-pixel_val
            down_df['topY'], down_df['bottomY'] = down_df['topY']+pixel_val, down_df['bottomY']+pixel_val
            left_df['leftX'], left_df['rightX'] = left_df['leftX']-pixel_val, left_df['rightX']-pixel_val
            right_df['leftX'], right_df['rightX'] = right_df['leftX']+pixel_val, right_df['rightX']+pixel_val
            left_up['leftX'], left_up['rightX'], left_up['topY'], left_up['bottomY'] = left_up['leftX']-pixel_val, left_up['rightX']-pixel_val, left_up['topY']-pixel_val, left_up['bottomY']-pixel_val
            left_down['leftX'], left_down['rightX'], left_down['topY'], left_down['bottomY'] = left_down['leftX']-pixel_val, left_down['rightX']-pixel_val, left_down['topY']+pixel_val, left_down['bottomY']+pixel_val
            right_up['leftX'], right_up['rightX'], right_up['topY'], right_up['bottomY'] = right_up['leftX']+pixel_val,right_up['rightX']+pixel_val, right_up['topY']-pixel_val,right_up['bottomY']-pixel_val
            right_down['leftX'], right_down['rightX'], right_down['topY'], right_down['bottomY'] = right_down['leftX']+pixel_val,right_down['rightX']+pixel_val, right_down['topY']+pixel_val,right_down['bottomY']+pixel_val

            list_augmented_df = [up_df, down_df, left_df, right_df, left_up, left_down, right_up, right_down]

        for idx, df in enumerate(list_augmented_df): 
            print(f'Augmenting:{pixel_val}pixels NULL VALUES BEFORE:-{df.isnull().sum().sum()}')
            df.fillna(0, inplace=True)
            print(f'Augmenting:{pixel_val}pixels NULLL VALUES AFTER:-{df.isnull().sum().sum()}')
            grouped_invoices_df = df.groupby('filePath')

            for filePath_values, grouped_df in grouped_invoices_df:
                ocr_dict_each_invoice = {}
                clst=[]
                line_grp = grouped_df.groupby('lineNumber')
                for lineno, linegrp_df in line_grp: 
                    #print(f'INSIDE-NULL VALUES BEFORE:-{grouped_df.isnull().sum().sum()}')
                    #linegrp_df.fillna(0, inplace=True)
                
                    #print(f'INSIDE-NULLL VALUES AFTER:-{grouped_df.isnull().sum().sum()}')
                    linegrp_df['text'] = grouped_df['Name']
                    linegrp_df['imageName'] = grouped_df['filePath']
                    #print(f"GROUPED DF SHAPE:{grouped_df.shape}")
                    # left out confidence, lang ---> 'lineNumber' for extratcFeatures
                    combinedWords = linegrp_df[['Name','text','imageName','pageNo','leftX','rightX','bottomY','topY','property']].to_dict('records')
                    clst.append(combinedWords)
                # Lines key for extractFeatures bot
                # Lines = make_listOflist(combinedWords) 
                #     print(combinedWords)
                #     print(len(combinedWords))

                page_Height = int(grouped_df['PageHeight'].unique()[0])
                page_Width = int(grouped_df['PageWidth'].unique()[0])
                fileRefNum = grouped_df['fileRefNum'].unique()[0]
                #innermost_dict_7 = {'documentType':'Tawazun_Doctype','orgId':'5c495dbfffa2a85b2c19a77f'}
                innermost_dict_7 = {'documentType':'Tawazun_Doctype','orgId':'5c495dbfffa2a85b2c19a77f', \
                                'fileRefNum':grouped_df['fileRefNum'].unique()[0], \
                               'filePath':grouped_df['filePath'].unique()[0], \
                               'fileName':grouped_df['fileName'].unique()[0],
                               'pixel_list':pixel_list}

                # appending to ocr dict
                ocr_dict_each_invoice["Lines"] = clst#Lines
                ocr_dict_each_invoice["combineWords"] = []#combinedWords
                ocr_dict_each_invoice["sortedWords"] =[] #combinedWords
                ocr_dict_each_invoice["raw"] = []#combinedWords
                ocr_dict_each_invoice["pageHeight"] = page_Height
                ocr_dict_each_invoice["pageWidth"] = page_Width
                ocr_dict_each_invoice["fileRefNum"] = fileRefNum
                ocr_dict_each_invoice["obj"] = innermost_dict_7
            
                # appending to ocr output final list 
                ocr_output.append(ocr_dict_each_invoice)

    print('Dumping augmented dict!!!!')    
    #print(f'Type FINAL_OP:{type(final_output)}')
    outputData={'outputFile': ocr_output,'statusCode': '200'}
    #print('output---Data-------->>>>',outputData)
    response_dump = writeBotOutput(outputData, data, config, input)
    input=data['input']
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    with open('augmentInvoice-output.json','w') as f:
        json.dump(taskData, f)
    #from BotsIOWrite import NpEncoder
    #taskData = json.dumps(taskData,cls=NpEncoder)

    head = {'authorization': data['token'], 'content-type': "application/json"}
    print('requestURL-----------------',config['requestURL'])
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    #dump_json = json.dumps(request.json)
    #test_json_load = json.loads(dump_json)
    #print(f'Dump json---:\n{test_json_load}')

    #response_dump = writeBotOutput(outputData, data, config, input)

    print('EXITING AUGMENT FUNCTION!!!')
    return json.dumps(request.json)

@app.route('/gibots-pyapi/writeAugmentedCsvApi',methods=['GET', 'POST'])
def writeAugmentedCsvApi():
    data=request.json
    print(f'WRITE AUGMENTED CSV data:-\n')
    #print(data)
    try:
        input = data['input']
        filePath = input['filePath']
        directions = input['directions']
        print(f'WRITING CSV FN filepath: {filePath}')
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    try:
        df_property=pd.read_csv(filePath)
        #=========REMOVE undefined property===============================
        #df_property = df_property[df_property['property']!='undefined']
        
        print('WriteAugment function read csv correctly...')
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    try:
        #op_json_filepath = str(input['extractFeatures_op'])
        #============== remove "/isLocal" from json filepath (eg ".json/isLocal")
        #with open(op_json_filepath[:-8]) as f:
        #    op_data = json.load(f)
            #WRONG-->op_data = json.loads(op_json_filepath[:-8])
        op_data = input['extractFeatures_op']
        print('Read output from extractFeatures bot successfully')
        #print(f'==extractFeatures_op key:\n {op_json_filepath} ')
        print(f"=======EXTRACTfeatures OUTPUT size:-\n{len(op_data)}")
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Could not read output from extractFeatures bot'})
    
    features = df_property.columns.tolist()
    #print(f'extractFEATURES OUTPUT:-\n{op_data}')
    print(f"*****LEN OP_DATA:{len(op_data)}")
    
    #=========MAP DICT FOR PROPERTY NAME==========
    #df_property['Name'] = df_property['Name'].apply(lambda x: str(x).strip())
    #mydict = dict(zip(df_property.Name, df_property.property))
    
    skipped_count=0
    df_output = pd.DataFrame(columns = features)
    for i in range(len(op_data)):
        #print(data[i])
        print(f"ITERATION:{i}----LEN DOCFEATURES:{len(op_data[i]['docFeatures'])}")
        #=========skip operations if docfeatures is empty
        if len(op_data[i]['docFeatures'])==0:
            print(f'skipping index {i}')
            skipped_count+=1
            continue
        #print(f'KEYS OF DOCFEATURES:{op_data[i]["docFeatures"]}')   
        #print(f"OPDATA[OBJ]:{op_data[i]['obj']}")
        # convert extra docFeatures dict to dataframe
        df_final = pd.DataFrame(op_data[i]['docFeatures'], columns = features)
        df_final['fileRefNum'] = op_data[i]['obj']['fileRefNum']
        df_final['filePath'] = op_data[i]['obj']['filePath']
        df_final['fileName.1'] = df_final['fileName'] = op_data[i]['obj']['fileName']
        pixel_list = op_data[i]['obj']['pixel_list']
        '''
        filename = ('.').join(df_final.loc[0]['filePath'].split(os.sep)[-1].split('.')[:-1])
#     print(filename)
        ref_no = df_final.loc[0]['fileRefNum']
    
        res=''.join(filename.split(ref_no))[1:]+'.pdf'          #get diff

        print(res.strip())
        df_final['fileName.1'] = df_final['fileName'] = res.strip()
        '''
        #print(f"{df_final.shape}-----\n{op_data[i]['obj']['fileRefNum']}---------\nunique fileREFnum:-{len(df_property['fileRefNum'].unique())}")
        #print(f"**DF FINAL PROP SHAPE:{df_final['property'].shape}------DF_PROP SHAPE:{df_property[df_property['fileRefNum']==op_data[i]['obj']['fileRefNum']]['property'].shape}")
        #==============MAP PROPERTY FIELDS FOR AUGMENTED DATA===================
        df_final['Name'] = df_final['Name'].apply(lambda x: str(x).strip())
        #df_final['property_map'] = df_final['Name'].replace(mydict)
        #df_final.update(df_final['Name'].map(mydict).rename('property_map'))
        
        #df_final['property'] = df_property[df_property['fileRefNum']==op_data[i]['obj']['fileRefNum']]['property']
        #print(f"**DF PROP SHAPE:{df_property[df_property['fileRefNum']==df_final['fileRefNum']]['property'].shape}------DF FINAL SHAPE:{df_final.shape}")
        # df_property = df_property.drop_duplicates(subset=['Name','index'], keep="first")
        # print(f"**AFTER DROP DUPLICATES:{df_property.shape}")
        # df_final['property']=df_property[df_property['Name']==df_final['Name']]['property']
        
        df_output=df_output.append(df_final, ignore_index=True)
    
    #=======APPEND ORIGINAL CSV===========
    df_property['Name'] = df_property['Name'].apply(lambda x: str(x).strip())
    df_output=df_output.append(df_property, ignore_index=True)
    df_output['property'].fillna('undefined',inplace=True)
    #=======FILL EMPTY INDEX COLUMNS======
    grouped_invoices_df = df_output.groupby('filePath')
    final_df = pd.DataFrame()
    for filePath_values, grouped_df in grouped_invoices_df:
        grouped_df['index'] = np.arange(1, len(grouped_df)+1)
        final_df = final_df.append(grouped_df)

    #convert pixel list to str to be used in filename of augmented csv
    pixel_list_str = '_'.join(map(str,pixel_list))

    final_csv_path = config['uploadFilePath2']+f"augmented_{directions}_{pixel_list_str}_{filePath.split('/')[-1]}"
    final_df.to_csv(final_csv_path,index=False)#,mode='a')
    print(f'SKIPPED COUNT:{skipped_count}')
    #final_csv_path = '/var/www/cuda-fs/AfterSpaces_Landmark_trainData.csv' 
    #test_output = {'KEY_TESTING': 'value_testing'}
    outputData={'outputFile': final_csv_path,'statusCode': '200'}
    #print('output---Data-------->>>>',outputData)

    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    print('requestURL-----------------',config['requestURL'])
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    #dump_json = json.dumps(request.json)
    #test_json_load = json.loads(dump_json)
    #print(f'Dump json---:\n{test_json_load}')
    print('EXITING WRITE CSV FUNCTION!!!!')
    return json.dumps(request.json)

@app.route('/gibots-pyapi/divideCsv',methods=['GET', 'POST'])
def divideCsv():
    data=request.json
    try:
        input = data['input']
        filePath = input['filePath']
        print(f'Path of CSV to be divided: {filePath}')
    except Exception as e:
        print(e)
        return json.dumps({'status':400 , 'info':'Please upload valid File'})
    df=pd.read_csv(filePath)
    grouped_df = df.groupby('fileName')

    i=1
    filePaths_array = []
    sample_df = pd.DataFrame()
    for fileNames, grp_df in grouped_df:
        sample_df = sample_df.append(grp_df)
        if i%50==0 or i==int(df.fileName.nunique()):
            fileName = os.path.basename(filePath)
            sample_df.to_csv(f"{fileName.split('.')[0]}_{i}.csv",index=False)
            filePaths_array.append(f"{fileName.split('.')[0]}_{i}.csv")
            print(f"Saving {i} files data in {fileName.split('.')[0]}_{i}.csv")
            sample_df = pd.DataFrame()
        i+=1
    
    outputData = {'filePaths_array': filePaths_array, 'array_length':int(len(filePaths_array)),'statusCode': '200'}
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    print('requestURL-----------------',config['requestURL'])
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    print('Divided main csv into sampled csv of size 50.....')
    return json.dumps(request.json)


import requests
import tracemalloc
import re
import random
import subprocess

import time
import psutil
process = psutil.Process(os.getpid())

pub_path = config['uploadFilePath']
pub_url = config['pub_url']

@app.route('/gibots-pyapi/ramco_prediction',methods = ['POST'])
def ramco_layoutv2_pred():
    T_ = time.time()
    print('\n'+'-'*25+'memory `1 -->',(process.memory_info().rss)/1048576, '\n')
    data=request.json
    print(f"input_data-----------{data}")
   
    print("[INFO] running process on -> ", data['input']['mlInput']['filePath'])

    input=data['input']['mlInput']

    got_input = {'orgId': input['orgId'], 'gstin': input['gstin'], 'subscriberId': input['subscriberId'],'documentType': input['documentType'],"modelType":input["modelType"] }
    head = {'authorization': data['token'], 'content-type': "application/json"}

    timestamp = str(time.time())

    with open("file_event_"+timestamp+".json", "w") as f:
        json.dump(data, f)

    f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
        "/home/anil/HDD/new_conda/envs/layoutv2/bin/python ramco_prediction_api.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True)))

    print(f_)

    outputML = json.load(open("file_"+timestamp+".json", "r"))

    os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
    os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")


    input=data['input']
    outputData={'mlOutput':outputML, 'statusCode': '200'}

    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'],'statusCode':'200' }
    print(f"task_data------{taskData}")
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    gc.collect(generation=0)
    gc.collect(generation=1)
    gc.collect(generation=2)

    print("-"*100)
    print('\nmemory `6 -->',(process.memory_info().rss)/1048576, '\n')
    print("[INFO] \t Total Time ", T_-time.time())

    return jsonify(outputData)
    
    
@app.route('/gibots-pyapi/mlPrediction',methods=['GET', 'POST'])
def mlPrediction():
    print('using this api mlPrediction')
    try:
        data=request.json
        
        #from prediction_testing import fieldDetectionTawazunApi
        print(data)
        input =data['input']
        mlInput = input['mlInput']
        model_name = input['mlModel'].lower()
        print(f"model_name---------{model_name}")
        #print(yes)
        try:
            filePath=mlInput['filePath']
            print(filePath)
        except Exception as e:
            print(e)
            raise Exception('Please upload valid File')
        try:
            modelType=mlInput['modelType']    
        except Exception as e:
            print(e)
            raise Exception('Model type invalid')
        try:
            documentType=mlInput['documentType']    
        except Exception as e:
            print(e)
            raise Exception('Document type invalid')
        try:
            orgId=mlInput['orgId']
        except Exception as e:
            print(e)
            raise Exception('Invalid organization')
        try:
            df=pd.read_csv(filePath)
        except Exception as e:
            print(e)
            raise Exception('Please upload valid File')
            
        #######################################################
        
        timestamp = str(time.time())

        with open("file_event_"+timestamp+".json", "w") as f:
            json.dump(data['input']['mlInput'], f)

        #model_name = "xgboost"
        if model_name == "layoutlm":
            print(f"Calling {model_name} for prediction......!!!!")
            f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
            "/home/ubuntu/anaconda3/envs/layoutlm/bin/python ramco_prediction_api.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True , universal_newlines=True)))
        else:
            print(f"Calling {model_name} for prediction......!!!!")
            f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
            "/home/ubuntu/anaconda3/bin/python tawazun_prediction_api.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True , universal_newlines=True)))
        
        print('FOUND SUBPROCESS DATA FROM TAWAZUN API----')
        print(f_)
        print('**'*50)
        
        result = json.load(open("file_"+timestamp+".json", "r"))
        
        print('Final output from fieldDetectorTawazun api -----',result)
        os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
        os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")

        
        #result=fieldDetectionTawazunApi(mlInput)
        
        print('Final output from fieldDetectorTawazun api -----',result)
        outputData={'mlOutput':result , 'statusCode': '200'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        print(taskData)
        response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)

        return jsonify(outputData)

    except Exception as e:
        print(e)
        outputData={'output':str(e), 'statusCode': '202'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)

        return jsonify(outputData)


 ############## Yolo segmentation bot ##########
 

# config_file_path = '/home/server/scanning/python-server/msme-prod-python/app/test/config.json'
# config = {}
# with open(config_file_path) as f:
#     config = json.load(f)
    
# @app.route('/gibots-pyapi/receipt_segmentation_bot1', methods=['GET','POST'])
# def predict():
#     try:
#         data = request.json
#         print('Input :',data)
#         input = data['input']
# 		#print('\nInput file:',input['doc_location'])
#         got_input = {'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'],'iterationId': data['iterationId'] }
#         head = {'authorization': data['token'], 'content-type': "application/json"}
#         response = requests.request("POST", config['acknowledgeURL'],verify=False, json=got_input, headers=head)
#         print("acknowledge api status --- ",response.status_code)
        
        
#         from detect import run
#         print('\nImport of function "run" from Yolov5/detect successful!')
#         try:
#             source = input['doc_location'] #image to detect upon
#             imagePath = input['imagePath']
#             model = config['model_location'] # trained model
#             conf_thresh = config['conf_thresh'] # confidence threshold
# 			#device = input['device'] # device (cpu or cuda to use, cuda is default)
			
#             pred = run(weights=model, source=imagePath, conf_thresh=conf_thresh, save_txt=True, save_crop=True)
			
#             outputData={'output':pred , 'statusCode': '200'}
#             print('output---Data-------->>>>',outputData)
#             taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
#             head = {'authorization': data['token'], 'content-type': "application/json"}
#             print('requestURL-----------------',config['requestURL'])
#             response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
#             print('\n\nReceipt segmentation completed.\n')
#         except Exception as e:
#             print(f'Error occured with image:{sample}.\nError: {e}\n\n')
            
    # except Exception as e2:
    #     print(f'\nError at prediction start: {e2}\n')

import requests
from flask import Flask, request, jsonify
@app.route('/gibots-pyapi/receipt_segmentation_bot1', methods=['GET','POST'])
def predict():
    T_ = time.time()
    print('\n'+'-'*25+'memory `1 -->',(process.memory_info().rss)/1048576, '\n')
    
    data = request.json
    #print('Input :',data)
    input = data['input']
    #print('\nInput file:',input['doc_location'])
    got_input = {'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'],'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", config['acknowledgeURL'],verify=False, json=got_input, headers=head)
    print("acknowledge api status --- ",response.status_code)

    timestamp = str(time.time())
    
    with open("file_event_"+timestamp+".json", "w") as f:
        json.dump(data, f)
   # print("json loaded for output")

    # str(data['input']['ImagesPath_Array'][-1]['imageFilePath'])
    f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
        "/home/server/scanning/env/y52/bin/python test_yolo.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True)))



    print(f_)

    yolooutput = json.load(open("file_"+timestamp+".json", "r"))
    #outputData = json.load(open("file_"+timestamp+".json", "r"))
    print('\nYOLOOUTPUT:',yolooutput,'\n')
    os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
    os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")

    input=data['input']
    taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': yolooutput, 'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)
    gc.collect(generation=0)
    gc.collect(generation=1)
    gc.collect(generation=2)

    print("-"*100)
    print('\nmemory `6 -->',(process.memory_info().rss)/1048576, '\n')
    print("[INFO] \t Total Time ", T_-time.time())

    return jsonify(yolooutput)
    
    
################################################################################################# Jsw Yolo code #################################################

@app.route('/gibots-pyapi/jswyolo_ocr_detection',methods=['GET', 'POST'])
def jswyolo_ocr_detection():

    T_ = time.time()
    print('\n'+'-'*25+'memory `1 -->',(process.memory_info().rss)/1048576, '\n')
    
    data = request.json
    if 'imagePath' in data['input'] and '/home/anil/HDD/www/msme42-fs' in data['input']['imagePath']:
        data['input']['imagePath'] = data['input']['imagePath'].replace('/home/anil/HDD/www/msme42-fs','/home/server/scanning')
    elif 'imagePath' in data['input'] and '/home/anil/JSW/CYLINDER' in data['input']['imagePath']:
        data['input']['imagePath'] = data['input']['imagePath'].replace('/home/anil/JSW/CYLINDER','/home/server/scanning/CYLINDER')
    print('Input :==================',data)
    input = data['input']
    acknowledgeURL = 'gibots-orch/orchestrator/acknowledge'
    if 'orch_url' in input:
        acknowledgeURL = input['orch_url']+acknowledgeURL
    else:
        acknowledgeURL = config['acknowledgeURL']
    #print('\nInput file:',input['doc_location'])
    got_input = {'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'],'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", acknowledgeURL, verify=False, json=got_input, headers=head)
    print("acknowledge api status --- ",response.status_code)


    with semaphore_jsw:
        timestamp = str(time.time())


        with open("file_event_"+timestamp+".json", "w") as f:
            json.dump(data, f)
        
        # str(data['input']['ImagesPath_Array'][-1]['imageFilePath'])
        f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
            "/home/ubuntu/anaconda3/envs/yolov52/bin/python JSW2.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True)))

        print(f_)

        yolooutput = json.load(open("file_"+timestamp+".json", "r"))

        os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
        os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")



        input=data['input']
        ioWriteURL = 'gibots-orch/orchestrator/botsiowrite'
        if 'orch_url' in input:
            ioWriteURL = input['orch_url']+ioWriteURL
        else:
            ioWriteURL = config['requestURL']

        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': yolooutput, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        response = requests.request("POST", ioWriteURL, verify=False, json=taskData, headers=head)
        gc.collect(generation=0)
        gc.collect(generation=1)
        gc.collect(generation=2)

        print("-"*100)
        print('\nmemory `6 -->',(process.memory_info().rss)/1048576, '\n')
        print("[INFO] \t Total Time ", T_-time.time())

        return jsonify(yolooutput)

################################################################################################# Symbol_detection_Yolo code #################################################

@app.route('/gibots-pyapi/symbol_detection',methods=['GET', 'POST'])
def symbol_detection():

    T_ = time.time()
    print('\n'+'-'*25+'memory `1 -->',(process.memory_info().rss)/1048576, '\n')
    
    data = request.json
    print("input_received --- ",data)
    if 'imageArr' in data['input']:
        for img in data['input']['imageArr']:
            img['imageFilePath'] = img['imageFilePath'].replace('/home/anil/HDD/www/msme42-fs','/home/server/scanning/msme42-fs').replace('/home/anil/JSW/CYLINDER','/home/server/scanning/CYLINDER')
    #print('Input :==================',data)
    input = data['input']
    acknowledgeURL = 'gibots-orch/orchestrator/acknowledge'
    if 'orch_url' in input:
        acknowledgeURL = input['orch_url']+acknowledgeURL
    else:
        acknowledgeURL = config['acknowledgeURL']
    print('\nInput file:',acknowledgeURL,data)
    got_input = {'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'],'iterationId': data['iterationId'] }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", acknowledgeURL, verify=False, json=got_input, headers=head)
    print("acknowledge api status --- ",response.status_code)


    with semaphore_jsw:
        timestamp = str(time.time())


        with open("file_event_"+timestamp+".json", "w") as f:
            json.dump(data, f)
        
        print("/home/ubuntu/anaconda3/envs/yolov52/bin/python symbol_detection.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp)
        f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
            "/home/ubuntu/anaconda3/envs/yolov52/bin/python symbol_detection.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True)))

        print(f_)

        yolooutput = json.load(open("file_"+timestamp+".json", "r"))
    
        os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
        os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")



        input=data['input']
        ioWriteURL = 'gibots-orch/orchestrator/botsiowrite'
        if 'orch_url' in input:
            ioWriteURL = input['orch_url']+ioWriteURL
        else:
            ioWriteURL = config['requestURL']
            
        yolooutput['uplodeStatus'] = True
        yolooutput['statusCode'] = '200'
        yolooutput['Documenttype'] = input['Documenttype']
        yolooutput['Filerefnum'] = input['Filerefnum']

        modPath = []
        for csvpath in yolooutput['csv_data'] : 
            csvpath = csvpath.replace('/home/server/scanning/msme42-fs','/home/anil/HDD/www/msme42-fs').replace('/home/server/scanning/CYLINDER','/home/anil/JSW/CYLINDER')   
            modPath.append(csvpath)
            
        yolooutput['csv_data'] = modPath
        
        for imgPath in yolooutput['newImgArr'] : 
            if 'imageFilePath' in imgPath:
                imgPath['imageFilePath'] = imgPath['imageFilePath'].replace('/home/server/scanning/msme42-fs','/home/anil/HDD/www/msme42-fs').replace('/home/server/scanning/CYLINDER','/home/anil/JSW/CYLINDER')   
        
        print(yolooutput)      
    
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': yolooutput, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        print(ioWriteURL,taskData)
        response = requests.request("POST", ioWriteURL, verify=False, json=taskData, headers=head)
        gc.collect(generation=0)
        gc.collect(generation=1)
        gc.collect(generation=2)

        print("-"*100)
        print('\nmemory `6 -->',(process.memory_info().rss)/1048576, '\n')
        print("[INFO] \t Total Time ", T_-time.time())

        return jsonify(yolooutput)



    

    

################################################################################################# Symbol_detection_Owlv2 code #################################################

@app.route('/gibots-pyapi/symbol_detection_owlv2',methods=['GET', 'POST'])
def symbol_detection_owlv2():

    T_ = time.time()
    data = request.json
    print("input_received --- ", data)

    if 'imageArr' in data['input']:
        for img in data['input']['imageArr']:
            img['imageFilePath'] = img['imageFilePath'].replace(
                '/home/anil/HDD/www/msme42-fs', '/home/server/scanning/msme42-fs').replace(
                '/home/anil/JSW/CYLINDER', '/home/server/scanning/CYLINDER')

    input = data['input']
    acknowledgeURL = 'gibots-orch/orchestrator/acknowledge'
    if 'orch_url' in input:
        acknowledgeURL = input['orch_url'] + acknowledgeURL
    else:
        acknowledgeURL = config['acknowledgeURL']

    got_input = {
        'projectId': data['projectId'], 'botId': data['botId'],
        'eventId': input['eventId'], 'iterationId': data['iterationId']
    }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", acknowledgeURL, verify=False, json=got_input, headers=head)
    print("acknowledge api status --- ", response.status_code)

    with semaphore_jsw:
        timestamp = str(time.time())

        with open("file_event_" + timestamp + ".json", "w") as f:
            json.dump(data, f)
        
        command = f"/home/ubuntu/anaconda3/envs/owlv2_env/bin/python owlv2.py -i file_event_{timestamp}.json -t {timestamp}"
        print(command)

        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')
            error_output = result.stderr.decode('utf-8')
            print("Command output:", output)
            print("Command error output:", error_output)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running command: {e.stderr.decode('utf-8')}")
            return jsonify({"error": "Failed to process image", "details": e.stderr.decode('utf-8')}), 500

        yolooutput = json.load(open(f"file_{timestamp}.json", "r"))

        os.remove(os.getcwd() + f"/file_{timestamp}.json")
        os.remove(os.getcwd() + f"/file_event_{timestamp}.json")

        input = data['input']
        ioWriteURL = 'gibots-orch/orchestrator/botsiowrite'
        if 'orch_url' in input:
            ioWriteURL = input['orch_url'] + ioWriteURL
        else:
            ioWriteURL = config['requestURL']

        yolooutput['uplodeStatus'] = True
        yolooutput['statusCode'] = '200'
        yolooutput['Documenttype'] = input['Documenttype']
        yolooutput['Filerefnum'] = input['Filerefnum']

        modPath = []
        for csvpath in yolooutput['csv_data']:
            csvpath = csvpath.replace('/home/server/scanning/msme42-fs', '/home/anil/HDD/www/msme42-fs').replace(
                '/home/server/scanning/CYLINDER', '/home/anil/JSW/CYLINDER')
            modPath.append(csvpath)

        yolooutput['csv_data'] = modPath

        for imgPath in yolooutput['newImgArr']:
            if 'imageFilePath' in imgPath:
                imgPath['imageFilePath'] = imgPath['imageFilePath'].replace(
                    '/home/server/scanning/msme42-fs', '/home/anil/HDD/www/msme42-fs').replace(
                    '/home/server/scanning/CYLINDER', '/home/anil/JSW/CYLINDER')

        print(yolooutput)

        taskData = {
            'projectId': data['projectId'], 'botId': data['botId'],
            'eventId': input['eventId'], 'status': 'Complete',
            'outputParameters': yolooutput, 'iterationId': data['iterationId']
        }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        response = requests.request("POST", ioWriteURL, verify=False, json=taskData, headers=head)
        print(ioWriteURL, taskData)
        print("[INFO] \t Total Time ", T_ - time.time())

        return jsonify(yolooutput)


################################################################################################# Symbol_detection_Paligemma code #################################################

@app.route('/gibots-pyapi/symbol_detection_paligemma',methods=['GET', 'POST'])
def symbol_detection_paligemma():

    T_ = time.time()
    data = request.json
    print("input_received --- ", data)

    if 'imageArr' in data['input']:
        for img in data['input']['imageArr']:
            img['imageFilePath'] = img['imageFilePath'].replace(
                '/home/anil/HDD/www/msme42-fs', '/home/server/scanning/msme42-fs').replace(
                '/home/anil/JSW/CYLINDER', '/home/server/scanning/CYLINDER')

    input = data['input']
    acknowledgeURL = 'gibots-orch/orchestrator/acknowledge'
    if 'orch_url' in input:
        acknowledgeURL = input['orch_url'] + acknowledgeURL
    else:
        acknowledgeURL = config['acknowledgeURL']

    got_input = {
        'projectId': data['projectId'], 'botId': data['botId'],
        'eventId': input['eventId'], 'iterationId': data['iterationId']
    }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    response = requests.request("POST", acknowledgeURL, verify=False, json=got_input, headers=head)
    print("acknowledge api status --- ", response.status_code)

    with semaphore_jsw:
        timestamp = str(time.time())

        with open("file_event_" + timestamp + ".json", "w") as f:
            json.dump(data, f)
        
        command = f"/home/ubuntu/anaconda3/envs/owlv2_env/bin/python paligemma.py -i file_event_{timestamp}.json -t {timestamp}"
        print(command)

        try:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')
            error_output = result.stderr.decode('utf-8')
            print("Command output:", output)
            print("Command error output:", error_output)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred while running command: {e.stderr.decode('utf-8')}")
            return jsonify({"error": "Failed to process image", "details": e.stderr.decode('utf-8')}), 500

        yolooutput = json.load(open(f"file_{timestamp}.json", "r"))

        os.remove(os.getcwd() + f"/file_{timestamp}.json")
        #os.remove(os.getcwd() + f"/file_event_{timestamp}.json")

        input = data['input']
        ioWriteURL = 'gibots-orch/orchestrator/botsiowrite'
        if 'orch_url' in input:
            ioWriteURL = input['orch_url'] + ioWriteURL
        else:
            ioWriteURL = config['requestURL']

        yolooutput['uplodeStatus'] = True
        yolooutput['statusCode'] = '200'
        yolooutput['Documenttype'] = input['Documenttype']
        yolooutput['Filerefnum'] = input['Filerefnum']

        modPath = []
        for csvpath in yolooutput['csv_data']:
            csvpath = csvpath.replace('/home/server/scanning/msme42-fs', '/home/anil/HDD/www/msme42-fs').replace(
                '/home/server/scanning/CYLINDER', '/home/anil/JSW/CYLINDER')
            modPath.append(csvpath)

        yolooutput['csv_data'] = modPath

        for imgPath in yolooutput['newImgArr']:
            if 'imageFilePath' in imgPath:
                imgPath['imageFilePath'] = imgPath['imageFilePath'].replace(
                    '/home/server/scanning/msme42-fs', '/home/anil/HDD/www/msme42-fs').replace(
                    '/home/server/scanning/CYLINDER', '/home/anil/JSW/CYLINDER')

        print(yolooutput)

        taskData = {
            'projectId': data['projectId'], 'botId': data['botId'],
            'eventId': input['eventId'], 'status': 'Complete',
            'outputParameters': yolooutput, 'iterationId': data['iterationId']
        }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        response = requests.request("POST", ioWriteURL, verify=False, json=taskData, headers=head)
        print(ioWriteURL, taskData)
        print("[INFO] \t Total Time ", T_ - time.time())

        return jsonify(yolooutput)


@app.route('/gibots-pyapi/TextfileGeneration',methods=['GET', 'POST'])
def TextfileGeneration():
    # sem.acquire()
    print('using this api TextfileGeneration')
    try:
        data=request.json
        input =data['input']
        combineLines = input['combineLines']
        file_name = data['input']['fileName']
        print('------------filename---', file_name)
        '''config_value = input['configValue'] #config values coming from bot input
        if config_value:
            print (config_value)
            config_value = config_value.replace("'", "\"")
            config_value_json = json.loads(config_value)
            print("config_json",config_value_json)
            print("MOunt_path",config_value_json['mountpath'])
            data['input']['config_value_json'] = config_value_json'''
        if(type(combineLines) == str and combineLines.find('isLocal') != -1):
            file = combineLines.replace('/isLocal','')
            file = file.replace('../javaJsonFolder/','/home/ubuntu/new_ssd/aiqod-staging-job/javaJsonFolder/')
            # if not config_value_json:
            #     file = file.replace('/home/anil/HDD/www/msme42-fs/','/home/user/')
            # else:
            #     file = file.replace(config_value_json['mountpath'],'/home/user/')
            file_opn = open(file,'r')
            combineLines = json.load(file_opn)
            file_opn.close()
            data['input']['combineLines'] = combineLines
            print ('Loaded from json', len(combineLines))
        
        #print(yes)
        try:
            filePath=data['input']['fileName']
            print(filePath)
        except Exception as e:
            print(e)
            raise Exception('Please upload valid File')
        
        
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
            for i,page in enumerate(html_content):
                res = html_to_positioned_text(page)
                output += res+f'\n--------------PAGE Number: {i+1}. END OF PAGE-----------------------\n'
            return output

        output = process_document_layout(combineLines)
        if not output:
            return json.dumps({'status':400 , 'info':'No data'})

        image_file_name = os.path.splitext(os.path.basename(file_name))[0]
        print('File name---',image_file_name)
        filename = f"{image_file_name}.txt"
        file_path = '/home/ubuntu/new_ssd/publicfolder/liberty-fs/handbook/'+filename
        
        with open(file_path, "w") as file:
            file.write(output)
        print('output filepath--------------',file_path)
        try:
            outputData = {'mlOutput':file_path,'statusCode':'200'}
        except Exception as e:
            print (e)
            outputData={'mlOutput':'Please upload valid File' , 'statusCode': '400'}
            

        
        outputData = {'mlOutput':'Done','statusCode':'200','txtFilePath':file_path,'docText':output.replace('\n','\\n')}

        
        #outputData['Execution_time'] = "{:.6f}".format(execution_time)
        #torch.cuda.empty_cache()
        #outputData={'mlOutput':'done' , 'statusCode': '200'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        print('response ------------------->',taskData)

        '''if 'requestURL' in config_value_json:
            response = requests.request("POST", config_value_json['requestURL'], json=taskData, headers=head)
        else:'''
        response = requests.request("POST", config['requestURL'], json=taskData, headers=head)

        return json.dumps(outputData)

    except Exception as e:
        # sem.release()
        import torch, gc
        #gc.collect()
        torch.cuda.empty_cache()
        print('ERROR: error in GEN Ai !!!',traceback.format_exc())
        print(e)
        outputData={'output':str(e), 'statusCode': '202'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        response = requests.request("POST", config['requestURL'],verify=False, json=taskData, headers=head)

        return json.dumps(outputData)


#Resume Extraction
import time
@app.route('/gibots-pyapi/resume_extraction',methods=['GET', 'POST'])

def resume_extraction():

    T_ = time.time()
    #print('\n'+'-'*25+'memory `1 -->',(process.memory_info().rss)/1048576, '\n')
    
    data = request.json
    t0 = time.time()
    print("input_data----->>",data)
    
    input=data['input']
    acknowledgeURL = 'gibots-orch/orchestrator/acknowledge'
    
    timestamp = str(time.time())
  
    print(json.dumps(request.json, indent=2))
    
    event_filename = f"file_event_{timestamp}.json"

    with open(event_filename, "w") as f:
        json.dump(data, f)
     # Run subprocess
    try:
        subprocess_output = subprocess.check_output(
            "/home/ubuntu/.conda/envs/python38/bin/python  resume_extraction.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp,
            shell=True
        )
        print(subprocess_output.decode())
        f_ = re.sub(r"b'|\\\\n'", '', str(subprocess_output))
    except subprocess.CalledProcessError as e:
        print("Subprocess failed:", e)
        return jsonify({"status": "error", "message": "Resume processing failed"}), 500

    output_filename = f"file_{timestamp}.json"
 
    # Safely try to load the output JSON
    if not os.path.exists(output_filename):
        print("No valid resume data extracted. Skipping...")
        return jsonify({"status": "skipped", "message": "No valid resume data extracted."}), 200

    with open(output_filename, "r") as f:
        output_r = json.load(f)

#    f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
#       "/home/ubuntu/.conda/envs/python38/bin/python  resume_extraction.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True)))

#    output_r = json.load(open("file_"+timestamp+".json", "r"))
    
#    os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
#    os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")
    import torch, gc
    gc.collect()
    torch.cuda.empty_cache()

    
    ioWriteURL = 'gibots-orch/orchestrator/botsiowrite'
    if 'orch_url' in input:
        ioWriteURL = input['orch_url']+ioWriteURL
    else:
        ioWriteURL = 'http://172.168.1.19:8992/gibots-orch/orchestrator/botsiowrite' #config['requestURL']
    
    taskData = {
        'projectId': data['projectId'],
        'botId': data['botId'],
        'eventId': input['eventId'],
        'status': 'Complete',
        'outputParameters': output_r,
        'iterationId': data['iterationId']
    }
    head = {'authorization': data['token'], 'content-type': "application/json"}
    try:
        response = requests.request("POST", ioWriteURL, verify=False, json=taskData, headers=head)
        response.raise_for_status()
        print("Response from Server: ", response.text)
    except requests.exceptions.RequestException as e:
        print(f"POST request failed: {e}")

    gc.collect(generation=0)
    gc.collect(generation=1)
    gc.collect(generation=2)
    
    t1 = time.time()
    total_time = round(t1-t0,2)

    print("Total_time taken to extract resume datas : ",total_time) 
    print("Output Data: ", output_r)
    print("-"*100)

    return json.dumps(output_r,default=str)
 





if __name__=='__main__':
    app.run('0.0.0.0',config["python-port"])
    
    
    
    
    
    
   

