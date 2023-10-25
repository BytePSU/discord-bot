import json
import requests
import os

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
            

def get_internship_file(filter=True):
    levelsfyi_link = "https://www.levels.fyi/js/internshipData.json"
    levelsfyi_json = requests.get(levelsfyi_link).text
    internships = json.loads(levelsfyi_json)

    if filter:
        internships = [yr for yr in internships if yr['yr'] == '2024']
        internships = [seasons for seasons in internships if seasons['season'] == 'Summer']

    return internships



def update_file():
    internships = get_internship_file()

    if not os.path.exists('database'):
        print("internship.py: Database folder missing, creating.")
        os.mkdir('database')

    with open('database/internships.json', 'w') as f:
        json.dump(internships, f, indent=4)
        f.close()


def open_file():
    with open('database/internships.json', 'r') as f:
        internships_data = json.load(f)
        f.close()

    return internships_data



def check_for_update():
    new_internships = get_internship_file()
    old_internships = open_file()

    if len(new_internships) != len(old_internships):
        return {
            "changed": True, 
            "amount": len(new_internships) - len(old_internships), 
            "old_amount": len(old_internships)
        }
    else:
        return {
            "changed": False, 
            "amount": 0, 
            "old_amount": len(old_internships)
        }

if __name__ == "__main__":
    print("internship.py: internship.py is not meant to be run directly unless for testing.")