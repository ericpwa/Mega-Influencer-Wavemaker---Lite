import json

from wavemaker_strategy import (
    CAMPAIGN_PACK_SCHEMA,
    CULTURAL_VOICE_PLAYBOOKS,
    DEFAULT_IMAGE_FORMAT_BY_PLATFORM,
    IMAGE_FORMAT_PLAYBOOKS,
    IMAGE_ENGINE_PLAYBOOKS,
    LAYOUT_PLAYBOOKS,
    MATURITY_RUBRIC,
    PERSONA_PLAYBOOKS,
    PLATFORM_PLAYBOOKS,
    VISUAL_STRATEGY_MODES,
    VISUAL_STYLE_PLAYBOOKS,
    build_campaign_prompt,
    build_strategy_profile,
    get_domain_config,
    get_domain_names,
    parse_json_response,
    recommend_image_format_for_platform,
    recommend_visual_style_and_layout,
)


def test_build_strategy_profile_includes_cultural_voice_and_rubric():
    profile = build_strategy_profile(
        platform="Threads",
        persona="Young Urban Professional",
        cultural_voice="台語風味",
        groundedness=9,
        trend_sensitivity=8,
        brand_safety=7,
        maturity_target=90,
        tone_recipe="70% 朋友聊天 + 20% 專業提醒 + 10% 幽默吐槽",
    )

    assert profile["platform_playbook"] == PLATFORM_PLAYBOOKS["Threads"]
    assert profile["persona_playbook"] == PERSONA_PLAYBOOKS["Young Urban Professional"]
    assert profile["cultural_voice_playbook"] == CULTURAL_VOICE_PLAYBOOKS["台語風味"]
    assert profile["maturity_rubric"] == MATURITY_RUBRIC
    assert profile["maturity_target"] == 90
    assert profile["image_engine_playbooks"] == IMAGE_ENGINE_PLAYBOOKS
    assert profile["visual_strategy"]["mode"] == "AI 自動推薦"


def test_domain_config_preserves_seven_expandable_domains():
    domain_names = get_domain_names()

    assert domain_names == [
        "Food & Cooking",
        "Travel & Lifestyle",
        "AI Workplace",
        "Corporate Strategy",
        "Labor Law",
        "Health & Wellness",
        "Beauty & Skincare",
    ]
    assert get_domain_config("Beauty & Skincare")["kb_file"] == "KB_07_Beauty_Skincare.txt"
    assert "expansion_note" in get_domain_config("Beauty & Skincare")


def test_build_campaign_prompt_contains_workflow_requirements():
    profile = build_strategy_profile(
        platform="Xiaohongshu",
        persona="Beauty Skincare Explorer",
        cultural_voice="晶晶體",
        groundedness=8,
        trend_sensitivity=9,
        brand_safety=8,
        maturity_target=92,
        tone_recipe="60% 種草 + 25% 真實體驗 + 15% playful",
    )

    prompt = build_campaign_prompt(
        domain="Beauty & Skincare",
        topic="夏天通勤防曬",
        count=2,
        kb_text="skincare knowledge",
        visual_config={"mj": "--ar 4:5", "banana": "Render product name on bottle."},
        strategy_profile=profile,
    )

    assert "Campaign Pack" in prompt
    assert "platform-native" in prompt
    assert "TA-native" in prompt
    assert "cultural voice" in prompt
    assert "Domain expansion note" in prompt
    assert "ChatGPT Image 2" in prompt
    assert "Gemini 3.1 Flash Image" in prompt
    assert "Midjourney" in prompt
    assert "exactly 2" in prompt
    assert "夏天通勤防曬" in prompt


def test_campaign_pack_schema_contains_multi_engine_image_prompts():
    visual_prompts = CAMPAIGN_PACK_SCHEMA["visual_prompts"]
    image_brief = CAMPAIGN_PACK_SCHEMA["image_generation_brief"]

    assert "chatgpt_image_prompt" in visual_prompts
    assert "gemini_image_prompt" in visual_prompts
    assert "midjourney_prompt" in visual_prompts
    assert "creative_direction" in image_brief
    assert "visual_strategy_mode" in image_brief
    assert "visual_style" in image_brief
    assert "layout_structure" in image_brief
    assert "on_image_text" in image_brief


