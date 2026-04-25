#!/usr/bin/env python3
import os
import re
import subprocess
from pathlib import Path

print("🚀 MRH Simple Downloader v1.0")

# Get commit message
msg = subprocess.run(['git', 'log', '-1', '--pretty=%B'], capture_output=True, text=True).stdout
print(f"📝 Message: {msg[:100]}")

# Check for YouTube
if 'dl-yt:' in msg:
    # Extract URL
    match = re.search(r'dl-yt:\s*([^\s]+)', msg)
    if match:
        url = match.group(1)
        # Remove (mp3) if present
        url = url.replace('(mp3)', '').strip()
        
        print(f"🎬 Downloading: {url}")
        
        # Create directory
        Path("downloads/youtube").mkdir(parents=True, exist_ok=True)
        
        # SIMPLE DOWNLOAD - let yt-dlp work in its own default way
        # Just let it save files wherever it wants, we'll find them
        result = subprocess.run(['yt-dlp', url], capture_output=True, text=True)
        
        print(f"📋 Return code: {result.returncode}")
        
        # Find the downloaded file
        print("\n🔍 Searching for downloaded file...")
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith(('.mp4', '.webm', '.mkv', '.mp3', '.m4a')):
                    size = os.path.getsize(os.path.join(root, file)) / (1024*1024)
                    print(f"✅ Found: {file} ({size:.2f} MB)")
                    # Move to youtube folder
                    import shutil
                    shutil.move(os.path.join(root, file), f"downloads/youtube/{file}")
                    print(f"📁 Moved to downloads/youtube/{file}")
        
        print("\n✅ Done")
