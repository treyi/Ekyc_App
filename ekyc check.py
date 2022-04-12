
# !pip install flaml

# !pip install streamlit

from plistlib import InvalidFileException

from click import FileError
from Testing import *
from get_utils.Extract_Aadhar_Data import *
from get_utils.Extract_Driving_License import *
from get_utils.Extract_Pan_Data import *
from get_utils.Extract_Passport_Data import *
from azure_ocr_extract import *
from Data.error_handling import *
import streamlit as st

def header(url):
     st.markdown(f'<p style="color:#FF0000;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def verif(url):
     st.markdown(f'<p style="color:#008000;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def main():
    try:
        st.write("""# eKYC """)
        File = st.file_uploader("Upload a file",type = ["jpeg","jpg","pdf","png"],accept_multiple_files=True)
        # print("File is------------------------",File[0][name])
        encoded_file=""  #convert_to_base64(File)
        if File is not None and is_valid_extension(encoded_file): #DP_02
            if is_valid_file_size(encoded_file): #DP_04
                if is_file_encrypted(encoded_file):
                    text=""
                    if len(File)==1:
                        text = get_azure_ocr(File[0])

                    elif len(File)==2:
                        text = get_azure_ocr(File[0])
                        text1 = get_azure_ocr(File[1])

                    if text!=None:
                        mode_value=-1
                        if st.button("Submit"):
                            mode_value=decide_card(text)
                            if mode_value!=-1:
                                if mode_value == 0:  ##Aadhaar card
                                    # ["Name","Aadhar ID","DoB","Gender","Enrollment No.","Father Name","Address"]
                                    result_dict= Validate(mode_value,text)    
                                    if result_dict:
                                        Name = st.text_input("Name as per the Document",result_dict["Name"])
                                        ID = st.text_input("Unique ID",result_dict["Aadhar ID"])
                                        Date = st.text_input("Date of Birth",result_dict["DoB"])
                                        gender=st.text_input("Gender",result_dict["Gender"])
                                        enrolment=st.text_input("Enrolment No",result_dict["Enrollment No."])
                                        father_name=st.text_input("Father's Name",result_dict["Father Name"])
                                        address=st.text_input("Address",result_dict["Address"])

                                elif mode_value == 1:  ##Driving License
                                    # ["Name","Unique ID","Issue Date","RTA Division"]
                                    result_dict= Validate(mode_value,text)    
                                    if result_dict:
                                        Name = st.text_input("Name as per the Document",result_dict["Name"])
                                        license_id = st.text_input("Unique ID",result_dict["Unique ID"])
                                        issue_date = st.text_input("Date of Issue",result_dict["Issue Date"])
                                        rta_div=st.text_input("RTA Division",result_dict["RTA Division"])
                        
                                elif mode_value == 2:  ##PAN CARD
                                    # ["Name","PAN no.","DoB","Father Name"]
                                    result_dict= Validate(mode_value,text)    
                                    if result_dict:
                                        name = st.text_input("Name as per the Document",result_dict["Name"])
                                        father_name=st.text_input("Father's Name",result_dict["Father Name"])
                                        pan_number = st.text_input("Unique ID",result_dict["PAN no."])
                                        date_of_birth = st.text_input("Date of Birth",result_dict["DoB"])
                                        
                                
                                elif mode_value == 3: ##Passport Data 
                                    # ["Surname","Name","Passport no.","DoB","Issue Date","Expiry Date","PassportType","Country code","Gender","Birth Location","Resident","Nation"]
                                    extract_passport_obj=Extract_Passport_Data()
                                    front_side_data=""
                                    back_side_data=""
                                    if len(File)==1:
                                        file_is_front=extract_passport_obj.decide_side(text)
                                        if file_is_front:
                                            front_side_data = Validate(mode_value,text)
                                        else:
                                            back_side_data = extract_passport_obj.extract_pass_back(text)
                                    elif len(File)==2:
                                        first_file_is_front=extract_passport_obj.decide_side(text)
                                        if first_file_is_front:
                                            front_side_data = Validate(mode_value,text)
                                            back_side_data = extract_passport_obj.extract_pass_back(text1)
                                        else:
                                            second_file_is_front=extract_passport_obj.decide_side(text1)
                                            if second_file_is_front:
                                                front_side_data = Validate(mode_value,text1)
                                                back_side_data = extract_passport_obj.extract_pass_back(text)
                                            
                                    
                                    if front_side_data!="":
                                        # ["Surname","Name","Passport no.","DoB","Issue Date","Expiry Date","PassportType","Country code","Gender","Birth Location","Nationality","Place_Of_Issue"]
                                        col1 , col2 = st.columns(2)
                                        cola, colb = st.columns(2)
                                        col3, col4 = st.columns(2)
                                        col5, col6 = st.columns(2)
                                        
                                        Surname = col2.text_input("Enter Surname",front_side_data["Surname"])
                                        name = col1.text_input("Enter your Name",front_side_data["Name"])
                                        passport_num = st.text_input("Enter Passport Number",front_side_data["Passport no."])
                                        date_of_birth = st.text_input("Enter your Date of Birth",front_side_data["DoB"])
                                        issued_date = cola.text_input("Enter Issued Date",front_side_data["Issue Date"])
                                        expiry_date = colb.text_input("Enter Expiry Date",front_side_data["Expiry Date"])
                                        passport_type = col3.text_input("Enter Type",front_side_data["PassportType"])
                                        counry_code = col4.text_input("Enter Country Code",front_side_data["Country code"])
                                        nationality = col5.text_input("Enter Nationality",front_side_data["Nationality"])
                                        gender = col6.text_input("Enter Gender",front_side_data["Gender"])
                                        place_of_birth = st.text_input("Enter Place of Birth",front_side_data["Birth Location"])
                                        place_of_issue = st.text_input("Enter Place of Issue",front_side_data["Place_Of_Issue"])
                                    if back_side_data!="":
                                        # ["father","mother","spouse","address","file"]
                                        print("back data is not null---------------------",back_side_data)
                                        father_name = st.text_input("Enter Father'S Name/Legal Guardian",back_side_data["father"])
                                        mother_name = st.text_input("Enter your Mother's Name",back_side_data["mother"])
                                        spouse_name = st.text_input("Enter Name of spouse",back_side_data["spouse"])
                                        address = st.text_input("Enter Address",back_side_data["address"])
                                        file_num = st.text_input("Enter File No.",back_side_data["file"])

                                                
                                    
                                st.image("check-mark-verified.gif",width = 400)
                            else:
                                raise FileNotFoundError
                else:
                    raise PermissionError
            else:
                raise FileError
        else:
            raise InvalidFileException    
        
    except InvalidFileException:
        print("Please choose only Image or PDF file to upload  ")
        return "DF_02"
    except PermissionError:
        print("Unable to process the file please check the file that is uploaded")
        return "DF_03"
    except FileError:
        print("User is trying to upload a file that is more than 1 MB in size 	File size cannot exceed 1 MB. Please choose a different file to upload")
        return "DF_04"
    except FileNotFoundError:
        print("An unsupported image(s) is detected in the file. Please try again with different file.")
        return "DF_06"
    # except Exception as e:
    #     print("Exception while processing input---------------------------------",str(e))
    #     st.image("wrong.gif",width = 400)            
if __name__ == '__main__':
    main()
