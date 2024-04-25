import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """was_published_recently() returns False for questions with future pub_date"""
        month_from_now = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=month_from_now)

        self.assertFalse(future_question.was_published_recently())