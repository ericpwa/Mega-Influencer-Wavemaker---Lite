import json
import re


DOMAIN_PLAYBOOKS = {
    "Food & Cooking": {
        "mj": "--ar 4:5 --style raw --v 6.0",
        "banana": "Render 'Dish Name' elegantly on a menu card.",
        "icon": "🍳",
        "kb_file": "KB_04_Food_Cooking.txt",
        "expansion_note": "Use this structure when adding cuisine, restaurant, recipe, or food commerce domains.",
    },
    "Travel & Lifestyle": {
        "mj": "--ar 16:9 --stylize 250 --v 6.0",
        "banana": "Render 'Location Name' on a vintage sign.",
        "icon": "✈️",
        "kb_file": "KB_05_Travel_Lifestyle.txt",
        "expansion_note": "Use this structure when adding destination, hotel, local guide, or lifestyle domains.",
    },
    "AI Workplace": {
        "mj": "--ar 1:1 --chaos 20 --v 6.0",
        "banana": "Render keywords on holographic UI.",
        "icon": "🤖",
        "kb_file": "KB_01_AI_Workplace.txt",
        "expansion_note": "Use this structure when adding productivity, SaaS, or future-of-work domains.",
    },
    "Corporate Strategy": {
        "mj": "--ar 3:2 --style raw --v 6.0",
        "banana": "Render title on presentation slide.",
        "icon": "💼",
        "kb_file": "KB_02_Corporate_Strategy.txt",
        "expansion_note": "Use this structure when adding management, finance, or B2B advisory domains.",
    },
    "Labor Law": {
        "mj": "--ar 16:9 --no blur --v 6.0",
        "banana": "Render legal terms on documents.",
        "icon": "⚖️",
        "kb_file": "KB_03_Labor_Law.txt",
        "expansion_note": "Use this structure when adding regulated, legal, compliance, or public-policy domains.",
    },
    "Health & Wellness": {
        "mj": "--ar 4:5 --stylize 100",
        "banana": "Render health stats on smart watch.",
        "icon": "🌿",
        "kb_file": "KB_06_Health_Wellness.txt",
        "expansion_note": "Use this structure when adding fitness, nutrition, sleep, or wellness domains.",
    },
    "Beauty & Skincare": {
        "mj": "--ar 4:5 --no skin_smoothing --v 6.0",
        "banana": "Render product name on bottle.",
        "icon": "💄",
        "kb_file": "KB_07_Beauty_Skincare.txt",
        "expansion_note": "Use this structure when adding cosmetics, fragrance, haircare, or personal-care domains.",
    },
}


PLATFORM_PLAYBOOKS = {
    "Threads": {
        "native_shape": "first-person thought, short paragraphs, high shareability, low ad-scent",
        "hook_bias": "relatable confession, contrarian take, or tiny daily-life truth",
        "cta_style": "soft question that invites replies or reposts",
    },
    "Instagram Reels": {
        "native_shape": "3-second spoken hook, visual scene, benefit reveal, concise CTA",
        "hook_bias": "scene conflict, before-after tension, or quick payoff",
        "cta_style": "save, share, comment, or DM keyword",
    },
    "Instagram Feed": {
        "native_shape": "scroll-stopping title, story-led caption, polished but human",
        "hook_bias": "aspirational pain point or concrete transformation",
        "cta_style": "saveable tip, comment prompt, or profile action",
    },
    "TikTok": {
        "native_shape": "fast spoken opening, punchy beats, creator-native wording",
        "hook_bias": "unexpected result, taboo honesty, or 'I tested this so you do not have to'",
        "cta_style": "watch-through, comment, stitch, or follow-up promise",
    },
    "Dcard": {
        "native_shape": "anonymous-feeling story, practical details, honest pros and cons",
        "hook_bias": "personal dilemma, regret, discovery, or comparison",
        "cta_style": "ask for experiences or recommendations",
    },
    "Xiaohongshu": {
        "native_shape": "searchable title, checklist energy, practical texture, proof points",
        "hook_bias": "regret-too-late, lazy guide, comparison, or real-use note",
        "cta_style": "save, collect, ask for list, or comment keyword",
    },
    "Facebook": {
        "native_shape": "community-friendly story, fuller context, clear value and discussion",
        "hook_bias": "shared experience, local relevance, or practical reminder",
        "cta_style": "comment, share with a friend, or join discussion",
    },
    "LinkedIn": {
        "native_shape": "clear point of view, professional lesson, compact case insight",
        "hook_bias": "counterintuitive business observation or sharp lesson learned",
        "cta_style": "thoughtful question or professional takeaway",
    },
}


