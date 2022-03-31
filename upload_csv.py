import streamlit as st
import sqlite3
from PIL import Image
import matplotlib.pyplot as plt
import pandas
def header(url):
     st.markdown(f'<p style="color:#FF0000;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def verif(url):
     st.markdown(f'<p style="color:#008000;font-size:24px;border-radius:2%;">{url}</p>', unsafe_allow_html=True)

def main():
    st.write("""# CSV TO SQLITE """)
    File = st.file_uploader("Upload a file",type = ["csv","xlsx"])
    #print(type(File))
    if File is not None:
        if st.button("Submit"):
          con = sqlite3.connect("data.sqlite")
          try:
               df = pandas.read_csv(File, encoding = 'unicode_escape')
          except:
               df = pandas.read_excel(File, sheet_name=None)
          #print(df)
          df1 = list(df.values())
          print(len(df1))
          df3 = list(df.keys())
          print(len(df3))
          for i in range(len(df1)):
               df1[i].to_sql(df3[i], con, if_exists='replace', index=False)
               x=con.execute("SELECT * FROM df3").fetchall()
               st.table(x)
          con.commit()
          con.close()
if __name__ == '__main__':
    main()