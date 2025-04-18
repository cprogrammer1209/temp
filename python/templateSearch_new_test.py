#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import copy
import numpy as np
import traceback
import re
import json
import pandas as pd
import pymongo
from fuzzywuzzy import fuzz
import numpy as np
import multiprocessing
import collections
from bson.objectid import ObjectId

import time 
#t0 = time.time()
#Template Search function
###################################################################################################
###################################################################################################
# read keyword json
keyword_config={}
with open('keywords.json', 'r') as f:
    keyword_config = json.load(f)
keys=collections.OrderedDict(keyword_config['keywordDict'])


import os
os.makedirs('debug_csv', exist_ok = True)




predicted_bbox = []
actual_debug = []
predicted_debug = []
indexes = []

def count_digits(s):
    digits = sum(c.isdigit() for c in str(s))
    alpha = sum(c.isalpha() for c in str(s))
    return digits,alpha


def remove_strings_inside_brackets(input_string):
    # Define a regular expression pattern to match strings inside brackets
    pattern = r'\(.*?\)'
    # Use re.sub() to replace all occurrences of the pattern with an empty string
    result = re.sub(pattern, '', input_string)
    return result

def indentifiersMap(tmp_string,list_identifiers):
    contains = 0
    tmp_string = tmp_string.lower().replace(' ','')
    for i in list_identifiers:
        if i in tmp_string:
            contains = 1
            break
    return contains

def modify_list(tmp_list):
    tmp_list = [x.lower().replace(' ','') for x in tmp_list]
    return tmp_list


def get_iou(bb1, bb2):
    """
    Calculate the Intersection over Union (IoU) of two bounding boxes.

    Parameters
    ----------
    bb1 : dict
        Keys: {'leftX', 'rightX', 'topY', 'bottomY'}
        The (leftX, topY) position is at the top left corner,
        the (rightX, bottomY) position is at the bottom right corner
    bb2 : dict
        Keys: {'leftX', 'rightX', 'topY', 'bottomY'}
        The (leftX, topY) position is at the top left corner,
        the (rightX, bottomY) position is at the bottom right corner

    Returns
    -------
    float
        in [0, 1]
    """
    #print('*********')
    #print('bb1-----',bb1)
    #print('\n')
    #print('bb2------',bb2)
    #print('\n')
    
    
    try:
        assert bb1['leftX'] < bb1['rightX']
        assert bb1['topY'] < bb1['bottomY']
        #assert bb2['leftX'] < bb2['rightX']
        assert bb2['topY'] < bb2['bottomY']

        # determine the coordinates of the intersection rectangle
        x_left = max(bb1['leftX'], bb2['leftX'])
        y_top = max(bb1['topY'], bb2['topY'])
        x_right = min(bb1['rightX'], bb2['rightX'])
        y_bottom = min(bb1['bottomY'], bb2['bottomY'])

        if x_right < x_left or y_bottom < y_top:
            return 0.0

        # The intersection of two axis-aligned bounding boxes is always an
        # axis-aligned bounding box
        intersection_area = (x_right - x_left) * (y_bottom - y_top)

        # compute the area of both AABBs
        bb1_area = (bb1['rightX'] - bb1['leftX']) * (bb1['bottomY'] - bb1['topY'])
        bb2_area = (bb2['rightX'] - bb2['leftX']) * (bb2['bottomY'] - bb2['topY'])

        # compute the intersection over union by taking the intersection
        # area and dividing it by the sum of prediction + ground-truth
        # areas - the interesection area
        iou = intersection_area / float(bb1_area + bb2_area - intersection_area)
        assert iou >= 0.0
        assert iou <= 1.0
        return iou
    except Exception as e:
        print(e)
        iou = 0
        return iou

def completeOverlap(bb1,bb2):
    #assert bb1['leftX'] < bb1['rightX']
    #assert bb1['topY'] < bb1['bottomY']
    #assert bb2['leftX'] < bb2['rightX']
    #assert bb2['topY'] < bb2['bottomY']
   
    try:
        
        assert bb1['leftX'] < bb1['rightX']
        #assert bb1['topY'] < bb1['bottomY']
        #assert bb2['leftX'] < bb2['rightX']
        assert bb2['topY'] < bb2['bottomY']
        
    except Exception as e:
        
        print('bb1',bb1)
        print('bb2',bb2)
        print('Assertion error for complete over lab')
        return False 
    # check if ocr word is completely inside the bbox of template defined
    # set error margin of 5px
    #if bb2['leftX']>=bb1['leftX']-5 and bb2['rightX']<=bb1['rightX']+5 and        bb2['topY']>=bb1['topY']-5 and bb2['bottomY']<=bb1['bottomY']+5:
    if bb2['leftX']>=bb1['leftX']-20 and bb2['rightX']<=bb1['rightX']+20 and  bb2['topY']>=bb1['topY']-20 and bb2['bottomY']<=bb1['bottomY']+20:
    
        return True
    else:
        return False
    
# Generates a single large bbox which covers given two text boxes
###########################################################################################
def merge_boxes(box_list):
    print('In merge box_list->',box_list)
    # create dict
    bbox_dict={'leftX':10000,'rightX':0,'topY':10000,'bottomY':0}
    for i in box_list:    
        if i[0]<=bbox_dict['leftX']:
            bbox_dict['leftX'] = i[0]
            
        if i[2]>=bbox_dict['rightX']:
            bbox_dict['rightX'] = i[2]

        if i[1]<=bbox_dict['topY']:
            bbox_dict['topY'] = i[1]

        if i[3]>=bbox_dict['bottomY']:
            bbox_dict['bottomY'] = i[3]
    
    if len(box_list[0])==6:
        print('Adding page---',box_list[0])
        #bbox_dict['pageNo'] = box_list[0][-1]
        bbox_dict['pageNo'] = box_list[0][-2]

    return bbox_dict
##############################################################################################



def closestBbox(list_bbox, template_anchor):
    distanceMin = 99999999
    for boxes in list_bbox:
        # euclidean distance = sqrt[(LeftX_of_bbox - LeftX_anchorBbox)^2 + (topY_of_bbox - topY_anchorBbox)^2]
        distance = (abs(boxes['leftX']-template_anchor['leftX'])**2 +  abs(boxes['topY']-template_anchor['topY'])**2) ** (1/2)
        print('\n')
        #print('distance -->',distance,'for box -->',boxes)
        if distance < distanceMin:
            closest_bbox = boxes
            distanceMin = distance
            
    # create dict and assign bbox coordinates of closest_bbox found above
    #print('****',closest_bbox)
    #print('***** closed box found ******',closest_bbox)
    bbox_dict={}
    bbox_dict['leftX'] = closest_bbox['leftX']
    bbox_dict['rightX'] = closest_bbox['rightX']
    bbox_dict['topY'] = closest_bbox['topY']
    bbox_dict['bottomY'] = closest_bbox['bottomY']
    bbox_dict['Name'] = closest_bbox['Name']
    bbox_dict['pageNo'] = closest_bbox['pageNo']
    bbox_dict['level_0']= closest_bbox['level_0']
    
    print('return from clossest function ---',bbox_dict)
    return bbox_dict



def calculateMultipliers(anchor_bbox1,field_bbox):
    #print('################################-----')
    #print('\n')
    #print('anchor_bbox1---',anchor_bbox1)
    #print('\n')
    #print('field_bbox---',field_bbox)
    #print('################################')
    
    # multipliers are the factor signifying relation between positions of anchor word and ml fields
    # TY Multiplier = (variable Top Y - AW1 TY)/(AW1 BY - AW1 TY)
    field_bbox['topY_multiplier'] = (field_bbox['topY']-anchor_bbox1['topY'])/(anchor_bbox1['bottomY']-anchor_bbox1['topY'])
    # Bottom Y Multiplier = (variable BY - variable TY)/(AW1 BY - AW1 TY)
    field_bbox['bottomY_multiplier'] = (field_bbox['bottomY']-field_bbox['topY'])/(anchor_bbox1['bottomY']-anchor_bbox1['topY'])
    # Width Multipler = (variable Rx - variable Lx )/ (AW1 Rx - AW1 lx)
    field_bbox['width_multiplier'] = (field_bbox['rightX']-field_bbox['leftX']) / (anchor_bbox1['rightX']-anchor_bbox1['leftX'])
    # variable Lx Multiplier = (variable Lx - AW1 Lx)/(AW1 Rx - AW1 Lx)
    field_bbox['leftX_multiplier'] = (field_bbox['leftX']-anchor_bbox1['leftX']) / (anchor_bbox1['rightX']-anchor_bbox1['leftX'])
    return field_bbox

    

def relativeBbox(predicted_anchor_bbox1,field_bbox,anchor1_dict):
    
    #list_1 = ['P_IGST_28','P_IGST_18','L_IGST_18','P_CGST_14','P_CGST_9','P_SGST_14','P_CGST_2_5','P_CGST_6','P_SGST_9','P_SGST_6','P_SGST_2_5','L_CGST_9','L_SGST_9']
    use_width = False
    if field_bbox['field'] in gst_variations:
        use_width = True
    
    if (use_width==False) and  (abs(anchor1_dict['topY']-predicted_anchor_bbox1['topY'])<5 or abs(anchor1_dict['bottomY']-predicted_anchor_bbox1['bottomY'])<5):
        #predicted_anchor_bbox1 = {'leftX':anchor1_dict['leftX'] , 'topY':anchor1_dict['topY'] ,'rightX':anchor1_dict['rightX'] ,'bottomY':anchor1_dict['bottomY']}
        
        if abs(anchor1_dict['leftX']-predicted_anchor_bbox1['leftX'])>50:
            predicted_anchor_bbox1 = {'leftX':predicted_anchor_bbox1['leftX'] , 'topY':anchor1_dict['topY'] ,'rightX':predicted_anchor_bbox1['rightX'] ,'bottomY':anchor1_dict['bottomY']}
        
        else:
            predicted_anchor_bbox1 = {'leftX':anchor1_dict['leftX'] , 'topY':anchor1_dict['topY'] ,'rightX':anchor1_dict['rightX'] ,'bottomY':anchor1_dict['bottomY']}
        
        
        print('changed predicted_anchor_bbox1 -----',predicted_anchor_bbox1)
        
    v1 = predicted_anchor_bbox1['bottomY']-predicted_anchor_bbox1['topY']
    v2 = anchor1_dict['bottomY']-anchor1_dict['topY']

    #list_1 = ['P_IGST_28','P_IGST_18','L_IGST_18','P_CGST_14','P_CGST_9','P_SGST_14','P_CGST_2_5','P_CGST_6','P_SGST_9','P_SGST_6','P_SGST_2_5','L_CGST_9','L_SGST_9']
    w1 = predicted_anchor_bbox1['rightX']-predicted_anchor_bbox1['leftX']
    w2 = anchor1_dict['rightX']-anchor1_dict['leftX']
   
    if use_width:
        #use_width_value = w2
        if abs(w1-w2)<70:
            use_width_value = w2
            print('using width ---template value',w2)
        else:
            use_width_value = w1
            print('using width ---csv value',w1)
    
    
    
    if abs(v1-v2)<5 :
        height = v1
        used_height = 'predicted anchor'
    else:
        
        height = v2
        used_height = 'actual anchor'
    
    print('height used ------',used_height)
    print('before relativebbox:',field_bbox)
    # dict to store the relative bbox on the target template
    relative_bbox = {}
    # a. variable Top Y = AW1 TY + (AW1 BY - AW1 TY) * variable Top Y Multiplier
    relative_bbox['topY'] = predicted_anchor_bbox1['topY']+(height)*field_bbox['topY_multiplier']
    # b. variable Bottom Y = variable TopY + Bottom Y Multiplier * mod(AW1 BY - AW1 BY)
    relative_bbox['bottomY'] = relative_bbox['topY']+field_bbox['bottomY_multiplier']*abs(height)
    # c. variable Lx = AW1 Lx + (AW1 Rx - AW1 Lx) * variable Lx Multiplier
    #relative_bbox['leftX'] = predicted_anchor_bbox1['leftX'] + field_bbox['leftX_multiplier']*(predicted_anchor_bbox1['rightX']-predicted_anchor_bbox1['leftX'])
    if use_width:
        print('using width---',use_width_value)
        relative_bbox['leftX'] = predicted_anchor_bbox1['leftX'] + field_bbox['leftX_multiplier']*(use_width_value)
        #relative_bbox['leftX'] = predicted_anchor_bbox1['leftX'] + field_bbox['leftX_multiplier']*(predicted_anchor_bbox1['rightX']-predicted_anchor_bbox1['leftX'])
    else:
        #relative_bbox['leftX'] = predicted_anchor_bbox1['leftX'] + field_bbox['leftX_multiplier']*(w2)
        relative_bbox['leftX'] = predicted_anchor_bbox1['leftX'] + field_bbox['leftX_multiplier']*(predicted_anchor_bbox1['rightX']-predicted_anchor_bbox1['leftX'])
 
    # d. variable Rx = variable Lx + variable Width Multiplier * (AW1 Rx - AW1 Lx)
    relative_bbox['rightX'] = relative_bbox['leftX'] + field_bbox['width_multiplier']*(predicted_anchor_bbox1['rightX']-predicted_anchor_bbox1['leftX'])
    # non relative fields whose value should not change in target template
    relative_bbox['pageNo'] = field_bbox['pageNo']
    relative_bbox['field'] = field_bbox['field']
    relative_bbox['Name'] = field_bbox['Name']
    relative_bbox['LEFT_Name'] = field_bbox['LEFT_Name']
    relative_bbox['TOP_Name'] = field_bbox['TOP_Name']
    relative_bbox['RIGHT_Name'] = field_bbox['RIGHT_Name']
    relative_bbox['BOTTOM_Name'] = field_bbox['BOTTOM_Name']
    print('after relativebbox:',relative_bbox)
    
    return relative_bbox    
    
