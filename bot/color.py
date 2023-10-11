from PIL import Image
import requests

def calc_avg_color(url):

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

if __name__ == "__main__":
    code = calc_avg_color("https://onwardstate.com/wp-content/uploads/2015/07/Screen-Shot-2015-08-04-at-1.56.47-AM.png")
    print(code)