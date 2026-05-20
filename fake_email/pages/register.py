import streamlit as st
import pymongo
myclient = pymongo.MongoClient("mongodb+srv://shivam:Shivam#123@cluster0.phjbab5.mongodb.net/?appName=Cluster0")
mydb = myclient["mydatabase"]
my=mydb["user_info"]




st.header("Register")
name=st.text_input("UserName")
password=st.text_input("Password", type="password")
con_password=st.text_input("Confirm Password", type="password")
if password !=con_password:
       st.error("Password do not match")
g=st.radio("Gender",['M','F'])
email=st.text_input("Email")
dob=st.date_input("DOB")
b1=st.button("SAVE")
def get_data():
       my.insert_one({"name":name,"password":password, "gender":g,"Email":email,"dob":str(dob)})
       st.success("Your data are saved!!")
       
 
if b1:
       get_data()



