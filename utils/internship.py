import json
import requests
import os
from deepdiff import DeepDiff
from re import sub

def check_for_key(internship, key):
    try:
        return internship[key]
    except:
        match key:
            case "link":
                return "https://www.levels.fyi/internships"
            case "icon":
                return "https://cdn.discordapp.com/embed/avatars/0.png"
            case _:
                return ''
            

def get_internship_file(filter=True):
    current_year = '2024'
    current_season = 'Summer'

    levelsfyi_link = "https://www.levels.fyi/js/internshipData.json"
    levelsfyi_json = requests.get(levelsfyi_link).text
    internships = json.loads(levelsfyi_json)

    if filter:
        internships = [yr for yr in internships if yr['yr'] == current_year]
        internships = [seasons for seasons in internships if seasons['season'] == current_season]

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
    changes = {'old_amount': 0, "added" : [], "removed" : [], "cat_added" : {}, "cat_removed" : {}, "cat_changed" : {}, "offset" : 0}

    new_internships = get_internship_file()
    old_internships = open_file()

    ddiff = DeepDiff(old_internships, new_internships, ignore_order=True, view='tree')

    if len(ddiff) > 0:
        for section in ddiff:
            match section:
                case "iterable_item_added" | "iterable_item_removed":
                    # paths[0] = internship id
                    for data in ddiff[section]:
                        print(ddiff[section])
                        paths = data.path(output_format='list')
                        changes[f'{"added" if section == "iterable_item_added" else "removed"}'].append(paths[0])
                case "dictionary_item_added" | "dictionary_item_removed":
                    # paths[0] = internship id
                    # paths[1] = new/removed category

                    # tree - {1, ["category1", "category2"]}

                    for data in ddiff[section]:
                        paths = data.path(output_format='list')

                        if section == "dictionary_item_added":
                            if paths[0] not in changes["cat_added"]:
                                changes["cat_added"][paths[0]] = [paths[1]]
                            else:
                                changes["cat_added"][paths[0]].append(paths[1])

                        elif section == "dictionary_item_removed":
                            if paths[0] not in changes["cat_removed"]:
                                changes["cat_removed"][paths[0]] = [paths[1]]
                            else:
                                changes["cat_removed"][paths[0]].append(paths[1])

                case "values_changed":
                    # paths[0] = internship id
                    # paths[1] = changed category
                    # data.t1 = old change
                    # data.t2 = new change

                    # tree - {1, [["catergory1", old_value, new_value], ["catergory2", old_value, new_value]]}
                    for data in ddiff[section]:
                        paths = data.path(output_format='list')

                        if paths[0] not in changes["cat_changed"]:
                            changes["cat_changed"][paths[0]] = [[paths[1], data.t1, data.t2]]
                        else:
                            changes["cat_changed"][paths[0]].append([paths[1], data.t1, data.t2])

        changes['old_amount'] = len(old_internships)
        changes['offset'] = len(changes['added']) - len(changes["removed"])

        return True, changes
                    
    else:
        return False, {}

if __name__ == "__main__":
    print("internship.py: internship.py is not meant to be run directly unless for testing.")