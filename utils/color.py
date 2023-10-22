from PIL import Image
import requests
import random

def calc_avg_color(url: str):

    data = requests.get(url, stream=True)

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
    return color_code
    

if __name__ == "__main__":
    print("color.py is not meant to be run directly unless for testing.")