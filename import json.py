import json
import random

# Function to generate random hex color
def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))

# Create a list of 1000 colors with names
colors = []
for i in range(1, 1001):
    color = {
        "name": f"Color {i}",
        "hex": random_color()
    }
    colors.append(color)

# Save as JSON file
with open("colors.json", "w") as f:
    json.dump(colors, f, indent=4)

print("✅ colors.json with 1000 colors has been created!")
