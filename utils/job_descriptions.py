import os 
import openai
import requests
import json
import re
from urllib.parse import quote
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv('GPT') 


def generate_job_summary(internship, ai):

    if ai:
        '''ChatGPT integration to provide brief summaries of companies'''
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user", 
                    "content": f"Summarize {internship} in 15 words or less WITHOUT restating the company's name. Be engaging!\n\nSummary:"}
            ],
            temperature=1,
            max_tokens=20,
        )

        return response.choices[0].message.content
    else:
        for attempt in range(2):
            
            wikimedia_search_api = f'https://en.wikipedia.org/w/api.php?action=opensearch&search={quote(internship, safe="")}{r"%20company" if attempt == 0 else ""}&namespace=0'
            internship_search = ''

            try:
                wikimedia_search_results = requests.get(wikimedia_search_api)
            except Exception as e:
                return f'Invalid request: ({e})', ''
            
            if wikimedia_search_results.status_code == 200:
                wikimedia_search_json = json.loads(wikimedia_search_results.text)

                print(wikimedia_search_json)
                if len(wikimedia_search_json[1]) > 0:
                    if internship in wikimedia_search_json[1][0]:
                        internship_search = wikimedia_search_json[1][0]
                        break

        wikimedia_more_results = f"https://en.wikipedia.org/w/index.php?fulltext=1&profile=advanced&search={quote(internship_search, safe='')}"


        if internship_search == '':
            return "Summary unavailable.", wikimedia_more_results
        else:
            wikimedia_api = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(internship_search, safe='')}?redirect=true"
            

            try:
                wikimedia_request = requests.get(wikimedia_api)
            except Exception as e:
                return f'Invalid request: ({e})', wikimedia_more_results

            if wikimedia_request.status_code == 200:
                wikimedia_json = json.loads(wikimedia_request.text)
                summary: str = wikimedia_json['extract']
                summary = re.split('[.!?][\s]{1,2}(?=[A-Z])', summary)

                return summary[0] + '.', wikimedia_more_results
            else:
                return "Summary unavailable..", wikimedia_more_results

        

