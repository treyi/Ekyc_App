
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
# file="MicrosoftTeams-image (20).png"  #TODO
# file="MicrosoftTeams-image (21).png"
# file="MicrosoftTeams-image (22).png"
# file="MicrosoftTeams-image (24).png"
# file="MicrosoftTeams-image (25).png"
# file="MicrosoftTeams-image (26).png"
# file="MicrosoftTeams-image (27).png"
# file="MicrosoftTeams-image (9).png"
# file="PAN.jpg"
# file="passport_1_front.jpg"
file="pass_1_back.jpg"
# file="passport_3_front.jpg"
# file="passport_3_back.jpg"
# file="short.jpeg"
# file="surya_AAdhar.jpg"
###---------------------testing method----------------------------
import base64


def convert_to_base64(file): 
    encoded_string=""
    with open(file,"rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
    return encoded_string

encoded_string=convert_to_base64(file)
file1 = open("myfile.txt", "w")
file1.writelines(str(encoded_string))
file1.close()
