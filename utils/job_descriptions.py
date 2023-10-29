import os 
import openai 
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv('GPT')


def generate_job_summary(internship):
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

