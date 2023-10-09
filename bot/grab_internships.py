import json
import requests


def checkForKey(company, key):
    try:
        return company[key]
    except:
        return 'Unknown'

def main():
    link = "https://www.levels.fyi/js/internshipData.json"
    json_data = requests.get(link).text
    internship_data = json.loads(json_data)

    amount = 0
    
    for company in internship_data:
        if checkForKey(company,'yr') == "2024":
            print("-------------------")
            print("New Internship:")
            print(checkForKey(company, 'company'))
            print(f"{checkForKey(company,'title')} - {checkForKey(company,'season')} {checkForKey(company,'yr')}")

            print(f"{checkForKey(company,'loc')}")
            print(f"${checkForKey(company,'monthlySalary')} / month (${checkForKey(company,'hourlySalary')} / hr)")
            print("-------------------")
            print()

            amount += 1

    print(f"There are {amount} internships available.")

if __name__ == "__main__":
    main()
