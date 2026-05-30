import base64
import io


IMAGE_BACKENDS = {
    "Prompt only (0 cost)": {
        "cost_mode": "0 cost",
        "description": "No API call. Copy prompts into ChatGPT, Gemini, or Midjourney manually.",
    },
    "Gemini Image (low cost)": {
        "cost_mode": "low cost",
        "description": "Generate one image on demand with Gemini / Nano Banana.",
    },
    "OpenAI Image (low cost)": {
        "cost_mode": "low cost",
        "description": "Generate one image on demand with OpenAI gpt-image-2.",
    },
}


GEMINI_IMAGE_MODEL = "gemini-3.1-flash-image"
OPENAI_IMAGE_MODEL = "gpt-image-2"


def generate_openai_image(api_key, prompt, size="1024x1024", quality="low"):
    if not api_key:
        raise ValueError("OpenAI API Key is required for OpenAI image generation.")

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    result = client.images.generate(
        model=OPENAI_IMAGE_MODEL,
        prompt=prompt,
        size=size,
        quality=quality,
    )
    image_b64 = result.data[0].b64_json
    return base64.b64decode(image_b64), "image/png"


def generate_gemini_image(api_key, prompt, aspect_ratio="1:1", image_size="1K"):
    if not api_key:
        raise ValueError("Gemini API Key is required for Gemini image generation.")

    from google import genai as google_genai
    from google.genai import types

    client = google_genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=GEMINI_IMAGE_MODEL,
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspect_ratio=aspect_ratio,
                image_size=image_size,
            ),
        ),
    )

    for part in getattr(response, "parts", []) or []:
        if hasattr(part, "as_image"):
            image = part.as_image()
            if image:
                buffer = io.BytesIO()
                image.save(buffer, format="PNG")
                return buffer.getvalue(), "image/png"
        inline_data = getattr(part, "inline_data", None)
        if inline_data and inline_data.data:
            mime_type = inline_data.mime_type or "image/png"
            return inline_data.data, mime_type

    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            inline_data = getattr(part, "inline_data", None)
            if inline_data and inline_data.data:
                mime_type = inline_data.mime_type or "image/png"
                return inline_data.data, mime_type

    raise RuntimeError("Gemini did not return image bytes.")


def extension_for_mime_type(mime_type):
    return {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/webp": "webp",
    }.get(mime_type, "png")
