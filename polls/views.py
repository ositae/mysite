from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
from bson import ObjectId

print(os.getenv('MONGO_URI'))

client = MongoClient(os.getenv('MONGO_URI'))
db = client["mysite3"]
print(client)
collection = db.polls_question

print(db.list_collection_names())
print(db.polls_question.find_one())

print('----Availiable Collections----')
for collection in db.list_collection_names():
    print('---> '+collection)
print('')
print('----Availiable Questions----')
all_questions = list(db.polls_question.find())
print(all_questions)
q_num = 1
print('')

new_q = {"question_text": "-----Cats or Do?---------", "pub_date": datetime.now()}

does_new_q_exist_in_db = False

db.polls_question.insert_one(new_q)
print('New question added to the database!')
print(new_q)



def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
