import json
import requests
import os
from deepdiff import DeepDiff
from re import sub

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
    changes = {'old_amount': 0, "added" : [], "removed" : [], "cat_added" : [], "cat_removed" : [], "cat_changed" : []}

    new_internships = get_internship_file()
    old_internships = open_file()

    ddiff = DeepDiff(old_internships, new_internships, ignore_order=True, view='tree')

    if len(ddiff) > 0:
        for section in ddiff:
            match section:
                case "iterable_item_added" | "iterable_item_removed":
                    for data in ddiff[section]:
                        print(ddiff[section])
                        paths = data.path(output_format='list')
                        changes[f'{"added" if section == "iterable_item_added" else "removed"}'].append(paths[0])
                case "dictionary_item_added" | "dictionary_item_removed":
                    for data in ddiff[section]:
                        paths = data.path(output_format='list')
                        changes[f'{"cat_added" if section == "dictionary_item_added" else "cat_removed"}'].append([paths[0], paths[1]])
                case "values_changed":
                    for data in ddiff[section]:
                        paths = data.path(output_format='list')
                        changes[f'cat_changed'].append([paths[0], paths[1], data.t1, data.t2])

        changes['old_amount'] = len(old_internships)

        return True, changes
                    
    else:
        return False, {}

if __name__ == "__main__":
    print("internship.py: internship.py is not meant to be run directly unless for testing.")