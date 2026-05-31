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


VISUAL_STRATEGY_MODES = {
    "AI 自動推薦": "AI chooses the most suitable visual style, layout, and format from the copy, platform, persona, and domain.",
    "使用者指定": "Strictly follow the user-selected visual style, layout, and format.",
    "AI 推薦後可修改": "AI recommends visual direction first, but user selections and custom instructions override the recommendation.",
}


VISUAL_STYLE_PLAYBOOKS = {
    "寫實攝影": "realistic photography, natural lighting, believable scene, high social trust",
    "日系生活感": "Japanese lifestyle mood, airy composition, warm everyday detail, subtle colors",
    "韓系清透感": "Korean clean aesthetic, soft light, translucent freshness, polished minimal styling",
    "小紅書種草風": "Xiaohongshu recommendation aesthetic, useful visual proof, trendy consumer texture",
    "Threads 極簡梗圖風": "minimal meme-like social graphic, concise text, high shareability",
    "高級品牌廣告風": "premium brand campaign, refined composition, confident negative space, luxury lighting",
    "資訊圖卡風": "infographic card, clear hierarchy, scannable data, useful visual structure",
    "電商產品主視覺": "e-commerce hero visual, product-centered, benefit callouts, conversion-focused",
    "社群迷因風": "meme-forward social visual, punchy framing, relatable humor, fast comprehension",
    "雜誌封面風": "magazine cover composition, editorial headline, strong focal subject, polished art direction",
    "3D / CG 渲染": "3D CG render, dimensional lighting, clean materials, polished digital craft",
    "插畫風": "illustrated social visual, expressive forms, friendly storytelling",
    "手繪風": "hand-drawn texture, human warmth, sketch-like charm, approachable details",
    "Q版/chili人像": "cute stylized chibi portrait, playful proportions, character-led emotional appeal",
    "3D盲盒公仔": "3D collectible blind-box figurine style, toy-like material, display-box presentation",
    "paper cutout 立體剪紙藝術": "layered paper cutout art, tactile shadows, dimensional craft, paper texture",
    "黑板粉筆板書": "blackboard chalk note style, hand-lettered marks, educational warmth, chalk texture",
    "claymorphism軟萌黏土": "soft claymorphism, rounded tactile shapes, pastel material, cute handmade feel",
    "多彩曼非斯": "colorful Memphis design, geometric forms, playful pattern, energetic composition",
    "自訂": "Use the user's custom visual style instruction.",
}


LAYOUT_PLAYBOOKS = {
    "單一主視覺 + 短標": "one hero image with a short headline and minimal supporting text",
    "大標題置中": "centered bold headline with strong visual balance",
    "左圖右文": "image on the left, text block on the right, clear split composition",
    "上圖下文": "image-led top area with supporting copy below",
    "產品置中 + 賣點環繞": "centered product with benefit callouts surrounding it",
    "Before / After": "before-after comparison layout with clear contrast",
    "三點式重點卡": "three key points in a structured card layout",
    "九宮格懶人包": "nine-grid explainer or recommendation layout",
    "封面標題 + 小副標": "cover-style headline with compact subheadline",
    "Quote 卡片": "quote-led layout with strong typography and minimal decoration",
    "留白高級感": "premium whitespace composition with restrained text placement",
    "自訂": "Use the user's custom layout instruction.",
}


IMAGE_FORMAT_PLAYBOOKS = {
    "1:1 IG / Threads": {"aspect_ratio": "1:1", "openai_size": "1024x1024", "usage": "square feed posts and general social sharing"},
    "4:5 IG Feed": {"aspect_ratio": "4:5", "openai_size": "1024x1536", "usage": "Instagram feed and portrait social cards"},
    "9:16 Reels / TikTok / Shorts": {"aspect_ratio": "9:16", "openai_size": "1024x1536", "usage": "vertical short video covers and story format"},
    "16:9 YouTube / Blog": {"aspect_ratio": "16:9", "openai_size": "1536x1024", "usage": "YouTube thumbnails, blog headers, and landscape banners"},
    "3:2 LinkedIn / Presentation": {"aspect_ratio": "3:2", "openai_size": "1536x1024", "usage": "LinkedIn posts, presentation visuals, and business content"},
    "自訂": {"aspect_ratio": "custom", "openai_size": "1024x1024", "usage": "Use the user's custom format instruction."},
}


DEFAULT_IMAGE_FORMAT_BY_PLATFORM = {
    "Threads": "1:1 IG / Threads",
    "Instagram Reels": "9:16 Reels / TikTok / Shorts",
    "Instagram Feed": "4:5 IG Feed",
    "TikTok": "9:16 Reels / TikTok / Shorts",
    "Dcard": "1:1 IG / Threads",
    "Xiaohongshu": "4:5 IG Feed",
    "Facebook": "1:1 IG / Threads",
    "LinkedIn": "3:2 LinkedIn / Presentation",
}


