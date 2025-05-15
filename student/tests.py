from django.test import TestCase, Client
from django.contrib.auth.models import User, Group
from django.urls import reverse
from .models import Student

class StudentTests(TestCase):

    def setUp(self):
        # Create student group
        self.student_group, created = Group.objects.get_or_create(name='STUDENT')

        # Create test user and student
        self.user = User.objects.create_user(username='student1', password='testpass123', first_name='John', last_name='Doe')
        self.student = Student.objects.create(
            user=self.user,
            address='123 Test Street',
            mobile='1234567890'
        )
        self.student_group.user_set.add(self.user)
        self.client = Client()

    def test_student_creation(self):
        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(self.student.user.username, 'student1')
        self.assertEqual(self.student.get_name, 'John Doe')

    def test_student_login(self):
        login = self.client.login(username='student1', password='testpass123')
        self.assertTrue(login)

    def test_student_dashboard_access(self):
        # Unauthenticated user should be redirected
        response = self.client.get(reverse('student-dashboard'))
        self.assertEqual(response.status_code, 302)

        # Login and access dashboard
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('student-dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_dashboard.html')

    def test_student_signup_view_get(self):
        response = self.client.get(reverse('studentsignup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/studentsignup.html')

    def test_student_signup_view_post(self):
        response = self.client.post(reverse('studentsignup'), {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'username': 'jane123',
            'password': 'pass456',
            'address': '456 Test Lane',
            'mobile': '9876543210',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='jane123').exists())
        self.assertTrue(Student.objects.filter(user__username='jane123').exists())

    def test_student_exam_page_access(self):
        self.client.login(username='student1', password='testpass123')
        response = self.client.get(reverse('student-exam'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student/student_exam.html')

    def test_student_profile_string_representation(self):
        self.assertEqual(str(self.student), 'John')
