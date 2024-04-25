import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

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


def create_question(question_text, days):
    """Create a question with question text and days offset to timezone.now()"""
    pub_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=pub_date)


class QuestionIndexViewTest(TestCase):

    def test_no_questions_displays_no_question_message(self):
        """The index page should display appropriate message with no latest questions."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")

        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question_gets_displayed_on_index(self):
        """Past published question are displayed on the index page."""
        question = create_question(question_text="Past Question", days=-1)
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Past Question")
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])
