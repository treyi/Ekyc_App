# from Azure_OCR import *
# from St_NER import *
import re



class Extract_Pan_Data():
    """
        This class handles various functions related to extracting data from PAN Card
    """
    def findPanCardNo(self,text_tag):  
        """ 
            Regex to check valid PAN Card number 
        """
        try:
            regex = "^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
            pan_card_num=""
            
            if text_tag != None:
                p = re.compile(regex)
                for i in range(len(text_tag)):
                    if(re.search(p, text_tag[i]) and len(text_tag[i]) == 10):
                        pan_card_num= text_tag[i]
                        break
            return pan_card_num
        except Exception as e:
            print("Exception as findPanCardNo",str(e))
    
    def find_names(self,text_tag):
        """
            Returns all names from the pan card data
        """
        reg="(^[A-Z]+\s.+\s[A-Z]+$)|(^[A-Z]+\s[A-Z]+$)"
        names=[]
        if(text_tag != None):
            for i in range(2,len(text_tag)):
                x=re.findall(reg,text_tag[i])
                if x:
                    print("x is--------------------",x)
                    for r in x:
                        if type(r)==tuple and r!="":
                            for e in r:
                                if e!="":
                                    names.append(e)
                        elif type(r)==str and r!="":
                            names.append(r)

                    
        return names

    def get_date_of_birth(self,text_tag):
        """
            Returns date of birth from pan_card data
        """
        
        regex = "[0-9]{2}/[0-9]{2}/[0-9]{4}" # Regex to searching date
        p = re.compile(regex)
        birth_date=""                         
        if text_tag!=None:
            for i in range(len(text_tag)):
                if(re.search(p, text_tag[i])):
                    x=re.findall(p, text_tag[i])
                    birth_date= x[0]
                    break
        return birth_date
    
    def get_pan_data(self,text_tag):  
        """
            extraction for PAN card data
        """
        required_fields=["Name","PAN no.","DoB","Father Name"]
        result_dict={}
        for field in required_fields:
            result_dict[field]=""
        names = self.find_names(text_tag)
        first_name=names[0] if names!=[] else ""
        father_name=names[1] if len(names)==2 else ""
        pan_card_num= self.findPanCardNo(text_tag)
        date_of_birth = self.get_date_of_birth(text_tag)
        
        result_dict["Name"]=first_name
        result_dict["PAN no."]=pan_card_num
        result_dict["DoB"]=date_of_birth
        result_dict["Father Name"]=father_name
        return result_dict


