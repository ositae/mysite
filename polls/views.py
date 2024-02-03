from django.shortcuts import render
from django.http import HttpResponse
from pymongo import MongoClient
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
from bson import ObjectId

print(os.getenv('MONGO_URI'))

client = MongoClient(os.getenv('MONGO_URI'))
db = client["polls"]
print(client)
collection = db.polls_question_1

print(db.list_collection_names())
print(db.polls_question_1.find_one())

print('----Availiable Collections----')
for collection in db.list_collection_names():
    print('---> '+collection)
print('')
print('----Availiable Questions----')
# all_questions = list(db.polls_question_1.find())
# print(all_questions)
q_num = 1
print('')

new_q = {"question_text": "What is your favorite food?", "pub_date": datetime.now()}
# db.polls_question_1.insert_one(new_q)
# print('New question added to the database!')

does_new_q_exist_in_db = False

# search  for a specific question by its number (q_num)
searched_q = db.polls_question_1.find_one({
    "question_text": new_q['question_text']
})
# print(searched_q)

# search by text
# questionText = db.polls_question_1.find_one({"question_text": 
#                                              {"$regex": "Indeed", "$options": "i"}
#                                             })
# print(questionText)

# questionText1 = db.polls_question_1.find_one({"question_text": 
#                                              {"$regex": "Cats", "$options": "i"}
#                                             })
# print(questionText1)

questionText2 = db.polls_question_1.find_one({"question_text": 
                                             {"$regex": "Or", "$options": "i"}
                                            })
print(questionText2)

# search by date
target_date = datetime(2024, 2, 3)
found_questions = db.polls_question_1.find({"pub_date": { "$gte": target_date, "$lt": target_date + timedelta(days=1)}})
for question in found_questions:
    print("---Questions with specified date---", question)

# update a question
# before_update = db.polls_question_1.find({"pub_date": { "$gte": target_date, "$lt": target_date + timedelta(days=1)}})
# print('---before---', before_update)
# update_time = datetime.now()
# after_update = db.polls_question_1.find_one_and_update({"pub_date": {"$gte": target_date, "$lt": target_date + timedelta(days=1)}}, {"$set": {"pub_date": update_time}},
# return_document=True)

# print("---after---", after_update)

# delete a question by ObjectId
deleted_question = db.polls_question_1.find_one_and_delete({"_id": "65bec9c56ba224f19961495b"})
print(deleted_question)


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
