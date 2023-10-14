import json
import requests

def check_for_key(internship, key):
    try:
        return internship[key] if internship[key] != "" else "Not Available"
    except:
        match key:
            case "link":
                return "https://www.levels.fyi/js/internshipData.json"
            case "icon":
                return "https://cdn.discordapp.com/embed/avatars/0.png"
            case _:
                return 'Not Available'

def update():
    levelsfyi_link = "https://www.levels.fyi/js/internshipData.json"
    levelsfyi_json = requests.get(levelsfyi_link).text
    internships = json.loads(levelsfyi_json)
    filtered_internships = [yr for yr in internships if yr['yr'] == '2024']
    filtered_internships = [seasons for seasons in filtered_internships if seasons['season'] == 'Summer']

    with open('database/internships.json', 'w') as f:
        json.dump(filtered_internships, f, indent=4)
        f.close()

if __name__ == "__main__":
    print("internship.py is not meant to be run directly unless for testing.")