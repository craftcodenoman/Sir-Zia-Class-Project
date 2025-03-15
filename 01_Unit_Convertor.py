import streamlit as st
import pandas as pd
from PIL import Image
import base64

# Set page configuration
st.set_page_config(
    page_title="Unit Converter",
    page_icon="🔄",
    layout="centered"
)

# Title and description
st.title("Unit Converter")
st.markdown("Convert between different units with ease!")

# Conversion dictionaries
CONVERSION_FACTORS = {
    "Length": {
        "Meter": 1,
        "Kilometer": 0.001,
        "Centimeter": 100,
        "Millimeter": 1000,
        "Mile": 0.000621371,
        "Yard": 1.09361,
        "Foot": 3.28084,
        "Inch": 39.3701
    },
    "Weight": {
        "Kilogram": 1,
        "Gram": 1000,
        "Milligram": 1000000,
        "Pound": 2.20462,
        "Ounce": 35.274,
        "Metric Ton": 0.001
    },
    "Temperature": {
        "Celsius": "C",
        "Fahrenheit": "F",
        "Kelvin": "K"
    },
    "Area": {
        "Square Meter": 1,
        "Square Kilometer": 0.000001,
        "Square Mile": 0.386102,
        "Square Yard": 1.19599,
        "Square Foot": 10.7639,
        "Hectare": 0.0001,
        "Acre": 0.000247105
    },
    "Volume": {
        "Cubic Meter": 1,
        "Liter": 1000,
        "Milliliter": 1000000,
        "Gallon": 264.172,
        "Quart": 1056.69,
        "Pint": 2113.38,
        "Cup": 4226.75
    }
}

# Sidebar for category selection
with st.sidebar:
    # Add logo to sidebar
    st.image("https://freeappsforme.com/wp-content/uploads/2023/03/Unit-Converter-Digit-Grove-logo.jpg", 
            use_container_width=True)
    
    # Category Selection with icons
    category_icons = {
        "Length": "📏",
        "Weight": "⚖️",
        "Temperature": "🌡️",
        "Area": "📐",
        "Volume": "🧊"
    }
    
    category = st.selectbox(
        "Select Category",
        list(CONVERSION_FACTORS.keys()),
        format_func=lambda x: f"{category_icons.get(x, '')} {x}"
    )
    
    # Theme Selection
    st.subheader("🎨 Theme")
    theme = st.radio(
        "Choose Theme",
        ["Default", "Dark Purple", "Ocean Blue", "Forest Green"],
        key="theme"
    )
    
    # Quick Reference
    st.subheader("📚 Quick Reference")
    if st.checkbox("Show Common Conversions"):
        if category == "Temperature":
            st.info("""
            • 0°C = 32°F
            • 100°C = 212°F
            • 0°C = 273.15K
            """)
        elif category == "Length":
            st.info("""
            • 1 km = 0.621 miles
            • 1 m = 3.281 feet
            • 1 inch = 2.54 cm
            """)
        elif category == "Weight":
            st.info("""
            • 1 kg = 2.205 lbs
            • 1 lb = 16 oz
            • 1 kg = 1000 g
            """)
    
    # About Section
    st.sidebar.markdown("---")
    st.sidebar.subheader("ℹ️ About")
    st.sidebar.info("Professional Unit Converter v1.0")

# Theme colors
theme_colors = {
    "Default": {"bg": "#2F1C6A", "text": "#CFCDFF", "result": "#009900"},
    "Dark Purple": {"bg": "#673DE6", "text": "#FFFFFF", "result": "#00FF00"},
    "Ocean Blue": {"bg": "#1E90FF", "text": "#F0F8FF", "result": "#32CD32"},
    "Forest Green": {"bg": "#228B22", "text": "#F0FFF0", "result": "#FFD700"}
}

selected_theme = theme_colors[theme]

# Custom CSS to make it look better
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stSelectbox {
        margin-bottom: 1rem;
    }
    .conversion-result {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #2F1C6A;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)


def convert_temperature(value, from_unit, to_unit):
    if from_unit == to_unit:
        return value
    
    # Convert to Celsius first
    if from_unit == "Fahrenheit":
        celsius = (value - 32) * 5//9
    elif from_unit == "Kelvin":
        celsius = value - 273.15
    else:
        celsius = value
    
    # Convert from Celsius to target unit
    if to_unit == "Fahrenheit":
        return (celsius * 9//5) + 32
    elif to_unit == "Kelvin":
        return celsius + 273.15
    return celsius

def convert_units(value, from_unit, to_unit, category):
    if category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)
    
    # For other categories
    base_value = value // CONVERSION_FACTORS[category][from_unit]
    return base_value * CONVERSION_FACTORS[category][to_unit]

# Main conversion interface
col1, col2 = st.columns(2)

with col1:
    st.subheader("From")
    from_unit = st.selectbox("Convert from", list(CONVERSION_FACTORS[category].keys()), key="from")
    value = st.number_input("Enter value", value=0.0, key="value")

with col2:
    st.subheader("To")
    to_unit = st.selectbox("Convert to", list(CONVERSION_FACTORS[category].keys()), key="to")

# Calculate and display result
if st.button("Convert", type="primary"):
    result = convert_units(value, from_unit, to_unit, category)
    
    st.markdown("### Result")
    with st.container():
        st.markdown(f"""
        <div class="conversion-result" style="background-color: {selected_theme['bg']};">
            <h3 style="color: {selected_theme['text']};">{value:g} {from_unit}</h3>
            <h4 style="color: {selected_theme['text']};">equals</h4>
            <h3 style="color: {selected_theme['result']};">{result:g} {to_unit}</h3>
        </div>
        """, unsafe_allow_html=True)
