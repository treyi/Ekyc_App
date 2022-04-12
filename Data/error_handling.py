import base64
from base64 import b64decode
from distutils import extension
import imghdr
from io import BytesIO
from sys import api_version
import PyPDF2
from pdf2image import convert_from_bytes



# file="Driving_Licence.jpeg"
# file="giriteja.pdf"
# file="long.jpeg"
# file="MicrosoftTeams-image (10).png"
# file="MicrosoftTeams-image (11).png"
# file="MicrosoftTeams-image (12).png"
# file="MicrosoftTeams-image (14).png"
# file="MicrosoftTeams-image (15).png"
# file="MicrosoftTeams-image (16).png"
# file="MicrosoftTeams-image (17).png"
# file="MicrosoftTeams-image (18).png"
# file="MicrosoftTeams-image (19).png"
# file="MicrosoftTeams-image (20).png"
# file="MicrosoftTeams-image (21).png"
# file="MicrosoftTeams-image (22).png"
# file="MicrosoftTeams-image (24).png"
# file="MicrosoftTeams-image (25).png"
# file="MicrosoftTeams-image (26).png"
# file="MicrosoftTeams-image (27).png"
# file="MicrosoftTeams-image (9).png"
# file="PAN.jpg"
# file="passport_1.jpg"
# file="passport_2.jpg"
# file="short.jpeg"
# file="surya_AAdhar.jpg"


def is_valid_multipage(encoded_string): #DP_01   ##TODO
    is_valid_multipage=False
    decoded_string = base64.b64decode(encoded_string)
    is_pdf = decoded_string[1:4] == b'PDF'
    if is_pdf:
        images = convert_from_bytes(decoded_string)
        pdf_images_length = len(images)
        is_valid_multipage=True if pdf_images_length<=2 else False
    return is_valid_multipage

def is_valid_extension(encoded_string):  #DP_02
    is_valid_extension=False
    decoded_string = b64decode(encoded_string)
    # extension = imghdr.what(None, h=decoded_string)
    extension = magic.from_buffer(decoded_string, mime=True)
    is_pdf = decoded_string[1:4] == b'PDF'
    is_valid_extension=True if (extension in ["jpeg","jpg","png"] or is_pdf==True) else False
    return is_valid_extension


def is_file_encrypted(encoded_string):  #DP_03
    is_encrypted=False
    decoded_string = base64.b64decode(encoded_string)
    is_pdf = decoded_string[1:4] == b'PDF'
    if is_pdf:
        is_encrypted = PyPDF2.PdfFileReader(BytesIO(decoded_string) ).isEncrypted
    return is_encrypted

def is_valid_file_size(encoded_string):   #DP_04
    is_valid_size=False
    file_size_in_bytes = (len(str(encoded_string)) - 814) / 1.37
    file_size_in_mb=file_size_in_bytes//1000
    is_valid_size=True if file_size_in_mb>0 and file_size_in_mb<1000 else False
    return is_valid_size

##DP_05 ==> technical error in code
##DP_06 ==> unclear pdf/image==> mode=-1

def populate_json(reference_id,error_code,created_date_time):
    #get model version and api version from .env file
    error_msgs={
                    "DP_01":"Please choose only 2 or less than 2 files to upload",
                    "DP_02":"Please choose only Image or PDF file to upload", 
                    "DP_03":"Unable to process the file please check the file that is uploaded", 
                    "DP_04":"File size cannot exceed 1 MB. Please choose a different file to upload", 
                    "DP_05":"Unable to process the file now. Please try again later.",
                    "DP_06":"An unsupported image(s) is detected in the file. Please try again with different file." 
                }
    results = {
                'ReferenceID':reference_id,
                'status':'Fail',
                "statusCode": error_code,
                'createdDateTime':created_date_time, #
                'lastUpdatedDateTime':"",  #datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                'Modelversion':"",      
                'api_version' :"",      
                'error_message':error_msgs[error_code],
                'FormData' : []
                }
    return results











###---------------------testing method----------------------------
def convert_to_base64(file): ##TODO testing method- remove later
    encoded_string=""
    with open(file,"rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
    return encoded_string
