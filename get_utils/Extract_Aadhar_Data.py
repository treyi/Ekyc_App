# from Azure_OCR import *
# from St_NER import *
from dateutil.parser import parse
import re



class Extract_Aadhar_Data():
    """
        This class handles various functions related to extracting data from Aadhar
    """
    def preprocess_text_tag(self,text_tag):
        """
            preprocess aadhaar text #TODO
        """
        reg="[a-zA-Z\S\s]+/\s"
        p = re.compile(reg)
        for i in range(len(text_tag)):
            if(re.search(p, text_tag[i])):
                x=re.sub(p,'',text_tag[i])
                text_tag[i]=x
        print('====AADHAR TEXT ===== ', text_tag)
        return text_tag
    
    
    def extract_gender(self,text_tag):
        """
            Extracts gender data from text tag
        """
        gender_m='male'
        gender_f='female'
        ind = [i for i in range(len(text_tag)) if (text_tag[i].lower().strip() == gender_m.lower().strip()) | (text_tag[i].lower().strip() == gender_f.lower().strip())]
        if ind==[]:
            print('yes')
            for i in range(len(text_tag)):
                if (re.findall('Male|MALE', text_tag[i])):
                    return 'Male'
                elif (re.findall('Female|FEMALE', text_tag[i])):
                    return 'Female'
                
            
            print('====IND==== ', ind)
        return text_tag[ind[0]]
    
    def extract_enrolment(self,text_tag):
        """
            returns enrollment number from adhaar text
        """
        x=""
        reg="[0-9]{4}/[0-9]{5}/[0-9]{5}"
        p = re.compile(reg)
        for i in range(len(text_tag)):
            if(re.search(p, text_tag[i])): 
                x=re.findall(p,text_tag[i])    
        return x
    
    def find_father(self,text_tag,name,is_long):
        """
            returns the name of the father in aadhaar card using S/O to identify father name
        """
        father_name=""
        for i in range(0,len(text_tag)):
            if (re.search('/O',text_tag[i])):
                print("yes------1111--------",text_tag[i])
                text=text_tag[i].replace(",","").replace("/O","")
                r=re.findall('[A-Za-z\s]+',text)
                print("r is------------------------",r)
                if r!=[]:
                    txt=[x for x in r if len(x)>1]
                    father_name= txt[0]
                break
                  
        if father_name=="" and is_long==True:
            print("father name is --------------",father_name,name)
            for i in range(0,len(text_tag)-1):
                text=text_tag[i]
                print("text---------------------------",text)
                name_exists=name in text
                print("name exists-------------------------",name_exists)
                if name_exists:
                    r=re.findall('[A-Za-z\s]+',text_tag[i+1])
                    father_name=r[0]
                    break
        return father_name

    
    def extract_address(self,text_tags,father_name,is_long):
            """
                 Extract address data from Aadhaar using regex - returns string o/p
            """
            pin_regex=re.compile("^[1-9]{1}[0-9]{2}[0-9]{3}$")  #TODO match for optional space b/n 3 digits
            start_ind=-1
            address_str=""

            for i in range(len(text_tags)):
                if (re.search('/O',text_tags[i])):
                    start_ind=i 
                    break
            if start_ind==-1 and father_name!="" and is_long==True:
                for i in range(0,len(text_tags)-1):
                    text=text_tags[i]
                    print("text---------------------------",text)
                    father_name_exists=father_name in text
                    print("father name exists-------------------------",father_name_exists)
                    if father_name_exists:
                        start_ind=i
                        break

            print("start index is----2222--------------",start_ind)
            
            if start_ind!=-1:
                address_list=[]
                pin_exists=False
                end_name_index=-1
                father_name_line=text_tags[start_ind]
                if "," in father_name_line:
                    end_name_index=father_name_line.index(",")
                    if end_name_index<len(father_name_line)-1:
                        remaining_str=father_name_line[end_name_index+1:len(father_name_line)]
                        print("remaining string----------------------",remaining_str)
                        address_list.append(remaining_str)     
                        
                print("address list----------------------------",address_list)
                for i in range(start_ind+1,len(text_tags)):
                    address_list.append(text_tags[i])
                    tag_digits=re.findall(r'\d+', text_tags[i])
                    if tag_digits !=[]:
                        for digit in tag_digits:
                            pin_match=re.match(pin_regex, digit)
                            print("m is-----------------",pin_match)
                            if pin_match is not None:
                                pin_exists=True
                                break
                        if pin_exists==True:
                            break

                print("address list is-------------------------------",address_list)
                address_str=" ".join(address_list)
            

            print("returned address is---------------",address_str)
            return address_str




    
    def match_pattern_aadhar(self,typ,text):   #matching for aadhar card
        """
            match aadhaar id or dob based on regex pattern
        """
        try:
            Aadhar_regex = "[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}"
            DOB_regex ="[0-9]{2}[-/.][0-9]{2}[-/.][0-9]{4}" #"\d{2}\/\d{2}\/\d{4}"
            
            num_of_digits = 10 if typ == "DOB" else 14
            regx= DOB_regex if typ == "DOB" else Aadhar_regex
            
            matched_pattern=""
            
            for element in text:     
                if typ == "DOB" and len(element) >= num_of_digits:
                    if (re.search('Year of Birth|YoB', element)):
                        match = re.match(r'.*([1-3][0-9]{3})', element)
                        if match is not None:
                            matched_pattern= match.group(1)
                            return matched_pattern    
                    
            for i in range(len(text)):
                if(re.search('DOB|Year of Birth|YoB', text[i])): 
                    start_ind=i
                    for i in range(start_ind,len(text)):
                        z = re.findall(regx, text[i])
                        if z:
                            matched_pattern= z[0]
                            return matched_pattern
            return matched_pattern
        except Exception as e:
            print("Exception in match_pattern_aadhaar",str(e))
            return None
    
    def extract_name(self,text):
        """ return names from aadhaar data """
        long=False
        name=""
        
        for i in range(len(text)):
            if (re.search('/O',text[i])):
                # print('====tex ii======== ', i)
                j=i
                long=True
                break
        if long == False:
            # print("----NO /O-----------")
            for i in range(len(text)):
                if 'To' in text[i] and any("/O" not in s for s in text):
                    # print('====text to ii======== ', i)
                    j=i+2
                    long=True
                    break
        if long==True:
            # print('=======LONG============')
            nm = text[j-1]
            print('-----Date or not ---- ', self.is_date(nm, fuzzy=True))
            if self.is_date(nm, fuzzy=True) == True:
                nm = text[j-2]
            if text.count(nm) == 1:
                names_lst = [i for i in text if i in nm]
                # print('===names_lst==== ',names_lst)
                nm = min(names_lst, key=len)
            print('Name====>> ', nm)
            name=nm

        else:
            # print('=======Short============')
            regex = re.compile('[A-Za-z]')
            t = []
            for i in text:
                len_match = len(regex.findall(i))
                if len_match == len(i.replace(' ', '')):
                    t.append(i)
            print('======.... ', t)
            try:
                if len(t[1]) < len(t[2]):
                    nm = t[2]
                else:
                    nm = t[1]
            except:
                nm = t[1]
            
            print('Count==== >>',text.count(nm))
            print('Name====>> ', nm)
            name=nm
        print("NAME IS_---------------------",name,long)
        return name,long
            
    
    def is_date(self,string, fuzzy=False):
        """
        Return whether the string can be interpreted as a date.

        :param string: str, string to check for date
        :param fuzzy: bool, ignore unknown tokens in string if True
        """
        try: 
            parse(string, fuzzy=fuzzy)
            return True

        except ValueError:
            return False


    def get_aadhar_data(self,text):  
        """extracts all the required fields from aadhar data and returns a dict"""
        
        required_fields=["Name","Aadhar ID","DoB","Gender","Enrollment No.","Father Name","Address"]
        
        result_dict={}
        for field in required_fields:
            result_dict[field]=""
       

        Aadhar_ID = self.match_pattern_aadhar("ID",text)
        date_of_birth = self.match_pattern_aadhar("DOB",text)
        
                
        # ["Name","Aadhar ID","DoB","Gender","Enrollment No.","Father Name","Address"]
        preprocessed_text=self.preprocess_text_tag(text)        
        name,is_long_format=self.extract_name(text)
        gender=self.extract_gender(preprocessed_text)
        father_name=self.find_father(preprocessed_text,name,is_long_format)
        address=self.extract_address(text,father_name,is_long_format)
        enroll_num=self.extract_enrolment(text)

        result_dict["Name"]=name
        result_dict["Aadhar ID"]=Aadhar_ID
        result_dict["DoB"]=date_of_birth
        result_dict["Gender"]=gender
        result_dict["Enrollment No."]=enroll_num
        result_dict["Father Name"]=father_name
        result_dict["Address"]=address

        return result_dict
