import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question_returns_False(self):
        """was_published_recently() returns False for questions with future pub_date"""
        month_from_now = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=month_from_now)

        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question_returns_False(self):
        "was_published_recently() returns False for pub_date older than 1 day."
        the_other_day = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=the_other_day)

        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_returns_True_for_todays_recent_publication(self):
        """was_published_recently() returns True for recent publication."""
        an_hour_ago = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=an_hour_ago)

        self.assertTrue(recent_question.was_published_recently())
