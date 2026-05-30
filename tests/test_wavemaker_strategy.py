import json

from wavemaker_strategy import (
    CULTURAL_VOICE_PLAYBOOKS,
    MATURITY_RUBRIC,
    PERSONA_PLAYBOOKS,
    PLATFORM_PLAYBOOKS,
    build_campaign_prompt,
    build_strategy_profile,
    get_domain_config,
    get_domain_names,
    parse_json_response,
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
    assert "exactly 2" in prompt
    assert "夏天通勤防曬" in prompt


def test_parse_json_response_accepts_fenced_json():
    payload = [{"maturity_score": 91, "primary_post": {"hook_title": "test"}}]
    text = "```json\n" + json.dumps(payload, ensure_ascii=False) + "\n```"

    assert parse_json_response(text) == payload
