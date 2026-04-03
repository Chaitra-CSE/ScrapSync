import streamlit as st
from PIL import Image
import json
import os
from datetime import datetime
import random
import tensorflow as tf
import numpy as np
import cv2
import base64

# ============ PAGE CONFIGURATION ============
st.set_page_config(
    page_title="ScrapSync - AI Waste Management",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============ ORIGINAL CUSTOM CSS ============
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

bg_base64 = get_base64_of_bin_file("background.png")

st.markdown(f"""
<style>
    /* OceanTwin Dash Inspired Dark Theme */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&family=JetBrains+Mono:wght@400;700&family=Space+Grotesk:wght@400;500;700&display=swap');
    
    .stApp {{
        background-color: #0b1121;
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
        color: #f1f5f9;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(11, 17, 33, 0.7); /* Deep dark overlay */
        pointer-events: none;
        z-index: 0;
    }}
    
    .main .block-container {{
        position: relative;
        z-index: 1;
        padding: 1.5rem 2rem;
        max-width: 1400px;
        margin: 0 auto;
    }}
    
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Dark Glassmorphism Cards */
    .glass-panel {{
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        border-radius: 16px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
    }}
    
    .custom-header {{
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        padding: 1.2rem 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.4);
    }}
    
    .brand {{
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }}
    
    .brand-icon {{
        font-size: 2.2rem;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.8);
    }}
    
    .brand-name {{
        font-size: 1.8rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 900;
        color: #020617 !important;
        letter-spacing: -0.02em;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.4);
    }}
    
    .brand-tagline {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #0f172a !important;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}
    
    .user-profile {{
        background: rgba(30, 41, 59, 0.6);
        padding: 0.6rem 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.1);
        font-family: 'Space Grotesk', sans-serif;
    }}
    
    .stats-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1.5rem;
        margin-bottom: 2rem;
    }}
    
    .stat-item {{
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(148, 163, 184, 0.15);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }}
    
    .stat-item:hover {{
        transform: translateY(-5px);
        border-color: rgba(56, 189, 248, 0.5);
        box-shadow: 0 10px 30px rgba(56, 189, 248, 0.15);
    }}
    
    .stat-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: #f8fafc;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
    }}
    
    .stat-label {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: #94a3b8;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .upload-area {{
        background: rgba(15, 23, 42, 0.3);
        border: 2px dashed rgba(56, 189, 248, 0.4);
        border-radius: 20px;
        padding: 2.5rem;
        text-align: center;
        transition: all 0.3s ease;
        backdrop-filter: blur(8px);
    }}
    
    .upload-area:hover {{
        border-color: #38bdf8;
        background: rgba(15, 23, 42, 0.5);
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);
    }}
    
    .result-panel {{
        background: rgba(15, 23, 42, 0.45);
        backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid rgba(56, 189, 248, 0.3);
        box-shadow: 0 0 30px rgba(56, 189, 248, 0.1);
    }}
    
    .listing-item {{
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(8px);
        padding: 1.2rem;
        margin: 1rem 0;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-left: 4px solid #38bdf8;
        transition: all 0.2s;
    }}
    
    .listing-item:hover {{
        transform: translateX(5px);
        background: rgba(30, 41, 59, 0.6);
        border-color: rgba(56, 189, 248, 0.3);
    }}
    
    .leaderboard-entry {{
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(8px);
        padding: 1rem 1.5rem;
        margin: 0.8rem 0;
        border-radius: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border: 1px solid rgba(255, 255, 255, 0.05);
        transition: transform 0.2s;
    }}
    
    .leaderboard-entry:hover {{
        transform: scale(1.02);
        background: rgba(30, 41, 59, 0.6);
    }}
    
    .rank-1 {{ border-left: 4px solid #fbbf24; background: linear-gradient(90deg, rgba(251, 191, 36, 0.1) 0%, transparent 100%); }}
    .rank-2 {{ border-left: 4px solid #cbd5e1; background: linear-gradient(90deg, rgba(203, 213, 225, 0.1) 0%, transparent 100%); }}
    .rank-3 {{ border-left: 4px solid #d97706; background: linear-gradient(90deg, rgba(217, 119, 6, 0.1) 0%, transparent 100%); }}
    
    .stButton > button {{
        background: rgba(56, 189, 248, 0.1);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.5);
        padding: 0.8rem 1.5rem;
        border-radius: 30px;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        letter-spacing: 0.05em;
        transition: all 0.2s;
        width: 100%;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.1);
    }}
    
    .stButton > button:hover {{
        background: rgba(56, 189, 248, 0.2);
        border-color: #38bdf8;
        color: #fff;
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(56, 189, 248, 0.3);
    }}
    
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: rgba(15, 23, 42, 0.5);
        backdrop-filter: blur(12px);
        padding: 0.5rem;
        border-radius: 40px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 30px;
        padding: 0.5rem 1.5rem;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        color: #94a3b8;
        background-color: transparent !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: rgba(56, 189, 248, 0.15) !important;
        color: #38bdf8 !important;
        border: 1px solid rgba(56, 189, 248, 0.3) !important;
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.15) !important;
    }}
    
    .stProgress > div > div > div {{
        background: linear-gradient(90deg, #38bdf8, #818cf8);
        border-radius: 20px;
        box-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }}
    .stProgress > div > div {{
        background: rgba(15, 23, 42, 0.6);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }}
    
    .login-card, [data-testid="stForm"] {{
        max-width: 480px;
        margin: 4rem auto;
        padding: 3rem;
        background: rgba(15, 23, 42, 0.5);
        backdrop-filter: blur(16px);
        border-radius: 24px;
        border: 1px solid rgba(56, 189, 248, 0.2);
        box-shadow: 0 0 40px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(56, 189, 248, 0.05);
        position: relative;
    }}
    
    .stTextInput > div > div > input {{
        border-radius: 12px !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        background: rgba(15, 23, 42, 0.6) !important;
        color: #f8fafc !important;
        padding: 0.8rem 1.2rem !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s;
    }}
    .stTextInput > div > div > input:focus {{
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }}
    
    .stSelectbox > div > div {{
        border-radius: 12px !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        background: rgba(15, 23, 42, 0.6) !important;
        color: #f8fafc !important;
    }}
    
    .section-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .section-title::after {{
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(56, 189, 248, 0.3), transparent);
        margin-left: 1rem;
    }}
    
    .divider {{
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(148, 163, 184, 0.2), transparent);
        margin: 2rem 0;
    }}
    
    /* Make inline elements glassmorphic */
    div[style*="background: #f8f9fa"], div[style*="background: #f4f9f6"] {{
        background: rgba(30, 41, 59, 0.4) !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        box-shadow: none !important;
        color: #e2e8f0 !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
    }}
    
    .stAlert {{
        border-radius: 12px !important;
        background: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(8px) !important;
        border: 1px solid rgba(148, 163, 184, 0.2) !important;
        color: #f8fafc !important;
    }}
    
    [data-testid="stMetric"] {{
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(8px);
        padding: 1.2rem;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        transition: transform 0.2s;
    }}
    [data-testid="stMetric"]:hover {{
        transform: scale(1.05);
        border-color: rgba(56, 189, 248, 0.3);
    }}
    
    /* Ensure global text legibility over dark backgrounds */
    .stMarkdown {{ color: #e2e8f0 !important; }}
    h1, h2, h3, h4, h5, h6 {{ color: #ffffff !important; font-family: 'Space Grotesk', sans-serif; }}
    p {{ color: #e2e8f0; }}
</style>
""", unsafe_allow_html=True)


# ============ WASTE CLASSIFIER MODEL ============
class WasteClassifier:
    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        tf.get_logger().setLevel('ERROR')
        
        model_paths = [
            'models/mobilenetv2_garbage.h5',
            '../Garbage-Classification-Using-MobileNetV2/models/mobilenetv2_garbage.h5',
            'mobilenetv2_garbage.h5'
        ]
        
        self.model = None
        for path in model_paths:
            if os.path.exists(path):
                self.model = tf.keras.models.load_model(path)
                break
        
        if self.model is None:
            self.model = self._create_mobilenetv2()
        
        self.class_names = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        self.category_mapping = {
            'cardboard': 'Paper', 'paper': 'Paper', 'plastic': 'Plastic',
            'metal': 'Metal', 'glass': 'Recyclable', 'trash': 'Other'
        }
        self.prices = {'Paper': 15, 'Plastic': 20, 'Metal': 45, 'Recyclable': 10, 'Other': 2}
    
    def _create_mobilenetv2(self):
        base_model = tf.keras.applications.MobileNetV2(
            weights='imagenet', include_top=False, input_shape=(224, 224, 3)
        )
        base_model.trainable = False
        model = tf.keras.Sequential([
            base_model, tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.5), tf.keras.layers.Dense(6, activation='softmax')
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model
    
    def preprocess_image(self, image):
        if isinstance(image, Image.Image):
            image = image.convert('RGB')
            image = np.array(image)
        else:
            # Handle if somehow passed as raw RGBA or Grayscale array
            if len(image.shape) == 3 and image.shape[2] == 4:
                image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
            elif len(image.shape) == 2:
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
                
        image = cv2.resize(image, (224, 224))
        image = image.astype('float32') / 255.0
        return np.expand_dims(image, axis=0)
    
    def predict(self, image):
        processed = self.preprocess_image(image)
        predictions = self.model.predict(processed, verbose=0)
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx])
        predicted_class = self.class_names[class_idx]
        return {
            'predicted_class': predicted_class,
            'predicted_class_upper': predicted_class.upper(),
            'confidence': confidence,
            'confidence_percent': f"{confidence*100:.1f}%",
            'mapped_category': self.category_mapping[predicted_class],
            'price_per_kg': self.prices[self.category_mapping[predicted_class]]
        }


