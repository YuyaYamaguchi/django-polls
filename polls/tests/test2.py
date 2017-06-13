import datetime

from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from polls.models import Question

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionViewTests(TestCase):
    """
    IndexViewのテスト
    """
    
    def test_index_view_with_no_questions(self):
        """
        Questionがない場合
        """
        
        response = self.client.get(reverse('polls:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_index_view_with_a_past_question(self):
        """
        Questionが1件ある場合
        """
        
        create_question("Past question.", -30)
        
        response = self.client.get(reverse('polls:index'))
        
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])
    
        
    def test_index_view_with_a_future_question(self):
        """
        未来日のQuestionが1件ある場合
        """
        
        create_question("Future question.", 30)
        
        response = self.client.get(reverse('polls:index'))
        
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    
    def test_index_view_with_future_question_and_past_question(self):
        """
        未来日と過去日ののQuestionが1件づつある場合
        """
        
        create_question("Future question.", 30)
        create_question("Past question.", -30)
        
        
        response = self.client.get(reverse('polls:index'))
        
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question.>'])
        
        
    def test_index_view_with_two_question(self):
        """
        Questionが2件ある場合
        """
        
        create_question("Past question 1.", -30)
        create_question("Past question 2.", -5)
        
        response = self.client.get(reverse('polls:index'))
        
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
        