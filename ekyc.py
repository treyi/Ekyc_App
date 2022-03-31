
# !pip install flaml

# !pip install streamlit

from Testing import *
from get_utils.Extract_Aadhar_Data import *
from get_utils.Extract_Driving_License import *
from get_utils.Extract_Pan_Data import *
from get_utils.Extract_Passport_Data import *
from azure_ocr_extract import *

import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt

def header(url):
     st.markdown(f'<p style="color:#FF0000;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def verif(url):
     st.markdown(f'<p style="color:#008000;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def main():
    st.write("""# eKYC """)
    File = st.file_uploader("Upload a file",type = ["jpeg","jpg","pdf","png"],accept_multiple_files=True)
    extract_passport_obj=Extract_Passport_Data()
    
    if File is not None:
        if len(File)>1 and File[1] is not None:  
            text1 = get_azure_ocr(File[1])
    
        if len(File)>0 and File[0] is not None:
            text = get_azure_ocr(File[0])
            mode_value=None
            print("text is---------------------------------------",text)
            if st.button("Submit"):
                if len(File)==2:
                    
                    t=extract_passport_obj.decide_side(text)
                    if t==True:
                        fr=True
                        mode_value=decide_card(text)
                        print('fr')
                    else:
                        fr=False
                        print('back')
                        r=extract_passport_obj.decide_side(text1)
                        if r==True:
                            mode_value=decide_card(text1)
                            print(mode_value)
                        else:
                            print('Error')
                else:
                    mode_value=decide_card(text)
                if mode_value == 3: ##passport TODO
                    if len(File)==2:
                        if fr==True:
                            ans = Validate(mode_value,text)
                        else:
                            ans = Validate(mode_value,text1)
                    else:
                        ans = Validate(mode_value,text)
                    
                    col1 , col2 = st.columns(2)
                    a2 = col2.text_input("Enter Surname",ans[0])
                    a1 = col1.text_input("Enter your Name",ans[1])
                    a12 = st.text_input("Enter Passport Number",ans[2])
                    a3 = st.text_input("Enter your Date of Birth",ans[3])
                    cola, colb = st.columns(2)
                    a4 = cola.text_input("Enter Issued Date",ans[4])
                    a5 = colb.text_input("Enter Expiry Date",ans[5])
                    col3, col4 = st.columns(2)
                    a6 = col3.text_input("Enter Type",ans[6])
                    a7 = col4.text_input("Enter Country Code",ans[7])
                    col5, col6 = st.columns(2)
                    a8 = col5.text_input("Enter Nationality",ans[11])
                    a9 = col6.text_input("Enter Sex",ans[8])
                    a10 = st.text_input("Enter Place of Birth",ans[9])
                    a11 = st.text_input("Enter Place of Issue",ans[10])
                    if len(File)==2:
                        if fr==False:
                            ans1 = validate_pass_back(text)
                        else:
                            ans1 = validate_pass_back(text1)
                    

                        #text1 , _ = get_ocr(File[1])
                        #ans1 = validate_pass_back(text1)
                        ap1 = st.text_input("Enter Father'S Name/Legal Guardian",ans1[0])
                        ap2 = st.text_input("Enter your Mother's Name",ans1[1])
                        ap3 = st.text_input("Enter Name of spouse",ans1[2])
                        ap4 = st.text_input("Enter Address",ans1[3])
                        ap5 = st.text_input("Enter File No.",ans1[4])

                elif mode_value == 0:  ##Aadhaar card
                    # ["Name","Aadhar ID","DoB","Gender","Enrollment No.","Father Name","Address"]
                    result_dict= Validate(mode_value,text)    
                    Name = st.text_input("Name as per the Document",result_dict["Name"])
                    ID = st.text_input("Unique ID",result_dict["Aadhar ID"])
                    Date = st.text_input("Date of Birth",result_dict["DoB"])
                    gender=st.text_input("Gender",result_dict["Gender"])
                    enrolment=st.text_input("Enrolment No",result_dict["Enrollment No."])
                    father_name=st.text_input("Father's Name",result_dict["Father Name"])
                    address=st.text_input("Address",result_dict["Address"])

                elif mode_value == 1:
                    # ["Name","Unique ID","Issue Date","RTA Division"]
                    result_dict= Validate(mode_value,text)    
                    Name = st.text_input("Name as per the Document",result_dict["Name"])
                    license_id = st.text_input("Unique ID",result_dict["Unique ID"])
                    issue_date = st.text_input("Date of Issue",result_dict["Issue Date"])
                    rta_div=st.text_input("RTA Division",result_dict["RTA Division"])
        
                elif mode_value == 2:  ##PAN CARD
                    # ["Name","PAN no.","DoB","Father Name"]
                    result_dict= Validate(mode_value,text)    
                    name = st.text_input("Name as per the Document",result_dict["Name"])
                    father_name=st.text_input("Father's Name",result_dict["Father Name"])
                    pan_number = st.text_input("Unique ID",result_dict["PAN no."])
                    date_of_birth = st.text_input("Date of Birth",result_dict["DoB"])
                                    
                    
                st.image("check-mark-verified.gif",width = 400)
            
    # except Exception as e:
    #     print("Exception 2222---------------------------------",str(e))            
if __name__ == '__main__':
    main()
