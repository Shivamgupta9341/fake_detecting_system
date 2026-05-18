"""
╔══════════════════════════════════════════════════════════╗
║         FAKE EMAIL DETECTION SYSTEM                      ║
║         Built with Streamlit + Scikit-learn + NLTK       ║
╚══════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────────────────
# 1.  IMPORTS
# ─────────────────────────────────────────────────────────
import re
import pickle
import io
import numpy as np
import pandas as pd
import nltk
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import time


#with st.spinner("Loading..."):
#    time.sleep(10)

#st.success("Loaded Successfully!")
# ─────────────────────────────────────────────────────────
# 2.  DOWNLOAD NLTK DATA
# ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def download_nltk():
    nltk.download("stopwords", quiet=True)
    nltk.download("punkt",     quiet=True)

download_nltk()


st.markdown("""
<style>

.stApp {
    background: linear-gradient(to right, #141e30, #243b55);
}

</style>
""", unsafe_allow_html=True)



# ─────────────────────────────────────────────────────────
# 3.  SAMPLE DATASET
# ─────────────────────────────────────────────────────────
def build_dataset() -> pd.DataFrame:
    spam_emails = [
        "Congratulations! You've won a $1,000 gift card. Click here to claim your prize now!",
        "FREE offer! Get rich quick with our amazing investment opportunity. Act now!",
        "Your account has been compromised. Click this link immediately to verify your password.",
        "You have been selected for a special lottery. Send your bank details to claim $500,000.",
        "URGENT: Your PayPal account will be suspended. Login now at paypal-secure-verify.com",
        "Win an iPhone 15 for FREE! Limited time offer. Click the link below to participate.",
        "Hot singles in your area want to meet you! Click here for free access tonight.",
        "Earn $5000 per week working from home. No experience needed. Sign up today!",
        "Your credit score has been updated. Verify your social security number here.",
        "Congratulations winner! You are today's lucky visitor. Claim your reward now.",
        "ALERT: Unusual login detected on your account. Verify now at secure-login-alert.net",
        "Double your Bitcoin investment in 24 hours. 100% guaranteed returns!",
        "You owe taxes. Pay immediately to avoid arrest. Call this number now.",
        "Buy cheap medications online. No prescription needed. Best price guaranteed!",
        "Your computer has a virus! Download our free antivirus software immediately.",
        "Special discount! Buy now and get 90% off. Limited stock available today only!",
        "Claim your inheritance money from a deceased relative. Reply with personal info.",
        "You've been pre-approved for a $50,000 loan. No credit check required!",
        "Make money online fast. Thousands already earning from home. Join free now!",
        "WARNING: Your email will expire in 24 hours. Update your account information.",
        "Free vacation package! You've been selected. Click to claim your trip to Bahamas.",
        "Invest in our crypto platform and earn passive income of $300 daily guaranteed.",
        "Your Amazon account is locked. Click here to unlock and verify your identity.",
        "Nigerian prince needs your help. Share your bank details for a reward.",
        "Lose 30 pounds in 30 days with this one weird trick doctors don't want you to know.",
    ]

    ham_emails = [
        "Hi John, can we reschedule tomorrow's meeting to 3 PM? Let me know if that works.",
        "Please find attached the quarterly report for your review. Let me know your feedback.",
        "Reminder: Your dentist appointment is scheduled for Monday at 10 AM.",
        "Thank you for your order! Your package will arrive within 3-5 business days.",
        "The project deadline has been moved to next Friday. Please update your tasks accordingly.",
        "Happy birthday! Hope you have a wonderful day filled with joy and celebration.",
        "Your subscription has been renewed successfully. Thank you for staying with us.",
        "Team lunch is planned for Thursday at noon. We'll be going to the Italian place.",
        "Please review the attached document and provide your comments by end of week.",
        "Your flight booking is confirmed. Departure: 9:00 AM. Check-in opens 24 hours before.",
        "The library book you reserved is now available for pickup. It will be held for 5 days.",
        "Monthly newsletter: Tips for better productivity and time management at work.",
        "Meeting notes from yesterday's call are attached. Action items are highlighted in yellow.",
        "Your tax return has been processed. Expected refund arrival: 7-10 business days.",
        "Congratulations on completing the Python course! Your certificate is attached.",
        "The invoice for last month's services is attached. Payment is due within 30 days.",
        "We're hosting a webinar next Tuesday at 2 PM on data science trends. Register here.",
        "Your password was changed successfully. If you didn't do this, contact support.",
        "Campus library will be closed on public holidays. Regular hours resume after.",
        "New study materials have been uploaded to the course portal. Check them out.",
        "Your application has been received. We'll be in touch within 5 business days.",
        "Friendly reminder to submit your timesheet before 5 PM on Friday.",
        "The bus schedule has changed. New timings are effective from next Monday.",
        "Your software update is ready to install. Restart your computer at your convenience.",
        "Welcome to the team! Your onboarding documents are ready for you to review.",
    ]

    data = (
        [(text, 1) for text in spam_emails] +
        [(text, 0) for text in ham_emails]
    )
    df = pd.DataFrame(data, columns=["email", "label"])
    return df.sample(frac=1, random_state=42).reset_index(drop=True)


# ─────────────────────────────────────────────────────────
# 4.  TEXT PREPROCESSING
# ─────────────────────────────────────────────────────────
stemmer    = PorterStemmer()
stop_words = set(stopwords.words("english"))

def preprocess(text: str) -> str:
    text   = text.lower()
    text   = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    tokens = [stemmer.stem(w) for w in tokens if w not in stop_words and len(w) > 1]
    return " ".join(tokens)


# ─────────────────────────────────────────────────────────
# 5.  MODEL TRAINING
# ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def train_model():
    df = build_dataset()
    df["clean"] = df["email"].apply(preprocess)

    X_train, X_test, y_train, y_test = train_test_split(
        df["clean"], df["label"], test_size=0.2, random_state=42
    )

    vectorizer  = TfidfVectorizer(max_features=500)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec  = vectorizer.transform(X_test)

    model = MultinomialNB()
    model.fit(X_train_vec, y_train)

    accuracy = accuracy_score(y_test, model.predict(X_test_vec))
    return vectorizer, model, round(accuracy * 100, 1)


# ─────────────────────────────────────────────────────────
# 6.  HELPER UTILITIES
# ─────────────────────────────────────────────────────────
SUSPICIOUS_WORDS = [
    "free", "winner", "won", "prize", "claim", "urgent", "alert",
    "click", "verify", "password", "account", "suspended", "bank",
    "lottery", "million", "guarantee", "offer", "limited", "act now",
    "earn", "income", "investment", "bitcoin", "crypto", "rich",
    "selected", "congratulations", "reward", "exclusive", "discount",
    "cheap", "buy now", "make money", "work from home", "no experience",
    "inheritance", "prince", "loan", "approved", "compromised",
]

def find_suspicious_words(text: str) -> list:
    lower = text.lower()
    return [w for w in SUSPICIOUS_WORDS if w in lower]

def extract_links(text: str) -> list:
    pattern = r"(https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9\-]+\.[a-zA-Z]{2,}(?:/[^\s]*)?)"
    return re.findall(pattern, text)


# ─────────────────────────────────────────────────────────
# 7.  STREAMLIT UI
# ─────────────────────────────────────────────────────────
def main():
    st.set_page_config(
        page_title="Fake Email Detector",
        page_icon="🛡️",
        layout="centered",
    )
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
        html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
        .stApp { background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: #e8e8ff; }
        .main-title { text-align:center; font-size:2.4rem; font-weight:700; color:#a78bfa; margin-bottom:0.2rem; }
        .sub-title  { text-align:center; font-size:1rem; color:#94a3b8; margin-bottom:2rem; }
        .card { background:rgba(255,255,255,0.06); border:1px solid rgba(167,139,250,0.25); border-radius:14px; padding:1.2rem 1.5rem; margin-bottom:1rem; }
        .card-title { font-size:0.85rem; font-weight:600; color:#a78bfa; text-transform:uppercase; letter-spacing:1px; margin-bottom:0.5rem; }
        .result-spam { background:linear-gradient(135deg,#7f1d1d,#991b1b); border:1px solid #ef4444; border-radius:14px; padding:1.4rem 1.8rem; color:#fecaca; font-size:1.2rem; font-weight:700; text-align:center; }
        .result-safe { background:linear-gradient(135deg,#064e3b,#065f46); border:1px solid #10b981; border-radius:14px; padding:1.4rem 1.8rem; color:#a7f3d0; font-size:1.2rem; font-weight:700; text-align:center; }
        .meter-container { background:rgba(255,255,255,0.08); border-radius:50px; height:14px; overflow:hidden; margin-top:0.5rem; }
        .meter-fill-spam { height:100%; background:linear-gradient(90deg,#f87171,#ef4444); border-radius:50px; }
        .meter-fill-safe { height:100%; background:linear-gradient(90deg,#34d399,#10b981); border-radius:50px; }
        .chip      { display:inline-block; background:rgba(239,68,68,0.18); color:#fca5a5; border:1px solid #f87171; border-radius:20px; padding:3px 12px; font-size:0.8rem; margin:3px; }
        .chip-link { display:inline-block; background:rgba(59,130,246,0.18); color:#93c5fd; border:1px solid #60a5fa; border-radius:20px; padding:3px 12px; font-size:0.8rem; margin:3px; word-break:break-all; }
        .accuracy-badge { text-align:center; color:#94a3b8; font-size:0.82rem; margin-top:-0.8rem; margin-bottom:1.5rem; }
        .stTextArea textarea { background:rgba(255,255,255,0.05) !important; border:1px solid rgba(167,139,250,0.4) !important; border-radius:10px !important; color:#e8e8ff !important; }
        .stButton > button { width:100%; background:linear-gradient(135deg,#7c3aed,#4f46e5); color:white; border:none; border-radius:10px; padding:0.7rem 1rem; font-size:1rem; font-weight:600; }
        #MainMenu, footer { visibility:hidden; }
    </style>
    """, unsafe_allow_html=True)
    


    vectorizer, model, accuracy = train_model()

    st.markdown('<p class="main-title">🛡️ Fake Email Detector</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Paste any email below to check if it\'s spam or safe</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="accuracy-badge">Model accuracy on test set: <strong>{accuracy}%</strong></p>', unsafe_allow_html=True)

    email_input = st.text_area("📧 Email Content", height=200, placeholder="Paste the full email text here...")

    if st.button("🔍 Analyse Email"):
        if not email_input.strip():
            st.warning("⚠️  Please paste some email text before analysing.")
        else:
            clean_text = preprocess(email_input)
            vectorised = vectorizer.transform([clean_text])
            prediction = model.predict(vectorised)[0]
            proba      = model.predict_proba(vectorised)[0]
            spam_pct   = round(proba[1] * 100, 1)
            safe_pct   = round(proba[0] * 100, 1)

            st.markdown("<br>", unsafe_allow_html=True)
            if prediction == 1:
                st.markdown(f'<div class="result-spam">🚨 &nbsp;SPAM DETECTED &nbsp;—&nbsp; {spam_pct}% Spam Probability</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-safe">✅ &nbsp;EMAIL LOOKS SAFE &nbsp;—&nbsp; {safe_pct}% Safe Probability</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            st.markdown('<div class="card"><p class="card-title">📊 Spam vs Safe Probability</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**🔴 Spam: {spam_pct}%**")
                st.markdown(f'<div class="meter-container"><div class="meter-fill-spam" style="width:{spam_pct}%"></div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f"**🟢 Safe: {safe_pct}%**")
                st.markdown(f'<div class="meter-container"><div class="meter-fill-safe" style="width:{safe_pct}%"></div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            found_words = find_suspicious_words(email_input)
            st.markdown('<div class="card"><p class="card-title">⚠️ Suspicious Words Found</p>', unsafe_allow_html=True)
            if found_words:
                st.markdown(" ".join(f'<span class="chip">{w}</span>' for w in found_words), unsafe_allow_html=True)
            else:
                st.markdown("✅ No suspicious words detected.")
            st.markdown('</div>', unsafe_allow_html=True)

            links = extract_links(email_input)
            st.markdown('<div class="card"><p class="card-title">🔗 Links Detected in Email</p>', unsafe_allow_html=True)
            if links:
                st.markdown(" ".join(f'<span class="chip-link">{l}</span>' for l in links), unsafe_allow_html=True)
                st.markdown("<small style='color:#94a3b8'>⚡ Do not click unknown URLs.</small>", unsafe_allow_html=True)
            else:
                st.markdown("🔒 No external links found.")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<p style='text-align:center;color:#475569;font-size:0.78rem;'>🛡️ Fake Email Detection System | Built with Streamlit + scikit-learn + NLTK</p>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────
# 8.  ENTRY POINT
# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
