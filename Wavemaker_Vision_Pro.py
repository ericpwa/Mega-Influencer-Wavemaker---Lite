import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import io
import os
from PIL import Image
from image_generation import (
    IMAGE_BACKENDS,
    extension_for_mime_type,
    generate_gemini_image,
    generate_openai_image,
)
from wavemaker_strategy import (
    CULTURAL_VOICE_PLAYBOOKS,
    IMAGE_ENGINE_PLAYBOOKS,
    IMAGE_FORMAT_PLAYBOOKS,
    LAYOUT_PLAYBOOKS,
    PERSONA_PLAYBOOKS,
    PLATFORM_PLAYBOOKS,
    VISUAL_STRATEGY_MODES,
    VISUAL_STYLE_PLAYBOOKS,
    build_campaign_prompt,
    build_strategy_profile,
    build_vision_campaign_prompt,
    get_domain_config,
    get_domain_names,
    parse_json_response,
)

# --- 1. 頁面基礎設定 ---
st.set_page_config(
    page_title="百萬網紅造浪推手 Pro",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 核心邏輯：視覺工程參數庫 ---
def get_engine_config(domain):
    return get_domain_config(domain)

def get_image_format_defaults(image_format):
    format_rule = IMAGE_FORMAT_PLAYBOOKS.get(image_format, IMAGE_FORMAT_PLAYBOOKS["自訂"])
    return format_rule["aspect_ratio"], format_rule["openai_size"]

def load_kb_content(filename):
    if filename and os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f: return f.read()
        except: return "(Error reading KB)"
    return "(General Mode)"

def render_campaign_pack(
    post,
    index=None,
    image_backend="Prompt only (0 cost)",
    gemini_image_api_key="",
    openai_api_key="",
    gemini_image_aspect_ratio="1:1",
    gemini_image_size="512",
    openai_image_size="1024x1024",
    openai_image_quality="low",
):
    title_prefix = f"📄 #{index + 1} " if index is not None else ""
    primary_post = post.get("primary_post", {})
    visual_prompts = post.get("visual_prompts", {})
    image_generation_brief = post.get("image_generation_brief", {})
    visual_insights = post.get("visual_insights", {})
    platform_variants = post.get("platform_variants", {})

    with st.expander(f"{title_prefix}{primary_post.get('hook_title', 'Campaign Pack')}", expanded=True):
        score = post.get("maturity_score", "N/A")
        readiness = post.get("readiness_level", "N/A")
        st.metric("成熟度 / 可發布度", f"{score}/100" if isinstance(score, int) else score, readiness)

        st.markdown("#### 主文案")
        st.subheader(primary_post.get("hook_title", ""))
        st.write(primary_post.get("caption_body", ""))
        st.caption(primary_post.get("cta", ""))
        hashtags = primary_post.get("hashtags", [])
        if hashtags:
            st.code(" ".join(hashtags), language=None)

        st.markdown("#### Hook 候選")
        for hook in post.get("hook_candidates", []):
            st.write(f"- {hook}")

        st.markdown("#### 平台變體")
        st.write("**短版**")
        st.write(platform_variants.get("short_post", ""))
        st.write("**長版**")
        st.write(platform_variants.get("long_post", ""))
        st.write("**口播版**")
        st.write(platform_variants.get("spoken_script", ""))

        st.markdown("#### 文案轉圖像 Brief")
        st.write("**創意方向**")
        st.write(image_generation_brief.get("creative_direction", ""))
        st.write("**視覺策略**")
        st.write(image_generation_brief.get("visual_strategy_mode", ""))
        st.write("**視覺風格**")
        st.write(image_generation_brief.get("visual_style", ""))
        st.write("**排版結構**")
        st.write(image_generation_brief.get("layout_structure", ""))
        st.write("**社群版型**")
        st.write(image_generation_brief.get("social_format", ""))
        custom_notes = image_generation_brief.get("custom_visual_notes", "")
        if custom_notes:
            st.write("**自訂視覺指令**")
            st.write(custom_notes)
        st.write("**圖上文字**")
        st.write(image_generation_brief.get("on_image_text", ""))
        safety_notes = image_generation_brief.get("brand_safety_notes", "")
        if safety_notes:
            st.caption(f"視覺安全提醒：{safety_notes}")

        st.markdown("#### 多引擎文生圖提示詞")
        prompt_tabs = st.tabs(["ChatGPT Image 2", "Gemini / Nano Banana", "Midjourney"])
        with prompt_tabs[0]:
            st.code(visual_prompts.get("chatgpt_image_prompt", ""), language=None)
        with prompt_tabs[1]:
            st.code(
                visual_prompts.get("gemini_image_prompt")
                or visual_prompts.get("nano_banana_prompt", ""),
                language=None,
            )
        with prompt_tabs[2]:
            st.code(
                visual_prompts.get("midjourney_prompt")
                or visual_prompts.get("mj_prompt", ""),
                language=None,
            )

        st.markdown("#### 實際文生圖")
        if image_backend == "Prompt only (0 cost)":
            st.caption("目前為 0 成本模式：不呼叫任何生圖 API，只輸出可複製的提示詞。")
        else:
            if image_backend == "Gemini Image (low cost)":
                generation_prompt = (
                    visual_prompts.get("gemini_image_prompt")
                    or visual_prompts.get("nano_banana_prompt", "")
                )
            else:
                generation_prompt = visual_prompts.get("chatgpt_image_prompt", "")

            if not generation_prompt:
                st.warning("這篇 Campaign Pack 沒有可用的文生圖提示詞。")
            elif st.button(
                f"生成 1 張圖片 - {image_backend}",
                key=f"generate_image_{index}_{image_backend}",
            ):
                with st.spinner("正在生成 1 張圖片，避免批量消耗額度..."):
                    try:
                        if image_backend == "Gemini Image (low cost)":
                            image_bytes, mime_type = generate_gemini_image(
                                gemini_image_api_key,
                                generation_prompt,
                                aspect_ratio=gemini_image_aspect_ratio,
                                image_size=gemini_image_size,
                            )
                        else:
                            image_bytes, mime_type = generate_openai_image(
                                openai_api_key,
                                generation_prompt,
                                size=openai_image_size,
                                quality=openai_image_quality,
                            )

                        state_key = f"generated_image_{index}_{image_backend}"
                        st.session_state[state_key] = {
                            "bytes": image_bytes,
                            "mime_type": mime_type,
                        }
                    except Exception as e:
                        st.error(f"圖片生成失敗：{e}")

            state_key = f"generated_image_{index}_{image_backend}"
            generated = st.session_state.get(state_key)
            if generated:
                st.image(generated["bytes"], caption=f"{image_backend} 生成結果", use_container_width=True)
                extension = extension_for_mime_type(generated["mime_type"])
                st.download_button(
                    "下載生成圖片",
                    generated["bytes"],
                    file_name=f"wavemaker_generated_{index + 1 if index is not None else 1}.{extension}",
                    mime=generated["mime_type"],
                    key=f"download_image_{index}_{image_backend}",
                )

        if visual_insights:
            st.markdown("#### 看圖說故事洞察")
            st.write("**圖片觀察**")
            st.write(visual_insights.get("image_observation", ""))
            st.write("**故事角度**")
            st.write(visual_insights.get("story_angle", ""))
            st.write("**視覺優化建議**")
            st.write(visual_insights.get("editing_suggestion", ""))

        risk_review = post.get("risk_review", [])
        if risk_review:
            st.warning("風險提醒\n" + "\n".join([f"- {item}" for item in risk_review]))

        rewrite_notes = post.get("rewrite_notes", [])
        if rewrite_notes:
            st.info("成熟度修正\n" + "\n".join([f"- {item}" for item in rewrite_notes]))

def flatten_campaign_pack(post):
    primary_post = post.get("primary_post", {})
    visual_prompts = post.get("visual_prompts", {})
    image_generation_brief = post.get("image_generation_brief", {})
    visual_insights = post.get("visual_insights", {})
    platform_variants = post.get("platform_variants", {})
    strategy_snapshot = post.get("strategy_snapshot", {})
    return {
        "platform": strategy_snapshot.get("platform", ""),
        "persona": strategy_snapshot.get("persona", ""),
        "cultural_voice": strategy_snapshot.get("cultural_voice", ""),
        "maturity_score": post.get("maturity_score", ""),
        "readiness_level": post.get("readiness_level", ""),
        "hook_title": primary_post.get("hook_title", ""),
        "caption_body": primary_post.get("caption_body", ""),
        "cta": primary_post.get("cta", ""),
        "hashtags": " ".join(primary_post.get("hashtags", [])),
        "short_post": platform_variants.get("short_post", ""),
        "long_post": platform_variants.get("long_post", ""),
        "spoken_script": platform_variants.get("spoken_script", ""),
        "creative_direction": image_generation_brief.get("creative_direction", ""),
        "visual_strategy_mode": image_generation_brief.get("visual_strategy_mode", ""),
        "visual_style": image_generation_brief.get("visual_style", ""),
        "layout_structure": image_generation_brief.get("layout_structure", ""),
        "social_format": image_generation_brief.get("social_format", ""),
        "custom_visual_notes": image_generation_brief.get("custom_visual_notes", ""),
        "on_image_text": image_generation_brief.get("on_image_text", ""),
        "visual_brand_safety_notes": image_generation_brief.get("brand_safety_notes", ""),
        "image_observation": visual_insights.get("image_observation", ""),
        "story_angle": visual_insights.get("story_angle", ""),
        "editing_suggestion": visual_insights.get("editing_suggestion", ""),
        "hook_candidates": "\n".join(post.get("hook_candidates", [])),
        "comment_starters": "\n".join(post.get("comment_starters", [])),
        "risk_review": "\n".join(post.get("risk_review", [])),
        "rewrite_notes": "\n".join(post.get("rewrite_notes", [])),
        "chatgpt_image_prompt": visual_prompts.get("chatgpt_image_prompt", ""),
        "gemini_image_prompt": visual_prompts.get("gemini_image_prompt", ""),
        "midjourney_prompt": visual_prompts.get("midjourney_prompt", ""),
        "mj_prompt": visual_prompts.get("mj_prompt", ""),
        "nano_banana_prompt": visual_prompts.get("nano_banana_prompt", ""),
    }

# --- 3. UI 側邊欄 ---
st.sidebar.title("🌊 設定中心")
api_key = st.sidebar.text_input("輸入 Gemini API Key", type="password")
openai_api_key = st.sidebar.text_input("輸入 OpenAI API Key（選填，只有使用 OpenAI 生圖時需要）", type="password")
domain_list = get_domain_names()
selected_domain = st.sidebar.selectbox("選擇造浪領域", domain_list)
current_config = get_engine_config(selected_domain)

st.sidebar.markdown("---")
st.sidebar.subheader("🧠 智能文案實戰工作流")
selected_platform = st.sidebar.selectbox("平台語感", list(PLATFORM_PLAYBOOKS.keys()))
selected_persona = st.sidebar.selectbox("TA / Persona", list(PERSONA_PLAYBOOKS.keys()))
selected_cultural_voice = st.sidebar.selectbox("多元語言文化", list(CULTURAL_VOICE_PLAYBOOKS.keys()))
tone_recipe = st.sidebar.text_input("語氣配方", value="70% 朋友聊天 + 20% 專業提醒 + 10% 幽默吐槽")
groundedness = st.sidebar.slider("接地氣程度", 1, 10, 8)
trend_sensitivity = st.sidebar.slider("趨勢敏感度", 1, 10, 8)
brand_safety = st.sidebar.slider("品牌安全", 1, 10, 8)
maturity_target = st.sidebar.slider("成熟度門檻", 80, 98, 90)

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 視覺風格與排版")
visual_strategy_mode = st.sidebar.selectbox("視覺策略模式", list(VISUAL_STRATEGY_MODES.keys()), index=0)
selected_visual_style = st.sidebar.selectbox("視覺風格", list(VISUAL_STYLE_PLAYBOOKS.keys()), index=0)
selected_layout_structure = st.sidebar.selectbox("排版結構", list(LAYOUT_PLAYBOOKS.keys()), index=0)
selected_image_format = st.sidebar.selectbox("圖像尺寸 / 平台版型", list(IMAGE_FORMAT_PLAYBOOKS.keys()), index=0)

custom_visual_style = ""
custom_layout = ""
custom_image_format = ""
if selected_visual_style == "自訂" or visual_strategy_mode == "AI 推薦後可修改":
    custom_visual_style = st.sidebar.text_area(
        "自訂視覺風格",
        placeholder="例如：台灣夜市霓虹、復古招牌、底片攝影感...",
        height=80,
    )
if selected_layout_structure == "自訂" or visual_strategy_mode == "AI 推薦後可修改":
    custom_layout = st.sidebar.text_area(
        "自訂排版結構",
        placeholder="例如：上方大標、中央產品、下方三個賣點徽章...",
        height=80,
    )
if selected_image_format == "自訂":
    custom_image_format = st.sidebar.text_input("自訂圖像尺寸 / 比例", placeholder="例如：2:3、1200x628、限時動態直式")

strategy_profile = build_strategy_profile(
    selected_platform,
    selected_persona,
    selected_cultural_voice,
    groundedness,
    trend_sensitivity,
    brand_safety,
    maturity_target,
    tone_recipe,
    visual_strategy_mode=visual_strategy_mode,
    visual_style=selected_visual_style,
    layout_structure=selected_layout_structure,
    image_format=selected_image_format,
    custom_visual_style=custom_visual_style,
    custom_layout=custom_layout,
    custom_image_format=custom_image_format,
)

with st.sidebar.expander("查看目前策略設定"):
    st.json(strategy_profile)

st.sidebar.markdown("---")
st.sidebar.subheader("🧩 AI 後台模型設定")
st.sidebar.caption("預設 0 成本：只產 prompt，不自動生圖。按單篇生成按鈕才會消耗 API 額度。")
copy_model = st.sidebar.selectbox("文案 / 策略模型", ["Gemini 2.5 Flash"], index=0)
image_backend = st.sidebar.selectbox("實際文生圖後台", list(IMAGE_BACKENDS.keys()), index=0)
st.sidebar.info(f"{IMAGE_BACKENDS[image_backend]['cost_mode']}：{IMAGE_BACKENDS[image_backend]['description']}")

if image_backend == "Gemini Image (low cost)":
    default_gemini_ratio, _ = get_image_format_defaults(selected_image_format)
    gemini_ratio_options = ["1:1", "4:5", "9:16", "16:9"]
    gemini_ratio_index = gemini_ratio_options.index(default_gemini_ratio) if default_gemini_ratio in gemini_ratio_options else 0
    gemini_image_aspect_ratio = st.sidebar.selectbox("Gemini 圖像比例", gemini_ratio_options, index=gemini_ratio_index)
    gemini_image_size = st.sidebar.selectbox("Gemini 圖像尺寸", ["512", "1K"], index=0)
else:
    gemini_image_aspect_ratio = "1:1"
    gemini_image_size = "512"

if image_backend == "OpenAI Image (low cost)":
    _, default_openai_size = get_image_format_defaults(selected_image_format)
    openai_size_options = ["1024x1024", "1024x1536", "1536x1024"]
    openai_size_index = openai_size_options.index(default_openai_size) if default_openai_size in openai_size_options else 0
    openai_image_size = st.sidebar.selectbox("OpenAI 圖像尺寸", openai_size_options, index=openai_size_index)
    openai_image_quality = st.sidebar.selectbox("OpenAI 圖像品質", ["low", "medium", "high"], index=0)
else:
    openai_image_size = "1024x1024"
    openai_image_quality = "low"

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 多引擎圖像生成中心")
st.sidebar.caption("文案生成後會同步產出 ChatGPT、Gemini / Nano Banana、Midjourney 可用的文生圖提示詞。")
with st.sidebar.expander("ChatGPT Image 2", expanded=False):
    st.write(IMAGE_ENGINE_PLAYBOOKS["ChatGPT Image 2"]["best_for"])
    st.code(IMAGE_ENGINE_PLAYBOOKS["ChatGPT Image 2"]["prompt_style"], language=None)
with st.sidebar.expander("Gemini / Nano Banana", expanded=False):
    st.write(IMAGE_ENGINE_PLAYBOOKS["Gemini 3.1 Flash Image (Nano Banana)"]["best_for"])
    st.code(IMAGE_ENGINE_PLAYBOOKS["Gemini 3.1 Flash Image (Nano Banana)"]["prompt_style"], language=None)
with st.sidebar.expander("Midjourney", expanded=True):
    st.write(IMAGE_ENGINE_PLAYBOOKS["Midjourney"]["best_for"])
    st.code(current_config["mj"], language=None)
    st.caption(IMAGE_ENGINE_PLAYBOOKS["Midjourney"]["prompt_style"])

# --- 4. 主畫面與分頁 ---
st.title("🌊 百萬網紅造浪推手: 視覺進化版")
st.caption("v4.0 - Platform-native, TA-native, Trend-aware Campaign Workflow")

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
            sys_prompt = build_campaign_prompt(
                selected_domain,
                topic,
                count,
                kb_text,
                current_config,
                strategy_profile,
            )

            with st.spinner("AI 正在執行平台化、TA 化、趨勢化文案工作流..."):
                try:
                    res = model.generate_content(sys_prompt)
                    data = parse_json_response(res.text)

                    for i, post in enumerate(data):
                        render_campaign_pack(
                            post,
                            i,
                            image_backend=image_backend,
                            gemini_image_api_key=api_key,
                            openai_api_key=openai_api_key,
                            gemini_image_aspect_ratio=gemini_image_aspect_ratio,
                            gemini_image_size=gemini_image_size,
                            openai_image_size=openai_image_size,
                            openai_image_quality=openai_image_quality,
                        )

                    df = pd.DataFrame([flatten_campaign_pack(post) for post in data])
                    buffer = io.BytesIO()
                    with pd.ExcelWriter(buffer, engine='openpyxl') as writer: df.to_excel(writer, index=False)
                    st.download_button("📥 下載 Campaign Pack Excel", buffer.getvalue(), f"Wavemaker_CampaignPack_{topic}.xlsx")
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
                        prompt_content = [build_vision_campaign_prompt(selected_domain, len(images), strategy_profile), *images]

                        res = model.generate_content(prompt_content)
                        data = parse_json_response(res.text)

                        st.success("✅ 視覺 Campaign Pack 完成！")
                        for i, post in enumerate(data):
                            col_img, col_txt = st.columns([1, 2])
                            with col_img:
                                # 修正: 使用 use_container_width 消除警告
                                st.image(uploaded_files[i], caption=f"圖片 #{i+1}", use_container_width=True)
                            with col_txt:
                                render_campaign_pack(
                                    post,
                                    i,
                                    image_backend=image_backend,
                                    gemini_image_api_key=api_key,
                                    openai_api_key=openai_api_key,
                                    gemini_image_aspect_ratio=gemini_image_aspect_ratio,
                                    gemini_image_size=gemini_image_size,
                                    openai_image_size=openai_image_size,
                                    openai_image_quality=openai_image_quality,
                                )

                        df = pd.DataFrame([flatten_campaign_pack(post) for post in data])
                        buffer = io.BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer: df.to_excel(writer, index=False)
                        st.download_button("📥 下載視覺 Campaign Pack Excel", buffer.getvalue(), "Wavemaker_Vision_CampaignPack.xlsx")

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
                        Strategy Profile: {json.dumps(strategy_profile, ensure_ascii=False)}
                        Output Requirement: Provide 3 distinct platform-native Vibe Directions.
                        Include persona fit, cultural voice fit, likely hook angle, and risk notes.
                        Language: Traditional Chinese.
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
                            final_prompt = [build_vision_campaign_prompt(selected_domain, len(images), strategy_profile, user_direction), *images]
                            try:
                                res = model.generate_content(final_prompt)
                                data = parse_json_response(res.text)
                                for i, post in enumerate(data):
                                    render_campaign_pack(
                                        post,
                                        i,
                                        image_backend=image_backend,
                                        gemini_image_api_key=api_key,
                                        openai_api_key=openai_api_key,
                                        gemini_image_aspect_ratio=gemini_image_aspect_ratio,
                                        gemini_image_size=gemini_image_size,
                                        openai_image_size=openai_image_size,
                                        openai_image_quality=openai_image_quality,
                                    )
                            except Exception as e:
                                st.error(f"生成失敗: {e}")

    elif not api_key:
        st.warning("👈 請先輸入 API Key")
    elif not uploaded_files:
        st.info("請上傳圖片以啟動視覺模式")
