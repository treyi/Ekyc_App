from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import FormRecognizerClient
import re

def format_ocr_data(form_pages):
  data_text = {}
  text_tag = []
  text_bbox = []
  for idx, content in enumerate(form_pages):
    for line_idx, line in enumerate(content.lines):
      text = line.text
      text_tag.append(text)
      data_text[text] = []
      bounding_box = line.bounding_box
      for i in bounding_box:
        data_text[text].append((int(i.x),int(i.y)))
      points = (data_text[text][0][0],data_text[text][0][1],data_text[text][2][0],data_text[text][2][1])
      text_bbox.append(points)
  return text_tag,text_bbox

endpoint = "https://quixyocr.cognitiveservices.azure.com/"
key = "03462e450efa4e338d200900d30d8c7b"
form_recognizer_client = FormRecognizerClient(endpoint, AzureKeyCredential(key))
form_recognizer_client = FormRecognizerClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def get_ocr(f):
    # with open(file_path,"rb")as f
    try:
      poller = form_recognizer_client.begin_recognize_content(form=f)
      form_pages = poller.result()
      text_tag,text_bbox = format_ocr_data(form_pages)
      return text_tag
    except Exception as e:
      print("EXCEPTION IN OCR---------------------------------")