import pytest

from image_generation import (
    GEMINI_IMAGE_MODEL,
    IMAGE_BACKENDS,
    OPENAI_IMAGE_MODEL,
    extension_for_mime_type,
    generate_gemini_image,
    generate_openai_image,
)


def test_default_backend_is_zero_cost_prompt_only():
    assert list(IMAGE_BACKENDS.keys())[0] == "Prompt only (0 cost)"
    assert IMAGE_BACKENDS["Prompt only (0 cost)"]["cost_mode"] == "0 cost"


def test_image_model_constants_are_current_targets():
    assert GEMINI_IMAGE_MODEL == "gemini-3.1-flash-image"
    assert OPENAI_IMAGE_MODEL == "gpt-image-2"


def test_extension_for_mime_type():
    assert extension_for_mime_type("image/png") == "png"
    assert extension_for_mime_type("image/jpeg") == "jpg"
    assert extension_for_mime_type("image/webp") == "webp"
    assert extension_for_mime_type("application/octet-stream") == "png"


def test_generation_requires_keys_before_importing_sdks():
    with pytest.raises(ValueError):
        generate_gemini_image("", "prompt")

    with pytest.raises(ValueError):
        generate_openai_image("", "prompt")
