import os

from groq import Groq
from dotenv import load_dotenv
import PyPDF2

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")

client = Groq(
    # This is the default and can be omitted
    api_key=os.getenv("GROQ_API_KEY"),
)



file_path="wordpress-pdf-invoice-plugin-sample.pdf"
with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                resume_text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    resume_text += page.extract_text()
context=resume_text

prompt=f""" your task is extract the data into json(key-value) format from a given context, the context is givenn below.
           here is the context : {context}

           Note : you are restricted to provide the response in json format with key-value pair only fromm the given context of text, do not include any other data into the response by own.
           """

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "you are a smart and efficient data extractor in json key-value pair from the text of a pdf. "
        },
        {
            "role": "user",
            "content": context,
        }
    ],
    model="llama3-8b-8192",
)

print(chat_completion.choices[0].message.content)