def get_max_iou_boxes(df,actual_box,threshold):
    max_iou_name = []
    bbox_list = []
    #print('actual_box______',actual_box)
    for i in range(len(df)):
        target_box = df[['Name','leftX','rightX','topY','bottomY','pageNo']].iloc[i].to_dict()
        iou = get_iou(target_box,actual_box)
        #print('iou------',iou , i)
        
        if iou > threshold and actual_box['pageNo']==target_box['pageNo']:
            max_iou_name.append(df['Name'].iloc[i])
            bbox_list.append(df[['leftX','topY','rightX','bottomY','pageNo','level_0']].iloc[i].to_list())
    
    print('bbox_list1->',bbox_list)
    return max_iou_name , bbox_list



#NEW CODE Functions
#****************************************************************************#
##################################################################################
#################################################################################

def pick_right_word(anchor_value,df):
    total_anchor_found = []
    anchor_matched = False
    replace_list = [',','(',')',';',':','amp ','amp; ','& ','- ','.00','.','%']
    for c in replace_list:
        anchor_value = str(anchor_value).replace(c,'')
    print('anchor_value after removing stop special characters ----------',anchor_value)        
    ###################################################################################################
    anchor = str(anchor_value).strip().lower()
    anchor_words = anchor.split(' ')
    print(f"Multiple OCR matching, ANCHOR WORDS:{anchor_words}")
    # pointer used to keep track of matched words
    box_list = []
    ptr=0
    reset_ptr_count = 0
    matched_df_words = []
    for i in range(len(df)):
        # split df row on space if there are more than 1 words in the df row
        dfName_lst = df['Name'].iloc[i].strip().lower().split(' ')
        #Reset condition if anchor start word is found twice in a row
        if ptr == 1 and  dfName_lst[0]==anchor_words[0]:
            print('FOUND CONTINUE VENDOR RESETTING---',ptr)                                    
            ptr = 0
            matched_df_words =[]
            box_list = []
            matched_df_words = []


        #Break if found complete vendor 
        if ptr==len(anchor_words):
            #vendor_found_count+=1
            #single_vendor_found = y[anchor_flag]

            fuzzy_match = fuzz.ratio(matched_df_words, anchor_words)
            print(' FUZZ RATIO FOUND ------>',fuzzy_match)
            ##################################################
            predicted_anchor_bbox = merge_boxes(box_list)
            #if predicted_anchor_bbox['topY']<quad:
            print(f'****** OCR matching->Predicted anchor box:{predicted_anchor_bbox}')
            print(' box_list------', box_list)
            print('Matched Anchor words ----',matched_df_words)
            print('Actaul Anchor words-----',anchor_words)

            if fuzzy_match >= 90:
                print('--------found complete match exit vendor search----')
                anchor_found_flag = True

            print('*#*'*50)
            anchor_matched = True
            #anchor_info = {'anchor_flag':anchor_flag,'template_name':y[anchor_flag],'actual_achor_value':y[anchor_flag],anchor_flag:bbox_vendorName,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox, 'anchor_key_values':anchor_key_values,'grid_bboxes':grid_bboxes}
            anchor_info = {'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox }
            
            print('anchor_info--',anchor_info)
            #break


            if anchor_matched:
                anchor_info['predicted_bbox']['Name'] = ' '.join(matched_df_words)
                anchor_info['predicted_bbox']['level_0'] = df['level_0'].iloc[i]
                
                total_anchor_found.append(anchor_info)
                ptr = 0
                matched_df_words =[]
                box_list = []
                matched_df_words = []


         #############################################################    
        if len(box_list)!=0 and ptr!=len(anchor_words):
            if abs(box_list[0][3]-df['topY'].iloc[i])>200 or int(box_list[-1][4])!= int(df['pageNo'].iloc[i]):
                print('WRONG WORD PREDICTED CLEAR PREDICTIONS at ----',i)
                ptr = 0
                matched_df_words =[]
                box_list = []
                matched_df_words = []

            level_0 = df['level_0'].iloc[i]                        
            if len(box_list) > 0 and abs(box_list[-1][5] - level_0) > 2 :
                print('----WRONG WORD FOR IN SAME LINE---',i)
                ptr = 0
                matched_df_words =[]
                box_list = []
                matched_df_words = []


        if len(dfName_lst)>1:
            # match ocr vendorName list splitted on words with template vendorName list
            if dfName_lst == anchor_words[ptr:]:
                reset_ptr_count = i
                matched_df_words.extend(df['Name'].iloc[i].split(' '))
                print('list matching....')
                box_list.append(df[['leftX','topY','rightX','bottomY','pageNo','level_0']].iloc[i].values.tolist())
                # if complete list is matched assign pointer to last word index
                ptr=len(anchor_words)


        # if direct list not matched search word by word using the pointer
        if ptr<len(anchor_words): 
            add_bbox_one = False
            for word in dfName_lst:
                #print('DEEEEBUG',word,anchor_words,ptr)
                try:
                    val = anchor_words[ptr]
                except Exception as e:
                    print('ERROR IN SERACHING VALUE FROM OCR')
                    print('--->>>>>>>>>>>>>',e)
                    break

                for c in replace_list:
                    word = word.replace(c,'')

                if fuzz.ratio(word,anchor_words[ptr])>=95:


                    reset_ptr_count = i
                    #print('df name:',df.Name.iloc[i])
                    # if single word matches with template vendorName word, 
                    # add it matched_df_words list; which is used to verify at end 
                    # if vendorName list of words matched with that of template list of words 
                    matched_df_words.append(word)
                    print('matched df name list:',matched_df_words,' at ',i)
                    # if word is matched temporarily remove that word from VendorName template list
                    anchor = anchor.replace(word,'')
                    print('anchor:',anchor_words[ptr:])
                    if len(dfName_lst)==1:
                        box_list.append(df[['leftX','topY','rightX','bottomY','pageNo','level_0']].iloc[i].values.tolist())
                    #print(df[['leftX','topY','rightX','bottomY']].iloc[i].values.tolist())
                    # increment the pointer to the next word
                    ptr+=1
                    add_bbox_one = True

            if add_bbox_one and len(dfName_lst)>1:   
                print('Append 2 in 1 box')
                box_list.append(df[['leftX','topY','rightX','bottomY','pageNo','level_0']].iloc[i].values.tolist())

    
    print('Status of pick right word flag ----',anchor_matched ,'for value -----',anchor_value)
    if anchor_matched==False:
        predicted_anchor_bbox = []
    
    print('Status of pick right word bbox----',predicted_anchor_bbox)
    return anchor_matched , predicted_anchor_bbox , total_anchor_found




def find_variable_anchor(y,df,variable_level_fields,value):    
    variable_anchor_field = None
    variableAnchor_found = False
    variableAnchor_bbox = None
    variablePageNo = None
    variable_anchor_dict = None
    variableAnchor_bbox_boxes = []
    variable_anchor_dict = None
    print('*******IN FIND ANCHOR variable ************')
    ##################################
    variable_field = variable_level_fields
    try:
        total_anchor_dict = [d for d in y['fdq'] if d['field']== variable_field][0]
    except Exception as e:
        print('----error for find variable anchor---',e)
        return variableAnchor_found , variableAnchor_bbox , variablePageNo ,variable_anchor_field, variable_anchor_dict



    #total_anchor_dict = [d for d in y['fdq'] if d['field']== variable_field][0]
    print('total_anchor_dict-------',total_anchor_dict)
    search_value = total_anchor_dict[value].strip()
    print('search_value--',search_value)
    list_search_value = search_value.split(' ')
    
    if len(list_search_value)>1:
        
        print('--Found more than one variable words seraching with pick_right_word function--')
        #new_df = df[df['Name'].apply(lambda x: fuzz.ratio(x.lower(),list_search_value[0].lower()))>=88]
        variableAnchor_found , variableAnchor_bbox ,total_anchor_found = pick_right_word(search_value,df)

        if variableAnchor_found and len(total_anchor_found)>1:
            variable_anchor_dict = total_anchor_dict
            variable_anchorPos = value.split('_')[0]
            print('---- Found Multiple tax anchor names ----')
            variableAnchor_bbox = [i['predicted_bbox'] for i in total_anchor_found]
            variable_anchor_dict2 = {'leftX':variable_anchor_dict[variable_anchorPos+'_leftX'],'topY':variable_anchor_dict[variable_anchorPos+'_topY'],'rightX':variable_anchor_dict[variable_anchorPos+'_rightX'],'bottomY':variable_anchor_dict[variable_anchorPos+'_bottomY']}
            variableAnchor_bbox = closestBbox(variableAnchor_bbox,variable_anchor_dict2)
        

        if variableAnchor_found:
            variable_anchorPos = value.split('_')[0]
            print('Found Final bbox from pick right word----',variableAnchor_bbox)
            variable_anchor_dict = total_anchor_dict
            
            variable_anchor_dict = {'leftX':variable_anchor_dict[variable_anchorPos+'_leftX'],'topY':variable_anchor_dict[variable_anchorPos+'_topY'],'rightX':variable_anchor_dict[variable_anchorPos+'_rightX'],'bottomY':variable_anchor_dict[variable_anchorPos+'_bottomY']}
            variablePageNo = variableAnchor_bbox['pageNo']
            variable_anchor_field = variable_field
            
        return variableAnchor_found , variableAnchor_bbox , variablePageNo ,variable_anchor_field, variable_anchor_dict
    #################################
          
    
    #if(len(variable_level_fields)>0):
    try:
        variable_field = variable_level_fields
        print('GETTING PREDICTION FOR FIELD AS ----',variable_field)
        total_anchor_dict = [d for d in y['fdq'] if d['field']== variable_field][0]
        print('total_anchor_dict-------',total_anchor_dict)
        # choose anchor word from LEFT or TOP name
        # if TOP_Name has word from the keyword list use that else, use word from LEFT_Name
        # to identify the totalAmount in target invoice
        new_df = df[df['Name'].apply(lambda x: fuzz.ratio(x.lower(),total_anchor_dict[value].lower()))>=88]
        #new_df = df[df['Name'].apply(lambda x: fuzz.ratio(x.split(' ')[-1].lower(),total_anchor_dict[value].split(' ')[-1].lower()))>75]
        
        print('SEARCHING FOR ------',total_anchor_dict[value], '  IN ',value)
        #if total_anchor_dict[value] in df['Name'].values and total_anchor_dict[value]!='':
        if len(new_df)!=0 and total_anchor_dict[value]!='': 
            variable_anchorWord = total_anchor_dict[value]
            variable_anchor_field = variable_field
            variable_anchorPos = value
            print('variable_anchorWord----',variable_anchorWord)
            variable_anchor_dict = total_anchor_dict
            variableAnchor_found = True
            print('\n')
            print('****** variable anchor found in ',value, '--',total_anchor_dict[value])

        #variableAnchor_found = True
    except IndexError as e:
        print(f'ERROR: Anchor dict not found for variable level fields:{e}')
        print('ERROR: error in Template search!!!',traceback.format_exc())
        variableAnchor_found = False
        pass

    print(f"***variableAnchor:{variable_anchor_field}***--variableAnchor_found:{variableAnchor_found}")
    if variableAnchor_found == True:
        try:
            #variableAnchor_bbox = new_df[['leftX','topY','rightX','bottomY','Name','level_0','pageNo']].values.tolist()
            variableAnchor_bbox = new_df[['leftX','topY','rightX','bottomY','Name','level_0','pageNo']].to_dict('r')
            
            print('############### variableAnchor_bbox ################',variableAnchor_bbox)
            
        except Exception as e:
            print('ERROR: error in Template search!!!',traceback.format_exc())
            print(e)
            variableAnchor_found = False

    if variableAnchor_found and len(variableAnchor_bbox)>1:
        print(f'<=Multiple variableAnchor values found. Selecting the bbox with minimum distance from Template anchor=>')
        
        variable_anchorPos = value.split('_')[0]
        variable_anchor_dict2 = {'leftX':variable_anchor_dict[variable_anchorPos+'_leftX'],'topY':variable_anchor_dict[variable_anchorPos+'_topY'],'rightX':variable_anchor_dict[variable_anchorPos+'_rightX'],'bottomY':variable_anchor_dict[variable_anchorPos+'_bottomY']}
        #print('yes----------')
        variableAnchor_bbox = closestBbox(variableAnchor_bbox,variable_anchor_dict2)
        variablePageNo = variableAnchor_bbox['pageNo']
        #variablePageNo = df['pageNo'].iloc[variablePageNo]
        print(f"variableAnchor_bbox page No:{variablePageNo}")
        print(f'Predicted variable anchor bbox:{variableAnchor_bbox}')
        variableAnchor_found = True


    elif variableAnchor_found and len(variableAnchor_bbox)==1:
        variableAnchor_found = True
        #variableAnchor_bbox = df[[f'{variable_anchorPos}_Name']==variable_anchorWord][['leftX','topY','rightX','bottomY']].iloc[0].to_dict()
        #variableAnchor_bbox = df[df['Name']==variable_anchorWord][['leftX','topY','rightX','bottomY','Name','level_0']].iloc[0].to_dict()
        #variableAnchor_bbox = new_df[['leftX','topY','rightX','bottomY','Name','level_0','pageNo']].iloc[0].to_dict()
        #variableAnchor_bbox_boxes = [variableAnchor_bbox.copy()]
        variableAnchor_bbox = variableAnchor_bbox[0]
        variablePageNo = variableAnchor_bbox['pageNo']
        #variableAnchor_bbox = df[df[f'{variable_anchorPos}_Name']==variable_anchorWord][['leftX','topY','rightX','bottomY']].iloc[0].to_dict()
        
        print(f'Predicted variable anchor bbox:{variableAnchor_bbox}')
    else:
        variableAnchor_found = False

    if variableAnchor_found == False:
        variableAnchor_bbox = None
        variablePageNo = None
        variable_anchor_field = None
        variable_anchor_dict = None
        variableAnchor_bbox_boxes = None
        return variableAnchor_found , variableAnchor_bbox , variablePageNo ,variable_anchor_field, variable_anchor_dict
  
    else:
        print('FOUND ANCHOR WORD IN variable')
        print('+++++++++++++++',value)
        variable_anchorPos = value.split('_')[0]
        variable_anchor_dict = {'leftX':variable_anchor_dict[variable_anchorPos+'_leftX'],'topY':variable_anchor_dict[variable_anchorPos+'_topY'],'rightX':variable_anchor_dict[variable_anchorPos+'_rightX'],'bottomY':variable_anchor_dict[variable_anchorPos+'_bottomY']}
        print('variable_anchor_dict =======',variable_anchor_dict)
        print('variable anchor pageNO---',variablePageNo)
        
        #variable_anchor_dict = {'leftX':variable_anchor_dict[value],'topY':variable_anchor_dict[value],'rightX':variable_anchor_dict[value],'bottomY':variable_anchor_dict[value]}
        return variableAnchor_found , variableAnchor_bbox , variablePageNo ,variable_anchor_field, variable_anchor_dict

    
################################################################################### 



###########################################
#DEBUG CODE NEW

def field_correction(df,relative_bbox,idx):
    print(' ***IN SECOND VALIDATION**')
    print('idx value got in this function---',idx)
    variable_fields = ['LEFT_Name','TOP_Name','RIGHT_Name','BOTTOM_Name']
    #variable_fields = variable_fields[start:]
    #modified_template_value = False
    print('USING VARIALE FIELDS +++++',variable_fields)
    result_found =[]
    res = False
    maxIOU_indices = idx
    for value in variable_fields:
        
        a0 = time.time()
        print('\n')
        print('**************TURN****************',value)
        print('CHECKING FOR VARIABLE-----',value)
        print('VARIABLE_bbox ACTUAL VALUE--------',relative_bbox[value])
        try:
            res,val = validate(df,idx,value,relative_bbox[value])
            print('VALIDATE FUNDCTION result -----',res,val)
        except Exception as e:
            print(e)
            print('------------**********---------NO PREDICTION FOUND FROM TEMPLATE PASS 2-------***********---------')
            res = False
        
        if relative_bbox[value]==''  or relative_bbox[value]==None:
            result_found.append('Empty')
            continue
        if relative_bbox[value]!='' and res==True :
            print('----COREECT RESULT FOUND IN Field Correction appending true for---- ',val)
            result_found.append('True')
        else:
            result_found.append('False')
            
        a1 = time.time()
        a1 = round(a1-a0,2)
        print('\n')
        print('__'*50)
        
        print('TIME TAKEN BY FIELDS CORRECTION FOR ONE  ----',a1)

    
        
            
    print('\n')
    print('--------------------------------------------------------------------------------')
    print('result_found-->>>',result_found)
    print('--------------------------------------------------------------------------------')
    
    
    count_result = 0
    #For LEFT
    if result_found[0]=='True':
        count_result+=4
        
    # For RIGHT
    if result_found[1]=='True':
        count_result+=1
        
    # For TOP
    if result_found[2]=='True':
        count_result+=3
        
    # FOR Bottom
    if result_found[3]=='True':
        count_result+=2
        
    print("FINAL COUNT FOUND-----------",count_result)
    
    #cnt = result_found.count('True')
    
    if count_result >= 6:
        print('***** VALIDATED CORRECT RESULT********')
        result_found = True
    else:
        print('***** INVALIDATED RESULT********')
        result_found = False

    
    #if cnt>1:
    #    result_found = True
    #else:
    #    result_found = False
        
    return result_found


def check_relative_anchors(y,df,relative_bbox,idx):
    print('__IN check relative anchors relative_bbox ----',relative_bbox)
    old_page_no = relative_bbox['pageNo']
    #temp_modifty = False
    use_variable = False
    variableAnchor_found = False
    if len(use_only_variable_anchors)>0 and relative_bbox['field'] in use_only_variable_anchors:
    #if y["documentType"]=='BGV_Form' and relative_bbox['field'] in temp_list:    
        print('_______use only variable anchors found true_______')
        #temp_modifty = True
        use_variable = True
        idx = []

    if anchor_set=='Vendor_GSTIN' and relative_bbox['field']=='Vendor_Name':
        print('----setting for vendor empty max---')
        use_variable = True
        idx = []

    global search_gst
    search_gst = False
    #if relative_bbox['field'] in ['P_IGST_28','P_IGST_18','L_IGST_18','P_CGST_14','P_CGST_9','P_CGST_6','P_CGST_2_5','P_SGST_14','P_SGST_9','P_SGST_6','P_SGST_2_5','L_CGST_9','L_SGST_9']:
    if relative_bbox['field'] in gst_variations:
        print('----setting for GST values to empty---')
        search_gst = True
        use_variable = True
        idx = []



    if use_variable:
        variable_fields =  ['LEFT_Name','TOP_Name','RIGHT_Name','BOTTOM_Name']
    only_one = False
    
    print('IN CHECK RESULT')
    print('\n')
    print('before modify-----',idx)
    
    modified_template_value = False
    modified_template_value_2 = False
    print('idx -----------',idx)
    default_indices = idx.copy()
    default_relative_bbox = relative_bbox.copy()
    
    maxIOU_indices = idx
    print('\n')
    check_two_times = 0
    variable_fields = ['LEFT_Name','RIGHT_Name','TOP_Name','BOTTOM_Name']
    start = 0
    res = False
    result_found = False
    for value in variable_fields:
        a0 = time.time()
        print('maxIOU_indices======',maxIOU_indices)
        print('In check_relative_anchors Function running check for --',value, 'for tempalte name---',relative_bbox[value])
        #maxIOU_indices_2 , modified_template_value_2 , relative_bbox_2 = field_correction(y,df,relative_bbox,maxIOU_indices,mapper,keys,value)
        try:
            res,val = validate(df,maxIOU_indices,value,relative_bbox[value])
            print('relative_bbox value --->>>>',relative_bbox[value])
            print('output from validate function----',res,val)
        except Exception as e:
            print(e)
            print('NO PREDICTION FOUND FROM TEMPLATE PASS 1')
            res = False
        
        a1 = time.time()
        a1 = round(a1-a0,2)
        print('\n')
        print('__'*50)
        print('TIME TAKEN BY VALIDATE FUNCTION ----',a1)

        
        #print('using value ----',value)
        if relative_bbox[value]=='' or relative_bbox[value]==None:
            start+=1
            print('Empty field found in db for --',value)
            continue
        
        if relative_bbox[value]!='' and res==True :
            print('##################################################',value,relative_bbox[value])
            print('FOUND RESULT---------',res)
            #print(cool)
            print('FOUND BY TRAVERSING -------',value,val)
            print('--------------------COREECT RESULT FOUND-------------')
            valid_result = True
            valid_result_set_by = variable_fields
            check_two_times+=1
            print('current value of check_two_time ------',check_two_times)
            print('maxIOU_indices------$$$$',maxIOU_indices)
            if check_two_times==2:
                print('check_two_times ----->>>>>>>>>> True')
                break
    
        else:
            
            a0 = time.time()
            start +=1
            print('----------INVALID RESULT WAS FOUND RUNNING VALIDATION STEPS---------- ')
            print('Searching check relative anchors with -->>>>>',value)
            variable_level_fields = relative_bbox['field']
            if use_fixed_page:
                print('modifty---------df')
                df = df[df['pageNo']==relative_bbox['pageNo']]
            
            
            variableAnchor_found , variableAnchor_bbox , variablePageNo , variable_anchor_field, variable_anchor_dict = find_variable_anchor(y,df,variable_level_fields,value)
            print('\n')
            #print('___varibaleAnchor_bbox_found___',variableAnchor_bbox)
            #if use_page:
            #    variableAnchor_bbox['pageNo'] = relative_bbox['pageNo']
            print('___varibaleAnchor_bbox_found___',variableAnchor_bbox)
            print('___variable_anchor_dict_found___',variable_anchor_dict)
            
            if variableAnchor_found:
                maxIOU_indices = []
                field_dict = [d for d in y['fdq'] if d['field']== variable_level_fields][0]
                print('variable_anchor_dict-----',variable_anchor_dict)
                print('field_dict-----',field_dict)
                
                field_dict = calculateMultipliers(variable_anchor_dict, field_dict)
                relative_bbox = relativeBbox(variableAnchor_bbox,field_dict,variable_anchor_dict)
                
                if use_variable:
                    relative_bbox['pageNo'] = variablePageNo
                
                if use_page:
                    relative_bbox['pageNo'] = old_page_no
                
                print('relative boxes -----^^^^^^^--------',relative_bbox)

                max_iou = 0
                max_iou_idx = None
                for i in range(len(df)):  
                    row_bbox = df[['leftX','rightX','topY','bottomY','pageNo']].iloc[i].to_dict()
                    # relative bbox calculation
                    field_dict = relative_bbox
                    iou = get_iou(field_dict, row_bbox)
                    #if field_dict['field']=='Vendor_Name':
                        #print('=================================',iou)
                    # if word is completely inside template bbox mark it 
                    completeOverlap_check = completeOverlap(field_dict, row_bbox)
                    #print(i,df['Name'].iloc[i],' IOU:',iou,completeOverlap_check)
                    if field_dict['pageNo']==row_bbox['pageNo']:    
                        if completeOverlap_check==True:
                            print('completeoverlap -----',df['level_0'].iloc[i])
                            maxIOU_indices.append(df['level_0'].iloc[i])
                            
                        # get max overlapping bbox
                        if iou > max_iou:
                            print('geting max--',df['level_0'].iloc[i])
                            max_iou = iou
                            max_iou_idx = df['level_0'].iloc[i]
                if max_iou_idx != None:    
                    maxIOU_indices.append(max_iou_idx)
                #print('maxIOU_indices found----',maxIOU_indices)
                #print('before***',maxIOU_indices)
                maxIOU_indices = list(set(maxIOU_indices))
                maxIOU_indices.sort()
                print('maxIOU_indices found----',maxIOU_indices)
                
                #print('after****>',maxIOU_indices)
                #####################################################
                if len(maxIOU_indices)==0:
                    continue
                
                #print('___max_IOU__',maxIOU_indices)
                #print('___abc___',df['pageNo'].iloc[maxIOU_indices[0]])
                #print('__abc__',set(df['pageNo'].values))
                #if temp_modifty and relative_bbox['pageNo'] == df['pageNo'].iloc[maxIOU_indices[0]]:
                if use_variable and only_one == False:
                    only_one = True
                    print(' SETING DEFAULTS ____________')
                    #only_one = True
                    default_indices = maxIOU_indices
                    default_relative_bbox = relative_bbox
                ################################################
                
                
                if len(maxIOU_indices)!=0:
                    result_found = field_correction(df,relative_bbox,maxIOU_indices)
                    print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                    
                    
                a1 = time.time()
                a1 = round(a1-a0,2)
                print('\n')
                print('__'*50)
                print('TIME TAKEN BY INVALID RESULT FOUND CODE ----',a1)
                
                if result_found:
                        break
                    
    print('maxIOU_indices in check_relative_anchors-----------',maxIOU_indices)
    #if len(maxIOU_indices)>0:
    #    modified_template_value = True
    if len(maxIOU_indices)==0 or result_found==False:
        print('---------Setting up default values---')
        maxIOU_indices = default_indices
        relative_bbox = default_relative_bbox
    
    print('after mofidy----',maxIOU_indices)
    return maxIOU_indices ,modified_template_value , relative_bbox



####################################################################################
####################################################################################################
#Validate Function
####################################################################################################
def validate(df,max_indices,value,actual_value):
    print('Using variable field in validate function ----',value)
    flag =False
    modifty_pixel = False

    idx = max_indices[0]
    print('default used index = ',idx)
    predicted_varibale_value = df[['LEFT_Name','RIGHT_Name','TOP_Name','BOTTOM_Name','Name','leftX','rightX','topY','bottomY','level_0']].iloc[idx].to_dict() 
    if len(max_indices)>1:
        print('Modiftying rightX value to end')
        modify_pixel = True
        #modify_right = df['rightX'].iloc[max_indices[-1]]
        for i in range(len(max_indices)):
            max_right = df['rightX'].iloc[max_indices[0]]
            if df['rightX'].iloc[max_indices[i]]>max_right:
                max_right = df['rightX'].iloc[max_indices[i]]
        predicted_varibale_value['rightX'] =  max_right
    print('predicted_varibale_value__>>',predicted_varibale_value)
    
    if value=='LEFT_Name':
        print('IN LEFT using indx value----',idx)        
        search_box = {'leftX': min(df['leftX']) ,'rightX': predicted_varibale_value['leftX'] ,'topY':predicted_varibale_value['topY'] ,'bottomY':predicted_varibale_value['bottomY']} 
    
    if value=='TOP_Name':
        print('IN TOP using indx value----',idx)
        search_box = {'leftX': predicted_varibale_value['leftX'] ,'rightX': predicted_varibale_value['rightX'] ,'topY':min(df['topY']) ,'bottomY':predicted_varibale_value['topY']} 
        
    if value=='RIGHT_Name':
        idx = max_indices[-1]  
        print('IN RIGHT using indx value----',idx)
        predicted_varibale_value = df[['LEFT_Name','RIGHT_Name','TOP_Name','BOTTOM_Name','Name','leftX','rightX','topY','bottomY']].iloc[idx].to_dict() 
        print('predicted_varibale_value__>>',predicted_varibale_value)
        search_box = {'leftX': predicted_varibale_value['rightX'] ,'rightX': max(df['rightX']) ,'topY':predicted_varibale_value['topY'] ,'bottomY':predicted_varibale_value['bottomY']} 
        
    if value=='BOTTOM_Name':
        print('IN BOTTOM using indx value----',idx)
        search_box = {'leftX': predicted_varibale_value['leftX'] ,'rightX': predicted_varibale_value['rightX'] ,'topY':predicted_varibale_value['bottomY'] ,'bottomY':max(df['bottomY'])} 
        
    candidate_boxes = []
    print('Index used at ',idx,' with name ',df['Name'].iloc[idx])
    for i in range(len(df)):
        #if df['leftX'] <= predicted_varibale_value['leftX']:
        target_box = df[['leftX','rightX','topY','bottomY','Name']].iloc[i].to_dict()
        iou = get_iou(search_box,target_box)
        
        name = df['Name'].iloc[i].strip().lower().split(' ')
        act_name = actual_value.strip().lower().split(' ')
        #print('-----------------------------------------',name,act_name)
        r1 = fuzz.ratio(name,act_name)
        if r1 >90 and iou>0:
            flag = True
            print('found ratio---',r1)
            print('--In complete found--')
            print('Found for idx in df----',i)
            print('FOUND MATCH FOR ------',name , act_name)
            return flag , predicted_varibale_value[value]

        for v in name:
            #match = fuzz.ratio(target_box['Name'].split(' ')[-1].strip().lower(),actual_value.strip().lower())
            match = fuzz.ratio(v.strip().lower(),actual_value.lower().strip())
            if iou>0 and match>=88:
                print('Found for idx in df----',i)
                print('FOUND MATCH FOR ------',v , actual_value)
                print('RATIO FOUND-----',match)
                #print('FOUND MATCH FOR ------',target_box['Name'])
                flag = True
                #print('predicted_varibale_value------',predicted_varibale_value[value])
                return flag , predicted_varibale_value[value]
            else:
                flag = False
        
            
    return flag , predicted_varibale_value[value]





#Grid Serach code
################################################################

def get_grid_num(xPieces, yPieces, imgwidth , imgheight , text_left ,text_top , anchor):
    #print('anchor used ----',anchor)
    
    #xPieces = 1
    grid_box = []
    height = imgheight // yPieces
    width = imgwidth // xPieces
    c=0
    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width+text_left, i * height+text_top, (j + 1) * width+text_left, (i + 1) * height+text_top)
            #box = (j * width+target_left, i * height+target_top, (j + 1) * width, (i + 1) * height)
            
            grid_box.append(box)
            c+=1
            
    grid_num = []
    for i in range(len(grid_box)):
    
        template_grid = {'leftX':grid_box[i][0],'rightX':grid_box[i][2],'topY':grid_box[i][1],'bottomY':grid_box[i][3]}
        print('************************')
        #print('anchor used bb1---',anchor)
        #print('template grid bb2-----',template_grid)
        iou = get_iou(anchor,template_grid)
        if iou > 0.002:
            grid_num.append(i)
    print('found template grid no---',grid_num)
    return grid_num ,grid_box


