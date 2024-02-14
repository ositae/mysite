from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect 
from django.http import Http404
# from pymongo import MongoClient
import os
from django.template import loader
from django.utils import timezone
from .models import Question, Choice
from dotenv import load_dotenv
load_dotenv()
# from bson import ObjectId
from django.urls import reverse
from django.views import generic
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings

recipientAddress = os.getenv('SMTP_EMAIL')

# print(os.getenv('MONGO_URI'))

# client = MongoClient(os.getenv('MONGO_URI'))
# db = client["polls"]
# print(client)
# collection = db.polls_question_1

# print(db.list_collection_names())
# print(db.polls_question_1.find_one())

# print('----Availiable Collections----')
# for collection in db.list_collection_names():
#     print('---> '+collection)
# print('')
# print('----Availiable Questions----')
# all_questions = list(db.polls_question_1.find())
# print(all_questions)
# q_num = 1
# print('')

# new_q = {"question_text": "----Cats or dogs?----", "pub_date": datetime.now()}

# create new question
# db.polls_question_1.insert_one(new_q)
# print('New question added to the database!')

# does_new_q_exist_in_db = False

# search  for a specific question by its number (q_num)
# searched_q = db.polls_question_1.find_one({
#     "question_text": new_q['question_text']
# })
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

# questionText2 = db.polls_question_1.find_one({"question_text": 
#                                              {"$regex": "Or", "$options": "i"}
#                                             })
# print(questionText2)

# search by date
# target_date = datetime(2024, 2, 3)
# found_questions = db.polls_question_1.find({"pub_date": { "$gte": target_date, "$lt": target_date + timedelta(days=1)}})
# for question in found_questions:
    # print("---Questions with specified date---", question)

# update a question
# before_update = db.polls_question_1.find({"pub_date": { "$gte": target_date, "$lt": target_date + timedelta(days=1)}})
# print('---before---', before_update)
# update_time = datetime.now()
# after_update = db.polls_question_1.find_one_and_update({"pub_date": {"$gte": target_date, "$lt": target_date + timedelta(days=1)}}, {"$set": {"pub_date": update_time}},
# return_document=True)

# print("---after---", after_update)

# delete a question by ObjectId
# deleted_question = db.polls_question_1.find_one_and_delete({"_id": ObjectId("65bed6c57284f367e43bc890")})
# print(deleted_question)

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")




# Create your views here.
# views = routes
# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")[:5]
#     context = { "latest_question_list": latest_question_list }
#     return render(request, "polls/index.html", context)

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html", {"question": question})

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', { "question": question })

def send_message(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"{form.cleaned_data['name']} sent you a message!"
            message = f"Name: {form.cleaned_data['name']}\n\nSubject: {form.cleaned_data['subject']}\n\nSender:{form.cleaned_data['sender']}\n\nMessage:\n{form.cleaned_data['message']}"
            sender = form.cleaned_data['sender']
            send_mail(subject, message, sender, [recipientAddress], fail_silently=False)
    else:
        form = ContactForm()
    return render(request, "polls/contact.html", {"form": form})





class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five publised questions"""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """ 
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

