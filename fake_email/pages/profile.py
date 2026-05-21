
import streamlit as st
import pymongo




# MongoDB Connection
myclient = pymongo.MongoClient("mongodb+srv://shivam:Shivam#123@cluster0.phjbab5.mongodb.net/?appName=Cluster0")

mydb = myclient["mydatabase"]
my = mydb["user_info"]





c1, c2, c3,c4 = st.columns(4)



# Session State
if "name" not in st.session_state or not st.session_state.get("login"):
    st.warning("Please login first.")
    st.switch_page("pages/login.py")
    

if 'name' not in st.session_state:
    st.session_state['name'] = ""
name = st.session_state['name']
#st.success(f"Welcome : {name}")

st.markdown(f"""
<div style="
padding:25px;
border-radius:20px;
background:linear-gradient(135deg,#00c6ff,#0072ff);
color:white;
box-shadow:0px 0px 15px #00c6ff;
">
<h1>👋 Welcome, {name}</h1>
<h4>Fake Email Detection System</h4>

<p>Stay safe from phishing and fake emails.</p>


</div>
""", unsafe_allow_html=True)



@st.dialog("User Profile")
def profile_popup():

    res = my.find({"name": name})

    for data in res:
        st.success(f"🧑 Name : {data['name']}")
        st.success(f"🔒 Password : {data['password']}")
        st.success(f"⚧ Gender : {data['gender']}")
        st.success(f"📧 Email : {data['Email']}")
        st.success(f"🎂 Dob : {data['dob']}")





@st.dialog("Change Password")
def password_popup():

    t1 = st.text_input("Old Password", type="password")
    t2 = st.text_input("New Password", type="password")

    if st.button("Update Password"):

        result = my.update_one({"name": name,"password": t1},{"$set": {"password": t2}})

        if result.modified_count > 0:
            st.success("Password Changed Successfully!")
        else:
            st.error("Old Password Incorrect!")



# Buttons
if c1.button("See Profile"):
    profile_popup()

if c2.button("Change Password"):
    password_popup()

if c3.button("Detecting System"):
    st.switch_page("pages/detecting_system.py")


if c4.button("📤 Logout"):

    st.session_state.clear()

    st.switch_page("main.py")
