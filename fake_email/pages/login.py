import streamlit as st
import pymongo
myclient = pymongo.MongoClient("mongodb+srv://shivam:Shivam#123@cluster0.phjbab5.mongodb.net/?appName=Cluster0")
mydb = myclient["mydatabase"]
my=mydb["user_info"]


st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
}

</style>
""", unsafe_allow_html=True)



st.header("Login into Fake Email Detecting System")
name=st.text_input("UserName")
password=st.text_input("Password", type="password")

if st.button(":red[SignIn]"):
    str=my.find({"name":name,"password":password})
    d=0
    for data in str:
        #st.success(f"Welcome:{data['name']}")
        #d=d+1
        st.session_state["name"]=data['name']
        st.switch_page("pages/profile.py")
        #st.session_state['name']
    else:

        st.error("Invalid Login !!!")
