import os

os.makedirs("logo-pdd", exist_ok=True)

# Concept A: Lens Monogram P
# Bold geometric P with a viewfinder/lens counter and inner shutter core
svg_a = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-a">
  <title id="title-a">PDD Concept A - Lens Monogram P</title>
  <path fill="#000000" fill-rule="evenodd" d="
    M 64,32
    L 144,32
    C 182.7,32 212,61.3 212,98
    C 212,134.7 182.7,164 144,164
    L 100,164
    L 100,212
    C 100,218.6 94.6,224 88,224
    L 64,224
    C 57.4,224 52,218.6 52,212
    L 52,44
    C 52,37.4 57.4,32 64,32 Z
    M 100,68
    L 100,128
    L 142,128
    C 159.7,128 172,115.7 172,98
    C 172,80.3 159.7,68 142,68
    L 100,68 Z
  "/>
  <circle cx="138" cy="98" r="16" fill="#000000"/>
</svg>'''

# Concept B: PDD Monogram Block
# Tight geometric P-D-D letterforms with uniform 22px stroke weight and 8px gaps
svg_b = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-b">
  <title id="title-b">PDD Concept B - PDD Monogram</title>
  <!-- Letter P (x=20..86) -->
  <path fill="#000000" fill-rule="evenodd" d="
    M 20,64
    L 56,64
    C 74.8,64 88,77.2 88,96
    C 88,114.8 74.8,128 56,128
    L 42,128
    L 42,192
    L 20,192 Z
    M 42,84
    L 42,108
    L 54,108
    C 61.7,108 66,103.7 66,96
    C 66,88.3 61.7,84 54,84 Z
  "/>
  <!-- First D (x=96..164) -->
  <path fill="#000000" fill-rule="evenodd" d="
    M 98,64
    L 128,64
    C 150.1,64 166,79.9 166,102
    L 166,154
    C 166,176.1 150.1,192 128,192
    L 98,192 Z
    M 120,86
    L 120,170
    L 128,170
    C 137.9,170 144,163.9 144,154
    L 144,102
    C 144,92.1 137.9,86 128,86 Z
  "/>
  <!-- Second D (x=176..244) -->
  <path fill="#000000" fill-rule="evenodd" d="
    M 176,64
    L 206,64
    C 228.1,64 244,79.9 244,102
    L 244,154
    C 244,176.1 228.1,192 206,192
    L 176,192 Z
    M 198,86
    L 198,170
    L 206,170
    C 215.9,170 222,163.9 222,154
    L 222,102
    C 222,92.1 215.9,86 206,86 Z
  "/>
</svg>'''

# Concept C: Viewfinder Prism
# Four camera-crop brackets framing a diamond design prism with a lens core
svg_c = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256" width="256" height="256" role="img" aria-labelledby="title-c">
  <title id="title-c">PDD Concept C - Viewfinder Prism</title>
  <!-- Top-Left Bracket -->
  <path fill="#000000" d="M 32,32 L 96,32 L 96,56 L 56,56 L 56,96 L 32,96 Z"/>
  <!-- Top-Right Bracket -->
  <path fill="#000000" d="M 224,32 L 224,96 L 200,96 L 200,56 L 160,56 L 160,32 Z"/>
  <!-- Bottom-Right Bracket -->
  <path fill="#000000" d="M 224,224 L 160,224 L 160,200 L 200,200 L 200,160 L 224,160 Z"/>
  <!-- Bottom-Left Bracket -->
  <path fill="#000000" d="M 32,224 L 32,160 L 56,160 L 56,200 L 96,200 L 96,224 Z"/>
  <!-- Center Diamond Prism with Aperture Hole -->
  <path fill="#000000" fill-rule="evenodd" d="
    M 128,68
    L 188,128
    L 128,188
    L 68,128 Z
    M 128,104
    A 24,24 0 1,0 128,152
    A 24,24 0 1,0 128,104 Z
  "/>
</svg>'''

with open("logo-pdd/concept-a-symbol.svg", "w", encoding="utf-8") as f:
    f.write(svg_a.strip())

with open("logo-pdd/concept-b-symbol.svg", "w", encoding="utf-8") as f:
    f.write(svg_b.strip())

with open("logo-pdd/concept-c-symbol.svg", "w", encoding="utf-8") as f:
    f.write(svg_c.strip())

print("Built 3 PDD SVG concepts.")
