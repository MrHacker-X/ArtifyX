#!/bin/bash
# ArtifyX setup - detects Termux automatically, works on any Linux/macOS box
# Original by MrHacker-X - modernized setup with dependency verification.

clear

# Banner (if present, else skip quietly)
if [ -f "core/bnr" ]; then
    cat core/bnr
fi

echo
echo -e "\033[1;31m[+] \033[1;32mDetecting your environment...\033[0m"

if [ -d "/data/data/com.termux/files" ]; then
    echo -e "\033[1;31m[+] \033[1;32mTermux detected - installing dependencies...\033[0m"
    echo
    termux-setup-storage
    apt update -y
    apt install python -y
    apt install python-pip -y
    PKG="pkg"
    PIP_FLAGS="--break-system-packages"
elif command -v apt >/dev/null 2>&1; then
    echo -e "\033[1;31m[+] \033[1;32mDebian/Ubuntu-family Linux detected.\033[0m"
    PKG="apt"
    PIP_FLAGS=""
elif command -v dnf >/dev/null 2>&1; then
    echo -e "\033[1;31m[+] \033[1;32mFedora/RHEL detected.\033[0m"
    PKG="dnf"
    PIP_FLAGS=""
elif command -v pacman >/dev/null 2>&1; then
    echo -e "\033[1;31m[+] \033[1;32mArch/Manjaro detected.\033[0m"
    PKG="pacman"
    PIP_FLAGS=""
elif command -v apk >/dev/null 2>&1; then
    echo -e "\033[1;31m[+] \033[1;32mAlpine detected.\033[0m"
    PKG="apk"
    PIP_FLAGS=""
else
    echo
    echo -e "\033[1;31m[~] \033[1;33mNo native installer found.\033[0m"
    echo -e "\033[1;31m[~] \033[1;37mContinuing with pip only - assuming Python + pip are already installed.\033[0m"
    PKG=""
    PIP_FLAGS=""
fi

# Install Python via the detected package manager (skip if nothing worked)
if [ -n "$PKG" ] && ! command -v python3 >/dev/null 2>&1 && ! command -v python >/dev/null 2>&1; then
    echo
    echo -e "\033[1;31m[+] \033[1;32mInstalling Python via $PKG...\033[0m"
    case "$PKG" in
        apt)      apt install python3 python3-pip -y ;;
        pkg)      pkg install python -y ;;
        dnf)      dnf install -y python3 python3-pip ;;
        pacman)   pacman -Sy --noconfirm python python-pip ;;
        apk)      apk add --no-cache python3 py3-pip ;;
    esac
fi

# Locate pip
PIP=$(command -v pip3 || command -v pip)
if [ -z "$PIP" ]; then
    echo
    echo -e "\033[1;31m[~] \033[1;31mERROR: pip not found.\033[0m"
    echo -e "\033[1;31m[~] \033[1;37mInstall pip manually, then run: pip install -r requirements.txt\033[0m"
    exit 1
fi

# Install Python dependencies
echo
echo -e "\033[1;31m[+] \033[1;32mInstalling Python dependencies...\033[0m"
if [ -n "$PIP_FLAGS" ]; then
    $PIP install $PIP_FLAGS -r requirements.txt || $PIP install --user $PIP_FLAGS -r requirements.txt
else
    $PIP install -r requirements.txt 2>/dev/null || $PIP install --user -r requirements.txt
fi

# Verify every dependency actually imports
echo
echo -e "\033[1;31m[+] \033[1;32mVerifying installation...\033[0m"
MISSING=0
for mod in openai rich; do
    if python3 -c "import $mod" 2>/dev/null || python -c "import $mod" 2>/dev/null; then
        echo -e "\033[1;31m[+] \033[1;32mOK: $mod\033[0m"
    else
        echo -e "\033[1;31m[~] \033[1;31mMISSING: $mod\033[0m"
        MISSING=$((MISSING + 1))
    fi
done

echo
if [ "$MISSING" -gt 0 ]; then
    echo -e "\033[1;31m[~] \033[1;31m$MISSING dependency(ies) failed to install - fix the error(s) above and re-run setup.sh\033[0m"
    exit 1
fi

echo -e "\033[1;31m[+] \033[1;32mArtifyX is installed successfully!\033[0m"
echo
echo -e "\033[1;31m[+] \033[1;37mNext steps:\033[0m"
echo -e "\033[1;31m    1. \033[1;32mEdit config.py and put your OpenAI API key in API_KEY = \"sk-...\"\033[0m"
echo -e "\033[1;31m    2. \033[1;32mRun: \033[1;31mpython3 artifyx.py\033[0m"
echo
