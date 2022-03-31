import os
import json
import re
import time
from requests import get,post
from azure.ai.formrecognizer import FormRecognizerClient
from azure.core.credentials import AzureKeyCredential


def get_azure_ocr(filename):
    endpoint = "https://quixyocr.cognitiveservices.azure.com/"
    apim_key = "03462e450efa4e338d200900d30d8c7b"
    post_url = endpoint +"/formrecognizer/v2.1/prebuilt/invoice/analyze"
    text_lst = []
 
    print('================FILENAME-===============---- ', filename)

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': apim_key,
    }

    params = {
        "includeTextDetails": True
    }
    
    # print("========2222222222222222222=======")
    # print(post_url)

    # with open(filename, "rb") as f:
    #     data_bytes = f.read()

    try:
        resp = post(url=post_url, data=filename,
                    headers=headers, params=params)
        if resp.status_code != 202:
            #print("POST analyze failed:\n%s" % resp.text)
            return None
        #print("POST analyze succeeded: %s" %
            #resp.headers["operation-location"])
        get_url = resp.headers["operation-location"]
    except Exception as e:
        print("POST analyze failed:\n%s" % str(e))
        return None

    n_tries = 50
    n_try = 0
    wait_sec = 6
    while n_try < n_tries:
        try:
            resp = get(url=get_url, headers={
                    "Ocp-Apim-Subscription-Key": apim_key})
            resp_json = json.loads(resp.text)
            if resp.status_code != 200:
                #print("GET Invoice results failed:\n%s" % resp_json)
                return None
            status = resp_json["status"]
            if status == "succeeded":
                print("Invoice analysis succeeded.")
                res = resp_json['analyzeResult']['readResults']
                text_lst = []
                for i in range(len(res[0]['lines'])):
                    #print('==== ',res[0]['lines'][i]['text'])
                    text_lst.append(res[0]['lines'][i]['text'])
                    regex = re.compile(r'([A-Z][a-z]+(?: [A-Z][a-z]\.)? [A-Z][a-z]+)')
            
                return text_lst
            if status == "failed":
                print("Analysis failed:\n%s" % resp_json)
                return None
            # Analysis still running. Wait and retry.
            time.sleep(wait_sec)
            n_try += 1
            
        except Exception as e:
            print("GET analyze results failed:\n%s" % str(e))
            return None

        
        

# text_lst = get_azure_ocr("Data/MicrosoftTeams-image.png")
# print(text_lst)
#res = text_lst['analyzeResult']['readResults']

# text_lst = []
# #bbox_lst = []
# for i in range(len(res[0]['lines'])):
#     text_lst.append(res[0]['lines'][i]['text'])

# print("Text_list: ",text_lst)

#with open("Danfoss singapore.json", 'w') as fp:
#    json.dump(json_out, fp, indent=4)


# print('--short----->>', get_azure_ocr('Data/short.jpeg'))
#regex = re.compile(r'([A-Z][a-z]+(?: [A-Z][a-z]\.)? [A-Z][a-z]+)')
#regex = re.compile('[A-Za-z]')
# print('--surya_AAdhar_rotate----->>', get_azure_ocr('Data/surya_AAdhar_rotate.jpg'))
# print('--MicrosoftTeams-image----->>', get_azure_ocr('Data/MicrosoftTeams-image.png'))
# print('--MicrosoftTeams-image (1)----->>', get_azure_ocr('Data/MicrosoftTeams-image (1).png'))