IMAGE_ENGINE_PLAYBOOKS = {
    "ChatGPT Image 2": {
        "role": "Text-to-image prompt for ChatGPT image generation",
        "prompt_style": "natural-language creative brief with subject, scene, mood, composition, lighting, visual hierarchy, and text placement",
        "best_for": "social post hero visuals, campaign concepts, lifestyle scenes, editorial graphics, and branded creative directions",
        "output_rule": "Write a self-contained prompt that can be pasted into ChatGPT. Mention desired aspect ratio, visual style, and any on-image text exactly.",
    },
    "Gemini 3.1 Flash Image (Nano Banana)": {
        "role": "Text-to-image prompt optimized for Gemini / Nano Banana style text rendering",
        "prompt_style": "clear layout instructions, readable typography, exact wording, object placement, and image-editing constraints",
        "best_for": "graphics that need reliable text on image, product labels, social cards, poster-style layouts, and fast iteration",
        "output_rule": "Prioritize precise text rendering, legible hierarchy, and where each text element should appear.",
    },
    "Midjourney": {
        "role": "Midjourney prompt with cinematic aesthetics and model parameters",
        "prompt_style": "dense visual keywords, medium/style descriptors, camera/lens cues, texture, color palette, composition, and parameter suffixes",
        "best_for": "high-impact mood boards, visual hooks, stylized campaign imagery, and scroll-stopping aesthetics",
        "output_rule": "End with Midjourney parameters such as aspect ratio, style, stylize, chaos, no-list, and version when useful.",
    },
}


PERSONA_PLAYBOOKS = {
    "Gen Z Trend Hunter": {
        "taste": "fast, meme-aware, allergic to brand lectures, likes identity signals",
        "pain_points": "fear of missing out, low patience, wants social currency",
        "avoid": "corporate slogans, over-explaining, elder-tone advice",
    },
    "Young Urban Professional": {
        "taste": "efficient, tasteful, practical, slightly witty, values time and ROI",
        "pain_points": "busy schedule, decision fatigue, wants credible shortcuts",
        "avoid": "cheap hype, vague inspiration, hard-sell pressure",
    },
    "Value-Seeking Family Buyer": {
        "taste": "clear benefits, safety, price-performance, real-life proof",
        "pain_points": "budget pressure, trust concerns, wants fewer bad purchases",
        "avoid": "flashy claims, niche slang, unsupported guarantees",
    },
    "Beauty Skincare Explorer": {
        "taste": "routine details, before-after realism, ingredients, honest texture",
        "pain_points": "sensitive skin anxiety, product overload, fear of wasting money",
        "avoid": "miracle claims, over-filtered perfection, fake expert tone",
    },
    "Knowledge Worker": {
        "taste": "sharp frameworks, practical examples, crisp language",
        "pain_points": "information overload, productivity pressure, credibility risk",
        "avoid": "empty thought leadership, buzzword fog, generic AI claims",
    },
    "Local Community Insider": {
        "taste": "neighborhood details, local humor, lived experience, useful tips",
        "pain_points": "wants relevant recommendations, dislikes outsider tone",
        "avoid": "tourist cliches, generic city praise, too-polished copy",
    },
}


