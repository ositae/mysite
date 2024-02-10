from django.test import TestCase
import datetime
from django.utils import timezone
from .models import Question, Choice
from django.urls import reverse

class Question_Model_Test(TestCase):
    def  test_create_question(question_text, days):
        """
        Create a question with the given 'question_test'  and publish it for the number of 'days'
        offset to now (negative for questions published in the past, positive for questions that have yet
        to be published).
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)
    
    def test_was_published_recently(self):
        """
        was_published_recently() should return True if the question published in the past.
        """
        time = timezone.now() + datetime.timedelta(days=90)
        recent_question = Question.objects.create(question_text="Past question", pub_date=time)
        self.assertIs(recent_question.was_published_recently(), False)

    def test_was_published_recently_old_question(self):
        """
        was_published_recently() should return False if the question published after one day.
        """
        old_time = timezone.now() - datetime.timedelta(hours=24)
        old_question = Question(pub_date=old_time)
        self.assertIs(old_question.was_published_recently(), False)

# Create your tests here.
