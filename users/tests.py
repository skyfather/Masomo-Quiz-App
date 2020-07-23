from django.test import TestCase
# from django_webtest import WebTest
from django.urls import reverse

from . models import CustomUser, Student
from learning.models import Subject
# Create your tests here.


def create_custom_user(username,is_student=False,is_teacher=False,password="secure"):
    custom_user = CustomUser.objects.create(username=username,is_student=is_student,is_teacher=is_teacher)
    # custom_user.set_password(password)
    return custom_user
    # CustomUser.objects.create(username="stud1",email="std1@students.com", is_student=True)
def create_student(user):
    return Student.objects.create(user=user)

def create_subject(name):
    return Subject.objects.create(name=name)

class StudentTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_custom_user(username="studentias",is_student=True, password="kriumkram")
        cls.stud = create_student(user=cls.user)

    def setUp(self):
        self.stud1 = Student.objects.get(user=self.stud)
        self.subj1 = create_subject("Science")
        self.subj2 = create_subject("Mathematics")
        self.subj3 = create_subject("English")
        self.stud1.interests.add(self.subj1)
        self.subj2.interested_students.add(self.stud1)

    def test_student_created(self):
        self.assertEqual(self.stud1.user.username,self.user.username)

    def test_student_interests(self):
        self.assertEqual(self.stud1.interests.count(),self.stud1.get_interests().count())
        self.assertIn(self.subj2, self.stud1.get_interests())
        self.assertNotIn(self.subj3, self.stud1.get_interests())

class StudentSignUpViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_custom_user(username="studentias",is_student=True, password="kriumkram")
        cls.stud1 = create_student(user=cls.user)

    def setUp(self):
        pass
    def test_is_student(self):
        # self.client.login(username=self.user.username, password='kriumkram')
        # self.client.force_login(self.user)
        self.response = self.client.post(reverse('student_signup'),{'username':self.user.username,'password1':'kriumkram','password2':'kriumkram'},follow=True)
        print("|||||||||||||||||||||||||||||||||||||||||||||")
        print(self.response)
        print(self.response.redirect_chain)
        print(self.response.request)
        print("|||||||||||||||||||||||||||||||||||||||||||||")
        #test if the user_type is student
        self.assertEqual(self.response.context['user_type'],'student')

class TeacherSignUpViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = create_custom_user(username="teacher1",is_teacher=True, password="kriumkram")
        # cls.stud1 = create_student(user=cls.user)

    def setUp(self):
        pass
    def test_is_teacher(self):
        # self.client.login(username=self.user.username, password='kriumkram')
        # self.client.force_login(self.user)
        self.response = self.client.post(reverse('teacher_signup'),{'username':self.user.username,'password1':'kriumkram','password2':'kriumkram'},follow=True)
        print("|||||||||||||||||||||||||||||||||||||||||||||")
        print(self.response)
        print(self.response.redirect_chain)
        print(self.response.request)
        print("|||||||||||||||||||||||||||||||||||||||||||||")
        #test if the user_type is student
        self.assertEqual(self.response.context['user_type'],'teacher')