# ============ DATABASE MANAGER ============
class SimpleDB:
    def __init__(self):
        self.data_dir = 'scrapsync_data'
        os.makedirs(self.data_dir, exist_ok=True)
        self.users_file = os.path.join(self.data_dir, 'users.json')
        self.listings_file = os.path.join(self.data_dir, 'listings.json')
        self._init_files()
    
    def _init_files(self):
        if not os.path.exists(self.users_file):
            self._save_json(self.users_file, {})
        if not os.path.exists(self.listings_file):
            self._save_json(self.listings_file, [])
    
    def _save_json(self, filepath, data):
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def _load_json(self, filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def create_user(self, username, pincode):
        users = self._load_json(self.users_file)
        if username not in users:
            users[username] = {
                'username': username, 'pincode': pincode, 'points': 0,
                'earnings': 0, 'listings': 0, 'level': 'Beginner',
                'joined_date': datetime.now().isoformat()
            }
            self._save_json(self.users_file, users)
        return users[username]
    
    def get_user(self, username):
        users = self._load_json(self.users_file)
        return users.get(username)
    
    def update_user(self, username, points_to_add=0, earnings_to_add=0, listing_count=0):
        users = self._load_json(self.users_file)
        if username in users:
            users[username]['points'] += points_to_add
            users[username]['earnings'] += earnings_to_add
            users[username]['listings'] += listing_count
            points = users[username]['points']
            if points >= 1000:
                users[username]['level'] = 'Pro Recycler'
            elif points >= 500:
                users[username]['level'] = 'Eco Expert'
            elif points >= 200:
                users[username]['level'] = 'Green Hero'
            self._save_json(self.users_file, users)
    
    def create_listing(self, seller, waste_type, weight, price, pincode):
        listings = self._load_json(self.listings_file)
        listing = {
            'id': len(listings) + 1, 'seller': seller, 'waste_type': waste_type,
            'weight': weight, 'price': price, 'pincode': pincode,
            'status': 'active', 'created_at': datetime.now().isoformat()
        }
        listings.append(listing)
        self._save_json(self.listings_file, listings)
        return listing
    
    def get_listings(self, pincode):
        listings = self._load_json(self.listings_file)
        region = pincode[:3]
        return [l for l in listings if l['status'] == 'active' and 
                (l['pincode'] == pincode or l['pincode'][:3] == region)]
    
    def get_leaderboard(self, pincode, limit=10):
        users = self._load_json(self.users_file)
        region = pincode[:3]
        local_users = [u for u in users.values() if u['pincode'] == pincode or u['pincode'][:3] == region]
        local_users.sort(key=lambda x: x['points'], reverse=True)
        return local_users[:limit]


# ============ LOGIN PAGE ============
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">♻️</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: #020617; text-shadow: 0 0 10px rgba(255,255,255,0.4);">ScrapSync</div>
            <div style="color: #0f172a; font-weight: 600;">Sync. Sell. Sustain.</div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.markdown("### Welcome")
            
            username = st.text_input("Username", placeholder="Enter your name", key="login_user")
            pincode = st.text_input("Pincode", placeholder="Enter area pincode", type="password", key="login_pin")
            
            submitted = st.form_submit_button("Get Started", use_container_width=True)
            if submitted:
                if not (username and pincode):
                    st.error("Please fill in both fields")
        
        if submitted and username and pincode:
            return username, pincode, True
        
        st.markdown("""
        <div class="divider"></div>
        <div style="display: flex; justify-content: space-around; text-align: center;">
            <div><div style="font-size: 1.5rem;">📸</div><div style="font-size: 0.75rem; color: #020617; font-weight: 600;">Upload</div></div>
            <div><div style="font-size: 1.5rem;">🤖</div><div style="font-size: 0.75rem; color: #020617; font-weight: 600;">AI Scan</div></div>
            <div><div style="font-size: 1.5rem;">💰</div><div style="font-size: 0.75rem; color: #020617; font-weight: 600;">Value</div></div>
            <div><div style="font-size: 1.5rem;">🎮</div><div style="font-size: 0.75rem; color: #020617; font-weight: 600;">Rewards</div></div>
        </div>
        """, unsafe_allow_html=True)
    
    return None, None, False


# ============ MAIN APP PAGE ============
def app_page(username, pincode, db, model):
    user = db.get_user(username)
    
    # Header
    st.markdown(f"""
    <div class="custom-header">
        <div class="brand">
            <div class="brand-icon">♻️</div>
            <div>
                <div class="brand-name">ScrapSync</div>
                <div class="brand-tagline">Sync. Sell. Sustain.</div>
            </div>
        </div>
        <div class="user-profile">
            <div style="font-weight: 500;">👤 {username}</div>
            <div style="font-size: 0.75rem; color: #6c757d;">📍 {pincode}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    if user:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="stat-item"><div class="stat-value">{user.get("points", 0)}</div><div class="stat-label">🏆 Points</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="stat-item"><div class="stat-value">₹{user.get("earnings", 0)}</div><div class="stat-label">💰 Earnings</div></div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div class="stat-item"><div class="stat-value">{user.get("listings", 0)}</div><div class="stat-label">♻️ Recycled</div></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="stat-item"><div class="stat-value">{user.get("level", "Beginner")}</div><div class="stat-label">📊 Level</div></div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📸 Scan & Sell", "🛒 Marketplace", "📊 Insights", "🏆 Rankings"])
    
    # Tab 1: Scan & Sell
    with tab1:
        colA, colB = st.columns([1, 1])
        
        with colA:
            st.markdown('<div class="upload-area">', unsafe_allow_html=True)
            uploaded = st.file_uploader("Drop your waste image here", type=['jpg', 'jpeg', 'png'], label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if uploaded:
                img = Image.open(uploaded)
                st.image(img, caption="Uploaded", use_column_width=True)
                if st.button("🔍 Analyze Waste", use_container_width=True):
                    with st.spinner("AI processing..."):
                        res = model.predict(img)
                        st.session_state.result = res
        
        with colB:
            if st.session_state.get('result'):
                res = st.session_state.result
                st.markdown(f"""
                <div class="result-panel">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; font-weight: 700; color: #38bdf8; text-shadow: 0 0 10px rgba(56,189,248,0.5);">{res['predicted_class_upper']}</div>
                        <div style="margin: 0.5rem 0;">🎯 {res['confidence_percent']} confidence</div>
                        <hr>
                        <div>📦 Category: <strong>{res['mapped_category']}</strong></div>
                        <div>💰 Rate: <strong>₹{res['price_per_kg']}/kg</strong></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                weight = st.number_input("Quantity (kg)", min_value=0.1, step=0.1, value=1.0)
                value = weight * res['price_per_kg']
                
                colX, colY, colZ = st.columns(3)
                with colX:
                    st.metric("💵 Value", f"₹{value:.2f}")
                with colY:
                    st.metric("🌱 CO₂ Saved", f"{weight*1.5:.1f}kg")
                with colZ:
                    st.metric("⭐ Points", "+30")
                
                if st.button("List for Sale", use_container_width=True):
                    db.create_listing(username, res['mapped_category'], weight, value, pincode)
                    db.update_user(username, 30, value, 1)
                    st.success("✓ Listed successfully!")
                    st.balloons()
                    del st.session_state.result
                    st.rerun()
    
    # Tab 2: Marketplace
    with tab2:
        st.markdown(f'<div class="section-title">📍 Local Marketplace • {pincode}</div>', unsafe_allow_html=True)
        
        types = ["All", "Paper", "Plastic", "Metal", "Recyclable", "Other"]
        selected = st.selectbox("Filter", types)
        
        listings = db.get_listings(pincode)
        if selected != "All":
            listings = [l for l in listings if l['waste_type'] == selected]
        
        if listings:
            for l in listings:
                st.markdown(f"""
                <div class="listing-item">
                    <div><strong>♻️ {l['waste_type']}</strong><br><small>📦 {l['weight']}kg • 👤 {l['seller']}</small></div>
                    <div><strong>₹{l['price']:.2f}</strong><br><small>📍 {l['pincode']}</small></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No listings found in your area")
    
    # Tab 3: Insights
    with tab3:
        st.markdown('<div class="section-title">📊 Your Impact</div>', unsafe_allow_html=True)
        
        if user:
            points = user.get('points', 0)
            if points < 200:
                prog = points / 200
                next_lvl = "Green Hero"
                need = 200 - points
            elif points < 500:
                prog = (points - 200) / 300
                next_lvl = "Eco Expert"
                need = 500 - points
            elif points < 1000:
                prog = (points - 500) / 500
                next_lvl = "Pro Recycler"
                need = 1000 - points
            else:
                prog = 1.0
                next_lvl = "Master"
                need = 0
            
            st.markdown(f"**Level Progress to {next_lvl}**")
            if need > 0:
                st.caption(f"{need} more points needed")
            st.progress(prog)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            colL, colR = st.columns(2)
            with colL:
                carbon = user.get('earnings', 0) * 0.5
                trees = int(carbon / 50)
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 12px;">
                    <div style="font-weight: 600;">🌍 Environment</div>
                    <div>CO₂ Saved: {carbon:.1f} kg</div>
                    <div>Trees Saved: {trees}</div>
                </div>
                """, unsafe_allow_html=True)
            with colR:
                st.markdown(f"""
                <div style="background: #f8f9fa; padding: 1rem; border-radius: 12px;">
                    <div style="font-weight: 600;">📈 Stats</div>
                    <div>Items: {user.get('listings', 0)}</div>
                    <div>Earned: ₹{user.get('earnings', 0)}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
            
            tips = [
                "♻️ Clean recyclables for better value",
                "📦 Flatten cardboard to save space",
                "🔋 Recycle e-waste separately",
                "🥤 Avoid single-use plastics"
            ]
            st.info(f"💡 Tip: {random.choice(tips)}")
    
    # Tab 4: Rankings
    with tab4:
        st.markdown('<div class="section-title">🏆 Local Champions</div>', unsafe_allow_html=True)
        
        board = db.get_leaderboard(pincode)
        if board:
            for idx, u in enumerate(board, 1):
                rank_class = ""
                if idx == 1:
                    rank_class = "rank-1"
                elif idx == 2:
                    rank_class = "rank-2"
                elif idx == 3:
                    rank_class = "rank-3"
                
                st.markdown(f"""
                <div class="leaderboard-entry {rank_class}">
                    <div><strong>{'🥇' if idx==1 else '🥈' if idx==2 else '🥉' if idx==3 else f'#{idx}'} {u['username']}</strong></div>
                    <div><strong>{u.get('points', 0)} pts</strong><br><small>{u.get('level', 'Beginner')}</small></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Be the first champion in your area!")
    
    # Logout
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.clear()
        st.rerun()


# ============ MAIN ============
def main():
    model = WasteClassifier()
    db = SimpleDB()
    
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'pincode' not in st.session_state:
        st.session_state.pincode = None
    if 'result' not in st.session_state:
        st.session_state.result = None
    
    if not st.session_state.logged_in:
        u, p, logged = login_page()
        if logged:
            st.session_state.logged_in = True
            st.session_state.username = u
            st.session_state.pincode = p
            st.rerun()
    else:
        app_page(st.session_state.username, st.session_state.pincode, db, model)

if __name__ == "__main__":
    main()