CULTURAL_VOICE_PLAYBOOKS = {
    "標準繁中": {
        "voice_rule": "Use natural Traditional Chinese with Taiwan-friendly phrasing.",
        "guardrail": "Avoid stiff PR wording and Mainland-only expressions.",
    },
    "台灣口語": {
        "voice_rule": "Use grounded Taiwanese Mandarin: casual particles, lived-in rhythm, and natural spoken phrasing.",
        "guardrail": "Do not force slang. Keep it readable and brand-safe.",
    },
    "台語風味": {
        "voice_rule": "Use Taiwanese Hokkien flavor through selected words, rhythm, and sentence endings when appropriate.",
        "guardrail": "Respect the language. Avoid caricature, random romanization, or mocking tone.",
    },
    "客語風味": {
        "voice_rule": "Use Hakka cultural warmth, community tone, thrift/practicality cues, and selected Hakka-flavored expressions only when natural.",
        "guardrail": "Do not invent heavy Hakka phrases. Prefer respectful light-touch localization.",
    },
    "晶晶體": {
        "voice_rule": "Use playful code-switching between Traditional Chinese and English with influencer-native rhythm.",
        "guardrail": "Keep clarity. Do not overdo English inserts or make it unreadable.",
    },
}


MATURITY_RUBRIC = {
    "ta_fit": 20,
    "platform_native": 15,
    "hook_strength": 15,
    "product_clarity": 15,
    "human_voice": 15,
    "action_trigger": 10,
    "brand_safety": 10,
}


CAMPAIGN_PACK_SCHEMA = {
    "strategy_snapshot": {
        "platform": "string",
        "persona": "string",
        "cultural_voice": "string",
        "angle": "string",
    },
    "maturity_score": "integer 0-100",
    "readiness_level": "string",
    "hook_candidates": ["5 platform-native hooks"],
    "primary_post": {
        "hook_title": "string",
        "caption_body": "string",
        "cta": "string",
        "hashtags": ["string"],
    },
    "platform_variants": {
        "short_post": "string",
        "long_post": "string",
        "spoken_script": "string",
    },
    "visual_prompts": {
        "mj_prompt": "English Midjourney prompt",
        "nano_banana_prompt": "English image text-rendering prompt",
        "chatgpt_image_prompt": "prompt for ChatGPT Image 2 text-to-image generation",
        "gemini_image_prompt": "prompt for Gemini 3.1 Flash Image / Nano Banana text-to-image generation",
        "midjourney_prompt": "tailored Midjourney prompt with parameters",
    },
    "image_generation_brief": {
        "creative_direction": "visual concept that turns the post copy into an image",
        "social_format": "recommended social image format or aspect ratio",
        "on_image_text": "short text that should appear on the image",
        "brand_safety_notes": "visual claims, legal, medical, beauty, or platform risks to avoid",
    },
    "visual_insights": {
        "image_observation": "what the image shows and what matters for copywriting",
        "story_angle": "best story angle derived from the image",
        "editing_suggestion": "practical visual optimization advice",
    },
    "comment_starters": ["2 reply prompts"],
    "risk_review": ["claims, compliance, or tone risks to check"],
    "rewrite_notes": ["what was improved to reach the target score"],
}


def get_domain_names():
    return list(DOMAIN_PLAYBOOKS.keys())


def get_domain_config(domain):
    return DOMAIN_PLAYBOOKS.get(
        domain,
        {
            "mj": "--ar 1:1",
            "banana": "Standard Text",
            "icon": "❓",
            "kb_file": "",
            "expansion_note": "General fallback domain.",
        },
    )


