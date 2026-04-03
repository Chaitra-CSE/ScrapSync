import os

css_block = r'''def get_base64_of_bin_file(bin_file):
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
        font-weight: 700;
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.02em;
    }}
    
    .brand-tagline {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}
    
    .user-profile {{
        background: rgba(30, 41, 59, 0.6);
        padding: 0.6rem 1.5rem;
        border-radius: 30px;
        border: 1px solid rgba(56, 189, 248, 0.3);
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
    
    .login-card {{
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
'''

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False
for i, line in enumerate(lines):
    if line.strip() == "import cv2":
        new_lines.append(line)
        new_lines.append("import base64\n")
        continue

    if "# ============ ORIGINAL CUSTOM CSS ============" in line:
        new_lines.append(line)
        new_lines.append(css_block + "\n")
        skip = True
        continue
    
    if skip and '""", unsafe_allow_html=True)' in line:
        skip = False
        continue

    if not skip:
        new_lines.append(line)

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("CSS Replaced Successfully!")