def recommend_image_format_for_platform(platform):
    return DEFAULT_IMAGE_FORMAT_BY_PLATFORM.get(platform, "1:1 IG / Threads")


STYLE_RECOMMENDATION_WEIGHTS = {
    "platform": {
        "Threads": {"Threads 極簡梗圖風": 6, "社群迷因風": 3, "資訊圖卡風": 1},
        "Instagram Reels": {"寫實攝影": 4, "韓系清透感": 2, "社群迷因風": 2},
        "Instagram Feed": {"高級品牌廣告風": 4, "小紅書種草風": 3, "雜誌封面風": 2},
        "TikTok": {"社群迷因風": 5, "寫實攝影": 3, "3D / CG 渲染": 1},
        "Dcard": {"日系生活感": 4, "寫實攝影": 3, "資訊圖卡風": 1},
        "Xiaohongshu": {"小紅書種草風": 6, "韓系清透感": 3, "電商產品主視覺": 1},
        "Facebook": {"寫實攝影": 4, "資訊圖卡風": 2, "日系生活感": 1},
        "LinkedIn": {"資訊圖卡風": 5, "高級品牌廣告風": 3, "3D / CG 渲染": 1},
    },
    "domain": {
        "Food & Cooking": {"寫實攝影": 4, "日系生活感": 2, "雜誌封面風": 1},
        "Travel & Lifestyle": {"日系生活感": 4, "寫實攝影": 3, "雜誌封面風": 2},
        "AI Workplace": {"3D / CG 渲染": 4, "資訊圖卡風": 3, "高級品牌廣告風": 1},
        "Corporate Strategy": {"高級品牌廣告風": 4, "資訊圖卡風": 3, "3D / CG 渲染": 1},
        "Labor Law": {"資訊圖卡風": 4, "黑板粉筆板書": 3, "高級品牌廣告風": 1},
        "Health & Wellness": {"日系生活感": 3, "寫實攝影": 3, "資訊圖卡風": 2},
        "Beauty & Skincare": {"韓系清透感": 5, "小紅書種草風": 3, "電商產品主視覺": 2},
    },
    "persona": {
        "Gen Z Trend Hunter": {"社群迷因風": 4, "3D盲盒公仔": 2, "claymorphism軟萌黏土": 1},
        "Young Urban Professional": {"高級品牌廣告風": 3, "韓系清透感": 2, "資訊圖卡風": 1},
        "Value-Seeking Family Buyer": {"寫實攝影": 3, "資訊圖卡風": 2, "日系生活感": 1},
        "Beauty Skincare Explorer": {"韓系清透感": 4, "小紅書種草風": 3, "電商產品主視覺": 1},
        "Knowledge Worker": {"資訊圖卡風": 4, "黑板粉筆板書": 2, "Threads 極簡梗圖風": 1},
        "Local Community Insider": {"日系生活感": 3, "寫實攝影": 3, "社群迷因風": 1},
    },
    "cultural_voice": {
        "台灣口語": {"社群迷因風": 2, "Threads 極簡梗圖風": 1},
        "台語風味": {"手繪風": 2, "日系生活感": 1},
        "客語風味": {"手繪風": 2, "日系生活感": 1},
        "晶晶體": {"小紅書種草風": 2, "多彩曼非斯": 1},
    },
}


LAYOUT_RECOMMENDATION_WEIGHTS = {
    "platform": {
        "Threads": {"Quote 卡片": 5, "大標題置中": 3, "單一主視覺 + 短標": 1},
        "Instagram Reels": {"封面標題 + 小副標": 5, "Before / After": 3, "單一主視覺 + 短標": 1},
        "Instagram Feed": {"產品置中 + 賣點環繞": 4, "封面標題 + 小副標": 3, "留白高級感": 2},
        "TikTok": {"大標題置中": 4, "Before / After": 3, "單一主視覺 + 短標": 2},
        "Dcard": {"三點式重點卡": 4, "上圖下文": 3, "Before / After": 2},
        "Xiaohongshu": {"九宮格懶人包": 7, "三點式重點卡": 3, "上圖下文": 1},
        "Facebook": {"上圖下文": 4, "三點式重點卡": 2, "左圖右文": 1},
        "LinkedIn": {"左圖右文": 4, "三點式重點卡": 3, "留白高級感": 2},
    },
    "domain": {
        "Food & Cooking": {"上圖下文": 3, "單一主視覺 + 短標": 2, "三點式重點卡": 1},
        "Travel & Lifestyle": {"單一主視覺 + 短標": 4, "封面標題 + 小副標": 2, "上圖下文": 1},
        "AI Workplace": {"左圖右文": 3, "三點式重點卡": 3, "大標題置中": 1},
        "Corporate Strategy": {"左圖右文": 4, "留白高級感": 3, "三點式重點卡": 2},
        "Labor Law": {"三點式重點卡": 4, "左圖右文": 2, "Quote 卡片": 1},
        "Health & Wellness": {"Before / After": 3, "三點式重點卡": 3, "上圖下文": 1},
        "Beauty & Skincare": {"產品置中 + 賣點環繞": 4, "Before / After": 3, "留白高級感": 1},
    },
    "persona": {
        "Gen Z Trend Hunter": {"大標題置中": 3, "Quote 卡片": 2, "Before / After": 1},
        "Young Urban Professional": {"留白高級感": 3, "左圖右文": 2, "三點式重點卡": 1},
        "Value-Seeking Family Buyer": {"Before / After": 3, "三點式重點卡": 2, "產品置中 + 賣點環繞": 1},
        "Beauty Skincare Explorer": {"Before / After": 4, "產品置中 + 賣點環繞": 3, "九宮格懶人包": 1},
        "Knowledge Worker": {"三點式重點卡": 4, "左圖右文": 2, "Quote 卡片": 1},
        "Local Community Insider": {"上圖下文": 3, "單一主視覺 + 短標": 2, "九宮格懶人包": 1},
    },
    "cultural_voice": {
        "晶晶體": {"大標題置中": 2, "Quote 卡片": 1},
        "台灣口語": {"Quote 卡片": 2, "單一主視覺 + 短標": 1},
        "台語風味": {"上圖下文": 2, "Quote 卡片": 1},
        "客語風味": {"三點式重點卡": 2, "上圖下文": 1},
    },
}


