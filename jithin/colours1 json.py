import json
import colorsys

colors = []

# Generate 1000 colors across the hue spectrum
for i in range(1000):
    hue = i / 1000.0
    lightness = 0.5
    saturation = 0.9
    r, g, b = colorsys.hls_to_rgb(hue, lightness, saturation)
    hex_color = '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))
    colors.append({
        "name": f"Color {i+1}",
        "hex": hex_color
    })

with open("colors.json", "w") as f:
    json.dump(colors, f, indent=4)

print("✅ 1000 well-balanced colors saved to colors.json!")
