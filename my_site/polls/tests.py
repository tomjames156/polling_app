import datetime

from django.urls import reverse
from django.utils import timezone
from django.test import TestCase
from polls.models import Question

# Create your tests here.

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_date(self): 
        """Returns False if a question was published recently with a future date"""

        time = timezone.now() + datetime.timedelta(days=1)
        future_question  = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Returns false if a question was published within the last day"""

        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_new_question(self):
        """Returns true if a question was published recently within the past day"""
        time = timezone.now() - datetime.timedelta(hours=23, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """Creates a question with a given range for the days -ve for published or past questions and +ve for future or unpublished questions"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """When no questions are available. Display something appropriate"""

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_past_questions(self):
        """Returns the set of questions that have been recently published"""

        question = create_question(question_text="Past Question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])


    def test_future_questions(self):
        """Returns the set of questions that have yet to be published"""

        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    
    def test_future_question_and_past_questions(self):
        """Returns only the past questions if both past and future questions exist"""

        question = create_question(question_text="Past question", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question])


    def test_two_past_questions(self):
        """Displays multiple questions"""
        question1 = create_question(question_text="Past Question 1", days=-30)
        question2 = create_question(question_text="Past Question 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], [question2, question1]) # cus the context returns desc order


# class QuestionDetailTestView(TestCase):

#     def test_future_question_detail(self):
#         """Only shows tests that are in the past"""

#         future_question = create_question(question_text="Future Question", days=5)
#         response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
#         self.assertEqual(response.status_code, 404)

#     def test_past_question_detail(self):
#         """Displays the y text if its a question published in the past"""

#         past_question = create_question(question_text="Past Question", days=-5)
#         url = reverse('polls:detail', args=(past_question.id,))
#         response = self.client.get(url)
#         self.assertContains(response.context, past_question.question_text)

# class QuestionResultsView(TestCase):

#     def test_future_question_results(self):
#         """Does not display result for future questions"""

        # future_question = create_question(question_text="Future Question", days=5)
        # url = reverse('polls:results', args=(future_question.id,))
        # response = self.client.get(url)
        # self.assertEqual(response.status_code, 404)
