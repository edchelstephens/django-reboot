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
        self.assertContains(response, question.question_text)
        self.assertQuerySetEqual(response.context["latest_question_list"], [question])

    def test_future_question_does_not_get_displayed_on_index(self):
        """Future publish date questions are not displayed on index."""
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))

        self.assertNotIn(future_question.question_text, response)
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_questions_only_past_questions_gets_displayed(self):
        """Only past questions are to be posted in the index page"""
        future_question = create_question(question_text="Future question", days=30)
        past_question = create_question(question_text="Past question", days=-1)
        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, future_question.question_text)
        self.assertContains(response, past_question.question_text)
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [past_question]
        )

    def test_two_past_questions_all_gets_displayed(self):
        """Two recent questions gets displayed."""

        question1 = create_question(question_text="Question 1", days=-1)
        question2 = create_question(question_text="Question 2", days=-2)

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question1.question_text)
        self.assertContains(response, question2.question_text)
        self.assertQuerySetEqual(
            response.context["latest_question_list"], [question1, question2]
        )

    def test_only_latest_5_questions_posted(self):
        """Only the latest 5 questions are posted on index."""

        question1 = create_question(question_text="Question 1", days=-1)
        question2 = create_question(question_text="Question 2", days=-2)

        question3 = create_question(question_text="Question 3", days=-3)
        question4 = create_question(question_text="Question 4", days=-4)

        question5 = create_question(question_text="Question 5", days=-5)
        question6 = create_question(question_text="Question 6", days=-6)

        question7 = create_question(question_text="Question 7", days=-7)
        question8 = create_question(question_text="Question 8", days=-8)

        question9 = create_question(question_text="Question 9", days=-9)
        question10 = create_question(question_text="Question 10", days=-10)

        response = self.client.get(reverse("polls:index"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, question1.question_text)
        self.assertContains(response, question2.question_text)
        self.assertContains(response, question3.question_text)
        self.assertContains(response, question4.question_text)
        self.assertContains(response, question5.question_text)

        self.assertNotContains(response, question6.question_text)
        self.assertNotContains(response, question7.question_text)
        self.assertNotContains(response, question8.question_text)
        self.assertNotContains(response, question9.question_text)
        self.assertNotContains(response, question10.question_text)

        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question1, question2, question3, question4, question5],
        )


class QuestionDetailViewTest(TestCase):

    def test_future_question(self):
        """Future questions should not be displayed."""
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Past question should be displayed."""

        past_question = create_question(question_text="Past Question", days=-1)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)
