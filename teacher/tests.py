from django.test import TestCase
from django.contrib.auth.models import User
from .models import Teacher

class TeacherModelTest(TestCase):
    def test_teacher_creation(self):
        user = User.objects.create_user(username='teacheruser', password='testpass')
        teacher = Teacher.objects.create(user=user, address='123 Main St', mobile='1234567890')
        self.assertEqual(teacher.get_name, 'teacheruser ')