def build_strategy_profile(
    platform,
    persona,
    cultural_voice,
    groundedness,
    trend_sensitivity,
    brand_safety,
    maturity_target,
    tone_recipe,
):
    return {
        "platform": platform,
        "platform_playbook": PLATFORM_PLAYBOOKS[platform],
        "persona": persona,
        "persona_playbook": PERSONA_PLAYBOOKS[persona],
        "cultural_voice": cultural_voice,
        "cultural_voice_playbook": CULTURAL_VOICE_PLAYBOOKS[cultural_voice],
        "groundedness": groundedness,
        "trend_sensitivity": trend_sensitivity,
        "brand_safety": brand_safety,
        "maturity_target": maturity_target,
        "tone_recipe": tone_recipe,
        "maturity_rubric": MATURITY_RUBRIC,
        "image_engine_playbooks": IMAGE_ENGINE_PLAYBOOKS,
    }


def build_campaign_prompt(
    domain,
    topic,
    count,
    kb_text,
    visual_config,
    strategy_profile,
):
    schema = json.dumps(CAMPAIGN_PACK_SCHEMA, ensure_ascii=False, indent=2)
    profile = json.dumps(strategy_profile, ensure_ascii=False, indent=2)
    return f"""
Role: Mega-Influencer Wavemaker, upgraded from a copy generator into a platform-native, TA-native, trend-aware campaign workflow.

Domain: {domain}
Topic: {topic}
Count: {count}
Knowledge Bank Context:
{kb_text}

Visual Specs:
- Legacy Midjourney defaults: {visual_config['mj']}
- Legacy Nano Banana defaults: {visual_config['banana']}
- Domain expansion note: {visual_config.get('expansion_note', 'General domain.')}

Strategy Profile:
{profile}

Workflow:
1. Diagnose the most persuasive content angle for the selected platform and persona.
2. Generate at least 12 hook ideas internally, score them by the maturity rubric, and keep the best 5.
3. Write copy that feels grounded, current, and human. Use concrete scenes, daily-life language, and specific benefits.
4. Apply the selected cultural voice respectfully. It should feel native to the audience, not like a costume.
5. Remove generic brand language, exaggerated claims, unsupported promises, and obvious AI phrasing.
6. Turn the final copy into an image_generation_brief and 3 text-to-image prompts: ChatGPT Image 2, Gemini 3.1 Flash Image / Nano Banana, and Midjourney.
7. Produce a complete Campaign Pack that is close to publish-ready.
8. If the maturity score is below the target, rewrite internally before final output.

Output:
Return STRICT JSON only. Return a JSON list with exactly {count} Campaign Pack objects.
Each object must follow this schema:
{schema}

Language:
- Use Traditional Chinese as the primary copy language unless the cultural voice requires light code-switching.
- The visual prompt fields should be English unless exact Traditional Chinese on-image text is required.
- Keep platform copy natural and publishable.
"""


def build_vision_campaign_prompt(
    domain,
    image_count,
    strategy_profile,
    user_direction=None,
):
    schema = json.dumps(CAMPAIGN_PACK_SCHEMA, ensure_ascii=False, indent=2)
    profile = json.dumps(strategy_profile, ensure_ascii=False, indent=2)
    direction = user_direction or "Auto-diagnose the strongest angle from the uploaded images."
    return f"""
Role: Social Media Visual Director and Mega-Influencer Wavemaker.
Domain: {domain}
Image count: {image_count}
User direction: {direction}

Strategy Profile:
{profile}

Task:
Analyze the uploaded images, identify the strongest platform-native story angle, and create one publish-ready Campaign Pack per image.
Respect the selected persona, platform, maturity target, and cultural voice. Avoid fake visual claims.
For each image, include visual_insights with concrete image observations, the strongest story angle, and visual optimization advice.
Also convert the post into image_generation_brief and 3 text-to-image prompts: ChatGPT Image 2, Gemini 3.1 Flash Image / Nano Banana, and Midjourney.

Return STRICT JSON only. Return a JSON list with exactly {image_count} Campaign Pack objects.
Each object must follow this schema:
{schema}
"""


def parse_json_response(text):
    cleaned = text.strip().replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        match = re.search(r"(\[.*\]|\{.*\})", cleaned, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(1))
