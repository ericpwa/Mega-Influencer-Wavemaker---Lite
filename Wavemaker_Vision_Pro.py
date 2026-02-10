import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import io
import os
from PIL import Image

# --- 1. 頁面基礎設定 ---
st.set_page_config(
    page_title="百萬網紅造浪推手 Pro",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 核心邏輯：視覺工程參數庫 ---
def get_engine_config(domain):
    configs = {
        "Food & Cooking": {
            "mj": "--ar 4:5 --style raw --v 6.0", 
            "banana": "Render 'Dish Name' elegantly on a menu card.",
            "icon": "🍳", "kb_file": "KB_04_Food_Cooking.txt"
        },
        "Travel & Lifestyle": {
            "mj": "--ar 16:9 --stylize 250 --v 6.0", 
            "banana": "Render 'Location Name' on a vintage sign.",
            "icon": "✈️", "kb_file": "KB_05_Travel_Lifestyle.txt"
        },
        "AI Workplace": {
            "mj": "--ar 1:1 --chaos 20 --v 6.0", 
            "banana": "Render keywords on holographic UI.",
            "icon": "🤖", "kb_file": "KB_01_AI_Workplace.txt"
        },
        "Corporate Strategy": {
            "mj": "--ar 3:2 --style raw --v 6.0", 
            "banana": "Render title on presentation slide.",
            "icon": "💼", "kb_file": "KB_02_Corporate_Strategy.txt"
        },
        "Labor Law": {
            "mj": "--ar 16:9 --no blur --v 6.0",
            "banana": "Render legal terms on documents.",
            "icon": "⚖️", "kb_file": "KB_03_Labor_Law.txt"
        },
        "Health & Wellness": {
            "mj": "--ar 4:5 --stylize 100",
            "banana": "Render health stats on smart watch.",
            "icon": "🌿", "kb_file": "KB_06_Health_Wellness.txt"
        },
        "Beauty & Skincare": {
            "mj": "--ar 4:5 --no skin_smoothing --v 6.0", 
            "banana": "Render product name on bottle.",
            "icon": "💄", "kb_file": "KB_07_Beauty_Skincare.txt"
        }
    }
    return configs.get(domain, {"mj": "--ar 1:1", "banana": "Standard Text", "icon": "❓", "kb_file": ""})

def load_kb_content(filename):
    if filename and os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f: return f.read()
        except: return "(Error reading KB)"
    return "(General Mode)"

# --- 3. UI 側邊欄 ---
st.sidebar.title("🌊 設定中心")
api_key = st.sidebar.text_input("輸入 Gemini API Key", type="password")
domain_list = ["AI Workplace", "Corporate Strategy", "Labor Law", "Food & Cooking", "Travel & Lifestyle", "Health & Wellness", "Beauty & Skincare"]
selected_domain = st.sidebar.selectbox("選擇造浪領域", domain_list)
current_config = get_engine_config(selected_domain)

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 視覺引擎狀態")
st.sidebar.info(f"MJ: `{current_config['mj']}`")
st.sidebar.warning(f"Banana: {current_config['banana']}")

# --- 4. 主畫面與分頁 ---
st.title(f"{current_config['icon']} 百萬網紅造浪推手: 視覺進化版")
st.caption("v3.2 - Bilingual Edition (CHT/ENG) & Vision Optimized")

tab_text, tab_vision = st.tabs(["📝 經典文字造浪", "👁️ 看圖說故事 (Vision)"])

# ==========================================
# TAB 1: 經典文字模式 (雙語版)
# ==========================================
with tab_text:
    st.header("📝 主題式生成")
    col1, col2 = st.columns([3, 1])
    with col1:
        topic = st.text_input("輸入核心主題", placeholder="例如：京都賞楓秘境")
    with col2:
        count = st.slider("生成篇數", 1, 10, 3, key="slider_text")

    if st.button("🚀 啟動文字造浪", key="btn_text"):
        if not api_key:
            st.error("❌ 請輸入 API Key")
        else:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('models/gemini-2.5-flash')
            kb_text = load_kb_content(current_config['kb_file'])
            
            sys_prompt = f"""
            Role: Mega-Influencer Wavemaker. Domain: {selected_domain}
            Context: {kb_text}. Topic: {topic}. Count: {count}.
            [VISUAL SPECS] MJ: {current_config['mj']}. Banana: {current_config['banana']}.
            
            Task: Generate {count} posts in STRICT JSON (hook_title, caption_body, hashtags, mj_prompt, nano_banana_prompt).
            
            **MANDATORY LANGUAGE FORMAT**:
            For 'hook_title' and 'caption_body', you MUST provide BOTH Traditional Chinese AND English.
            Format:
            [Traditional Chinese Text]
            
            [English Text]
            """
            
            with st.spinner("AI 正在撰寫雙語文案..."):
                try:
                    res = model.generate_content(sys_prompt)
                    data = json.loads(res.text.replace("```json","").replace("```","").strip())
                    
                    for i, post in enumerate(data):
                        with st.expander(f"📄 #{i+1} {post.get('hook_title')}", expanded=True):
                            st.write(post.get('caption_body'))
                            st.code(post.get('mj_prompt'))
                            st.code(post.get('nano_banana_prompt'))
                    
                    df = pd.DataFrame(data)
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer: df.to_excel(writer, index=False)
                    st.download_button("📥 下載 Excel", buffer.getvalue(), f"Wavemaker_{topic}.xlsx")
                except Exception as e:
                    st.error(f"生成失敗: {e}")

# ==========================================
# TAB 2: 視覺模式 (Vision 雙語版)
# ==========================================
with tab_vision:
    st.header("👁️ AI 視覺協作中心")
    uploaded_files = st.file_uploader("上傳參考圖片 (支持多張)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    vision_mode = st.radio("選擇協作模式", ["⚡ 自動分析模式 (Auto)", "🤝 專家協作模式 (Co-pilot)"], horizontal=True)
    
    if "vision_analysis" not in st.session_state:
        st.session_state.vision_analysis = ""
    
    if uploaded_files and api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # --- 模式 A: 自動分析 (雙語) ---
        if vision_mode == "⚡ 自動分析模式 (Auto)":
            if st.button("🚀 開始視覺分析與生成", key="btn_vision_auto"):
                images = [Image.open(f) for f in uploaded_files]
                
                with st.spinner("AI 正在看圖並構思雙語內容..."):
                    try:
                        prompt_content = [
                            f"""
                            Role: Social Media Visual Director. Domain: {selected_domain}
                            Task: Analyze these {len(images)} images.
                            Output: STRICT JSON list with {len(images)} objects.
                            
                            **MANDATORY LANGUAGE FORMAT**:
                            All text fields (hook_title, caption_body, visual_analysis, editing_suggestion) MUST be Bilingual.
                            Structure:
                            [Traditional Chinese Content]
                            
                            [English Content]
                            
                            JSON Keys:
                            1. hook_title
                            2. caption_body
                            3. visual_analysis (Explain lighting/composition)
                            4. editing_suggestion (Professional advice)
                            5. mj_prompt (English only)
                            """,
                            *images
                        ]
                        
                        res = model.generate_content(prompt_content)
                        data = json.loads(res.text.replace("```json","").replace("```","").strip())
                        
                        st.success("✅ 雙語分析完成！")
                        for i, post in enumerate(data):
                            col_img, col_txt = st.columns([1, 2])
                            with col_img:
                                # 修正: 使用 use_container_width 消除警告
                                st.image(uploaded_files[i], caption=f"圖片 #{i+1}", use_container_width=True)
                            with col_txt:
                                st.subheader(post.get('hook_title'))
                                st.write(post.get('caption_body'))
                                st.info(f"🔍 **視覺分析**: \n{post.get('visual_analysis')}")
                                st.warning(f"🎨 **修圖建議**: \n{post.get('editing_suggestion')}")
                                
                        df = pd.DataFrame(data)
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer: df.to_excel(writer, index=False)
                        st.download_button("📥 下載視覺報告 Excel", buffer.getvalue(), "Wavemaker_Vision_Auto.xlsx")

                    except Exception as e:
                        st.error(f"分析失敗: {e}")

        # --- 模式 B: 專家協作 (雙語) ---
        elif vision_mode == "🤝 專家協作模式 (Co-pilot)":
            if st.button("🔍 第一步：請求 AI 診斷", key="btn_vision_copilot_step1"):
                images = [Image.open(f) for f in uploaded_files]
                with st.spinner("AI 正在解讀..."):
                    prompt = [
                        f"""
                        Analyze these images for {selected_domain}.
                        Output Requirement: Provide 3 distinct 'Vibe Directions' (e.g., Emotional, Professional, Humorous).
                        Language: Bilingual (Traditional Chinese + English).
                        """, 
                        *images
                    ]
                    res = model.generate_content(prompt)
                    st.session_state.vision_analysis = res.text
            
            if st.session_state.vision_analysis:
                st.markdown("### 🤖 AI 診斷報告與建議")
                st.write(st.session_state.vision_analysis)
                st.markdown("---")
                
                user_direction = st.text_area("👤 您的決定", placeholder="例如：我想要方案 2，語氣再幽默一點...")
                
                if st.button("✍️ 第二步：確認並生成", key="btn_vision_copilot_step2"):
                    if not user_direction:
                        st.warning("請先輸入您的決定！")
                    else:
                        images = [Image.open(f) for f in uploaded_files]
                        with st.spinner("AI 正在創作..."):
                            final_prompt = [
                                f"""
                                Context: User uploaded images. User Direction: {user_direction}.
                                Task: Generate {len(images)} posts. Output: STRICT JSON list.
                                
                                **MANDATORY LANGUAGE FORMAT**:
                                All text fields (hook_title, caption_body, editing_suggestion) MUST be Bilingual.
                                [Traditional Chinese Content]
                                
                                [English Content]
                                """,
                                *images
                            ]
                            try:
                                res = model.generate_content(final_prompt)
                                data = json.loads(res.text.replace("```json","").replace("```","").strip())
                                for i, post in enumerate(data):
                                    st.subheader(f"貼文 #{i+1}: {post.get('hook_title')}")
                                    st.write(post.get('caption_body'))
                                    st.warning(f"🎨 修圖建議: \n{post.get('editing_suggestion')}")
                                    st.markdown("---")
                            except Exception as e:
                                st.error(f"生成失敗: {e}")

    elif not api_key:
        st.warning("👈 請先輸入 API Key")
    elif not uploaded_files:
        st.info("請上傳圖片以啟動視覺模式")