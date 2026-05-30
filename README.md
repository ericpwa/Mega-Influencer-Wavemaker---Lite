# 🌊 Mega-Influencer Wavemaker (Lite) | 超級網紅造浪推手

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://eric-wavemaker-tw.streamlit.app/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**Empowering you to build a million-follower community.**
**協助您擁有百萬粉絲的社群網紅，自動化生成【病毒式貼文】、【平台化 Campaign Pack】、【視覺圖像提示詞】及【策略洞察】。**

Mega-Influencer Wavemaker is no longer only a simple copy generator. It now works as a **platform-native, TA-native, trend-aware smart copy workflow** that helps teams move faster from idea to publish-ready social content.

## 🚀 Key Features (核心功能)

### 1. 📝 Text Wavemaker (經典文字造浪)
- **7-Domain Knowledge Bank**: Built-in strategies for AI, Business, Law, Food, Travel, Health, and Beauty.
- **Expandable Domain Playbooks**: The 7 professional domains are preserved in one workflow layer and can be extended by adding a new domain config and knowledge-bank file.
- **Dual-Engine Prompts**: Generates **Midjourney** (Artistic) and **Gemini-Nano Banana** (Text Rendering) prompts simultaneously.
- **Strategic Output**: Unlike generic AI, it embeds specific marketing hooks and "Woo Factors" based on the chosen domain.
- **Campaign Pack Output**: Generates a publish-ready package with primary copy, short/long variants, spoken scripts, hooks, CTA, hashtags, visual prompts, comment starters, risk review, and rewrite notes.
- **Maturity Scoring**: Uses a 100-point readiness rubric covering TA fit, platform-native language, hook strength, product clarity, human voice, action trigger, and brand safety.

### 2. 🧠 Intelligent Copy Workflow (智能文案實戰工作流)
- **Platform-Native Playbooks**: Supports Threads, Instagram Reels, Instagram Feed, TikTok, Dcard, Xiaohongshu, Facebook, and LinkedIn.
- **TA / Persona Layer**: Tunes language and angles for audiences such as Gen Z trend hunters, young urban professionals, family buyers, skincare explorers, knowledge workers, and local community insiders.
- **Groundedness Controls**: Lets you tune how 接地氣, trend-sensitive, and brand-safe the copy should be.
- **Hook Engine Prompting**: Forces the model to generate and score multiple hooks internally before producing the final Campaign Pack.
- **AI-Flavored Copy Review**: Instructs the workflow to remove generic brand language, exaggerated claims, unsupported promises, and obvious AI phrasing.
- **Multicultural Voice Layer**: Adds respectful language/culture modes including 標準繁中, 台灣口語, 台語風味, 客語風味, and 晶晶體.

### 3. 👁️ Vision Pro (視覺協作中心)
- **Auto Analysis**: Upload photos to get instant copy, visual analysis, and professional editing suggestions.
- **Co-pilot Mode**: Interactive brainstorming where AI diagnoses the "Vibe" first, then collaborates with you to create the perfect post.
- **Workflow-Aware Output**: Vision mode now follows the same platform, persona, cultural voice, and maturity-target settings as text mode.
- **Image-to-Story Insights**: Each visual Campaign Pack can include image observation, story angle, and practical editing suggestions.

## 🛠️ How to Use (如何使用)

1. **Access the App**: Click the [Streamlit App Link](https://eric-wavemaker-tw.streamlit.app/).
2. **Enter Credentials**: Input your Google Gemini API Key in the sidebar.
3. **Select Domain**: Choose your niche (e.g., *Travel & Lifestyle*).
4. **Configure Workflow**:
   - Pick a platform (e.g., *Threads* or *TikTok*).
   - Pick a TA / Persona.
   - Pick a cultural voice such as *台灣口語*, *台語風味*, *客語風味*, or *晶晶體*.
   - Tune groundedness, trend sensitivity, brand safety, and maturity target.
5. **Ignite**:
   - **Text Mode**: Enter a topic (e.g., "Kyoto Hidden Gems") and click Generate.
   - **Vision Mode**: Upload an image and choose "Auto" or "Co-pilot".
6. **Download**: Get your Campaign Pack in a structured **Excel report**.

## 🏗️ Tech Stack (技術架構)

- **Frontend**: Streamlit
- **AI Core**: Google Gemini 2.5 Flash (via `google-generativeai`)
- **Data Handling**: Pandas, OpenPyXL
- **Image Processing**: Pillow
- **Workflow Layer**: `wavemaker_strategy.py`

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
*Developed by (Eric PWA) PAN WEN AN*
