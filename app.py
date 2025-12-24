import streamlit as st
import requests
from io import BytesIO
from PIL import Image

# Page Configuration
st.set_page_config(page_title="AI Image Generator", page_icon="🎨", layout="centered")

# --- CUSTOM CSS FOR THE CLEAN CARD LAYOUT ---
st.markdown("""
    <style>
        [data-testid="stSidebar"] {display: none;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}

        .stApp { background-color: #f8f9fa; }

        .main .block-container {
            background-color: #ffffff;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.05);
            max-width: 700px;
            margin-top: 20px;
            border: 1px solid #eee;
        }

        .stButton>button {
            width: 100%; border-radius: 12px; height: 3.5em; 
            background-color: #2a9d8f; color: white; font-weight: bold; border: none;
        }
        .stButton>button:hover { background-color: #21867a; color: white; }
        
        /* Center the generated image */
        .stImage { display: flex; justify-content: center; border-radius: 15px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

# --- APP CONTENT ---
st.markdown("<h1 style='text-align: center; color: #264653;'>🎨 AI Image Generator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #2a9d8f;'>Turn your imagination into stunning visuals instantly.</p>", unsafe_allow_html=True)

# Input Section
prompt = st.text_area("Describe the image you want to create:", placeholder="e.g. A futuristic city with flying cars at sunset, cinematic lighting, 8k")

col1, col2 = st.columns(2)
with col1:
    aspect_ratio = st.selectbox("Aspect Ratio:", ["1:1 (Square)", "16:9 (Widescreen)", "9:16 (Story)"])
with col2:
    seed = st.number_input("Random Seed (Change for new version):", value=42)

# Mapping ratios for the API
ratio_map = {"1:1 (Square)": "1024x1024", "16:9 (Widescreen)": "1920x1080", "9:16 (Story)": "1080x1920"}
width, height = ratio_map[aspect_ratio].split('x')

if st.button("Generate Masterpiece ✨"):
    if not prompt:
        st.warning("Please describe what you want to see!")
    else:
        try:
            with st.spinner("AI is painting your image..."):
                # 1. Prepare URL & Headers
                encoded_prompt = requests.utils.quote(prompt)
                image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed={seed}&model=flux"
                
                # We pretend to be a real browser to avoid being blocked
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
                
                # 2. Attempt the request
                response = requests.get(image_url, headers=headers, timeout=60)
                
                # 3. Validation Logic
                if response.status_code == 200:
                    content_type = response.headers.get("Content-Type", "")
                    
                    if "image" in content_type:
                        image_data = BytesIO(response.content)
                        img = Image.open(image_data)
                        st.image(img, caption=f"Result for: {prompt}", use_container_width=True)
                        
                        st.download_button(
                            label="Download Image 📥",
                            data=response.content,
                            file_name="ai_generated_image.jpg",
                            mime="image/jpeg"
                        )
                    else:
                        # If it's not an image, show the text error the server sent
                        server_msg = response.text[:100] # Get first 100 chars of error
                        st.error(f"Server is busy or limit reached. Message: {server_msg}")
                        st.info("💡 Pro Tip: Try changing the 'Seed' number slightly and click Generate again!")
                else:
                    st.error(f"Server error ({response.status_code}). Trying a different prompt usually helps.")
                    
        except Exception as e:
            st.error(f"Connection Error: {e}")

st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 0.8em; color: gray;'>Powered by <b>TheTechInfo.net</b></p>", unsafe_allow_html=True)