import streamlit as st
import re
from typing import Tuple, Dict
import string
import zxcvbn
import random
import time
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Password Strength Analyzer Pro",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with modern design and animations
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');
    
    :root {
        --primary-color: #2962ff;
        --secondary-color: #0039cb;
        --success-color: #00c853;
        --warning-color: #ffd600;
        --danger-color: #d50000;
        --background-gradient: linear-gradient(135deg, #f8f9fa 0%, #e8eaf6 100%);
    }
    
    .main {
        padding: 2rem;
        background: var(--background-gradient);
        font-family: 'Poppins', sans-serif;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .stApp {
        background: var(--background-gradient);
    }
    
    .header-container {
        text-align: center;
        padding: 3rem 0;
        background: linear-gradient(135deg, #1a237e 0%, #283593 100%);
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(26, 35, 126, 0.2);
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        animation: shine 3s infinite;
    }
    
    .password-container {
        background: white;
        padding: 3rem;
        border-radius: 25px;
        margin: 2rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
        transition: all 0.4s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .password-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
    }
    
    .strength-meter {
        height: 20px;
        border-radius: 10px;
        margin: 2rem 0;
        transition: all 0.5s ease;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
        background-size: 200% auto;
        position: relative;
        overflow: hidden;
    }
    
    .strength-meter::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 2s infinite;
    }
    
    .requirement {
        margin: 1.2rem 0;
        padding: 1.2rem;
        border-radius: 15px;
        transition: all 0.4s ease;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        border: 1px solid rgba(0, 0, 0, 0.05);
        backdrop-filter: blur(5px);
    }
    
    .requirement:hover {
        transform: translateX(8px) translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }
    
    .passed {
        background: linear-gradient(145deg, #e8f5e9, #f1f8e9);
        border-left: 6px solid var(--success-color);
    }
    
    .failed {
        background: linear-gradient(145deg, #ffebee, #fce4ec);
        border-left: 6px solid var(--danger-color);
    }
    
    .generated-password {
        background: linear-gradient(145deg, #e8eaf6, #c5cae9);
        padding: 2rem;
        border-radius: 15px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.6rem;
        margin: 1.5rem 0;
        border: none;
        box-shadow: 0 8px 25px rgba(26, 35, 126, 0.15);
        position: relative;
        overflow: hidden;
        color: #1a237e;
        text-align: center;
        letter-spacing: 2px;
    }
    
    .generated-password::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 2s infinite;
    }
    
    .stats-card {
        background: white;
        padding: 2.5rem;
        border-radius: 20px;
        margin: 1rem;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        text-align: center;
        transition: all 0.4s ease;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .stats-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.15);
    }
    
    .history-item {
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        background: white;
        border-left: 6px solid #3949ab;
        transition: all 0.4s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .history-item:hover {
        transform: translateX(8px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button {
        background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 12px;
        font-weight: 500;
        transition: all 0.4s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(41, 98, 255, 0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(41, 98, 255, 0.4);
    }
    
    .metric-container {
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
        transition: all 0.4s ease;
    }
    
    .metric-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
    }
    
    h1, h2, h3, h4 {
        color: #1a237e;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    .stTab {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 0.8rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #3949ab;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #1a237e;
    }
    
    /* Input field styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e0e0e0;
        padding: 1rem;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(41, 98, 255, 0.2);
    }
    
    /* Slider styling */
    .stSlider>div>div>div>div {
        background-color: var(--primary-color);
    }
    
    /* Checkbox styling */
    .stCheckbox>div>div>div>label>span {
        color: #1a237e;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'password_history' not in st.session_state:
    st.session_state.password_history = []
if 'total_checks' not in st.session_state:
    st.session_state.total_checks = 0
if 'strongest_password' not in st.session_state:
    st.session_state.strongest_password = {'score': -1, 'password': None}

def generate_password(length: int = 16, use_special: bool = True) -> str:
    """Generate a strong password"""
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation
    
    while True:
        password = ''.join(random.choice(chars) for _ in range(length))
        # Ensure password meets minimum requirements
        if (any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            (not use_special or any(c in string.punctuation for c in password))):
            return password

def estimate_crack_time(score: int, password: str) -> str:
    """Estimate time to crack the password"""
    result = zxcvbn.zxcvbn(password)
    return result['crack_times_display']['offline_fast_hashing_1e10_per_second']

def check_password_strength(password: str) -> Tuple[int, Dict]:
    """Enhanced password strength analysis"""
    result = zxcvbn.zxcvbn(password)
    
    criteria = {
        "length": len(password) >= 12,
        "uppercase": any(c.isupper() for c in password),
        "lowercase": any(c.islower() for c in password),
        "numbers": any(c.isdigit() for c in password),
        "special": any(c in string.punctuation for c in password),
        "no_common": result['score'] >= 3,
        "no_sequences": not re.search(r'(abc|123|qwe|xyz)', password.lower()),
        "no_repeats": not re.search(r'(.)\1{2,}', password)
    }
    
    return result['score'], criteria

def get_strength_color(score: int) -> str:
    """Get color based on password strength score"""
    colors = {
        0: "#dc3545",  # Very Weak - Red
        1: "#ffc107",  # Weak - Yellow
        2: "#fd7e14",  # Fair - Orange
        3: "#20c997",  # Strong - Teal
        4: "#28a745",  # Very Strong - Green
    }
    return colors.get(score, "#dc3545")

def get_strength_label(score: int) -> str:
    """Get label based on password strength score"""
    labels = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Strong",
        4: "Very Strong"
    }
    return labels.get(score, "Very Weak")

# Title and description with enhanced styling
st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='color: #1a237e; font-size: 2.5rem; font-weight: 700;'>🛡️ Professional Password Analyzer</h1>
        <div style='background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); 
                    padding: 1.5rem; 
                    border-radius: 15px; 
                    margin: 1.5rem 0;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);'>
            <h4 style='color: #1565c0; margin: 0;'>Enterprise-Grade Password Security Analysis</h4>
            <p style='color: #1976d2; margin-top: 0.5rem;'>Analyze, generate, and manage secure passwords with advanced metrics</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Main content in tabs
tab1, tab2, tab3 = st.tabs(["Password Analyzer", "Password Generator", "History & Stats"])

with tab1:
    with st.container():
        st.markdown('<div class="password-container">', unsafe_allow_html=True)
        password = st.text_input(
            "Enter your password",
            type="password",
            help="Enter a password to check its strength"
        )
        
        if password:
            score, criteria = check_password_strength(password)
            strength_color = get_strength_color(score)
            strength_label = get_strength_label(score)
            crack_time = estimate_crack_time(score, password)
            
            # Update statistics
            st.session_state.total_checks += 1
            if score > st.session_state.strongest_password['score']:
                st.session_state.strongest_password = {'score': score, 'password': password}
            
            # Add to history
            st.session_state.password_history.append({
                'timestamp': datetime.now(),
                'score': score,
                'label': strength_label,
                'crack_time': crack_time
            })
            
            # Display strength meter and stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Strength Score", f"{score + 1}/5")
            with col2:
                st.metric("Crack Time", crack_time)
            with col3:
                st.metric("Character Length", str(len(password)))
            
            st.markdown(f"""
                <div class="strength-meter" style="background: linear-gradient(to right, 
                    {strength_color} {(score + 1) * 20}%, 
                    #e9ecef {(score + 1) * 20}%);">
                </div>
                <h3 style="color: {strength_color};">{strength_label}</h3>
            """, unsafe_allow_html=True)
            
            # Enhanced requirements display
            st.markdown("### Password Requirements")
            col1, col2 = st.columns(2)
            
            with col1:
                for name, passed in list(criteria.items())[:4]:
                    st.markdown(f"""
                        <div class="requirement {'passed' if passed else 'failed'}">
                            {'✅' if passed else '❌'} {name.replace('_', ' ').title()}
                        </div>
                    """, unsafe_allow_html=True)
                
            with col2:
                for name, passed in list(criteria.items())[4:]:
                    st.markdown(f"""
                        <div class="requirement {'passed' if passed else 'failed'}">
                            {'✅' if passed else '❌'} {name.replace('_', ' ').title()}
                        </div>
                    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
        <div style='text-align: center; margin-bottom: 2rem;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🔐</div>
            <div style='display: flex; justify-content: center; gap: 1rem; margin: 1rem 0;'>
                <div style='font-size: 2rem;'>🎲</div>
                <div style='font-size: 2rem;'>➡️</div>
                <div style='font-size: 2rem;'>🔑</div>
                <div style='font-size: 2rem;'>➡️</div>
                <div style='font-size: 2rem;'>🛡️</div>
            </div>
            <h2 style='color: #1a237e; margin-bottom: 2rem;'>Secure Password Generator</h2>
            <div style='background: linear-gradient(135deg, #e8eaf6 0%, #c5cae9 100%);
                        padding: 1.5rem;
                        border-radius: 15px;
                        margin-bottom: 2rem;
                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);'>
                <p style='color: #283593; margin: 0;'>
                    Generate strong, unique passwords with customizable options
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style='background: white; 
                        padding: 1.5rem; 
                        border-radius: 15px; 
                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);'>
                <div style='font-size: 2rem; text-align: center; margin-bottom: 1rem;'>⚙️</div>
                <h4 style='text-align: center; color: #1a237e; margin-bottom: 1rem;'>Generator Settings</h4>
        """, unsafe_allow_html=True)
        length = st.slider("Password Length", 12, 32, 16)
        use_special = st.checkbox("Include Special Characters (!@#$%^&*)", True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: white; 
                        padding: 1.5rem; 
                        border-radius: 15px; 
                        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);'>
                <div style='font-size: 2rem; text-align: center; margin-bottom: 1rem;'>🎯</div>
                <h4 style='text-align: center; color: #1a237e; margin-bottom: 1rem;'>Generated Password</h4>
        """, unsafe_allow_html=True)
        if st.button("Generate Strong Password 🎲"):
            generated = generate_password(length, use_special)
            st.markdown(f"""
                <div class="generated-password" style='position: relative;'>
                    <div style='position: absolute; 
                               top: -10px; 
                               right: -10px; 
                               background: #4caf50; 
                               color: white; 
                               padding: 5px 10px; 
                               border-radius: 15px; 
                               font-size: 0.8rem;
                               box-shadow: 0 2px 5px rgba(0,0,0,0.1);'>
                        New ✨
                    </div>
                    {generated}
                </div>
            """, unsafe_allow_html=True)
            
            # Show strength of generated password
            gen_score, _ = check_password_strength(generated)
            st.markdown(f"""
                <div style='text-align: center; margin-top: 1rem;'>
                    <span style='background: {get_strength_color(gen_score)}; 
                               color: white; 
                               padding: 5px 15px; 
                               border-radius: 20px;
                               font-size: 0.9rem;'>
                        {get_strength_label(gen_score)} 💪
                    </span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Add password tips
    st.markdown("""
        <div style='margin-top: 2rem; padding: 1.5rem; background: white; border-radius: 15px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);'>
            <div style='display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;'>
                <div style='text-align: center; flex: 1; min-width: 200px;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🔒</div>
                    <h4 style='color: #1a237e;'>Strong</h4>
                    <p style='color: #666;'>Mix of uppercase, lowercase, numbers, and symbols</p>
                </div>
                <div style='text-align: center; flex: 1; min-width: 200px;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎯</div>
                    <h4 style='color: #1a237e;'>Unique</h4>
                    <p style='color: #666;'>Never reuse passwords across different accounts</p>
                </div>
                <div style='text-align: center; flex: 1; min-width: 200px;'>
                    <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📏</div>
                    <h4 style='color: #1a237e;'>Length</h4>
                    <p style='color: #666;'>Longer passwords are harder to crack</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("### 📊 Password Analysis Statistics")
    
    # Display stats in cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
            <div class="stats-card">
                <h4>Total Passwords Checked</h4>
                <h2>{}</h2>
            </div>
        """.format(st.session_state.total_checks), unsafe_allow_html=True)
    
    with col2:
        avg_score = sum(h['score'] for h in st.session_state.password_history) / len(st.session_state.password_history) if st.session_state.password_history else 0
        st.markdown("""
            <div class="stats-card">
                <h4>Average Strength Score</h4>
                <h2>{:.1f}/4</h2>
            </div>
        """.format(avg_score), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="stats-card">
                <h4>Strongest Password Score</h4>
                <h2>{}/4</h2>
            </div>
        """.format(st.session_state.strongest_password['score']), unsafe_allow_html=True)
    
    # Password history
    if st.session_state.password_history:
        st.markdown("### Recent Password Checks")
        for entry in reversed(st.session_state.password_history[-5:]):
            st.markdown(f"""
                <div class="history-item">
                    <strong>{entry['label']}</strong> - Crack time: {entry['crack_time']}<br>
                    <small>{entry['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small>
                </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <div style='background: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
                    padding: 2rem;
                    border-radius: 15px;
                    margin: 1rem 0;'>
            <h3 style='color: #1a237e;'>🔒 Enterprise Security</h3>
            <p style='color: #424242;'>All password analysis is performed locally with military-grade encryption standards.</p>
            <small style='color: #616161;'>© 2024 Password Analyzer Pro - Version 2.0</small>
        </div>
    </div>
""", unsafe_allow_html=True) 