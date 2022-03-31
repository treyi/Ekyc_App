# from Azure_OCR import *
# from St_NER import *
import re



class Extract_Passport_Data():
    """
        This class handles various functions related to extracting data from Passport
    """

    def preprocess_text_tag(self,text_tag):   # removing spaces and text before slash
        reg="[a-zA-Z\S\s]+/\s"
        p = re.compile(reg)
        for i in range(len(text_tag)):
            if(re.search(p, text_tag[i])):
                x=re.sub(p,'',text_tag[i])
                text_tag[i]=x
        return text_tag

    def find_passport_no(self,text_tag):         # finding passport number
        try:
            reg="(^[A-Z₱][0-9]+)"
            p = re.compile(reg)
            passport_num=""
            if text_tag != None:
                for i in range(len(text_tag)):
                    if(re.search(p, text_tag[i])):
                        passport_num=re.findall(p,text_tag[i])
                        
            return passport_num
        except Exception as e:
            print("Exception in find passport no.",str(e))
            return None    
    
    
    def get_value(self,text_tag,match_index):
        """
            returns place of issue, nation or birthdate depending on match_index
        """
        reg='^[A-Z0-9/s]+'
        p= re.compile(reg)
        value=""
        for i in range(match_index,len(text_tag)):
            if (re.findall(p,text_tag[i])):
                value=text_tag[i]
                print('=-=-=ISSUE-=-=-- ',value)
                break
        return value

    def get_gender(self,text_tag,match_index):
        gender_reg='^[A-Z]$'
        q= re.compile(gender_reg)
        gender=""
        for i in range(match_index,len(text_tag)):
            if (re.findall(q,text_tag[i])):
                gender=text_tag[i]
                print('=-=-=GENDER-=-=-- ',gender)
                break
        return gender
    
    def extract_code_and_type(self,text_tag):
        reg_type="^P|S|D$"
        reg_code='^[A-Z]{3}$'
        p = re.compile(reg_type)
        c= re.compile(reg_code)
        for i in range(len(text_tag)):
            if(re.search(p, text_tag[i])): 
                type_list=re.findall(p,text_tag[i])    
            if(re.search(c, text_tag[i])): 
                code_list=re.findall(c,text_tag[i]) 
        type=type_list[0] if type_list!=[] else ""
        code=code_list[0] if code_list!=[] else ""
        return type,code
    
    def find_surname(self,text_tag):
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
    
    def find_give_name(self,text_tag):
        reg="(^[A-Z]+\s[A-Z]+\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)|(^[A-Z]+$)"
        p = re.compile(reg)
        given_name=""
        if(text_tag != None):
            name_keyword_index=-1
            for i in range(len(text_tag)):
                if(re.search('Given Name', text_tag[i])):
                    name_keyword_index=i
            for i in range(name_keyword_index,len(text_tag)):
                if (re.findall(p,text_tag[i])):
                    given_name= text_tag[i]
        return given_name
    

    def find_all_dates(self,text_tag):
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
        return birth_date,issue_date,expiry_date
    

    
    def get_passport_data(self,text_tag):
        text_tag=self.preprocess_text_tag(text_tag)
        result_dict={}
        required_fields=["Surname","Name","Passport no.","DoB","Issue Date","Expiry Date","Type","Country code","Gender","Birth Location","Resident","Nation"]
        for field in required_fields:
            result_dict[field]=""
        for i in range(len(text_tag)):
            if(re.search('D[a-z]+e of B[a-z]+h|[A-Za-z]+te of B[a-z]+|D[a-z]+ of [A-Za-z]+h', text_tag[i])): 
                z=i    
            if(re.search('P[a-z]+e of B[a-z]+h|[A-Za-z]+ce of B[a-z]+|P[a-z]+ of [A-Za-z]+h', text_tag[i])):
                j=i
            if(re.search('P[a-z]+e of I[a-z]+e|[A-Za-z]+ce of I[a-z]+|P[a-z]+ of [A-Za-z]+e', text_tag[i])):
                k=i
          
        nation=self.get_value(text_tag,0)
        place_of_residence=self.get_value(text_tag,j+1)
        birth_location=self.get_value(text_tag,k+1)
        gender=self.get_gender(text_tag,z+1)
        type,code=self.extract_code_and_type(text_tag)
        passport_num = self.find_passport_no(text_tag)
        surname = self.find_surname(text_tag)
        given_name = self.find_give_name(text_tag)
        birth_date,issue_date,expiry_date=self.find_all_dates(text_tag)
        
        result_dict["Surname"]=surname
        result_dict["Name"]= given_name
        result_dict["Passport no."]= passport_num
        result_dict["DoB"]=birth_date
        result_dict["Issue Date"]=issue_date
        result_dict["Expiry Date"]=expiry_date
        result_dict["Type"]=type
        result_dict["Country code"]= code
        result_dict["Gender"]=gender
        result_dict["Birth Location"]= birth_location
        result_dict["Resident"]= place_of_residence 
        result_dict["Nation"]= nation
        return result_dict




    def extract_father_mother_spouse(self,text_tag):
        
        reg="(^[A-Z]+\s[A-Z]+\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)|(^[A-Z]+$)"
        q = re.compile(reg)
        z,j,s,r,t,y=0,0,0,0,0,0
        for i in range(len(text_tag)):
            if(re.search('^L[a-z]+l G[a-z]+n$|^[A-Za-z]+l [A-Za-z]+n$|^L[a-z]+ G[a-z]+$', text_tag[i])): 
                z=i 
            if(re.search('^N[a-z]+e of M[a-z]+r$|^[A-Za-z]+e of [A-Za-z]+r$|^N[a-z]+ of M[a-z]+$', text_tag[i])): 
                j=i
            if(re.search('^N[a-z]+e of S[a-z]+e$|^[A-Za-z]+e of [A-Za-z]+e$|^N[a-z]+ of S[a-z]+$', text_tag[i])): 
                s=i
            if(re.search('^Address$|^A[a-z]+s$|^[A-Za-z]+ss$|^Ad[a-z]+$', text_tag[i])): 
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
            if (re.search(q,text_tag[i])):
                spouse=text_tag[i]
                break
        address=[]
        for i in range(r+1,t):
            address.append(text_tag[i])
        
        address=" ".join(address) if address!=[] else ""
        file=""
        for i in range(y+1,len(text_tag)):
            file=text_tag[i]
            break
        
        return father,mother,spouse,address,file


    def decide_side(self,text_tag):    # used for checking the side of passport
        y=-1
        for i in range(len(text_tag)):
            if(re.search('F[a-z]+e No|[A-Za-z]+le No', text_tag[i])): 
                y=i 
        front=True if y==-1 else False 
        return front



    def extract_pass_back(self,text_tag):     #extraction for passport back side
        text_tag=self.preprocess_text_tag(text_tag)
        passport_backside_details=""
        if text_tag!=None:
            passport_backside_details=self.extract_father_mother_spouse(text_tag)
        return passport_backside_details