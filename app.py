"""
Text-to-Image Generator (beach theme)
Generates images from text prompts using Hugging Face's Inference API
(FLUX.1-schnell / Stable Diffusion XL). Needs a FREE Hugging Face token.
"""
import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()
st.set_page_config(page_title="Text to Image", page_icon="🏖️", layout="centered")

MODELS = {
    "FLUX.1 Schnell (fast, high quality)": "black-forest-labs/FLUX.1-schnell",
    "Stable Diffusion XL": "stabilityai/stable-diffusion-xl-base-1.0",
}

STYLES = {
    "None": "",
    "Photorealistic": ", photorealistic, 8k, highly detailed, sharp focus",
    "Anime": ", anime style, vibrant colors, studio ghibli inspired",
    "Digital Art": ", digital art, trending on artstation, concept art",
    "Oil Painting": ", oil painting, textured brush strokes, classical art",
    "3D Render": ", 3d render, octane render, soft lighting",
}

WAVE = (
    "data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 100' "
    "preserveAspectRatio='none'%3E%3Cpath d='M0 50 Q150 0 300 50 T600 50 T900 50 T1200 50 V100 H0Z' "
    "fill='rgba(255,255,255,0.55)'/%3E%3C/svg%3E"
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@500;700;800&family=Nunito:wght@400;600;700&display=swap');
html, body, [class*="css"], .stApp { font-family:'Nunito', sans-serif; }

/* Sky -> shallow water -> sand */
.stApp { background:linear-gradient(180deg, #8fdcf5 0%, #c6f0ef 38%, #f7e8c0 100%); background-attachment:fixed; }
[data-testid="stHeader"] { background:transparent; }

/* Text colors (explicit, so it also works when Streamlit is in dark mode) */
.stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label, .stApp .stMarkdown,
.stApp .stCaption, [data-testid="stWidgetLabel"] p { color:#0b4a5a; }

.hero { padding:6px 0 14px; text-align:center; }
.hero h1 { margin:0; font-family:'Baloo 2', sans-serif; font-size:3rem; font-weight:800; color:#0b4a5a; }
.hero h1 .sun { color:#ff7a59; }
.hero p { margin:2px 0 0; font-size:1.05rem; }

/* Inputs: solid white boxes with dark text (covers every nested layer Streamlit adds) */
.stTextArea textarea, .stTextInput input,
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="textarea"],
[data-baseweb="select"], [data-baseweb="select"] > div, [data-baseweb="select"] > div > div {
  background:#ffffff !important; color:#0b4a5a !important; -webkit-text-fill-color:#0b4a5a;
}
[data-baseweb="input"], [data-baseweb="textarea"], [data-baseweb="select"] > div {
  border:2px solid #4fc3c9 !important; border-radius:14px !important;
}
[data-baseweb="select"] *, [data-baseweb="input"] svg, [data-baseweb="select"] svg { color:#0b4a5a !important; fill:#0b4a5a !important; }
.stTextArea textarea::placeholder, .stTextInput input::placeholder { color:#4d7f8a !important; -webkit-text-fill-color:#4d7f8a; opacity:1; }
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within, [data-baseweb="select"]:focus-within > div {
  border-color:#ff7a59 !important; box-shadow:0 0 0 2px rgba(255,122,89,.3) !important;
}
/* Every nested layer inside the select / input boxes (this is what was still dark) */
[data-baseweb="select"] div, [data-baseweb="select"] span,
[data-baseweb="input"] div, [data-baseweb="base-input"] div, [data-baseweb="textarea"] div,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background-color:#ffffff !important; color:#0b4a5a !important; -webkit-text-fill-color:#0b4a5a !important; opacity:1 !important;
}
[data-baseweb="select"] input { background:transparent !important; }
/* Sidebar: deep-sea panel with white text. Boxes inside it are dark teal, so white text always shows. */
[data-testid="stSidebar"] { background:#0b4a5a !important; border-right:3px dashed #4fc3c9; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] label p, [data-testid="stSidebar"] p,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p, [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
  color:#ffffff !important; font-weight:700;
}
[data-testid="stSidebar"] [data-baseweb="select"] div, [data-testid="stSidebar"] [data-baseweb="select"] span {
  background-color:#08323d !important; color:#ffffff !important; -webkit-text-fill-color:#ffffff !important; opacity:1 !important;
}
[data-testid="stSidebar"] [data-baseweb="select"] > div { border:2px solid #4fc3c9 !important; border-radius:12px !important; }
[data-testid="stSidebar"] [data-baseweb="select"] svg { fill:#ffffff !important; color:#ffffff !important; }
[data-testid="stSidebar"] .stButton button { background:#ff7a59 !important; border:0 !important; border-radius:99px !important; box-shadow:0 4px 0 #d4553a; }
[data-testid="stSidebar"] .stButton button, [data-testid="stSidebar"] .stButton button * { color:#ffffff !important; font-weight:700; }
[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.3); }
[data-testid="stSidebar"] button[kind="header"], [data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] * { color:#ffffff !important; }

/* Dropdown list that opens under a select */
[data-baseweb="popover"] ul, [data-baseweb="popover"] li, [data-baseweb="menu"] { background:#ffffff !important; color:#0b4a5a !important; }
[data-baseweb="popover"] li:hover { background:#d9f4f4 !important; }
[data-baseweb="popover"] li * { color:#0b4a5a !important; }
/* Top-right toolbar (Deploy, menu) */
[data-testid="stToolbar"], [data-testid="stToolbar"] * { color:#0b4a5a !important; }

/* Coral buttons */
.stButton > button, .stDownloadButton > button {
  border:0; border-radius:99px; padding:.65rem 1.6rem; font-weight:700; color:#fff !important; background:#ff7a59;
  box-shadow:0 4px 0 #d4553a; transition:background .2s;
}
.stButton > button:hover, .stDownloadButton > button:hover { background:#ff9272; color:#fff !important; }
.stButton > button p, .stDownloadButton > button p { color:#fff !important; }

/* Generated image: white photo-print frame */
[data-testid="stImage"] img { border:10px solid #fff; border-radius:8px; box-shadow:0 14px 30px rgba(11,74,90,.25); }

/* One calm moving thing: a slow wave along the bottom */
.waves { position:fixed; left:0; bottom:0; width:100%; height:80px; overflow:hidden; pointer-events:none; z-index:0; }
.waves div { width:200%; height:100%; background:url("__WAVE__") repeat-x; background-size:50% 100%; animation:flow 18s linear infinite; }
@keyframes flow { to { transform:translateX(-50%); } }
.block-container { position:relative; z-index:1; padding-bottom:110px; }
@media (prefers-reduced-motion: reduce) { .waves div { animation:none; } }
</style>
""".replace("__WAVE__", WAVE)

HERO = """
<div class="waves"><div></div></div>
<div class="hero">
<h1>🌴 Text to Image <span class="sun">☀️</span></h1>
<p>Describe a scene and watch it wash up on the shore. 🐚</p>
</div>
"""

st.markdown(CSS, unsafe_allow_html=True)
st.markdown(HERO, unsafe_allow_html=True)

def restart():
    """Clear the prompt boxes and the generated image, ready for a fresh start."""
    for k in ("result", "prompt", "negative"):
        st.session_state.pop(k, None)


# ---------------- Sidebar ----------------
st.sidebar.header("🏝️ Settings")
# The token is no longer typed in the page. It is read from the .env file (HF_TOKEN=...)
token = os.getenv("HF_TOKEN", "")
model_name = st.sidebar.selectbox("Model", list(MODELS.keys()))
style = st.sidebar.selectbox("Style", list(STYLES.keys()))
size = st.sidebar.selectbox("Size", ["1024x1024", "768x768", "512x512", "1024x768", "768x1024"])
width, height = map(int, size.split("x"))
st.sidebar.markdown("---")
st.sidebar.button("🔄 Restart", on_click=restart, help="Clears the prompt and the generated image")

# ---------------- Main ----------------
prompt = st.text_area(
    "Your prompt",
    placeholder="A cozy tea stall on a rainy evening in Hyderabad, warm lights, cinematic",
    height=100,
    key="prompt",
)
negative = st.text_input("Negative prompt (optional)", placeholder="blurry, low quality, distorted", key="negative")

if st.button("✨ Generate", type="primary"):
    if not token:
        st.error("No Hugging Face token found. Add a line HF_TOKEN=your_token to a .env file next to this app, then restart it.")
    elif not prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        client = InferenceClient(token=token)
        full_prompt = prompt.strip() + STYLES[style]
        kwargs = {"width": width, "height": height}
        if negative.strip():
            if "FLUX" in model_name:
                st.info("FLUX doesn't use negative prompts, so that field was ignored. Try Stable Diffusion XL to use it.")
            else:
                kwargs["negative_prompt"] = negative.strip()

        with st.spinner("Generating image... (10-60 seconds)"):
            try:
                image = client.text_to_image(full_prompt, model=MODELS[model_name], **kwargs)
            except Exception as e:
                st.error(f"Generation failed: {e}")
                st.info(
                    "Common fixes: check your token, wait a minute if the model is loading, "
                    "or try the other model / a smaller size."
                )
                st.stop()

        buf = BytesIO()
        image.save(buf, format="PNG")
        # Keep the result in session_state so clicking Download doesn't make it disappear
        st.session_state["result"] = {"png": buf.getvalue(), "caption": prompt.strip()}

result = st.session_state.get("result")
if result:
    st.image(result["png"], caption=result["caption"])
    st.download_button("⬇️ Download PNG", result["png"], "generated.png", "image/png")