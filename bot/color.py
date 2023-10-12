from PIL import Image
import requests
import random

def calc_avg_color(url):

    data = requests.get(url, stream=True)
    response = requests.get(url)

    color_code = "#ffffff"

    if data.status_code == 200:
        # Open image
        img = Image.open(data.raw)

        # Convert image to RGB
        img = img.convert('RGB')

        # convert pixels to a list
        pixels = list(img.getdata())

        # Calculate average RGB values
        sum_colors = {"r": 0, "g": 0, "b": 0}
        total_pixels = len(pixels)

        # Add up the red, green, and blue colors
        for r, g, b in pixels:
            sum_colors["r"] += r
            sum_colors["g"] += g
            sum_colors["b"] += b

        # Calculate the avg color and round down
        avg_red = sum_colors["r"] // total_pixels
        avg_green = sum_colors["g"] // total_pixels
        avg_blue = sum_colors["b"] // total_pixels

        # Convert average RGB values to hexadecimal
        color_code = f"#{avg_red:02x}{avg_green:02x}{avg_blue:02x}"
        return color_code
    else:
        with open('utils/embed_colors.txt', 'r') as f:
            random_colors = [int(line.strip(), 16) for line in f.readlines()]
            random_colors = random.choice(random_colors)
            return random_colors