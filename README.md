<div align="center">

# ⃤ A R T I F Y X ⃤

### *Type words, get art - five AI-generated images from one prompt, right in your terminal.*

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/AI-OpenAI%20Images-412991?style=flat-square&logo=openai&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Linux%20%7C%20macOS-38;5;150?style=flat-square)
![Images](https://img.shields.io/badge/Prompts%20to%205%20images-38;5;245?style=flat-square)
![Stars](https://img.shields.io/github/stars/MrHacker-X/ArtifyX?style=flat-square&color=orange)
![Forks](https://img.shields.io/github/forks/MrHacker-X/ArtifyX?style=flat-square&color=cyan)

</div>

---

## 📋 Table of Contents

- [🎯 Why ArtifyX?](#-why-artifyx)
- [🧭 What It Does](#-what-it-does)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [✨ Features](#-features)
- [⌨️ Usage](#%EF%B8%8F-usage)
- [⚙️ Configuration](#%EF%B8%8F-configuration)
- [🧰 Tech Stack](#-tech-stack)
- [⚠️ Disclaimer](#%EF%B8%8F-disclaimer)
- [🤝 Contributing](#-contributing)
- [📜 License](#-license)
- [👨‍💻 Developer](#-developer)

---

## 🎯 Why ArtifyX?

> Text-to-image tools either want you to click through a web app or run a heavyweight framework. **ArtifyX is one prompt loop in your terminal**: describe what you want, and five images land in your phone's storage.
>
> **v2.0 modernizes the engine.** The original was wired to the legacy OpenAI SDK and a hand-rolled HTTP call that broke when the images API moved. Everything is now upgraded: OpenAI SDK v1+, DALL·E model choice, live config validation, and an output path that works outside Termux instead of assuming `/sdcard`. Setup now supports every major Linux family - not just Termux - and verifies each dependency before claiming success.

---

## 🧭 What It Does

| # | Step | What happens |
|---|------|-------------|
| 1️⃣ | **Prompt** | You type an image description in the terminal |
| 2️⃣ | **Generate** | ArtifyX calls the OpenAI images API (`dall-e-2` / `dall-e-3`) |
| 3️⃣ | **Save** | Up to 10 images are decoded and saved as timestamped PNG files |

**What this tool is NOT:** it is **not** a batch-generation farm, and **not** a way around OpenAI's usage policies or content rules - prompts that violate them will be refused by the API.

---

## 🚀 Quick Start

```bash
git clone https://github.com/MrHacker-X/ArtifyX.git
cd ArtifyX
./setup.sh                     # installs deps (Termux / apt / dnf / pacman / apk)
nano config.py                 # or: export OPENAI_API_KEY="sk-..."
python3 artifyx.py               # prompt loop starts
```

<details>
<summary><b>🔑 Where do I get an API key?</b></summary>

Create one at [platform.openai.com/api-keys](https://platform.openai.com/api-keys) - every generated image is billed to that key, so keep it private.

</details>

---

## 📦 Installation

### Termux (Android)

```bash
apt update -y && apt install git -y
git clone https://github.com/MrHacker-X/ArtifyX.git
cd ArtifyX
chmod +x setup.sh
./setup.sh
```

### Desktop Linux / macOS

```bash
git clone https://github.com/MrHacker-X/ArtifyX.git
cd ArtifyX
./setup.sh          # or: pip install -r requirements.txt
```

### Supported Systems

| OS | Status | Notes |
|----|--------|-------|
| 📱 Termux (Android) | ✅ Fully supported | Auto-detected; storage permission requested |
| 🐧 Debian / Ubuntu / Kali | ✅ Fully supported | `apt` detected automatically |
| 🐧 Fedora / RHEL | ✅ Fully supported | `dnf` detected automatically |
| 🐧 Arch / Manjaro | ✅ Fully supported | `pacman` detected automatically |
| 🐧 Alpine | ✅ Fully supported | `apk` detected automatically |
| 🍎 macOS | ✅ Fully supported | pip-only path, needs Python preinstalled |

> 💡 The setup script **verifies every dependency** at the end and tells you exactly what's missing - it will never print "installed successfully" when it isn't.

---

## ✨ Features

| | Feature | Description |
|---|---------|-------------|
| 🎨 | **Model choice** | `dall-e-2` (cheap, up to 10 images) or `dall-e-3` (richer, single image) |
| ✨ | **Premium color theme** | Custom violet-gold terminal palette with elegant glyphs and a live generation spinner — auto-degrades from truecolor to 256 to basic colors on older terminals |
| 🖼️ | **Prompt → 5 images** | One prompt, multiple PNGs per run (count configurable 1-10) |
| 🛡️ | **Per-loop error containment** | A failed API call reports and returns to the prompt - the tool never crashes out |
| 🧪 | **Model/size validation** | Invalid `MODEL`/`IMAGE_SIZE` combos fail at startup with the allowed values listed |
| 📱 | **Portable output** | Saves to `/sdcard/ArtifyX` on Termux, `~/ArtifyX` on desktop, fully overridable |
| 🔑 | **Fail-fast auth** | Missing API key → one clear line at startup, no stack trace |
| 🧰 | **Cross-platform setup** | One script detects Termux + 4 Linux package managers, handles PEP 668, verifies imports |
| 🪶 | **Minimal dependencies** | 2 packages: `openai`, `rich` |

<details>
<summary><b>🔄 What changed from the original v1.x?</b></summary>

| v1.x (old) | v2.0 (now) |
|------------|------------|
| Legacy openai 0.28 + hand-rolled `requests` POST | **openai SDK v1+** images API |
| Silent HTTP errors, `raise ValueError` on any bad status | Real error messages with cause + fix hint |
| Hard-coded `/sdcard/ArtifyX` (broke on desktop Linux) | Portable: `/sdcard/ArtifyX` on Termux, `~/ArtifyX` elsewhere, env-overridable |
| Unused `text-davinci-003` variable | DALL·E model choice via config | 
| `setup.sh` only worked in Termux | Works on Termux + apt/dnf/pacman/apk + pip-only platforms |
| `pip install datetime` (a package that doesn't exist the way you'd think) | Removed - `datetime` is stdlib |
| No requirements.txt | Added: `openai~=1.0`, `rich` |
| 5 separate API calls per prompt | One call with `n=5`, images decoded from base64 |
| Missing key → crash mid-run | Fail-fast validation at startup |

</details>

---

## ⌨️ Usage

Run the tool, type a prompt, get art:

```bash
python3 artifyx.py
```

| Input | Result |
|-------|--------|
| any text | e.g. `a fox astronaut painting a mountain sunrise` → five PNG images saved |
| `exit` or `bye` | Exits cleanly with a summary |
| empty input | Re-prompts - nothing wasted |
| a failed prompt | Error message, loop continues on the next prompt |

Images are saved as `{timestamp}_{NN}.png` so simultaneous generations never overwrite each other.

---

## ⚙️ Configuration

Everything lives in [`config.py`](config.py) - and every setting can be overridden from the shell:

| Setting | Env var | Default | Description |
|---------|---------|---------|-------------|
| API key | `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| Model | `ARTIFYX_MODEL` | `dall-e-2` | `dall-e-2` or `dall-e-3` |
| Images per prompt | `ARTIFYX_NUM_IMAGES` | `5` | 1-10 on dall-e-2; fixed at 1 on dall-e-3 |
| Image size | `ARTIFYX_SIZE` | `512x512` | See allowed sizes per model in config.py |
| Output folder | `ARTIFYX_OUTPUT_DIR` | auto | `/sdcard/ArtifyX` on Termux, `~/ArtifyX` on desktop |

```bash
# either edit config.py, or:
export OPENAI_API_KEY="sk-..."
export ARTIFYX_MODEL="dall-e-3"
export ARTIFYX_SIZE="1024x1024"
```

---

## 🧰 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.8+ |
| AI | `openai` SDK v1+ — Images API (`b64_json` responses) |
| Terminal UI | `rich` — custom violet/gold theme (truecolor, graceful degradation) |
| Setup | POSIX bash with 5 environment detections |

---

## ⚠️ Disclaimer

> ### Read this before using ArtifyX.
>
> 1. **You pay per image.** Every generation is billed to your OpenAI key. Five images per prompt add up quickly - keep the count sensible and your key private.
> 2. **OpenAI's policies apply.** Your prompts must comply with OpenAI's [usage policies](https://openai.com/policies) and content policy - the API refuses violating prompts, and you are responsible for what you send.
> 3. **Personal use.** ArtifyX is a personal creative tool, not a bulk-generation service.
> 4. **No warranty.** Provided "as is", with no warranty of any kind. The author is **not liable** for any misuse, cost, or damage resulting from its use.

---

## 🤝 Contributing

Contributions are welcome!

```bash
# 1. fork it
# 2. create your branch
git checkout -b feature/amazing-feature
# 3. commit
git commit -m "Add amazing feature"
# 4. push
git push origin feature/amazing-feature
# 5. open a Pull Request
```

Ideas worth exploring: style presets (`--style cyberpunk`), a `--one-shot` CLI flag for scripts, transparent-webp output pairs, an optional prompt-enhancer before the image call.

---

## 📜 License

ArtifyX is the original project by MrHacker-X - see the [`LICENSE`](https://github.com/MrHacker-X/ArtifyX) file in the upstream repository for details.

---

## 👨‍💻 Developer

| | |
|---|---|
| **Dev** | MrHacker-X |
| **GitHub** | [github.com/MrHacker-X](https://github.com/MrHacker-X) |
| **Email** | [contact@vritrasec.com](mailto:contact@vritrasec.com) |
| **Website** | [vritrasec.com](https://vritrasec.com) |
| **Network** | [link.vritrasec.com](https://link.vritrasec.com) |

---

<div align="center">

### ⭐ Star the repo if ArtifyX colored your ideas ⭐

*Built by MrHacker-X - create art, credit artists.*

</div>