#lst = get_azure_ocr('Data/giriteja.pdf')
#lst = ['Government of India', 'ŠOŠETO JÓ5', 'KANKANALA HAREESH', '83 36/ DOB: 17/06/1996', '3749 4977 3380', 'JŐšvá / Male', 'Issue Date: 30/09/2011', '3749 4977 3380', 'ERT 3ITER, HA']
#lst = ['-', 'Government of India', 'Alimineti Surya Prakash Reddy', '835 36 / DOB: 15/06/1998', 'Daxve / Male', '6304 6829 3217']
#lst = ['Government of India', 'LO', 'Vechalapu Raja Mavullu Kumar', '5e3 838/DOB: 12/03/2001', 'Jažvč/ MALE', '4014 7239 0748', 'VID : 9187 4510 7415 7397', 'esc']
#lst = ['>', '×', 'Government of India', 'Riyasat', 'UFFH fafel/ DOB: 01/01/1991', '95q / MALE', '6754 3973 8680', 'FRT HTER, ART YOUTOT']
# lst = ['Unique Identification Authority of India', 'Government of India', 'E-Aadhaar Letter', '62.5225/ Enrolment No .: 1391/30058/01624', 'Date: 05/08/2013', 'Muppidi V S Giri Teja Reddy (Swb 2 0 05 88 da 8%)', 'S/O: M Sasidhar Reddy, H NO 11-236/2, Sarapaka', 'Burgampad mandal, Burgampahad, Burgampahad,', 'Khammam', 'Andhra Pradesh, 507114', '50 e06 2020/ Your Aadhaar No .:', 'INFORMATION', 'Aadhaar is proof of identity, not of citizenship.', '6962 3446 8289', 'To establish identity, authenticate online.', 'This is electronically generated letter.', 'Signature valid', 'Digitally signed by', 'Kharakwal Amitabh', 'Date: 05/08/2013', 'www', '1947', '1800 300 1947', 'help@uidai.gov.in', 'www.uidai.gov.in', 'Aadhaar is valid throughout the country.', 'You need to enrol only once for Aadhaar.', 'Please update your mobile number and e-mail', 'address. This will help you to avail various services', 'in future.', 'bevolvos.', 'GOVERNMENT OF INDIA', 'AADHAAR', 'UNIQUE IDENTIFICATION AUTHORITY OF INDIA', 'Address:', 'Muppidi V S Giri Teja Reddy', 'S/O: M Sasidhar Reddy, H NO', '11-236/2, Sarapaka', 'pelos no./YoB:1995', 'do 11-236/2, 5-das', 'Burgampad mandal,', 'Dopo Male', 'Burgampahad, Burgampahad,', 'Khammam', 'Andhra Pradesh, 507114', '6962 3446 8289', '000 238, 507114', 'LO', 'Aadhaar - Aam Aadmi ka Adhikar']

#lst = ['wo wwit # 36 poli This passport contains 36 pages.', 'ARRA HORTON REPUBLIC OF INDIA', 'Type', 'Country Code', 'Passport No.', 'P', 'IND', 'P 1185460', 'MUPPIDI VENKATA SATHYASAI', 'Surname,', 'Given Name(s)', 'GIRITEJA REDDY', 'Nationality', 'Sex', 'ate of Birth', 'HERT/INDIAN', 'M', '21/05/1995', 'Place of Birth', 'GUNTUR, ANDHRA PRADESH', 'Girlja', 'Place of Issue', 'TIRUCHIRAPPALLI', 'Date of issue', '25/10/2016', 'Date of Expiry', '24/10/2026', 'P<INDMUPPIDI<VENKATA<SATHYASAI << GIRITEJA<RED', 'P1185460<6IND9505210M2610243 <<<<<<<<<<<<<<< 0']
# lst = ['HRA TURION REPUBLIC OF INDIA', '2124/ Type', 'Reg als / Country Code', 'URTare -i./ Passport No.', 'P', 'IND', 'J 1641130', 'JO-TA / Surname', 'JOSHI', 'PRIT TIT TH / Given Name(s)', 'PRIYA RAJENDRA', '₹recTac / Nationality', 'forT / Sex', 'INDIAN', 'F', '09/04/1969 th', '-', 'GI RIT / Place of Birth', 'LUCKNOW, U.P', 'VINI TY PI RIM / Place of Issue', 'MUMBAI', 'P. Josh', 'GIRI BA af farer / Date of Issue', '11/06/2010', '10/06/202 Spiry', 'P<INDJOSHI << PRIYA<RAJENDRA <<<<<<<<<<<<<<<<<<', 'J1641130<5IND6904096F2006109 <<<<<<<<<<<<<<< 4']
# text_tag = ['HRA URTOJ REPUBLIC OF INDIA', 'Type', 'Country Code', 'Passport No.', 'P', 'IND', 'Surname', 'J 1618712', 'JOSHI', 'Given Name(s)', 'RAJENDRA BADRIPRASAD', 'Nationality', 'Sex', 'Date of Birth', 'INDIAN', 'M', '24/12/1964', 'Place of Birth', 'MUMBAI', 'Place of Issue', 'MUMBAI', 'Date of Issue', 'Date of Expiry', '14/05/2010', '13/05/2020', 'P<INDJOSHI << RAJENDRA<BADRIPRASAD <<<<<<<<<<<<', 'J1618712<3IND6412249M2005135 <<<<<<<<<<<<<<< 4']
# print(text_tag)
# t = []
# for i in lst:
#     len_match = len(regex.findall(i))
#     if len_match == len(i.replace(' ', '')):
#         #print(i)
#         t.append(i)

# try:
#     if len(t[1]) < len(t[2]):
#         name = t[2]
#     else:
#         name = t[1]
# except:
#     name = t[1]
# print('Count==== >>',lst.count(name))
# print('Name====>> ', name)

# for i in range(len(text_tag)):
#     for i in range(len(text_tag)):
#       if 'Surname' in text_tag[i] and 'Given Name(s)' in text_tag[i+1]:
#           nm = text_tag[i-1]
#       elif "Surname" in text_tag[i]:
#           nm = text_tag[i+1]

# print("===Name==== ", nm)







