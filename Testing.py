from get_utils.Extract_Aadhar_Data import *
from get_utils.Extract_Driving_License import *
from get_utils.Extract_Pan_Data import *
from get_utils.Extract_Passport_Data import *
# from helper import extract_Aadhar_data 

def Validate(doc_type,text):
    extract_aadhar_obj=Extract_Aadhar_Data()
    extract_DrivingLicence_obj=Extract_Driving_License()
    extract_pan_obj=Extract_Pan_Data()
    extract_passport_obj=Extract_Passport_Data()
    
    Extracted_data = []
    if doc_type == 0:
        Extracted_data = extract_aadhar_obj.get_aadhar_data(text)
    elif doc_type == 1:
        Extracted_data = extract_DrivingLicence_obj.get_DrivingLicence_data(text)
    elif doc_type == 2:
        Extracted_data = extract_pan_obj.get_pan_data(text)
    elif doc_type == 3:
        Extracted_data = extract_passport_obj.get_passport_data(text)
    return Extracted_data

# def validate_pass_back(text):
#   extract_passport_obj=Extract_Passport_Data()
#   extract_back = extract_passport_obj.extract_pass_back(text)
#   return extract_back

def decide_card(text_tag):
  """
  mode values for each id type are as follows:
    aadhaar=0
    drivers_licence=1
    pan_card=2
    passport=3
  """
  print("INSIDE DECIDE CARD",text_tag)
  extract_aadhar_obj=Extract_Aadhar_Data()
  extract_DrivingLicence_obj=Extract_Driving_License()
  extract_pan_obj=Extract_Pan_Data()
  extract_passport_obj=Extract_Passport_Data()
  
  
  Driving_ID_regex = "^(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}"+"|([a-zA-Z]{2}[0-9]{2}[\\/][a-zA-Z]{3}[\\/][0-9]{2}[\\/][0-9]{5})"+"|([a-zA-Z]{2}[0-9]{2}(N)[\\-]{1}((19|20)[0-9][0-9])[\\-][0-9]{7})"+"|([a-zA-Z]{2}[0-9]{14})"+"|([a-zA-Z]{2}[\\-][0-9]{13})$"
  
  drivers_license_data=extract_DrivingLicence_obj.match_pattern_drive(Driving_ID_regex,'ID',text_tag)
  print("driving-------1111----------------",drivers_license_data)
  aadhar_data=extract_aadhar_obj.find_aadhar_number(text_tag)
  print("aadhaar-------2222----------------",aadhar_data)
  pan_data=extract_pan_obj.findPanCardNo(text_tag)
  print("pan_data-------3333----------------",pan_data)
  passport_data=extract_passport_obj.find_passport_no(text_tag)
  print("passport_data-------4444----------------",passport_data)
  passport_keyword_exists= extract_passport_obj.passport_keyword_exists(text_tag)
  print("passport_keyword-------5555----------------",passport_keyword_exists)

  mode_value=-1
  if aadhar_data is not None and aadhar_data!="":
    print("IT IS AN AADHAAR CARD!!!!")
    mode_value=0
  elif drivers_license_data is not None and drivers_license_data!="":
    print("IT IS AN DRIVING LICENSE!!!!")
    mode_value=1
  elif pan_data is not None and pan_data!="":
    print("IT IS AN PAN DATA!!!!")
    mode_value=2
  elif (passport_data is not None and passport_data!="") or (passport_keyword_exists==True):
    print("IT IS AN PASSPORT DATA!!!!")
    mode_value=3
  else:
    mode_value=-1
  
  print("mode value---------------",mode_value)
  return mode_value
  
    