def _score_visual_options(valid_options, weight_groups, context):
    scores = {option: 0 for option in valid_options if option != "自訂"}
    for group_name, group_weights in weight_groups.items():
        for option, points in group_weights.get(context.get(group_name), {}).items():
            if option in scores:
                scores[option] += points
    return scores


def _highest_scored_option(scores, fallback):
    if not scores:
        return fallback
    return max(scores, key=lambda option: (scores[option], -list(scores).index(option)))


def recommend_visual_style_and_layout(platform, persona, cultural_voice, domain):
    context = {
        "platform": platform,
        "persona": persona,
        "cultural_voice": cultural_voice,
        "domain": domain,
    }
    style_scores = _score_visual_options(VISUAL_STYLE_PLAYBOOKS.keys(), STYLE_RECOMMENDATION_WEIGHTS, context)
    layout_scores = _score_visual_options(LAYOUT_PLAYBOOKS.keys(), LAYOUT_RECOMMENDATION_WEIGHTS, context)
    return {
        "visual_style": _highest_scored_option(style_scores, "寫實攝影"),
        "layout_structure": _highest_scored_option(layout_scores, "單一主視覺 + 短標"),
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
        "visual_strategy_mode": "AI 自動推薦 / 使用者指定 / AI 推薦後可修改",
        "visual_style": "selected or AI-recommended visual style",
        "layout_structure": "selected or AI-recommended layout structure",
        "social_format": "recommended social image format or aspect ratio",
        "custom_visual_notes": "user custom visual style/layout/format instructions when provided",
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
    visual_strategy_mode="AI 自動推薦",
    visual_style="自訂",
    layout_structure="自訂",
    image_format="自訂",
    custom_visual_style="",
    custom_layout="",
    custom_image_format="",
):
    visual_style_playbook = VISUAL_STYLE_PLAYBOOKS.get(visual_style, VISUAL_STYLE_PLAYBOOKS["自訂"])
    layout_playbook = LAYOUT_PLAYBOOKS.get(layout_structure, LAYOUT_PLAYBOOKS["自訂"])
    format_playbook = IMAGE_FORMAT_PLAYBOOKS.get(image_format, IMAGE_FORMAT_PLAYBOOKS["自訂"])
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
        "visual_strategy": {
            "mode": visual_strategy_mode,
            "mode_rule": VISUAL_STRATEGY_MODES[visual_strategy_mode],
            "style": visual_style,
            "style_rule": visual_style_playbook,
            "layout": layout_structure,
            "layout_rule": layout_playbook,
            "format": image_format,
            "format_rule": format_playbook,
            "custom_visual_style": custom_visual_style.strip(),
            "custom_layout": custom_layout.strip(),
            "custom_image_format": custom_image_format.strip(),
        },
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
6. Apply the visual_strategy exactly:
   - If mode is AI 自動推薦, recommend the best visual style, layout, and format from the playbooks.
   - If mode is 使用者指定, strictly follow the selected style, layout, format, and custom notes.
   - If mode is AI 推薦後可修改, explain the recommendation in image_generation_brief but honor selected/custom overrides.
7. Turn the final copy into an image_generation_brief and 3 text-to-image prompts: ChatGPT Image 2, Gemini 3.1 Flash Image / Nano Banana, and Midjourney.
8. Each visual prompt must explicitly include visual style, layout structure, image format/aspect ratio, on-image text placement, and text safety.
9. Produce a complete Campaign Pack that is close to publish-ready.
10. If the maturity score is below the target, rewrite internally before final output.

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
Apply the visual_strategy in the Strategy Profile when choosing visual style, layout, image format, and on-image text placement.
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
