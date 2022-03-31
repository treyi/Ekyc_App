import nltk
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import os
import re
from sner import Ner
 
#java_path = '/usr/java/jdk1.8.0_292'
java_path = 'C:/Program Files/Java/jdk-14.0.2'
os.environ['JAVA_HOME'] = java_path
 
# st = StanfordNERTagger('/home/quixymluser/bank/banks/core/utils/stanford-ner-2020-11-17/classifiers/english.all.3class.distsim.crf.ser.gz','/home/quixymluser/bank/banks/core/utils/stanford-ner-2020-11-17/stanford-ner.jar',
#  encoding='utf-8')
st = Ner(host='localhost',port=9199)
def get_Names(Text):
    ''' If there is MR or MRS mostly it is a Name'''
    
    #Name=''
    Final_Names=[]
    
    
    ''' If there is No MR or MRS Applying NER for first 25 sentences '''           
    for idx,i in enumerate(Text):   
        #print(i)         
        #pattern='[a-zA-Z.]'
        pattern='([a-zA-Z]+\s[a-zA-Z]+\s[a-zA-Z]+)|([a-zA-Z]+\s[a-zA-Z]+)'
        match = re.search(pattern, i) 
        Name=[]  #added
        if(match):
            #tokenized_text = word_tokenize(i)
            classified_text = st.tag(i)
            #print(classified_text)
            for j in classified_text:
                #print(j)

                if(j[1]=='PERSON'):
                    #Name=i
                    #print(j[0]) #added

                    Name.append(j[0]) #added
            Name=' '.join(Name)   #added
            #print(Name) 
                    #break
            if(Name):
                #Name=Name.rstrip()
                #print(Name)
                #print('Name:',Name)
                Final_Names.append(Name)
                #if len(Final_Names)>2:
                #    break
                
            #Name=''
            
    #print(Final_Names)
    return Final_Names
Text1=['Unique Identification Authority of India',
 'Government of India',
 'E-Aadhaar Letter',
 '62.5225/ Enrolment No .: 1391/30058/01624',
 'Date: 05/08/2013',
 'Muppidi V S Giri Teja Reddy (Swb 2 0 05 88 da 8%)',
 'S/O: M Sasidhar Reddy, H NO 11-236/2, Sarapaka',
 'Burgampad mandal, Burgampahad, Burgampahad,',
 'Khammam',
 'Andhra Pradesh, 507114',
 '50 e06 2020/ Your Aadhaar No .:',
 'INFORMATION',
 'Aadhaar is proof of identity, not of citizenship.',
 '6962 3446 8289',
 'To establish identity, authenticate online.',
 'This is electronically generated letter.',
 'Signature valid',
 'Digitally signed by',
 'Kharakwal Amitabh',
 'Date: 05/08/2013',
 'www',
 '1947',
 '1800 300 1947',
 'help@uidai.gov.in',
 'www.uidai.gov.in',
 'Aadhaar is valid throughout the country.',
 'You need to enrol only once for Aadhaar.',
 'Please update your mobile number and e-mail',
 'address. This will help you to avail various services',
 'in future.',
 'bevolvos.',
 'GOVERNMENT OF INDIA',
 'AADHAAR',
 'UNIQUE IDENTIFICATION AUTHORITY OF INDIA',
 'Address:',
 'Muppidi V S Giri Teja Reddy',
 'S/O: M Sasidhar Reddy, H NO',
 '11-236/2, Sarapaka',
 'pelos no./YoB:1995',
 'do 11-236/2, 5-das',
 'Burgampad mandal,',
 'Dopo Male',
 'Burgampahad, Burgampahad,',
 'Khammam',
 'Andhra Pradesh, 507114',
 '6962 3446 8289',
 '000 238, 507114',
 'LO',
 'Aadhaar - Aam Aadmi ka Adhikar']
#print(get_Names(Text1))

