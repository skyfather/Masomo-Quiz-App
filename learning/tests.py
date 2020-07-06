from django.test import TestCase,TransactionTestCase,RequestFactory
from django.test import Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator,Page, PageNotAnInteger, EmptyPage
from .views.quiz import QuizList,CreateQuizView,QuizDetailView,QuizUpdateView,QuizDeleteView,quiz_taking,quiz_results
from .models import Quiz,Subject, Question, Answer, QuizTaker, QuizTakerResponse
from users.models import CustomUser, Student
# Create your tests here.


def create_custom_user2(username,is_student=False,is_teacher=False,password="secure"):
    custom_user = CustomUser.objects.create(username=username,is_student=is_student,is_teacher=is_teacher)
    # custom_user.set_password(password)
    return custom_user
    # CustomUser.objects.create(username="stud1",email="std1@students.com", is_student=True)
def create_custom_user(username,email="user@mail.com",is_student=False,is_teacher=False,password="secure"):
    return get_user_model().objects.create_user(username=username,email=email,password=password,is_student=is_student,is_teacher=is_teacher)
def create_student(user):
    return Student.objects.create(user=user)

def create_subject(name):
    return Subject.objects.create(name=name)
def create_quiz(name,subject,owner):
    return Quiz.objects.create(name=name,subject=subject,owner=owner)
def create_question(question,quiz):
    return Question.objects.create(question=question,quiz=quiz)
def create_answer(answer,question,is_correct=False):
    return Answer.objects.create(answer=answer,question=question,is_correct=is_correct)
def create_quiz_taker(quiz,student):
    return QuizTaker.objects.create(quiz=quiz,student=student)
def create_quiz_taker_response(quiztaker,question,answer):
    return QuizTakerResponse.objects.create(quiztaker=quiztaker,question=question,answer=answer)


class QuizTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subject1 = create_subject(name="Science")
        cls.teacher = create_custom_user2(username="teacher_1",password="secure",is_teacher=True)
        cls.quiz1 = create_quiz(name="First Quiz", subject=cls.subject1, owner=cls.teacher)
    def test_quiz(self):
        self.assertIsInstance(self.quiz1,Quiz)
        self.assertEqual(self.quiz1.subject,self.subject1)

class QuestionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subject1 = create_subject(name="Science")
        cls.teacher = create_custom_user2(username="teacher_1",password="secure",is_teacher=True)
        cls.quiz1 = create_quiz(name="First Quiz", subject=cls.subject1, owner=cls.teacher)
        cls.question1 = create_question(question="What is science",quiz=cls.quiz1)
    def test_question(self):
        self.assertIsInstance(self.question1,Question)
        self.assertNotEqual(self.quiz1.get_questions(),Question.objects.all())

class AnswerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subject1 = create_subject(name="Science")
        cls.teacher = create_custom_user2(username="teacher_1",password="secure",is_teacher=True)
        cls.quiz1 = create_quiz(name="First Quiz", subject=cls.subject1, owner=cls.teacher)
        cls.quiz2 = create_quiz(name="Second Quiz", subject=cls.subject1, owner=cls.teacher)
        cls.question1 = create_question(question="What is science",quiz=cls.quiz1)
        cls.question2 = create_question(question="What is matter",quiz=cls.quiz2)

        cls.answer1 = create_answer(answer="An attempt to explain a phenomenon",question=cls.question1,is_correct=True)
        cls.answer2 = create_answer(answer="Just humanity ego in reasoning things out",question=cls.question1)
        cls.answer3 = create_answer(answer="It's an art",question=cls.question2,is_correct=False)
    def test_answer(self):
        self.assertIsInstance(self.answer1,Answer)
        self.assertIsInstance(self.answer3,Answer)

    def test_answer_is_correct(self):
        self.assertEqual(self.answer3.is_correct,False)

class QuizTakerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subject1 = create_subject(name="Science")
        cls.subject2 = create_subject(name="Mathematics")
        cls.teacher = create_custom_user2(username="teacher_1",password="secure",is_teacher=True)
        cls.quiz1 = create_quiz(name="First Quiz", subject=cls.subject1, owner=cls.teacher)
        cls.quiz2 = create_quiz(name="Second Quiz", subject=cls.subject1, owner=cls.teacher)
        cls.question1 = create_question(question="What is science",quiz=cls.quiz1)
        cls.question2 = create_question(question="What is matter",quiz=cls.quiz2)

        cls.answer1 = create_answer(answer="An attempt to explain a phenomenon",question=cls.question1,is_correct=True)
        cls.answer2 = create_answer(answer="Just humanity ego in reasoning things out",question=cls.question1)
        cls.answer3 = create_answer(answer="It's an art",question=cls.question2,is_correct=False)

        cls.stud_user1 = create_custom_user(username="stud1",email="std1@students.com", is_student=True)
        cls.stud_user2 = create_custom_user(username="stud2",email="std2@students.com", is_student=True)

        cls.student1 = create_student(user=cls.stud_user1)
        cls.student2 = create_student(user=cls.stud_user2)
        #Set interests for students
        cls.student1.interests.add(cls.subject1)
        cls.student2.interests.set([cls.subject1,cls.subject2])

        cls.quiz_taker1 = create_quiz_taker(quiz=cls.quiz1, student=cls.student1)
        cls.quiz_taker2 = create_quiz_taker(quiz=cls.quiz1, student=cls.student2)

    def test_quiz_taker(self):
        self.assertEqual(self.quiz_taker1.student, self.student1)
        self.assertEqual(self.quiz_taker1.quiz, self.quiz1)

class QuizTakerResponseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subject1 = create_subject(name="Science")
        cls.subject2 = create_subject(name="Mathematics")
        cls.teacher = create_custom_user2(username="teacher_1",password="secure",is_teacher=True)
        cls.quiz1 = create_quiz(name="First Quiz", subject=cls.subject1, owner=cls.teacher)
        cls.quiz2 = create_quiz(name="Second Quiz", subject=cls.subject1, owner=cls.teacher)
        cls.question1 = create_question(question="What is science",quiz=cls.quiz1)
        cls.question2 = create_question(question="What is matter",quiz=cls.quiz2)
        cls.question3 = create_question(question="How does lunar eclipse occur",quiz=cls.quiz2)

        cls.answer1 = create_answer(answer="An attempt to explain a phenomenon",question=cls.question1,is_correct=True)
        cls.answer2 = create_answer(answer="Just humanity ego in reasoning things out",question=cls.question1)
        cls.answer3 = create_answer(answer="It's an art",question=cls.question2,is_correct=False)
        cls.answer4 = create_answer(answer="When the sun is overshadowed by moon",question=cls.question3,is_correct=False)

        cls.stud_user1 = create_custom_user(username="stud1",email="std1@students.com", is_student=True)
        cls.stud_user2 = create_custom_user(username="stud2",email="std2@students.com", is_student=True)

        cls.student1 = create_student(user=cls.stud_user1)
        cls.student2 = create_student(user=cls.stud_user2)
        #Set interests for students
        cls.student1.interests.add(cls.subject1)
        cls.student2.interests.set([cls.subject1,cls.subject2])

        cls.quiz_taker1 = create_quiz_taker(quiz=cls.quiz1, student=cls.student1)
        cls.quiz_taker2 = create_quiz_taker(quiz=cls.quiz1, student=cls.student2)

        cls.stud_response1 = create_quiz_taker_response(quiztaker=cls.quiz_taker1, question=cls.question1, answer=cls.answer1)
        cls.stud_response2 = create_quiz_taker_response(quiztaker=cls.quiz_taker1, question=cls.question1, answer=cls.answer2)
        cls.stud_response3 = create_quiz_taker_response(quiztaker=cls.quiz_taker2, question=cls.question1, answer=cls.answer1)

    def setUp(self):
        self.stud_response1 = QuizTakerResponse.objects.get(quiztaker=self.quiz_taker1, question=self.question1, answer=self.answer1)
        self.stud_response2 = QuizTakerResponse.objects.get(quiztaker=self.quiz_taker1, question=self.question1, answer=self.answer2)
        self.stud_response3 = QuizTakerResponse.objects.get(quiztaker=self.quiz_taker2, question=self.question1, answer=self.answer1)

    def test_response_creation(self):
        self.assertIsInstance(self.student1, Student)
        self.assertIsInstance(self.quiz_taker1, QuizTaker)
        self.assertIsInstance(self.stud_response1,QuizTakerResponse)

    def test_response_answer(self):
        self.assertEqual(self.stud_response1.answer, self.answer1)
        self.assertEqual(self.stud_response1.answer.is_correct,True)
        self.assertEqual(self.stud_response2.answer.is_correct,False)

    def test_quiz_responses(self):
        self.assertEqual(self.quiz_taker1.get_quiz_response().count(),2)
        self.assertEqual(self.quiz_taker2.get_quiz_response().count(),1)

    def test_response_to_quiz_subject_not_in_interests(self):
        with self.assertRaises(Quiz.DoesNotExist):
            self.stud_response4 = QuizTakerResponse.objects.create(quiztaker=self.quiz_taker1, question=self.question2, answer=self.answer3)

class QuizViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.subject1 =Subject.objects.create(name="Science")
        # cls.subject2 =Subject.objects.create(name="Mathematics")
        cls.teacher = create_custom_user2(username="teacher_1",password="secure",is_teacher=True)
        cls.quiz1 = Quiz.objects.create(name="First Quiz", subject=cls.subject1, owner=cls.teacher)
        cls.quiz2 = Quiz.objects.create(name="Second Quiz", subject=cls.subject1, owner=cls.teacher)


    def test_quiz_list(self):
        # response = self.client.get('/quiz/')
        response = self.client.get(reverse('quiz_list'))
        #check if the response is 200 OK
        self.assertEqual(response.status_code,200)
        self.assertContains(response,text=self.quiz1.name,count=1,status_code=200)
        self.assertIn(self.quiz2, response.context['object_list'])
        self.assertEqual(len(response.context['object_list']),2)

    def test_quiz_create(self):
        self.factory = RequestFactory()
        request = self.factory.get(reverse('create_quiz'))
        request.user = create_custom_user(username="stud1",is_teacher=True)
        response = CreateQuizView.as_view()(request)
        self.assertEqual(response.status_code,200)

    #No reason to test this
    def test_quiz_details(self):
        response = self.client.get(reverse('quiz_detail', args=[self.quiz1.pk]))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, self.quiz1.name)
        #test question list in the context
        self.assertEqual(len(response.context['question_list']),len(self.quiz1.get_questions()))

class QuizTakeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_custom_user(username="studentias",is_student=True, password="kriumkram")
        cls.user2 = create_custom_user(username="stud2",is_student=True)
        cls.stud1 = create_student(user=cls.user)
        cls.stud2 = create_student(user=cls.user2)
        cls.subj1 = create_subject("Science")
        #Add the subject to student interests
        cls.stud1.interests.add(cls.subj1)

        cls.teacher = create_custom_user2(username="teacher_1",password="secure",is_teacher=True)
        cls.quiz = create_quiz(name="First Science Quiz",subject=cls.subj1,owner=cls.teacher)
        # cls.quiz2 = create_quiz(name="Second Science Quiz",subject=cls.subj1)
        cls.question1 = create_question(question="Does Mars support life?",quiz=cls.quiz)
        cls.answer1 = create_answer(answer="Yes",question=cls.question1)
        cls.answer2 = create_answer(answer="Who knows",question=cls.question1, is_correct=True)
        cls.answer3 = create_answer(answer="No",question=cls.question1)

    def setUp(self):
        self.factory = RequestFactory()

        self.quiz1 = Quiz.objects.get(id=self.quiz.id)
        # self.quiz2 = Quiz.objects.get(id=self.quiz2.id)
        self.question_list = self.quiz1.get_questions()

    def test_view_response(self):
        self.response = self.client.get(reverse('take_quiz', args=[self.quiz1.pk]))
        # self.assertIsInstance(self.quiz1,Quiz)
        # self.assertEqual(self.response.status_code,200) # Status codeshould be 302->>redirects to login
        redirect_url = reverse('login')+f'?next=/quiz/{self.quiz1.pk}/take/'
        self.assertRedirects(self.response, redirect_url)

    def test_post_start_quiz(self):

        request = self.factory.post('take_quiz',{'start_quiz':'quiz_name'})
        request.user = self.user
        request.session = {}
        response = quiz_taking(request,self.quiz1.pk)

        #test response
        self.assertEqual(response.status_code,200)
        #test quiztaker in session
        self.assertEqual(request.session['quiz_taker'],self.user.username)
        #test quiz taken
        self.assertEqual(request.session['quiz_taken'],self.quiz1.name)

    def test_successful_post(self):
        create_quiz_taker(quiz=self.quiz1,student=self.stud1)

        request = self.factory.post('take_quiz',{'question':self.question1,'question_choice':self.answer3})
        request.user = self.user
        request.session = {}
        response = quiz_taking(request,self.quiz1.pk)

        self.assertEqual(response.status_code,200)
        #test the one answering the question
        self.assertEqual(request.session['taker'],self.user.username)
        # #test the redirect of final question i.e self.question1 to the results page
        # self.assertEqual(response.redirect_chain, f'http://127.0.0.1:8000/quiz/{self.quiz1.pk}/result/')

    def test_unsuccessful_post(self):
        create_quiz_taker(quiz=self.quiz1,student=self.stud1)

        request = self.factory.post('take_quiz',{'question':self.question1,'question_choice':'Just kidding'})
        request.user = self.user
        request.session = {}

        self.assertRaises(Answer.DoesNotExist, quiz_taking, request, self.quiz1.pk)

class QuizResultsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_custom_user(username="studentias",is_student=True, password="kriumkram")
        cls.stud1 = create_student(user=cls.user)
        cls.subj1 = create_subject("Science")
        cls.teacher = create_custom_user2(username="teacher_1",password="secure",is_teacher=True)
        cls.quiz1 = create_quiz(name="First Science Quiz",subject=cls.subj1,owner=cls.teacher)
        cls.question1 = create_question(question="Does Mars support life?",quiz=cls.quiz1)
        cls.answer1 = create_answer(answer="Yes",question=cls.question1)

    def setUp(self):
        self.stud1.interests.add(self.subj1)
        self.quiz_taker = create_quiz_taker(quiz=self.quiz1,student=self.stud1)
        self.quiz_taker_response = create_quiz_taker_response(quiztaker=self.quiz_taker,question=self.question1,answer=self.answer1)

    def test_final_post_results_redirect(self):
        # self.client.login(username=self.user.username, password='kriumkram')
        # self.client.force_login(self.user)
        self.response = self.client.get('/quiz/1/result/',follow=True)
        print("|||||||||||||||||||||||||||||||||||||||||||||")
        print(self.response)
        print(self.response.redirect_chain)
        print(self.response.request)
        print("|||||||||||||||||||||||||||||||||||||||||||||")
