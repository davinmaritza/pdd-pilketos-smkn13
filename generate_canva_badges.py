#!/usr/bin/env python3
"""
generate_canva_assets.py
Generates transparent PNG circular badges and candidate cards ready to drag-and-drop into Canva:
- Salsya Aprilia Hikmah (57%, 715 Suara, XI AK 5) - Rank 1
- Bima Pangestu Sejati (35%, 435 Suara, XI AK 6) - Rank 2
- Loviola Amira Prameswari (8%, 105 Suara, XI AK 6) - Rank 3
"""

import os
import cv2
import numpy as np

ASSETS_DIR = "/home/suzirz/Documents/Tugas/MPK/assets/candidates"
OUT_DIR = "/home/suzirz/Documents/Tugas/MPK/assets/canva_rekap_assets"
os.makedirs(OUT_DIR, exist_ok=True)

CANDIDATES = [
    {
        "key": "salsya",
        "name": "SALSYA APRILIA HIKMAH",
        "class": "XI AK 5",
        "votes": 715,
        "percent": 57,
        "rank": 1,
        "color": (45, 175, 212) # Gold in BGR
    },
    {
        "key": "bima",
        "name": "BIMA PANGESTU SEJATI",
        "class": "XI AK 6",
        "votes": 435,
        "percent": 35,
        "rank": 2,
        "color": (200, 200, 200) # Silver in BGR
    },
    {
        "key": "loviola",
        "name": "LOVIOLA AMIRA PRAMESWARI",
        "class": "XI AK 6",
        "votes": 105,
        "percent": 8,
        "rank": 3,
        "color": (70, 120, 180) # Bronze in BGR
    }
]

for cand in CANDIDATES:
    img_path = os.path.join(ASSETS_DIR, f"{cand['key']}_portrait.jpg")
    img = cv2.imread(img_path)
    if img is None:
        continue
        
    h, w = img.shape[:2]
    # Crop head area (upper 65% square)
    size = min(w, int(h * 0.70))
    x_start = (w - size) // 2
    y_start = int(h * 0.05)
    crop = img[y_start:y_start+size, x_start:x_start+size]
    
    # Resize to standard badge size 600x600
    target_dim = 600
    resized = cv2.resize(crop, (target_dim, target_dim), interpolation=cv2.INTER_LANCZOS4)
    
    # Create circular mask
    mask = np.zeros((target_dim, target_dim), dtype=np.uint8)
    center = (target_dim // 2, target_dim // 2)
    radius = (target_dim // 2) - 16
    cv2.circle(mask, center, radius, 255, -1)
    
    # 4-channel RGBA
    b, g, r = cv2.split(resized)
    rgba = cv2.merge([b, g, r, mask])
    
    # Add metallic border
    border_color = (34, 180, 220, 255) if cand['rank'] == 1 else ((210, 210, 210, 255) if cand['rank'] == 2 else (60, 120, 180, 255))
    cv2.circle(rgba, center, radius, border_color, 14, cv2.LINE_AA)
    cv2.circle(rgba, center, radius - 7, (255, 255, 255, 180), 3, cv2.LINE_AA)
    
    out_badge = os.path.join(OUT_DIR, f"{cand['key']}_circle_badge.png")
    cv2.imwrite(out_badge, rgba)
    print(f"Generated badge: {out_badge}")

print("All Canva candidate badges created successfully.")