#################################################################################


def  extract_fields(template_data):
    global use_page
    field_dict = template_data[0]
    anchor_flag = template_data[1]
    df = template_data[2]
    #ml_fields_dict = y['fdq']
    maxIOU_indices = []
    # This is to handle the case when more than one fields are having same variable level anchor words
    #####################################################
    field_dict_keys = field_dict.keys()
    use_page = False
    if 'page_id' in field_dict_keys:
        use_page = True
        matched_names = df[df['Name'].apply(lambda x: fuzz.ratio(x.lower(),field_dict['page_id'].lower())) >=75]['Name']
        print('MATCHED NAMES--------->>>>>>',matched_names)
        use_page_id = set(df[df['Name'].apply(lambda x: fuzz.ratio(x.lower(),field_dict['page_id'].lower())) >=75]['pageNo'].values)
        print('MATCHED PAGEs----',use_page_id,'for field name - ' ,field_dict['field'])
    
    variablePageNo = field_dict['pageNo']
    do_nothing=False
    if use_page:
        if len(use_page_id)==0:
            print('---------SKIPING---------')
            do_nothing = True
            field_dict['plot_box'] = False
            return field_dict, maxIOU_indices
        else:
            #print('___Changing page number for use page___')
            print('___Changing page number for use page___',list(use_page_id))
            variablePageNo = list(use_page_id)[0]
            variable_anchor_dict['pageNo'] = variablePageNo
            field_dict['pageNo'] = variablePageNo
    
    
    max_iou = 0
    max_iou_idx = None
    # list of indices which matches with the template bbox
    print('__USING field_dict___',field_dict)
    # calculate and append multipliers to field dict,
    # use InvoiceTotalAmount as anchor for variable level fields
    a0 = time.time()
    #variable_anchor_dict = taxable data 
    if field_dict['field'] in variable_level_fields and variableAnchor_found == True:
        
        print(' In variable level for ---- ',field_dict['field'])
        print('**********************')
        print('\n')
        print('#'*100)
        print(f"***ANCHOR USED:{variable_anchor_field} for field:{field_dict['field']}")
        print(f"variable_anchor_dict:{variable_anchor_dict}")
        print(f"variableAnchor_bbox:{variableAnchor_bbox}")
        print('--------------------------------')
        # for variable level fields use InvoiceTotalAmt as anchor
        field_dict['pageNo'] = variablePageNo
        print('calling-----mUX--^^^^^^^^^^^^^^^^^^^^^^^^^')
        #if variableAnchor_found:
        #variable_anchor_dict = variable anchor in template
        # field_dict = value to be extracted 

        field_dict = calculateMultipliers(variable_anchor_dict, field_dict)
        #field_dict = calculateMultipliers(variableAnchor_bbox, variable_anchor_dict)
        print('variablePageNo---',variablePageNo)
        field_dict['pageNo'] = variablePageNo
        # calculate relative bbox coordinates
        relative_bbox = relativeBbox(variableAnchor_bbox,field_dict,variable_anchor_dict)
        #predicted_bbox.append(relative_bbox)
        #print('PREDICTED BOX DATA',relative_bbox)

    else:

        # for non variable level fields use VendorName as anchor
        print('\n')
        print('**********************')
        print('\n')
        print('#'*100)
        print(f"***ANCHOR USED:{anchor_flag} for field:{field_dict['field']}")
        print('\n')
        print(f"anchor1_dict:{anchor1_dict}")
        print('\n')
        print(f"predicted_anchor_bbox:{predicted_anchor_bbox}")
        print('\n')
        print('**********************')

        field_dict = calculateMultipliers(anchor1_dict, field_dict)

        # calculate relative bbox coordinates
            
        relative_bbox = relativeBbox(predicted_anchor_bbox,field_dict,anchor1_dict)
        #predicted_bbox.append(relative_bbox)
        #print('PREDICTED BOX DATA',relative_bbox)
        if field_dict['field'] =='Vendor_Name':
            
            relative_bbox['leftX'] = predicted_anchor_bbox['leftX']
            
            relative_bbox['rightX'] = predicted_anchor_bbox['rightX']
            
            relative_bbox['topY'] = predicted_anchor_bbox['topY']
            
            relative_bbox['bottomY'] = predicted_anchor_bbox['bottomY']
            
            relative_bbox['pageNo'] = predicted_anchor_bbox['pageNo']
            
            print('Changing Relative bbox---',relative_bbox)      
  
        if field_dict['field'] in static_fields:
            #staticField_actual_values.append(field_dict['Name'])
            #staticField_actual_values[field_dict['field']]=field_dict['Name']

            if field_dict['field'] == static_fields[0]:
                print('__USING ALT NAME AS STATIC__')
                staticField_actual_values[field_dict['field']]= alt_anchor_value    
            else:
                staticField_actual_values[field_dict['field']]=field_dict['Name']


    # iterate through all csv rows to check which bbox is closest to bbox saved in template

    for i in range(len(df)):
        row_bbox = df[['leftX','rightX','topY','bottomY','pageNo']].iloc[i].to_dict()
        # relative bbox calculation
        field_dict = relative_bbox

        #iou = get_iou(field_dict, row_bbox)
        iou = get_iou(field_dict, row_bbox)

        #if field_dict['field']=='Vendor_Name':
            #print('=================================',iou)
        # if word is completely inside template bbox mark it 
        #completeOverlap_check = completeOverlap(field_dict, row_bbox)

        completeOverlap_check = completeOverlap(field_dict, row_bbox)
        #print(i,df['Name'].iloc[i],' IOU:',iou,completeOverlap_check,max_iou)
        if field_dict['pageNo']==row_bbox['pageNo']:
            if completeOverlap_check==True:
                maxIOU_indices.append(df['level_0'].iloc[i])
                print('*************set for complete overlap******************',i,df[['Name','level_0']].iloc[i])
            # get max overlapping bbox
            if iou > max_iou:
                print('Having max iou---',iou,' for index -- ',df['level_0'].iloc[i])
                max_iou = iou
                max_iou_idx = df['level_0'].iloc[i]
    if max_iou_idx != None:

        maxIOU_indices.append(max_iou_idx)

    print('MAX IOU INDEXX ----',max_iou_idx)
    maxIOU_indices = list(set(maxIOU_indices)) 
    maxIOU_indices.sort()
    # text values of predicted indices
    #print('++++++++++++++++++++++')
    print('maxIOU_indices------***----',maxIOU_indices)


    '''if close_bbox_check==None:
        close_bbox_check =relative_bbox['topY']
    else:

        diff = abs(close_bbox_check-relative_bbox['topY'])
        print('OBSERVED DIFFERENCE _-------',diff)
        if abs(diff)< 150:
            #close_bbox_check = relative_bbox['topY']
            relative_anchor_call = False
        else:
            close_bbox_check = relative_bbox['topY']'''


    print('name at above location ---',list(df['Name'].iloc[maxIOU_indices].values))
    #if  len(maxIOU_indices)<2 and data['documentType']=='Invoice_Document' and relative_anchor_call==True:
    #if  data['documentType']=='Invoice_Document' and relative_anchor_call==True:

    if maxIOU_indices in predicted_idx_found:
        print('***************************RESULT ALREADY THERE MANKING IT EMPTY**********')
        maxIOU_indices = []


    a1 = time.time()
    a1 = round(a1-a0,2)
    print('\n')
    print('__'*50)
    print('TIME TAKEN FOR PREDICTION WITH BASE CODE ----',a1)


    df2 = df[['Name','leftX','topY','rightX','bottomY','LEFT_Name','TOP_Name','RIGHT_Name','BOTTOM_Name','pageNo','level_0']].copy()
    
    a0 = time.time()
    
    maxIOU_indices,modified_template_value ,relative_bbox = check_relative_anchors(y,df2,relative_bbox,maxIOU_indices)
    
    
    #try:
    #    maxIOU_indices,modified_template_value ,relative_bbox= check_relative_anchors(y,df2,relative_bbox,maxIOU_indices)
    #except Exception as e:
    #    print('ERROR: error in Template search!!!',traceback.format_exc())
    #    print('GOT ERROR IN RELATIVE ANCHORS ---- ',e)


    a1 = time.time()
    a1 = round(a1-a0,2)
    print('\n')
    print('__'*50)
    print('TIME TAKEN BY check relative anchors function ----',a1)




    #a0  = time.time()
        #if modified_template_value:
        #    maxIOU_indices = [relative_bbox2['index']]
    #predicted_bboxes.append(relative_bbox)
    

    a0 = time.time()
    s1 = set([num for sublist in predicted_idx_found for num in sublist])
    s2 = set(maxIOU_indices)

    print('s1----',s1)
    print('s2-----',s2)
    r1 = s2-s1
    predicted_idx_found.append(maxIOU_indices)
    maxIOU_indices = list(r1)
    print('GOT FINAL MAX_IOU-----------',maxIOU_indices)

    #if do_nothing:
    #    print('____FOUND DO NOTING FLAG_____MAKING PREDICTIONS EMPTY')
    #    maxIOU_indices = []
    predicted_text = df.loc[(df.index.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'Name'].values
    # check if static fields match, if not save the original trained values from template

    if field_dict['field'] in static_fields:
        #staticField_actual_values.append(field_dict['Name'])
        #staticField_actual_values[field_dict['field']]=field_dict['Name']
        if field_dict['field'] == static_fields[0]:
            print('__USING ALT NAME AS STATIC__')
            staticField_actual_values[field_dict['field']] = alt_anchor_value    
        else:
            staticField_actual_values[field_dict['field']] = field_dict['Name']


    print(field_dict.keys())
    print('\n')
    print(f"------->TEMPLATE SET FOR: {predicted_text} as {field_dict['field']} at index:{maxIOU_indices}")
    # assign the Property value and add entry 'TEMPLATE' in result column to signify field was matched
    # using TemplateSearch
    df.loc[(df.index.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'Property'] = field_dict['field']
    df.loc[(df.index.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'result'] = 'Template'
    df.loc[(df.index.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'confidence'] = np.random.uniform(0.98,0.99)
    # replace empty Property column with 'undefined'
    df['Property'] = df['Property'].replace(np.nan, 'undefined', regex=True)

    a1 = time.time()
    a1 = round(a1-a0,2)
    print('\n')
    print('__'*50)
    print('TIME TAKEN BY END CODE ----',a1)
    
    return relative_bbox , maxIOU_indices
    
    


##################################################################################

#print('@*@'*100)
#anchor_info = {}
# iterating for all the tempalates to match the target file
def find_template(org_data):

    print('##$$##'*100)
    
    #y = org_data[0]
    not_use_grid = True
    y = org_data[0]
    anchor_flag = org_data[1]
    df = org_data[2]
    
    templateId_temp = str(y['_id'])
    anchor_info = {}
    a0 = time.time()
    #if anchor_found_flag:
    #    break
    anchor_found_flag = False
    
    predicted_grid_num = None
    height_width_found = False
    anchor_matched = False     
    #print('template_no ------ ',template_no)
    #print('anchor--------------------------------------------------flags')

    if anchor_flag not in y.keys() or y[anchor_flag]==None: 
        print('______________________________FOUND NULL IN ANCHOR SKIPPING FOR__________________________________',{anchor_flag}, 'of Vendor ',{y['templateName']})
        return anchor_info
    
    if anchor_flag=='Vendor_GSTIN' and len(y['Vendor_GSTIN_alt']) < 1:
        print('______________________________FOUND ONLY ONE VENDOR GSTIN SKIPPING FOR VENDOR GSTIN SEARCH__________________________________',{anchor_flag}, 'of Vendor ',{y['templateName']})
        return anchor_info
    
    
    print('anchor flag used --',anchor_flag)
    print('template vendor name-----',y[anchor_flag])
    # VendorName info stored in db
    try:
        ak_bbox = [d for d in y['fdq'] if d['field']==anchor_flag][0]
    except Exception as e:
        print("ERROR found for anchor key----",e)
        return anchor_info

        
    # Getting the XScale and YScale values to adjust the anchor bbox in target file 
    try:

        template_left = y['doc_leftX']
        template_top = y['doc_topY']
        template_right = y['doc_rightX']
        template_bottom = y['doc_bottomY']

        print('doc text corrds used -----------------------')
        print(template_left,template_top ,template_right , template_bottom)



        template_text_height = template_bottom - template_top
        template_text_width = template_right - template_left


        ##########################################3

        target_top = min(df['topY'])
        target_bottom = max(df['bottomY'])
        target_left = min(df['leftX'])
        target_right = max(df['rightX'])

        target_text_width = target_right - target_left
        target_text_height = target_bottom - target_top
        #####################################################

        #XScale = template_text_width/target_text_width
        #YScale = template_text_height/target_text_height
        XScale = target_text_width/template_text_width
        YScale = target_text_height/template_text_height

        print('Calculated scales -----',XScale,YScale)
        print('BEFORE AK BBOX----',ak_bbox)
        #target 
        ak_bbox['leftX'] = ak_bbox['leftX']*XScale
        ak_bbox['rightX'] = ak_bbox['rightX']*XScale
        ak_bbox['topY'] = ak_bbox['topY']*YScale
        ak_bbox['bottomY'] = ak_bbox['bottomY']*YScale
        print('AFTER AK BBOX----',ak_bbox)

        height_width_found = True
        X_Y_Scale = [XScale,YScale]
    except Exception as e:
        X_Y_Scale = [1,1]
        template_text_height = 0
        template_text_width = 0
        target_text_height = 0
        target_text_width = 0
        print('__*___'*50)
        print('Error in loading text height and width---',e)


    #template_h , template_w  = template_text_height , template_text_width
    # Getting the grid for actul anchor in tempalate 
    #print('\n')
    a1 = time.time()
    a1 = round(a1-a0,2)
    print('\n')
    print('TIME TAKEN BY FIND SCALE VALUES ----',a1)


    a0 = time.time()
    anchor_key_values  = [d for d in y['fdq'] if d['field']==anchor_flag][0]
    anchor_key_values = {'leftX':anchor_key_values['leftX'],'topY':anchor_key_values['topY'],'rightX':anchor_key_values['rightX'],'bottomY':anchor_key_values['bottomY']}
    
    print('height_width_found---',height_width_found)
    if height_width_found:
        print('height---',template_text_height )
        print('width---',template_text_width)
        #actual_grid_num = get_grid_num(2,4 , template_text_width ,template_text_height ,anchor_key_values)

        print('anchor_key_values ---',anchor_key_values)
        print(template_text_width ,template_text_height ,template_left,template_top )
        grid_data = {'anchor_key_values':anchor_key_values,'template_text_width':template_text_width,'template_text_height':template_text_height,'template_left':template_left,'template_top':template_top}

        print('-----------actaul grid data sending-------------',grid_data)

        actual_grid_num , grid_bboxes = get_grid_num(2,6 , template_text_width ,template_text_height ,template_left,template_top , anchor_key_values)
        a1 = time.time()
        a1 = round(a1-a0,2)
        print('\n')
        print('TIME TAKEN TO FIND ACTAUAL GRID ----',a1)

        print('***************actual_grid_num************',actual_grid_num)

    print('anchor flag used --',anchor_flag)
    print('template vendor name-----',y[anchor_flag])

    #################################################################################3
    # search for VendorName at the exact same location as stored in db
    print('\n')
    a0 = time.time()
    print(f'DIRECT BBOX matching...all_bbox:{ak_bbox}')
    #lst = df[(df['leftX']>=ak_bbox['leftX']) & (df['topY']>=ak_bbox['topY']) & (df['rightX']<=ak_bbox['rightX']) & (df['bottomY']<=ak_bbox['bottomY']) & (df['pageNo'] == ak_bbox['pageNo'])]['Name'].values.tolist()
    #bbox_vendorName = (' ').join(lst)

    lst , box_list= get_max_iou_boxes(df,ak_bbox,0.7)
    bbox_vendorName = (' ').join(lst)

    print('\n')
    print('len(matched VendorName):',len(lst),'bbox vendor:',bbox_vendorName,' -- template vendor:',y[anchor_flag],'fuzzy match:', fuzz.ratio(bbox_vendorName, y[anchor_flag]))
    # fuzzy match predicted and stored VendorName
    fuzzy_match = fuzz.ratio(bbox_vendorName, y[anchor_flag])
    print('FUZZ MATCH---',fuzzy_match)
    if len(lst)>0 and fuzzy_match> 90:
        print('start 4')
        #box_list = df[(df['leftX']>=ak_bbox['leftX']-2) & (df['topY']>=ak_bbox['topY']-8) & (df['rightX']<=ak_bbox['rightX']+2) & (df['bottomY']<=ak_bbox['bottomY']+2)][['leftX','topY','rightX','bottomY']].values.tolist()
        #predicted_anchor_bbox = merge_boxes(box_list[0],box_list[-1])
        print('BOX_LIST---',box_list)
        predicted_anchor_bbox = merge_boxes(box_list)      
        if height_width_found:
            predicted_grid_num ,grid_bboxes = get_grid_num(2,6,target_text_width,target_text_height,target_left,target_top,predicted_anchor_bbox)
            if predicted_grid_num==actual_grid_num and len(actual_grid_num)!=0 or not_use_grid:
                print('Found Predicted grid num------',predicted_grid_num)
                print('*#*'*50)
                print('actual_grid_num--',actual_grid_num)
                print('predicted_grid_num --',predicted_grid_num)
                print('*#*'*50)
                if fuzzy_match==100:
                    print('--------found complete match exit vendor search----')
                    anchor_found_flag = True
                anchor_matched = True
                anchor_info = {'alt_anchor_value':bbox_vendorName,'templateId':templateId_temp ,'anchor_flag':anchor_flag,'template_name':y[anchor_flag],'actual_achor_value':y[anchor_flag],anchor_flag:bbox_vendorName,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox, 'anchor_key_values':anchor_key_values,'grid_bboxes':grid_bboxes}
            else:
                anchor_matched = False

        else:
            #print('BOX_LIST---',box_list)
            #predicted_anchor_bbox = merge_boxes(box_list)
            print('final--------------bbox_anchor-----------',predicted_anchor_bbox)
            anchor_matched = True
            anchor_info = {'alt_anchor_value':bbox_vendorName,'templateId':templateId_temp ,'anchor_flag':anchor_flag,'template_name':y[anchor_flag],'actual_achor_value':y[anchor_flag],anchor_flag:bbox_vendorName,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox, 'anchor_key_values':anchor_key_values,'grid_bboxes':grid_bboxes}

    a1 = time.time()
    a1 = round(a1-a0,2)
    print('\n')
    print('__'*50)
    print('TIME TAKEN BY DIRECT BBOX MATCHING VALUES ----',a1)



    a0 = time.time()
    # If bbox direct bbox not  match serach in OCR for anchor values
    if anchor_matched == False and ak_bbox!=None:
        anchor_arry = y[anchor_flag+'_alt']
        print('-----alternate keys in anchor----',anchor_arry)
        for anchor_value in anchor_arry:
            print('running for ----------',anchor_value)
            box_list = []
            print('SEARCHING ANCHOR TEXT IN OCR.....')
            # search vendorName in ocr text whose fuzzy match > 95%
            #anchorKey_matchedText = df[df['Name'].map(lambda x: fuzz.ratio(x,y[anchor_flag]))>95][:1]
            anchorKey_matchedText = df[df['Name'].map(lambda x: fuzz.ratio(remove_strings_inside_brackets(x),anchor_value))>90][:1]
            #anchorKey_matchedText = anchorKey_matchedText[anchorKey_matchedText['topY'].map(lambda x: x<1500)][:1]
            #anchorKey_matchedText = anchorKey_matchedText[anchorKey_matchedText['topY']<1500][:1]

            print(f'anchorKey_matchedText:{anchorKey_matchedText[["level_0","Name","Property"]]}')

            # when vendorName is matched with single row of ocr 
            if len(anchorKey_matchedText)==1:
                predicted_anchor_bbox = anchorKey_matchedText[['leftX','topY','rightX','bottomY','pageNo']].iloc[0].to_dict()
                #anchor_matched = True
                predicted_val = anchorKey_matchedText['Name'].iloc[0]
                matched_df_words = predicted_val.split(' ')
                anchor_words = anchor_value.split(' ')
                fuzzy_match = fuzz.ratio(predicted_val,anchor_value)
                print('going sin------------------------',fuzzy_match)
                print(f"Single OCR matched:{anchorKey_matchedText['Name'].iloc[0]}")
                print(f'Predicted anchor box:{predicted_anchor_bbox}')
                if height_width_found:
                    predicted_grid_num ,grid_bboxes = get_grid_num(2,6,target_text_width,target_text_height,target_left,target_top,predicted_anchor_bbox)

                    #predicted_grid_num = get_grid_num(2,4,target_text_width,target_text_height,predicted_anchor_bbox)
                    print('Found Predicted grid num------',predicted_grid_num)
                    if predicted_grid_num==actual_grid_num and len(actual_grid_num)!=0 or not_use_grid:
                        print('*#*'*50)
                        print('actual_grid_num--',actual_grid_num)
                        print('predicted_grid_num --',predicted_grid_num)
                        print('*#*'*50)
                        anchor_matched = True
                        anchor_info = {'alt_anchor_value':anchor_value,'templateId':templateId_temp ,'anchor_flag':anchor_flag,'template_name':y[anchor_flag],'actual_achor_value':y[anchor_flag],anchor_flag:bbox_vendorName,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox, 'anchor_key_values':anchor_key_values,'grid_bboxes':grid_bboxes}
                        print('anchor_info---',anchor_info)
                        if fuzzy_match==100:
                            print('--------found complete match exit vendor search----')
                            anchor_found_flag = True


                        #anchor_info = {'anchor_flag':anchor_flag,'template_name':y['Vendor_Name'],'actual_achor_value':y[anchor_flag],anchor_flag:bbox_vendorName,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox}
                    else:
                        anchorKey_matchedText = []
                        anchor_matched = False

                else:
                    anchor_matched = True
                    anchor_info = {'alt_anchor_value':anchor_value,'templateId':templateId_temp ,'anchor_flag':anchor_flag,'template_name':y[anchor_flag],'actual_achor_value':y[anchor_flag],anchor_flag:bbox_vendorName,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox, 'anchor_key_values':anchor_key_values,'grid_bboxes':grid_bboxes}
                    print('anchor_info---',anchor_info)



            # when vendorName is splitted in multiple rows of ocr
            ###################################################################################################
            if len(anchorKey_matchedText)==0:
                replace_list = [',','(',')',';',':','amp ','amp; ','& ','-','.']
                replace_list.extend(igonore_words)
                
                anchor_value = remove_strings_inside_brackets(anchor_value)
                actual_anchor_value = anchor_value
                
                for c in replace_list:
                    #anchor_value = str(anchor_value).replace(c,'')
                    
                    anchor_value = str(anchor_value).strip().lower().replace(c.lower(),'')
                print('anchor_value after removing stop special characters ----------',anchor_value)
                
                anchor = str(anchor_value).strip().lower()
                anchor_words = anchor.split(' ')
                print(f"Multiple OCR matching, ANCHOR WORDS:{anchor_words}")
                # pointer used to keep track of matched words
                ptr=0
                reset_ptr_count = 0
                matched_df_words = []
                for i in range(len(df)):
                    # split df row on space if there are more than 1 words in the df row
                    dfName_lst = df['Name'].iloc[i].strip().lower().split(' ')
                    
                    #Reset condition if anchor start word is found twice in a row
                    if ptr == 1 and  dfName_lst[0]==anchor_words[0]:
                        print('FOUND CONTINUE VENDOR RESETTING---',ptr)                                    
                        ptr = 0
                        matched_df_words =[]
                        box_list = []
                        matched_df_words = []
                    
                        
                    #Break if found complete vendor 
                    if ptr==len(anchor_words):
                        #vendor_found_count+=1
                        #single_vendor_found = y[anchor_flag]

                        fuzzy_match = fuzz.ratio(matched_df_words, anchor_words)
                        print(' FUZZ RATIO FOUND ------>',fuzzy_match)
                        ##################################################
                        predicted_anchor_bbox = merge_boxes(box_list)
                        #if predicted_anchor_bbox['topY']<quad:
                        print(f'****** OCR matching->Predicted anchor box:{predicted_anchor_bbox}')
                        print('height used ---',height_width_found) 
                        print(' box_list------', box_list)
                        print('--############--',y[anchor_flag])
                        print('Matched Anchor words ----',matched_df_words)
                        print('Actaul Anchor words-----',anchor_words)
            
                        if height_width_found: 
                            #predicted_grid_num = get_grid_num(2,4,target_text_width,target_text_height,predicted_anchor_bbox)
                            predicted_grid_num ,grid_bboxes = get_grid_num(2,6,target_text_width,target_text_height,target_left,target_top,predicted_anchor_bbox)

                            if predicted_grid_num==actual_grid_num and len(actual_grid_num)!=0 or not_use_grid:
                                print('Found Predicted grid num------',predicted_grid_num)
                                if fuzzy_match >= 90:
                                    print('--------found complete match exit vendor search----')
                                    anchor_found_flag = True

                                print('*#*'*50)
                                print('actual_grid_num--',actual_grid_num)
                                print('predicted_grid_num --',predicted_grid_num)
                                print('*#*'*50)
                                anchor_matched = True
                                anchor_info = {'alt_anchor_value':actual_anchor_value,'templateId':templateId_temp ,'anchor_flag':anchor_flag,'template_name':y[anchor_flag],'actual_achor_value':y[anchor_flag],anchor_flag:bbox_vendorName,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox, 'anchor_key_values':anchor_key_values,'grid_bboxes':grid_bboxes}
                                print('anchor_info--',anchor_info)
                                break
                                
                            else:
                                anchor_matched = False
                                print('---------FOUND WRONG GRID RESETING VALUES------------')
                                ptr = 0
                                matched_df_words =[]
                                box_list = []
                                matched_df_words = []   
                                
                        else:
                            anchor_matched = True
                            anchor_name = ' '.join(matched_df_words)
                            #anchor_info = {'template_name':y['Vendor_Name'],'actual_achor_value':anchor_value,anchor_flag:anchor_name,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox}
                            #anchor_info = {'anchor_flag':anchor_flag,'template_name':y['Vendor_Name'],'actual_achor_value':y[anchor_flag],anchor_flag:bbox_vendorName,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox}
                            #predicted_grid_num = get_grid_num(2,4,target_text_width,target_text_height,predicted_anchor_bbox) 
                            anchor_info = {'alt_anchor_value':actual_anchor_value,'templateId':templateId_temp ,'anchor_flag':anchor_flag,'template_name':y[anchor_flag],'actual_achor_value':y[anchor_flag],anchor_flag:bbox_vendorName,'match':fuzzy_match,'predicted_bbox':predicted_anchor_bbox, 'anchor_key_values':anchor_key_values,'grid_bboxes':grid_bboxes}

                    #############################################################    
                    if len(box_list)!=0 and ptr!=len(anchor_words):
                        if abs(box_list[0][3]-df['topY'].iloc[i])>200 or int(box_list[-1][4])!= int(df['pageNo'].iloc[i]):
                            print('WRONG WORD PREDICTED CLEAR PREDICTIONS at ----',i)
                            ptr = 0
                            matched_df_words =[]
                            box_list = []
                            matched_df_words = []

                        level_0 = df['level_0'].iloc[i]                        
                        if len(box_list) > 0 and abs(box_list[-1][5] - level_0) > 3 :
                            print('----WRONG WORD FOR IN SAME LINE---',i)
                            ptr = 0
                            matched_df_words =[]
                            box_list = []
                            matched_df_words = []

                    
                    if len(dfName_lst)>1:
                        # match ocr vendorName list splitted on words with template vendorName list
                        if dfName_lst == anchor_words[ptr:]:
                            reset_ptr_count = i
                            matched_df_words.extend(df['Name'].iloc[i].split(' '))
                            print('list matching....')
                            box_list.append(df[['leftX','topY','rightX','bottomY','pageNo','level_0']].iloc[i].values.tolist())
                            # if complete list is matched assign pointer to last word index
                            ptr=len(anchor_words)
                            
                    
                    # if direct list not matched search word by word using the pointer
                    if ptr<len(anchor_words): 
                        add_bbox_one = False
                        for word in dfName_lst:
                            #print('DEEEEBUG',word,anchor_words,ptr)
                            try:
                                val = anchor_words[ptr]
                            except Exception as e:
                                print('ERROR IN SERACHING VALUE FROM OCR')
                                print('--->>>>>>>>>>>>>',e)
                                break
                            
                            for c in replace_list:
                                word = word.replace(c,'')
                                word = remove_strings_inside_brackets(word)
                            if fuzz.ratio(word,anchor_words[ptr])>=95:                             
                                reset_ptr_count = i
                                #print('df name:',df.Name.iloc[i])
                                # if single word matches with template vendorName word, 
                                # add it matched_df_words list; which is used to verify at end 
                                # if vendorName list of words matched with that of template list of words 
                                matched_df_words.append(word)
                                print('matched df name list:',matched_df_words,' at ',i)
                                # if word is matched temporarily remove that word from VendorName template list
                                anchor = anchor.replace(word,'')
                                print('anchor:',anchor_words[ptr:])
                                if len(dfName_lst)==1:
                                    box_list.append(df[['leftX','topY','rightX','bottomY','pageNo','level_0']].iloc[i].values.tolist())
                                #print(df[['leftX','topY','rightX','bottomY']].iloc[i].values.tolist())
                                # increment the pointer to the next word
                                ptr+=1
                                add_bbox_one = True
                                
                        if add_bbox_one and len(dfName_lst)>1:   
                            print('Append 2 in 1 box')
                            box_list.append(df[['leftX','topY','rightX','bottomY','pageNo','level_0']].iloc[i].values.tolist())

            ###################################################################################################
            #if height of template and predicted anchor is similar and width significantly less, 
            #adjust width/ht according to ratio of template and predicted values  
            if anchor_matched == 'Trueeeee':

                if('rightX' in predicted_anchor_bbox):
                    width_template_anchor_bbox = ak_bbox['rightX'] - ak_bbox['leftX']
                    width_predicted_anchor_bbox = predicted_anchor_bbox['rightX'] - predicted_anchor_bbox['leftX']
                    # width diff >= 20% of anchor width
                if  abs(width_predicted_anchor_bbox - width_template_anchor_bbox) >= width_template_anchor_bbox*0.2 :
                        ht_predicted_anchor_bbox = predicted_anchor_bbox['bottomY'] - predicted_anchor_bbox['topY']
                        ht_template_anchor_bbox = ak_bbox['bottomY'] - ak_bbox['topY']          
                        ht_width_ratio_template = ht_template_anchor_bbox/width_template_anchor_bbox
                        # diff less than 10% of word height
                        if abs(ht_template_anchor_bbox - ht_predicted_anchor_bbox) <= ht_template_anchor_bbox*0.1:
                            predicted_anchor_bbox['rightX'] = predicted_anchor_bbox['leftX'] + width_template_anchor_bbox#(ht_predicted_anchor_bbox/ht_width_ratio_template)
                            print(f'Multiple OCR matching->Predicted anchor_box after WIDTH adjustment:{predicted_anchor_bbox}')
                break
                #This break is for alternate key loop
    #return anchor_info , anchor_found_flag
    return anchor_info 
###################################################################################




#NEW CODE END
#****************************************************************************#
########################################################################################################
######################################################################################################
def templateSearch_Base2(df,config,data):
    
    
    global predicted_anchor_bbox
    global variable_level_fields
    global static_fields
    global staticField_actual_values
    global predicted_idx_found
    global y
    global anchor_set
    global use_fixed_page
    global use_only_variable_anchors
    global anchor_flag_list
    global gst_variations
    global igonore_words
    global alt_anchor_value
    

    #global vendor_found_count 
    #vendor_found_count = 0
    #global single_vendor_found
    #single_vendor_found = ""
    
   
    j0 = time.time()
    a0 = time.time()
    t0 = time.time()
    
    org_df = df.copy()
    orgId = str(data['orgId'])
    print("Connection Established   :   ",config['dbConnection']);
    myclient = pymongo.MongoClient(config['dbConnection'])
    db = myclient[config['db']]
    template_found = False
    templateId = None    
    global_search = False
    avoid_inf_loop = False
    df.dropna(subset=['Name'], how='all', inplace=True)
    df.reset_index(inplace = True)
    # mapper = {'Taxable_Amount': 'List_Taxable_Amount', 'Place_Of_Supply': 'List_Place_Of_Supply', 'Country_of_Supply': 'List_Country_of_Supply', 'Tax_Rate': 'List_Tax_Rate', 'Total_Tax': 'List_Total_Tax', 'Payment_Terms': 'List_Payment_Terms', 'Payment_Due_Date': 'List_Payment_Due_Date', 'IGST': 'List_IGST', 'CGST': 'List_CGST', 'SGST': 'List_SGST', 'PO_Date': 'List_PO_Date', 'Customer_TRN': 'List_IsCustTRNOrNot', 'Currency': 'List_CurrencyorNot', 'Vendor_Name': 'List_SupNameorNot', 'Supplier_Address': 'List_AddressorNot', 'Invoice_Title': 'List_IsTitleOrNot', 'Customer_Name': 'List_CusNameorNot', 'Invoice_Number': 'List_InvoiceorNot', 'Invoice_Date': 'List_DateorNot', 'PO_Number': 'List_POorNot', 'Tax_Amount': 'List_TaxorNot', 'InvoiceTotalAmount': 'List_TotalorNot', 'Supplier_TRN': 'List_IsSuppTRNOrNot'}
    # variable_level_fields = ['Tax_Amount','Taxable_Amount','InvoiceTotalAmount','CGST','SGST','IGST']
    #static_fields = ['Vendor_Name','Vendor_GSTIN','Supplier_Address']
    staticField_dict = {}  
    staticField_actual_values = {}
    scanData = list(db.get_collection("scanningfields").find({'documentType': data['documentType']}))
    anchor_flag = 'Vendor_Name'
    #print(len(scanData))
    #print(f"---------------------------------------------------{scanData[0]}")
    
    #Doing this to reset index
    if 'level_0' in df.columns:
        df.drop(['level_0'],axis=1,inplace=True)
        df.reset_index(inplace=True)
    


    if(len(scanData) > 0):
        mapper = scanData[0]['mapper']
        
        variable_level_fields = scanData[0]['table_level_fields']
        static_fields = scanData[0]['static_fields']
        anchor_flag_list =  scanData[0]['anchorKey'] if 'anchorKey' in scanData[0] else ''
        keys = scanData[0]['keys']
        try:
            gst_variations = scanData[0]['GST_Variations']
        except Exception as e:
            gst_variations = []
            print('Exception for GST variations ----',e)
        

        try:
            igonore_words = scanData[0]['ignoreWords']
        except Exception as e:
            print(e)
            igonore_words = []
            print('______________No Ignore words present in scaningFields_______________')
        

        try:
            use_fixed_page = scanData[0]['use_fixed_page']
            use_only_variable_anchors = scanData[0]['use_only_variable_anchors']
        except Exception as e:
            use_fixed_page = False
            use_only_variable_anchors = []

            print('Exception-----',e)
            print('--CAN NOT LOAD THE USE FIXED PAGE DATA FROM SCANNING FIELDS ---')

        
    print('___length found of use_only_variable_anchors----',use_only_variable_anchors)
    '''pages = list(set(df['pageNo'].values))
    if len(pages)>8:
        print('PAGES EXCEEDED')
        valid_pages = pages[:2]+pages[-2:]
        df = df[df['pageNo'].isin(valid_pages)]'''
    
    
    
    
    #Code used when ML is giving vendor name
    ################################################
    vendor_df = df[df['Property']==anchor_flag[0]]
    vendorName_list = []
    bbox_list = []
    predicted_idx_found = []
    lineNo=0
    for idx,row in vendor_df.iterrows():
    #     print(vendor_df['index'].loc[idx])
        row_Name = vendor_df['Name'].loc[idx]
        row_lineNo = vendor_df['lineNumber'].loc[idx]
        row_bbox = vendor_df[['leftX','topY','rightX','bottomY']].loc[idx].values.tolist()
        # add 1st entry to VendorName list. NOTE: Can have problems if 1st prediction is wrong
        if lineNo==0:
            lineNo=int(row_lineNo)
            # add row Name in list only if not already added
            if row_Name not in vendorName_list:
                vendorName_list.append(row_Name)
                bbox_list.append(row_bbox)
        # if next entries are <=2 lineNo away then add them to VendorName list
        if int(row_lineNo) - lineNo <= 2:
            lineNo=int(row_lineNo)
            # add row Name in list only if not already added
            if row_Name not in vendorName_list:
                vendorName_list.append(row_Name)
                bbox_list.append(row_bbox)
    
    # vendorName_list
    predicted_vendorName = (' ').join(vendorName_list)
    print(f'*****ANCHOR USED:{anchor_flag} predicted:{predicted_vendorName}')
    ##################################################################################
    
    # predicted anchor boxes (merge bbox if value divided in multiple rows by ocr)
    predicted_anchor_bbox = df[df['Property']==anchor_flag][['leftX','topY','rightX','bottomY','pageNo']].values.tolist()
    if len(bbox_list)>1:
        predicted_anchor_bbox = merge_boxes(bbox_list[0],bbox_list[-1])
    elif len(bbox_list)==1:
        predicted_anchor_bbox = df[df['Property']==anchor_flag][['leftX','topY','rightX','bottomY','pageNo']].iloc[0].to_dict()

    print(f'Predicted anchor bbox:{predicted_anchor_bbox}')
    
    
    
    a1 = time.time()
    a1 = round(a1-a1,2)
    
    print('\n')
    print('__'*50)
    print('TIME TAKEN BY START VARIABLES AND ML CODE----',a1)
    ###################################################################################################
    #Template Serach Start 
    ###################################
    # static fields: whose values will directly be fetched from template stored in db
    
    
    #predicted_bbox = []
    anchor_matched = False
    print('anchor_flag_list used---',anchor_flag_list)
    # get list of all templates trained by same orgId
    orgId_lst = list(db.get_collection("templatetrainings").find({'documentType': data['documentType']}))
    #orgId_lst = list(db.get_collection("templatetrainings").find({"Vendor_Name":"Ashvar Cars India Pvt. Ltd."}))
    
    
    anchor_details = []
    anchor_found_flag = False
    
    
    try:
        
        results = []
        # Iteration for Document level anchors
        for anchor_flag in anchor_flag_list:    
            #import multiprocessing
            print("Running for flag 1")
            d0 = time.time()
            
            #anchor_flag = 'Vendor_Name'
            #org_data = {}
            #org_data['orgId_data'] = orgId_lst
            #org_data['anchor'] = anchor_flag

            args  = [(val,anchor_flag,df) for val in orgId_lst]
            num_processes = multiprocessing.cpu_count()
            print('num_processes---',num_processes)
            num_processes = num_processes - 2
            pool = multiprocessing.Pool(processes=16)
            anchor_info  = pool.map(find_template, args)
            
            
            #results.extend(anchor_info)
            #flag = res[1]
            pool.terminate()

            pool.close()
            #pool.terminate()
            pool.join()
            #pool.close()
            print('res----',anchor_info)
            #print('flag ---',flag)
            d1 = time.time()
            print('Total time by multiprocessing-----',round(d1-d0,2))
            anchor_details.append(anchor_info)
            
            
            
            
        j1 = time.time()
          
        #########################################################################
        print('\n')
        print('ANCHOR DETAIL FOUND-->>',anchor_details)
        print('\n')

        ########################################################################
        max_match = 0
        vendor_used = ''
        min_dist = 999999999999
        templateId = ''
        unique_anchor_matched = False
        
        
        #global predicted_anchor_bbox

        for i in range(len(anchor_details)):
            for j in range(len(anchor_details[i])):
                if unique_anchor_matched:
                    break
            
                if len(anchor_details[i][j])!=0:
                    #print(anchor_details[i][j])
                    boxes = anchor_details[i][j]['predicted_bbox']
                    template_anchor = anchor_details[i][j]['anchor_key_values']
                    #if anchor_details[i][j]['match'] > max_match:   
                    distance = (abs(boxes['leftX']-template_anchor['leftX'])**2 +  abs(boxes['topY']-template_anchor['topY'])**2) ** (1/2)
                    matching = anchor_details[i][j]['match']
                    ##############################################
                    templateId = anchor_details[i][j]['templateId']
                    template = list(db.get_collection("templatetrainings").find({ "_id" :ObjectId(templateId)}))
                    if 'unique_identifier' in template[0].keys():
                        #template = list(db.get_collection("templatetrainings").find({ "_id" :ObjectId(i)}))
                        try:
                            unique_anchor = template[0]['unique_identifier']
                            print('unique_anchor--',unique_anchor)
                            #min_top = min(df['topY'])
                            #max_top = max(df['bottomY'])
                            #template_top = template[0]['doc_topY']
                            template_bottom = template[0]['doc_bottomY']
                            unique_anchor_name = unique_anchor['Name']
                            unique_anchor_bottom = unique_anchor['bottomY']
                            print('template_bottom--',template_bottom)
                            print('unique_anchor_bottom--',unique_anchor_bottom)
                            unique_anchor_threshold = (unique_anchor_bottom+50)/template_bottom
                            unique_anchor_threshold = max(df['bottomY'])*unique_anchor_threshold
                            df_anchor = df[df['bottomY']<unique_anchor_threshold]
                            unique_anchor_matched , _ , _ = pick_right_word(unique_anchor_name,df_anchor)
                            if unique_anchor_matched:
                                templateId = anchor_details[i][j]['templateId']
                                #final_template = template
                                min_dist = distance
                                alt_anchor_value = anchor_details[i][j]['alt_anchor_value']
                                templateId = anchor_details[i][j]['templateId']
                                max_match = anchor_details[i][j]['match']
                                vendor_used = anchor_details[i][j]['actual_achor_value']
                                anchor_flag = anchor_details[i][j]['anchor_flag']
                                predicted_anchor_bbox = anchor_details[i][j]['predicted_bbox']
                                anchor_set = anchor_flag
                                break
                        except Exception as e:
                            print('ERROR: error in Template search!!!',traceback.format_exc())
                            print('Found Exception ----',e)
                            print('---Found Exception In unique identifier---')

                    ##############################################

                    if distance < min_dist and matching >= max_match:
                        alt_anchor_value = anchor_details[i][j]['alt_anchor_value']
                        templateId = anchor_details[i][j]['templateId']
                        min_dist = distance
                        max_match = anchor_details[i][j]['match']
                        vendor_used = anchor_details[i][j]['actual_achor_value']
                        anchor_flag = anchor_details[i][j]['anchor_flag']
                        predicted_anchor_bbox = anchor_details[i][j]['predicted_bbox']
                        anchor_set = anchor_flag


        
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print('Vendor used to set tempate ----',vendor_used, anchor_flag , templateId)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')




        a0 = time.time()
        orgId_lst = list(db.get_collection("templatetrainings").find({'documentType':  data['documentType']}))
        #orgId_lst = list(db.get_collection("templatetrainings").find({ "_id" :ObjectId(templateId)}))
        
        
        for template in orgId_lst:
        #print('template')
            if anchor_flag in template.keys() and template[anchor_flag]==vendor_used:
                print('set template------',vendor_used,anchor_flag)
                anchor_matched = True
                y = template

                try:
                    template_name = y['templateName']
                except Exception as e:
                    print(e)
                    print('Template name not avaiable---')
                    template_name = 'Not Available'
                
                break

        a1 = time.time()
        a1 = round(a1-a0,2)
        print('\n')
        print('__'*50)
        print('TIME TAKEN TO SET TEMPLATE AFTER VENDOR FOUND ----',a1)
        j1 = time.time()
        print("Time taken for template find ----------------",round(j1-j0,2))
        
        ####################################################################################
        ####################################################################################
        
        f0 = time.time()
        
        global variableAnchor_found
        global variable_anchor_field
        global variablePageNo
        global variable_anchor_dict
        global variableAnchor_bbox
        #global predicted_bboxes
        
        
        if anchor_matched==True or global_search:
            global anchor1_dict
            a0 = time.time()
            print('VENDOR NAME USED ------------------',y[anchor_flag])
            #anchor_flag = 'Vendor_Name'
            #print(f'ENTRY MATCHED for orgId:{orgId} and subscriberId:{subscriberId}')
            variableAnchor_found = False
            try:
                print(f"SELECTED ANCHOR FLAG:- {anchor_flag}")
                anchor1_dict = [d for d in y['fdq'] if d['field']==anchor_flag][0]
                #anchor1_dict = [d for d in y['fdq'] if d['field']=='Vendor_Name'][0]
            except IndexError as e:
                print(f'ERROR: {anchor_flag} Anchor dict not found:{traceback.format_exc()}')  
           
            variableAnchor_found = False
            variableAnchor_bbox = None
            variablePageNo = None
            variable_anchor_field = None
            variable_anchor_dict = None
            
            # get InvoiceTotalAmt or TaxableAmount as anchor for variable level fields
            #variable_level_fields = ["Invoice_Total_Amount"]
            #keys = {'List_TotalorNot':['received']}
            #mapper = {'Invoice_Total_Amount':'List_TotalorNot'}
            variable_anchor_field = None
            variable_fields = ['LEFT_Name','TOP_Name','RIGHT_Name','TOP_Name']
            if(len(variable_level_fields)>0) :
                for value in variable_fields:
                    variableAnchor_found , variableAnchor_bbox , variablePageNo , variable_anchor_field, variable_anchor_dict = find_variable_anchor(y,df,variable_level_fields[0],value)
                    if variableAnchor_found:
                        break
            
            a1 = time.time()
            a1 = round(a1-a0,2)
            print('\n')
            print('__'*50)
            print('TIME TAKEN TO SET ANCHOR FOR VARIABLE LEVEL FIELDS  ----',a1)

            
            print('\n')
            print('#############################')    
            print(variableAnchor_found)
            print(variableAnchor_bbox) 
            print(variablePageNo)
            print(variable_anchor_field)
            print(variable_anchor_dict)
            print('#############################')    
            
            
            template_found = True
            templateId = str(y['_id'])
            ml_fields_dict = y['fdq']
            predicted_bbox = []
            close_bbox_check = None
            temp_check = []
            relative_anchor_call = True
            
            
            #import multiprocessing
            ###############################################################################
            ###############################################################################
            print("Running code for fields extract")
            d0 = time.time()
            #anchor_flag = 'Vendor_Name'
            #org_data = {}
            #org_data['orgId_data'] = orgId_lst
            #org_data['anchor'] = anchor_flag

            ml_fields_dict  = [(val,anchor_flag,df) for val in ml_fields_dict]
            num_processes = multiprocessing.cpu_count()
            print('num_processes---',num_processes)
            num_processes = num_processes -2 
            pool = multiprocessing.Pool(processes=16)
            predicted_bboxes_df = pool.map(extract_fields,ml_fields_dict)
            
        
            #print(len(predicted_bbox))
            #results.extend(anchor_info)
            #flag = res[1]
            pool.terminate()

            pool.close()
            #pool.terminate()
            pool.join()
            
            predicted_bboxes = [i[0] for i in predicted_bboxes_df ]
            for i in range(len(predicted_bboxes_df)):
                field_dict = predicted_bboxes_df[i][0]
                maxIOU_indices = predicted_bboxes_df[i][1]
                #predicted_text = df.loc[(df.index.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'Name'].values
                predicted_text = df.loc[(df['level_0'].isin(maxIOU_indices)) & (df['pageNo'] == int(field_dict['pageNo']))]['Name'].values
    
                # check if static fields match, if not save the original trained values from template

                if field_dict['field'] in static_fields:
                    #staticField_actual_values.append(field_dict['Name'])
                    #staticField_actual_values[field_dict['field']]=field_dict['Name']
                    if field_dict['field'] == static_fields[0]:
                        print('__USING ALT NAME AS STATIC__')
                        staticField_actual_values[field_dict['field']]= alt_anchor_value    
                    else:
                        staticField_actual_values[field_dict['field']]=field_dict['Name']

                print('\n')
                print(f"------->TEMPLATE SET FOR: {predicted_text} as {field_dict['field']} at index:{maxIOU_indices}")
                print('---'*50)
                # assign the Property value and add entry 'TEMPLATE' in result column to signify field was matched
                # using TemplateSearch
                #df.loc[(df.index.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'Property'] = field_dict['field']
                #df.loc[(df.index.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'result'] = 'Template'
                #df.loc[(df.index.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'confidence'] = np.random.uniform(0.98,0.99)
                df.loc[(df.level_0.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'Property'] = field_dict['field']
                df.loc[(df.level_0.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'result'] = 'Template'
                df.loc[(df.level_0.isin(maxIOU_indices)) & (df.pageNo==int(field_dict['pageNo'])),'confidence'] = np.random.uniform(0.98,0.99)

                # replace empty Property column with 'undefined'
                df['Property'] = df['Property'].replace(np.nan, 'undefined', regex=True)
                print('\n')
                #print('_______________________________############___________________________________')
                #print(df[['Name','Property','result']].loc[maxIOU_indices])
                #print('_______________________________________________________________________________')
            
            df[['Name','pageNo','Property','result']].to_csv('temp.csv',index=False)
            print(df.Property.value_counts())
            
            d1 = time.time()
            print('Total time by multiprocessing finding template -----',round(j1-j0,2))
            print('------------------')
            print('Time taken to extract fields with multiprocessing---',round(d1-d0,2))
            print('****'*50)
    except Exception as e:
        
        print('ERROR: error in Template search!!!',traceback.format_exc())
        print(e)
        
        
        
    ############################################################################
    #############################################################################
    
    
    
    
    if template_found:
        for i in range(len(df)):
            if df['result'].iloc[i]!='Template' and df['result'].iloc[i]!='undefined':
                #print(df['Name'].iloc[i],i)
                df['Property'].iloc[i] = 'undefined'
    
    # Making all values predicted by ml and two pass undefied if template values are set
    template_values_set = set(df[df['result']=='Template']['Property'].values)
    if len(template_values_set)!=0:
        print('-----TOTAL VALUES SET BY TEMPLATE -----',template_values_set)
        for i in range(len(df)):
            if df['result'].iloc[i]!='Template' and df['Property'].iloc[i] in template_values_set:
                df['Property'].iloc[i] = 'undefined'
    df[['Name','pageNo','Property','result']].to_csv('temp2.csv',index=False)
                        
    #Code for static fields to set in csv
    ###################################################################
    print('***staticField_actual_values****',staticField_actual_values)
    #staticField_actual_static_values = {'Vendor_Name': 'JUPITER DYECHEM PVT. LTD.', 'Invoice_Title': 'TAX INVOICE', 'Vendor_GSTIN': '24AABCA2390M1ZP'}
    static_keys = staticField_actual_values.keys()
    static_values = list(static_keys)
    for i in range(len(static_values)):
        indexes = df[df['Property']==static_values[i]]['level_0'].values
        #print('field name ---',static_values[i])
        #print(indexes)
        if len(indexes)==1:
            print('Setting value for 1')
            df['Name'].iloc[indexes[0]]=staticField_actual_values[static_values[i]]
        elif len(indexes)>1:
            df['Name'].iloc[indexes[0]]=staticField_actual_values[static_values[i]]
            for j in indexes[1:]:
                print('removing extra rows ',j)
                df['Property'].iloc[j]='undefined'
                df['result'].iloc[j]='undefined'
                print(df['Property'].iloc[j])    
    
    df[['Name','pageNo','Property','result']].to_csv('temp3.csv',index=False)
            
    # Creating boundings boexes of predicted boxes from template on input file of images
    try:
        imgs = data['imagesPath']
        color = (0, 0, 255)
        fontScale = 1
        thickness = 2
        font = cv2.FONT_HERSHEY_SIMPLEX
        print('total images ----',len(imgs))
        print('images-->',imgs)
        for i in range(len(imgs)):
            image = cv2.imread(imgs[i]['imageFilePath'])
            print('Reading image -----',imgs[i]['imageFilePath'])
            print('Plotting for boxes -',len(predicted_bboxes))
            #for j in y['fdq']:
            for j in predicted_bboxes:
                if  'plot_box' in j.keys():
                    print('plotting skipping for --',j['field'])
                    continue
                if j['pageNo']==i :
                    startX = int(j['leftX'])
                    startY = int(j['topY'])
                    endX = int(j['rightX'])
                    endY = int(j['bottomY'])
                    org = (endX,startY)
                    org2 = (endX,endY+20)
                    text = j['field']
                    text2 = str(startX)+'_'+str(startY)+'_'+str(endX)+'_'+str(endY)
                    cv2.rectangle(image, (startX, startY), (endX, endY), (255,0,0), 3)
                    image = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False)
                    image = cv2.putText(image, text2, org2, font, fontScale, color, thickness, cv2.LINE_AA, False)

            name = imgs[i]['imageFilePath'].split('/')
            name[-1] = "001XXX100_local_"+name[-1]
            name  = '/'.join(name)
            print('Writting in debug image path ------',name)
            cv2.imwrite(name ,image)   

    except Exception as e:
        print('plotting debug bbox status -->',e)

    ######################################################
    
    
    try:
        df_debug = df[['Name','Property','result']]
        name = vendor_used+'.csv'
        df_debug.to_csv('debug_csv/'+name,index=False)
    except Exception as e:
        print('e')

    if template_found:
        print('TEMPLATE FOUND ID-->>>>>',templateId)
        print('Template Vendor Name used---->>>>>',vendor_used)
        print('Template Name ----',template_name)
        print('TEMPLATE ACTUAL NAME USED ------->',alt_anchor_value)        
    else:
        print('NO TEMPLATE WAS FOUND')
        
    t1 = time.time()
    total_time = round(t1-t0,2)
    print('Total time taken by template------',total_time)   
    return df, template_found, templateId, staticField_dict

