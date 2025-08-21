import copy
import time
import requests
import json
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pymongo
with open('config.json','r') as file:
    conf_val = json.load(file)
from datetime import datetime
from werkzeug.datastructures import MultiDict

base_url = 'https://demo.aiqod.com:3443'
app = Flask(__name__)
cors = CORS(app)
myclient = pymongo.MongoClient('mongodb://domo-1:domonodel@127.0.0.1:27017/demo')
db = myclient['demo']

def convertPdfToPng(filePath, userId, orgId, subscriberId, url):
    payload = {
        "input": {
            "filePath": filePath,
            "userId": userId,
            "subscriberId": subscriberId,
            "orgId": orgId,
            "return": True
        },
        "output": {},
        "iterationId": 0,
        "functionName": "convertPdftoPng"
    }
    r = requests.post(f'{url}/gibots-api/bots/botCommonFunction', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    return r.json()

def document_preprocess(ImageFilePathArray,userId,subscriberId,orgId,url):
    payload = {
        "input": {
            "InputArray": ImageFilePathArray,
            "text_allignment_check": "yes",
            "preprocess_image": "no",
            "deskew_correction": "no",
            "stretching_document": "no",
            "ml_denoise_document": "no",
            "white_text_on_gray_check": "no",
            "userId": userId,
            "subscriberId": subscriberId,
            "orgId": orgId,
            "return": True
        },
        "output": {},
        "iterationId": 0
    }
    r = requests.post(f'{url}/gibots-pyimg/DocumentPreprocess_ocri', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    return r.json()

def get_ocr(ImagesPath_Array,fileReferenceNumber,documentType,userId,subscriberId,orgId,url):
    payload = {
        "input": {
            "ImagesPath_Array": ImagesPath_Array,
            "fileRefNum": fileReferenceNumber,
            "documentType": documentType,
            "density_threshold": 100,
            "language_identify": "English",
            "tesseract_model": "eng",
            "rec_model":"paddleocr",
            "eventId": "123129",
            "userId": userId,
            "subscriberId": subscriberId,
            "orgId": orgId,
            "return": True,
            "json_respond": True
        },
        "output": {},

        "iterationId": 0
    }
    r = requests.post(f'{url}/gibots-ocr/tesseract_ocr_wbw', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    return r.json()

def preMLOps(ocr_output,referenceNumber,userId,subscriberId,orgId,url):
    print('ocr_out',ocr_output)
    payload = {
        "input": {
            "INPUT": ocr_output,
            "fileRefNum": referenceNumber,
            "a":"4.166666667",
            "functionArray": '["combineLines","extractFeatures","saveDocTrainData","identifyTable","extractTableData","genrateCsv","runTrainingForInvoice","prepareFormData","prepareCreateSave","multiPageArray","saveObjectData"]',
            "imageFlow": None,
            "userId": userId,
            "subscriberId": subscriberId,
            "orgId": orgId,
            "return": True,
            "jsonRespond": True,
            "eventId": "1239192"
        },
            "output": {},
        "projectId": "123",
        "botId": "789",
        "iterationId": 0
    }
    r = requests.post(f'{url}/adhigam-api/website/preMlFunctions', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    return r.json()

def prediction(mlInput,runTrainingForInvoice,referenceNumber,templateName,userId,subscriberId,orgId,url):
    payload = {
        "input": {
            "mlInput": mlInput,
            "combineLines":runTrainingForInvoice,
            "ai_model_name": "gemini",
            "refNo": referenceNumber,
            "template_based": templateName,
            "configValue": "{'anchor_only':['Vendor_Name','Vendor_GSTIN'],'db':'demo','dbConnection':'mongodb://domo-1:domonodel@172.168.1.199:27017/?authSource=demo','requestURL':'http://localhost:2005/gibots-orch/orchestrator/botsiowrite','acknowledgeURL':'http://localhost:2005/gibots-orch/orchestrator/acknowledge', 'mountpath':'/home/server/scanning/'}",
            "userId": userId,
            "subscriberId": subscriberId,
            "orgId": orgId,
            "return": True,
            "eventId": ""
        },
        "output": {},

        "iterationId": 0
    }
    r = requests.post(f'{url}/gibots-pyapi/genai_prediction', data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    return r.json()

def extraction_process_steps(filePath,ref_no,doc_type,template_name,userId,orgId,subscriberId):
    # filePath = "/home/user/save-data-here/public-folder/demo-files/File5b7a65fc403397343d250dbd40ee9526_SIEMENS_LTD_nw.pdf"
    # ref_no = "File5b7a65fc403397343d250dbd40ee9526"
    # doc_type = "IMPORT"
    # userId = "67ed114950023d3c8c0ef91d"
    # orgId = "662b515be421fedde2247c47"
    # subscriberId = "5beaabd82ac6767c86dc311c"
    # template_name = "SIEMENS LTD"
    time_details = {}
    start_time = time.monotonic()
    time_details['filePath'] = filePath
    time_details['ref_no'] = ref_no
    # PDF to PNG conversion
    pdf_start = time.monotonic()
    output = convertPdfToPng(filePath, userId, subscriberId, orgId,'http://localhost:2004')
    pdf_end = time.monotonic()
    print(f"convertPdfToPng took: {pdf_end - pdf_start:.4f} seconds")
    time_details['pdf_conversion_time'] = pdf_end - pdf_start

    image_path_array = output['data']['imagesPathaaray']

    # Document preprocessing
    preprocess_start = time.monotonic()
    output = document_preprocess(image_path_array, userId, subscriberId, orgId,'http://localhost:5022')
    preprocess_end = time.monotonic()
    print(f"document_preprocess took: {preprocess_end - preprocess_start:.4f} seconds")
    time_details['preprocess_time'] = preprocess_end - preprocess_start
    output_image_array = output["outputArray"]

    # OCR
    ocr_start = time.monotonic()
    output = get_ocr(output_image_array, ref_no, doc_type, userId, subscriberId, orgId,'http://localhost:2011')
    ocr_end = time.monotonic()
    print(f"get_ocr took: {ocr_end - ocr_start:.4f} seconds")
    time_details['ocr_time'] = ocr_end - ocr_start
    ocr_output = output['ocr_output']

    # Pre-ML operations
    premlops_start = time.monotonic()
    output = preMLOps(ocr_output, ref_no, userId, subscriberId, orgId,'http://localhost:2001')
    premlops_end = time.monotonic()
    print(f"preMLOps took: {premlops_end - premlops_start:.4f} seconds")
    time_details['premlops_time'] = premlops_end - premlops_start
    mlInput = output['data']['mlInput']
    runTrainingForInvoice = output['data']['runTrainingForInvoice']

    # Prediction
    prediction_start = time.monotonic()
    output = prediction(mlInput, runTrainingForInvoice, ref_no, template_name, userId, subscriberId, orgId,'http://localhost:5021')
    prediction_end = time.monotonic()
    print(f"prediction took: {prediction_end - prediction_start:.4f} seconds")
    time_details['prediction_time'] = prediction_end - prediction_start
    end_time = time.monotonic()
    print(f"Total execution time: {end_time - start_time:.4f} seconds")
    return output, len(output_image_array), time_details

def format_result(result):
    table_details = result['multiTable']
    header_details = copy.deepcopy(result)
    del header_details['multiTable']
    del header_details['isTmp']
    del header_details['ocrConfidence']
    if 'referenceNumber' in header_details:
        del header_details['referenceNumber']
    if 'STatus' in header_details:
        del header_details['STatus']
    if 'Invoice_Status' in header_details:
        del header_details['Invoice_Status']
    if 'InvoiceStatus' in header_details:
        del header_details['InvoiceStatus']
    if 'createdAt' in header_details:
        del header_details['createdAt']
    del header_details['file_name']
    del header_details['filePath']
    del header_details['fileName']
    final_result = {}
    final_result['Headers'] = header_details
    for item in table_details:
        for tablename in item:
            final_result[tablename] = item[tablename]

    return final_result

@app.route('/aiqod-api-nw/process-file',methods=['POST','GET'])
def doc_extraction():
    try:
        current_datetime = datetime.now()
        current_time = time.monotonic()
        print('hit')
        if not 'File' in request.files:
            return jsonify({'error':'File not valid'}), 400

        if 'File' in request.files:
    # Create a new mutable MultiDict
            modified_files = MultiDict(request.files)
    # Get all files from the 'file' field
            files = modified_files.getlist('File')
    # Remove the original 'file' key
            del modified_files['File']
    # Reassign them to 'myfile'
            for f in files:
                modified_files.add('myfile', f)
            request.files = modified_files
# Format the datetime object
        start_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        api_key =  request.headers.get("ApiKey", "")
        if not api_key:
            return jsonify({'error':'API Key not provided'}), 400
        if not api_key == '8a99f6ae45abff1267d2b50eaec542f4':
            return jsonify({'error':'API Key not Valid'}), 400
        

        

        files_grouped_by_fieldname = {}
        for fieldname in request.files:
            files = request.files.getlist(fieldname)
            files_grouped_by_fieldname[fieldname] = files

        # Construct multipart/form-data
        multipart_files = []
        for fieldname, files in files_grouped_by_fieldname.items():
            for file in files:
                # (fieldname, (filename, fileobject, mimetype))
                multipart_files.append(
                    (fieldname, (file.filename, file.stream, file.mimetype))
                )

        # Add form fields
        form_data = request.form.to_dict()

        # Token and headers
        token = conf_val['token']
        if not token:
            return jsonify({'error':'Auth token not provided'}), 400
        headers = {
            "Authorization": f"{token}",
        }
        print('before scanfiedl')
        response = requests.post(
            f"http://localhost:2001/adhigam-api/mapper/scan/multi",
            files=multipart_files,
            data=form_data,
            headers=headers
        )
        print('after scanfield')
        response_data = response.json()

        # Validation logic
        job_type = form_data.get("JobType")
        pdf_client_name = form_data.get("PdfClientName")
        
        if not pdf_client_name:
            return jsonify({"error": "The PdfClientName is expected But not Provided", "msg": "Error while Uploading"}), 400
        templateData = list(
            db.get_collection("Genai_Prompt_Templates").find({
                'template_name': {
                    '$regex': f'^{pdf_client_name}$',
                    '$options': 'i'
                },
                'type': {
                    '$regex': f'^{job_type}$',
                    '$options': 'i'
                }
            })
        )

        if not templateData:
            return jsonify({"error": "Template not found", "msg": "Error while Uploading"}), 400
        
        if len(templateData)>=1:
            pdf_client_name = templateData[0]['template_name']

        
        if job_type.lower() == 'imp':
            doc_type = 'IMPORT'
        elif job_type.lower() == 'exp':
            doc_type = 'EXPORT'

        orgId = "662b515be421fedde2247c47"
        output = None
        time_details = {}
        for data in response_data['data']:
            org_file_path = data['filePath']
            ref_no = data['fileRefNum']
            user_id = data['userId']
            sub_id = data['subscriberId']
            res,pg_count,time_dets = extraction_process_steps(org_file_path,ref_no,doc_type,pdf_client_name,user_id,orgId,sub_id)
            result = res['data']
            if result and type(result) is dict:
                result['InvoiceStartTime'] = start_time
                result['InvoiceResponseTime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result['Status'] = 'Success'
                result['PdfCount'] = str(1)
                result['PageCount'] = str(pg_count)
                result['CompanyID'] = form_data.get("CompanyId") if form_data.get("CompanyId") else 'ERI00010'
                result['UserID'] = form_data.get("UserID") if form_data.get("UserID") else 'K'
                result['BranchCode'] = form_data.get("BranchCode") if form_data.get("BranchCode") else 'ACC, Chennai'
                result['JobNo'] = form_data.get("JobNo") if form_data.get("JobNo") else '123'
                result['WorkingPeriod'] = form_data.get("WorkingPeriod") if form_data.get("WorkingPeriod") else '2025-2026'
                result['FileName'] = result.get('file_name', '1')

                output = format_result(result)
                time_dets['start_time'] = start_time
                time_dets['end_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                time_dets['time_taken'] = time.monotonic() - current_time
                time_dets['page_count'] = pg_count
                time_details = time_dets
        if time_details:
            db.get_collection('RoyalTech_api_timing').insert_one(time_details)
        return jsonify(output), 200



    except Exception as e:
        print('error',e)
        return jsonify({'error':e}), 400


if __name__=='__main__':
    print('Starting extractin process')
    #
    app.run('0.0.0.0',5020)