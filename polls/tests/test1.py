import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from polls.models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexDetailTests(TestCase):
    
    def test_detail_view_with_a_future_question(self):

        future_question = create_question("Future question.", 5)
        
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        
        self.assertEqual(response.status_code, 404)
        
        
    def test_detail_view_with_a_past_question(self):

        past_question = create_question("Past question.", -5)
        
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        
        self.assertContains(response, past_question.question_text)