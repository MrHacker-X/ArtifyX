"""
ArtifyX configuration.

Every setting can also be supplied as an environment variable -
the environment (or shell export) always takes precedence over
whatever is written in this file.
"""

import os

# ---------------------------------------------------------------
# Required credentials
# ---------------------------------------------------------------

# Your OpenAI API key - https://platform.openai.com/api-keys
# or: export OPENAI_API_KEY="sk-..."
API_KEY = os.environ.get("OPENAI_API_KEY", "test-to-launch-tool")

# ---------------------------------------------------------------
# Optional behavior
# ---------------------------------------------------------------

# Image model: "dall-e-2" (n up to 10, cheap) or "dall-e-3" (1 image, richer)
# or: export ARTIFYX_MODEL="dall-e-2"
MODEL = os.environ.get("ARTIFYX_MODEL", "dall-e-2")

# Number of images generated per prompt (dall-e-2 supports 1-10; dall-e-3 is fixed at 1)
# or: export ARTIFYX_NUM_IMAGES="5"
NUM_IMAGES = int(os.environ.get("ARTIFYX_NUM_IMAGES", "5"))

# Image size - allowed values per model:
#   dall-e-2: 256x256, 512x512, 1024x1024
#   dall-e-3: 1024x1024, 1024x1792, 1792x1024
# or: export ARTIFYX_SIZE="512x512"
IMAGE_SIZE = os.environ.get("ARTIFYX_SIZE", "512x512")

# Where generated images are saved
# or: export ARTIFYX_OUTPUT_DIR="/sdcard/ArtifyX"
def _default_output_dir() -> str:
    if os.path.isdir("/sdcard"):          # Termux / Android
        return "/sdcard/ArtifyX"
    return os.path.join(os.path.expanduser("~"), "ArtifyX")

OUTPUT_DIR = os.environ.get("ARTIFYX_OUTPUT_DIR", _default_output_dir())

# ---------------------------------------------------------------
# Validation - fail fast with a clear message, not a stack trace
# ---------------------------------------------------------------

if not API_KEY:
    raise SystemExit(
        "OpenAI API key not configured.\n"
        "  Set API_KEY in config.py, or export OPENAI_API_KEY in your shell."
    )

_VALID_SIZES = {
    "dall-e-2": ("256x256", "512x512", "1024x1024"),
    "dall-e-3": ("1024x1024", "1024x1792", "1792x1024"),
}

if MODEL not in _VALID_SIZES:
    raise SystemExit(f"Unsupported model '{MODEL}'. Use 'dall-e-2' or 'dall-e-3'.")

if IMAGE_SIZE not in _VALID_SIZES[MODEL]:
    raise SystemExit(
        f"Size '{IMAGE_SIZE}' is not valid for {MODEL}.\n"
        f"  Allowed: {', '.join(_VALID_SIZES[MODEL])}"
    )

if MODEL == "dall-e-3" and NUM_IMAGES != 1:
    NUM_IMAGES = 1  # dall-e-3 only supports one image per request

if not (1 <= NUM_IMAGES <= 10):
    raise SystemExit("NUM_IMAGES must be between 1 and 10.")
