# ArtifyX - CLI tool that turns text prompts into AI-generated art
# Original concept by MrHacker-X - https://github.com/MrHacker-X/ArtifyX
# Premium color edition: fresh violet-gold theme on the rich console,
# original core/bnr banner kept exactly as-is.

import base64
import os
import sys
import datetime
import logging

from rich.console import Console
from openai import OpenAI

from config import API_KEY, MODEL, NUM_IMAGES, IMAGE_SIZE, OUTPUT_DIR

logging.basicConfig(level=logging.INFO)
logging.getLogger("openai").setLevel(logging.WARNING)

console = Console(highlight=False)

# ── Premium theme ────────────────────────────────────────────────
# Deep violet + warm gold on soft white - a brand-new, premium look.
ACCENT = "#7C4DFF"   # violet - headings, actions, the tool's identity
GOLD   = "#FFC94A"   # gold   - success, progress, warm emphasis
TEXT   = "grey93"    # nearly-white body text
DIM    = "grey54"    # muted secondary text
ERROR  = "#FF5370"   # soft red for failures
WARN   = "#FFB86C"   # warm amber for hints

_client: OpenAI = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=API_KEY)
    return _client


def banner() -> None:
    """Original ArtifyX banner (core/bnr) - unchanged from v1.x."""
    print()
    os.system("cat core/bnr")
    print()
    console.print(
        f"  [{DIM}]◇[/] [bold][{ACCENT}]transform[/][/] [{DIM}]text · [/]"
        f"[white]model[/white] [{GOLD}]{MODEL}[/] [{DIM}]·[/] "
        f"[white]size[/white] [{GOLD}]{IMAGE_SIZE}[/] [{DIM}]·[/] "
        f"[white]images[/white] [{GOLD}]{NUM_IMAGES}[/]",
        highlight=False,
    )
    console.print(
        f"  [{DIM}]◇[/] [{DIM}]saving to[/] [{ACCENT}]{OUTPUT_DIR}[/]",
        highlight=False,
    )
    console.print(f"[{ACCENT}]┄{'┄' * 60}[/]", style="dim")
    print()


def check_client() -> bool:
    """True if OpenAI credentials look present, False otherwise."""
    if not API_KEY:
        console.print(
            f"  [{ERROR}]◆ no API key[/] [{DIM}]— set API_KEY in config.py "
            f"or export OPENAI_API_KEY[/]",
            highlight=False,
        )
        return False
    return True


def generate_images(prompt: str):
    """Ask the OpenAI images API for NUM_IMAGES images (b64 encoded)."""
    response = get_client().images.generate(
        model=MODEL,
        prompt=prompt,
        n=NUM_IMAGES,
        size=IMAGE_SIZE,
        response_format="b64_json",
    )
    if not response.data:
        raise ValueError("OpenAI returned no images for that prompt.")
    return [d.b64_json for d in response.data]


def save_images(b64_list, folder_path: str):
    """Decode and save each generated image, print the saved filename."""
    os.makedirs(folder_path, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    saved = []
    for i, b64 in enumerate(b64_list, start=1):
        file_name = f"{timestamp}_{i:02d}.png"
        path = os.path.join(folder_path, file_name)
        with open(path, "wb") as f:
            f.write(base64.b64decode(b64))
        pad = str(i).rjust(len(str(len(b64_list))))
        console.print(
            f"  [{GOLD}]◆[/] [{DIM}]image {pad}/{len(b64_list)}[/]  "
            f"[{TEXT}]{file_name}[/]",
            highlight=False,
        )
        saved.append(path)
    return saved


def good_bye() -> None:
    print()
    console.rule(style=DIM)
    console.print(
        f"  [{GOLD}]◆[/] [{TEXT}]thanks for using "
        f"[bold][{ACCENT}]ArtifyX[/][/]",
        highlight=False,
    )
    console.print(
        f"  [{DIM}]YouTube[/] [{ACCENT}]youtube.com/@Technolex[/]   "
        f"[{DIM}]Telegram[/] [{ACCENT}]t.me/LinkCentralX[/]   "
        f"[{DIM}]GitHub[/] [{ACCENT}]MrHacker-X[/]",
        highlight=False,
    )
    console.print()
    print()


def main() -> None:
    while True:
        try:
            prompt = console.input(
                f"[{GOLD}]◆[/] [bold][{ACCENT}]Image Detail[/][/] [{DIM}]›[/] "
            ).strip()
        except (EOFError, KeyboardInterrupt):
            good_bye()
            sys.exit(0)
        if not prompt:
            console.print(
                f"  [{WARN}]◇[/] [{TEXT}]enter a description, or type "
                f"[bold]exit[/bold] / [bold]bye[/bold][{DIM}] to quit[/]",
                highlight=False,
            )
            continue
        if prompt.lower() in ("exit", "bye"):
            good_bye()
            sys.exit(0)
        break

    console.print(
        f"\n  [{ACCENT}]◇[/] [{TEXT}]creating [bold][{GOLD}]{NUM_IMAGES}[/][/] "
        f"piece{'s' if NUM_IMAGES > 1 else ''} from your words…[/]",
        highlight=False,
    )
    print()

    try:
        with console.status(
            f"[{ACCENT}]generating art…[/]",
            spinner="dots12",
            spinner_style=GOLD,
        ):
            b64_list = generate_images(prompt)
    except Exception as e:
        console.print(
            f"\n  [{ERROR}]◆[/] [{ERROR}]failed to generate[/] "
            f"[{DIM}]— {e}[/]",
            highlight=False,
        )
        console.print(
            f"  [{WARN}]◇[/] [{DIM}]check your API key, prompt content, "
            f"and model/size settings in config.py[/]",
            highlight=False,
        )
        print()
        return

    save_images(b64_list, OUTPUT_DIR)
    console.print(
        f"\n  [{GOLD}]◆ done[/] [{DIM}]—[/] [{TEXT}]{len(b64_list)} "
        f"image(s) in [/][{ACCENT}]{OUTPUT_DIR}[/]",
        highlight=False,
    )
    print()


if __name__ == "__main__":
    from core.remote_control import RemoteControl

    with RemoteControl(tool_id="artifyx"):
        try:
            if not check_client():
                sys.exit(1)
            banner()
            while True:
                main()
                console.rule(style=ACCENT, align="center")
        except KeyboardInterrupt:
            good_bye()
            sys.exit(0)
