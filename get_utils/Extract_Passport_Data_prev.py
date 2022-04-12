import re
class Extract_Passport_Data():
    """
        This class handles various functions related to extracting data from Passport
    """

    def preprocess_text_tag(self,text_tag):   # removing spaces and text before slash
        """ 
            preprocess pan text 
            input: list of strings
            output: list of strings 
        """
        try:
            reg="[a-zA-Z\S\s]+/\s"
            p = re.compile(reg)
            for i in range(len(text_tag)):
                if(re.search(p, text_tag[i])):
                    x=re.sub(p,'',text_tag[i])
                    text_tag[i]=x
            return text_tag
        except Exception as e:
            print("Exception in preprocess_text_tag in Extract_Passport_Data class",str(e))
            return None

    def find_passport_no(self,text_tag):        
        """
            returns passport number from ocr text using regex
            input:list of strings
            output:string 
        """
        try:
            if text_tag != None:
                reg="(^[A-Z₱][0-9]+)"
                p = re.compile(reg)
                passport_num=""
                for i in range(len(text_tag)):
                    if(re.search(p, text_tag[i])):
                        match=re.findall(p,text_tag[i])
                        if match:
                            passport_num=match[0]
            
            return passport_num
        except Exception as e:
            print("Exception in find passport no.",str(e))
            return ""    
    
    def passport_keyword_exists(self,text_tag):         
        """
            checks if passport keyword exists at the back or front of the passport
            input: list of strings
            output: boolean
        """
        try:
            if text_tag != None:
                passport_str="passport"
                passport_keyword_exists=False
                for i in range(len(text_tag)):
                    if(passport_str in text_tag[i].lower()):
                        passport_keyword_exists=True
                        break                       
            
            return passport_keyword_exists
        except Exception as e:
            print("Exception in find passport keyword exists method",str(e))
            return False    
    
    
    
    def get_gender(self,text_tag):
        """
            returns the gender from the given text
            input:list of strings
            output: string=> male/female/""
        """
        try:
            gender_reg='^[A-Z]$'
            q= re.compile(gender_reg)
            gender=""
            for i in range(len(text_tag)):
                if(re.search('D[a-z]+e of B[a-z]+h|[A-Za-z]+te of B[a-z]+|D[a-z]+ of [A-Za-z]+h', text_tag[i])): 
                    print("111--------------------------------------------",text_tag[i])
                    for j in range(i+1,len(text_tag)):
                        print("222--------------------------------------------",text_tag[i])
                        match=re.findall(q,text_tag[j])
                        print("333--------------------------------------------",match)
                        if match:
                            print("444--------------------------------------------",match)
                            gender_match=match[0]
                            print("555--------------------------------------------",gender_match)
                            gender="Male" if gender_match=="M" else "Female"
                            print("6666-------------------------11111-----------",gender)
                            break
                    if gender!="":
                        break
            print("gender is-------------------2222-------------",gender)
            return gender
        except Exception as e:
            print("Exception in get_gender method in Extract_Passport_Data class",str(e))
            return ""

    def extract_code_and_type(self,text_tag):
        """
            returns the code and type of the passport using regex
            input: list of strings
            output: tuple =>(passport_type,code)
        """
        try:
            reg_type="^P|S|D$"
            reg_code='^[A-Z]{3}$'
            p = re.compile(reg_type)
            c= re.compile(reg_code)
            for i in range(len(text_tag)):
                if(re.search(p, text_tag[i])): 
                    type_list=re.findall(p,text_tag[i])    
                if(re.search(c, text_tag[i])): 
                    code_list=re.findall(c,text_tag[i]) 
            passport_type=type_list[0] if type_list!=[] else ""
            code=code_list[0] if code_list!=[] else ""
            return passport_type,code
        except Exception as e:
            print("Exception in extract_code_and_type method in Extract_Passport_Data class",str(e))
            return None
    
    def find_surname(self,text_tag):
        """
            finds surname from the given text by searching for surname keyword
            input:list of strings
            output:string
        """
        try:
            reg="(^[A-Z]+\s[A-Z\s]*\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)|(^[A-Z]+$)"
            p = re.compile(reg)
            surname=""
            if text_tag != None:
                j=-1
                for i in range(len(text_tag)):
                    if(re.search('Surname', text_tag[i])):
                        j=i
                j = 6 if j==-1 else j
                for i in range(j,len(text_tag)):
                    if (re.findall(p,text_tag[i])):
                        surname= text_tag[i]
                        break
            return surname
        except Exception as e:
            print("Exception in extract_code_and_type method in Extract_Passport_Data class",str(e))
            return ""
        
    
    def get_nationality(self,text_tag): 
        """
            extracts nationality from the given text
            input:list of strings
            output:string
        """
        try:
            reg='^[A-Z0-9/s]+'
            p = re.compile(reg)
            nationality=""
            for i in range(len(text_tag)):
                if(re.search('D[a-z]+e of B[a-z]+h|[A-Za-z]+te of B[a-z]+|D[a-z]+ of [A-Za-z]+h', text_tag[i])): 
                    for k in range(i+1,len(text_tag)):
                        print("------------222------------------------",text_tag[k])
                        if (re.search(p,text_tag[k])):
                            print("------------3333------------------------",text_tag[k])
                            text_tag[i]=re.sub('[A-Z]+/','',text_tag[k])
                            nationality= text_tag[k]
                            break
                    if nationality:
                        break
            return nationality
        except Exception as e:
            print("Exception in extract_code_and_type method in Extract_Passport_Data class",str(e))
            return ""

    def find_given_name(self,text):
        """
            finds givenname from the given text by searching for given keyword
            input:list of strings
            output:string
        """
        try:
            reg="(^[A-Z]+\s[A-Z]+\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)|(^[A-Z]+$)"
            p = re.compile(reg)
            given_name=""
            j=-1
            for i in range(len(text)):
                if(re.search('Given Name', text[i])):
                    j=i
                    for i in range(j,len(text)):
                        if (re.findall(p,text[i])):
                            given_name= text[i]
                            break
            return given_name
        except Exception as e:
            print("Exception in find_given_name method in Extract_Passport_Data class",str(e))
            return ""
     
    def get_place_of_issue(self,text):
        """
            finds place of issue from the given text using regex for the words place of issue
            input:list of strings
            output:string
        """
        try:
            p= re.compile('^[A-Z0-9/s]+')
            place_of_issue=""
            j=-1
            for i in range(len(text)):
                if(re.search('P[a-z]+e of I[a-z]+e|[A-Za-z]+ce of I[a-z]+|P[a-z]+ of [A-Za-z]+e', text[i])):
                    j=i
                    for i in range(j+1,len(text)):
                        if (re.findall(p,text[i])):
                            place_of_issue= text[i]
                            break
            return place_of_issue
        except Exception as e:
            print("Exception in get_place_of_issue method in Extract_Passport_Data class",str(e))
            return ""

    def find_all_dates(self,text_tag):
        """
            extracts all dates from the given text using regex 
            input:list of strings
            output:list of dates
        """
        try:
            reg="[0-9]{2}/[0-9]{2}/[0-9]{4}"
            p = re.compile(reg)
            all_dates=[]
            if(text_tag != None):
                for i in range(len(text_tag)):
                    if (re.findall(p,text_tag[i])):
                        all_dates.append(text_tag[i])

            print('===DATE=== ',all_dates)
            birth_date=all_dates[0] if len(all_dates)>0 else ""
            issue_date=all_dates[1] if len(all_dates)>1 else ""
            expiry_date=all_dates[2] if len(all_dates)>2 else ""
            return [birth_date,issue_date,expiry_date]
        except Exception as e:
            print("Exception in find_all_dates method in Extract_Passport_Data class",str(e))
            return []

    def get_place_of_birth(self,text):
        """
            finds place of birth from the given text using regex for the words place of birth
            input:list of strings
            output:string
        """
        try:
            birth_place=""
            p= re.compile('^[A-Z0-9/s]+')
            for i in range(len(text)):
                if(re.search('P[a-z]+e of B[a-z]+h|[A-Za-z]+ce of B[a-z]+|P[a-z]+ of [A-Za-z]+h', text[i])):
                    for k in range(i+1,len(text)):
                        if (re.findall(p,text[k])):
                            birth_place=text[k]
                            break
                    if birth_place!=None:
                        break
            return birth_place
        except Exception as e:
            print("Exception in get_place_of_birth method in Extract_Passport_Data class",str(e))
            return ""

    def get_passport_data(self,text):
        """
            calls all functions to extract required fields from given text
            input:list of strings
            output:dictionary of required fields
        """
        try:
            text_tag=self.preprocess_text_tag(text)
            print("teext tag is----------------------------",text_tag)
            result_dict={}
            required_fields=["Surname","Name","Passport no.","DoB","Issue Date","Expiry Date","Type","Country code","Gender","Birth Location","Resident","Nation"]
            for field in required_fields:
                result_dict[field]=""
            gender=self.get_gender(text_tag)
            place_of_issue=self.get_place_of_issue(text_tag)
            nationality=self.get_nationality(text_tag)
            place_of_birth=self.get_place_of_birth(text_tag)
            passport_type_and_code=self.extract_code_and_type(text_tag)
            if passport_type_and_code:
                passport_type,code=passport_type_and_code
            passport_num = self.find_passport_no(text_tag)
            surname = self.find_surname(text_tag)
            given_name = self.find_given_name(text_tag)
            all_dates_result=self.find_all_dates(text_tag)
            if all_dates_result:
                birth_date,issue_date,expiry_date=all_dates_result
            
            result_dict["Surname"]=surname
            result_dict["Name"]= given_name
            result_dict["Passport no."]= passport_num
            result_dict["DoB"]=birth_date
            result_dict["Issue Date"]=issue_date
            result_dict["Expiry Date"]=expiry_date
            result_dict["PassportType"]=passport_type
            result_dict["Country code"]= code
            result_dict["Gender"]=gender
            result_dict["Birth Location"]= place_of_birth
            result_dict["Nationality"]= nationality 
            result_dict["Place_Of_Issue"]=place_of_issue 
            return result_dict
        except Exception as e:
            print("Exception in get_passport_data method in Extract_Passport_Data class",str(e))
            return None




    def extract_pass_back(self,text_tag):
        """
            extracts the name of father, mother and spouse from the given data using regex
            input:list of strings
            output:dictionary of required fields for backside of the passport
        """
        try:
            reg="([A-Z]+\s[A-Z]+\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)|(^[A-Z]+$)"
            q = re.compile(reg)
            z,j,s,r,t,y=0,0,0,0,0,0
            for i in range(len(text_tag)):
                print("-----TEXT STRING----- ", text_tag[i])
                # if(re.search('^L[a-z]+l G[a-z]+n$|^[A-Za-z]+l [A-Za-z]+n$|^L[a-z]+ G[a-z]+$', text_tag[i])):
                if(re.search('Father|Name of Father|Legal Guardian', text_tag[i])): 
                    z=i 
                # if(re.search('^N[a-z]+e of M[a-z]+r$|^[A-Za-z]+e of [A-Za-z]+r$|^N[a-z]+ of M[a-z]+$', text_tag[i])):
                if(re.search('Mother|Name of Mother', text_tag[i])): 
                    j=i
                # if(re.search('^N[a-z]+e of S[a-z]+e$|^[A-Za-z]+e of [A-Za-z]+e$|^N[a-z]+ of S[a-z]+$', text_tag[i])): 
                if(re.search('Spouse|Name of Spouse', text_tag[i])): 
                    s=i
                # if(re.search('^Address$|^A[a-z]+s$|^[A-Za-z]+ss$|^Ad[a-z]+$', text_tag[i])):
                if(re.search('Address$|^Ad[a-z]+$', text_tag[i])):  
                    r=i
                if(re.search('O[a-z]+ P[a-z]+t No|P[a-z]+e of I[a-z]+e', text_tag[i])): 
                    t=i
                if(re.search('F[a-z]+e No|[A-Za-z]+le No', text_tag[i])): 
                    y=i 
        
            father=""
            for i in range(z+1,len(text_tag)):

                if (re.search(q,text_tag[i])):
                    father=text_tag[i]
                    break 
            mother=""
            for i in range(j+1,len(text_tag)):
                if (re.search(q,text_tag[i])):
                    mother=text_tag[i]
                    break
            spouse=""
            for i in range(s+1,r+1):
                print('---sssss------ ', s)
                if (re.search(q,text_tag[i])):
                    print('=====QQQQQ====== ',q)
                    print("spouse name------------------------------",spouse)
                    spouse=text_tag[i]
                    break
            address=[]
            for i in range(r+1,t):
                print('-=-==-=-=rrrrr=-=-=-=-= ', r)
                # if (re.search(r,text_tag[i])):
                print('========iiiiiii====== ', text_tag[i])
                address.append(text_tag[i])
            
            address=" ".join(address) if address!=[] else ""
            file=""
            for i in range(y+1,len(text_tag)):
                file=text_tag[i]
                break
            
            passport_backside_details={}
            # ["father","mother","spouse","address","file"]
            passport_backside_details["father"]=father
            passport_backside_details["mother"]=mother
            passport_backside_details["spouse"]=spouse
            passport_backside_details["address"]=address
            passport_backside_details["file"]=file
            return passport_backside_details
        except Exception as e:
            print("Exception in extract_pass_back method in Extract_Passport_Data class",str(e))
            return {}


    def decide_side(self,text_tag):    
        """
            used for checking the side of passport
            input: list of strings
            output: boolean
        """
        try:
            y=-1
            for i in range(len(text_tag)):
                if(re.search('F[a-z]+e No|[A-Za-z]+le No', text_tag[i])): 
                    y=i 
            front=True if y==-1 else False 
            return front
        except Exception as e:
            print("Exception in decide_side method in Extract_Passport_Data class",str(e))
            return {}



    