def test_visual_style_layout_and_format_playbooks_match_product_requirements():
    assert list(VISUAL_STRATEGY_MODES.keys()) == ["AI 自動推薦", "使用者指定", "AI 推薦後可修改"]
    assert len(VISUAL_STYLE_PLAYBOOKS) == 20
    assert "Q版/chili人像" in VISUAL_STYLE_PLAYBOOKS
    assert "3D盲盒公仔" in VISUAL_STYLE_PLAYBOOKS
    assert "paper cutout 立體剪紙藝術" in VISUAL_STYLE_PLAYBOOKS
    assert "黑板粉筆板書" in VISUAL_STYLE_PLAYBOOKS
    assert "claymorphism軟萌黏土" in VISUAL_STYLE_PLAYBOOKS
    assert "多彩曼非斯" in VISUAL_STYLE_PLAYBOOKS
    assert "自訂" in VISUAL_STYLE_PLAYBOOKS
    assert len(LAYOUT_PLAYBOOKS) == 12
    assert len(IMAGE_FORMAT_PLAYBOOKS) == 6


def test_platform_image_format_recommendations_keep_manual_options_available():
    assert DEFAULT_IMAGE_FORMAT_BY_PLATFORM["Threads"] == "1:1 IG / Threads"
    assert DEFAULT_IMAGE_FORMAT_BY_PLATFORM["Instagram Feed"] == "4:5 IG Feed"
    assert DEFAULT_IMAGE_FORMAT_BY_PLATFORM["Instagram Reels"] == "9:16 Reels / TikTok / Shorts"
    assert DEFAULT_IMAGE_FORMAT_BY_PLATFORM["TikTok"] == "9:16 Reels / TikTok / Shorts"
    assert DEFAULT_IMAGE_FORMAT_BY_PLATFORM["LinkedIn"] == "3:2 LinkedIn / Presentation"
    assert recommend_image_format_for_platform("Unknown Platform") == "1:1 IG / Threads"
    assert set(DEFAULT_IMAGE_FORMAT_BY_PLATFORM.values()).issubset(IMAGE_FORMAT_PLAYBOOKS.keys())


def test_visual_style_and_layout_recommendations_follow_workflow_context():
    tiktok_recommendation = recommend_visual_style_and_layout(
        platform="TikTok",
        persona="Gen Z Trend Hunter",
        cultural_voice="台灣口語",
        domain="Food & Cooking",
    )
    linkedin_recommendation = recommend_visual_style_and_layout(
        platform="LinkedIn",
        persona="Knowledge Worker",
        cultural_voice="標準繁中",
        domain="Corporate Strategy",
    )
    beauty_recommendation = recommend_visual_style_and_layout(
        platform="Xiaohongshu",
        persona="Beauty Skincare Explorer",
        cultural_voice="晶晶體",
        domain="Beauty & Skincare",
    )

    assert tiktok_recommendation == {
        "visual_style": "社群迷因風",
        "layout_structure": "大標題置中",
    }
    assert linkedin_recommendation == {
        "visual_style": "資訊圖卡風",
        "layout_structure": "左圖右文",
    }
    assert beauty_recommendation == {
        "visual_style": "小紅書種草風",
        "layout_structure": "九宮格懶人包",
    }


def test_visual_strategy_options_are_injected_into_prompt():
    profile = build_strategy_profile(
        platform="Instagram Feed",
        persona="Gen Z Trend Hunter",
        cultural_voice="台灣口語",
        groundedness=8,
        trend_sensitivity=9,
        brand_safety=8,
        maturity_target=90,
        tone_recipe="80% 種草 + 20% 幽默",
        visual_strategy_mode="使用者指定",
        visual_style="3D盲盒公仔",
        layout_structure="產品置中 + 賣點環繞",
        image_format="4:5 IG Feed",
        custom_visual_style="透明展示盒、可愛配件",
        custom_layout="產品置中，三個賣點在周圍",
    )

    prompt = build_campaign_prompt(
        domain="Beauty & Skincare",
        topic="新品保濕霜",
        count=1,
        kb_text="beauty knowledge",
        visual_config={"mj": "--ar 4:5", "banana": "Render product name on bottle."},
        strategy_profile=profile,
    )

    assert "visual_strategy" in prompt
    assert "使用者指定" in prompt
    assert "3D盲盒公仔" in prompt
    assert "產品置中 + 賣點環繞" in prompt
    assert "4:5 IG Feed" in prompt


def test_parse_json_response_accepts_fenced_json():
    payload = [{"maturity_score": 91, "primary_post": {"hook_title": "test"}}]
    text = "```json\n" + json.dumps(payload, ensure_ascii=False) + "\n```"

    assert parse_json_response(text) == payload
