import os
import re
import subprocess
import time
import traceback
from flask_cors import CORS, cross_origin
import json
import requests

conf={}
with open('config.json', 'r') as f:
    conf = json.load(f)
    print('config loaded')
from flask import *

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/gibots-pyapi/genai_prediction',methods=['GET', 'POST'])
def genai_prediction():
    # sem.acquire()
    print('using this api mlPrediction')
    try:
        data=request.json
        input =data['input']
        mlInput = input['mlInput']
        combineLines = input['combineLines']
        ai_model_name = input['ai_model_name']
        ref_no = input['refNo']
        config_value = input['configValue']
        if(type(mlInput) == str and mlInput.find('isLocal') != -1):
            file = mlInput.replace('/isLocal','')
            file_opn = open(file,'r')
            mlInput = json.load(file_opn)
            file_opn.close()
            data['input']['mlInput'] = mlInput
            print ('Loaded from json', len(mlInput))

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
        
        from genai_online_royal_dev import fieldDetection
        '''
        with open("file_event_"+timestamp+".json", "w") as f:
            json.dump(data, f)

        f_ = re.sub('b\'|\\\\n\'', '', str(subprocess.check_output(
             "/home/user/anaconda3/envs/genai-online/bin/python genai_online.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True , universal_newlines=True)))
        print('FOUND SUBPROCESS DATA FROM TAWAZUN API----')
        print(f_)
        print('**'*50)

        outputData = json.load(open("file_"+timestamp+".json", "r"))
        #done by yuvraj shankar
        '''
        outputData = fieldDetection(data,timestamp)
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
        if input.get('return',False):
            return json.dumps(outputData)
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
            "/home/user/anaconda3/envs/demo-python-img/bin/python ml_prediction_api.py -i "+ "file_event_"+timestamp+".json" + " -t " + timestamp, shell=True , universal_newlines=True)))
        
        print('FOUND SUBPROCESS DATA FROM TAWAZUN API----')
        print(f_)
        print('**'*50)
        
        result = json.load(open("file_"+timestamp+".json", "r"))
        
        print('Final output from fieldDetectorTawazun api -----',result)
        os.system("rm "+os.getcwd()+"/file_"+timestamp+".json")
        os.system("rm "+os.getcwd()+"/file_event_"+timestamp+".json")

        
        #result=fieldDetectionTawazunApi(mlInput)
        
        print('Final output from fieldDetectorTawazun api -----',result)
        outputData={'mlOutput':result ,'template_found': result['isTmp'],'isTmp':result['isTmp'], 'statusCode': '200'}
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


@app.route('/gibots-pyapi/TextfileGeneration',methods=['GET', 'POST'])
def TextfileGeneration():
    # sem.acquire()
    print('using this api TextfileGeneration')
    try:
        data=request.json
        input =data['input']
        #mlInput = input['mlInput']
        combineLines = input['combineLines']
        #ai_model_name = input['ai_model_name']
        #ref_no = input['refNo']
        file_name = data['input']['filePath']
        print('------------filename---', file_name)
        org_filename = os.path.basename(file_name)
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
            # if not config_value_json:
            #     file = file.replace('/home/anil/HDD/www/msme42-fs/','/home/user/')
            # else:
            #     file = file.replace(config_value_json['mountpath'],'/home/user/')
            file_opn = open(file,'r')
            combineLines = json.load(file_opn)
            file_opn.close()
            data['input']['combineLines'] = combineLines
            print ('Loaded from json', len(combineLines))
        #print(input['mlInput'],input['eventId'],request.remote_addr)
        #print(yes)
        
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
            print("======",ind)
            if ind >= len(avg_height):
                print(f"Index {ind} is out of range for avg_height.")
                continue
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
                output += f'\n---PAGE NO: {ind+1}. END OF PAGE---'
        '''
        # print(output)
            # print(type(output))
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
                    f'\n--------------PAGE Number: {i+1}. END OF PAGE-----------------------\n'
            return output

        output = process_document_layout(combineLines)
        if not output:
            return json.dumps({'status':400 , 'info':'No data'})

        image_file_name = os.path.splitext(os.path.basename(file_name))[0].split('.')[0]
        print('File name---',image_file_name)
        filename = f"{image_file_name}.txt"
        file_path = '/home/user/save-data-here/public-folder/demo-files/'+filename
        output = f'Filename: {org_filename}\n Content:{output}'
        with open(file_path, "w") as file:
            file.write(output)
        print('output filepath--------------',file_path)
        try:
            outputData = {'mlOutput':file_path,'statusCode':'200'}
        except Exception as e:
            print (e)
            outputData={'mlOutput':'Please upload valid File' , 'statusCode': '400'}
            

        
        if 'return' in input:
            return json.dumps(outputData)

        
        #outputData['Execution_time'] = "{:.6f}".format(execution_time)
        #torch.cuda.empty_cache()
        #outputData={'mlOutput':'done' , 'statusCode': '200'}
        taskData = { 'projectId': data['projectId'], 'botId': data['botId'], 'eventId': input['eventId'], 'status': 'Complete', 'outputParameters': outputData, 'iterationId': data['iterationId'] }
        head = {'authorization': data['token'], 'content-type': "application/json"}
        print('response ------------------->',taskData)

        #if 'requestURL' in config_value_json:
        #    response = requests.request("POST", config_value_json['requestURL'], json=taskData, headers=head)
        #else:
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


if __name__=='__main__':
    app.run('0.0.0.0',5021)