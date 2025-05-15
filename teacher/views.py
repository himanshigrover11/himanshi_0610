from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from quiz import models as QMODEL
from student import models as SMODEL
from quiz import forms as QFORM

from django.shortcuts import render
from teacher.models import Teacher
from django.db.models import Sum

def admin_view_teacher(request):
    teachers = Teacher.objects.all()
    pending_teachers = Teacher.objects.filter(status=False).count()
    approved_teachers = Teacher.objects.filter(status=True).count()
    salary_sum = Teacher.objects.filter(status=True).aggregate(Sum('salary'))['salary__sum'] or 0

    context = {
        'teachers': teachers,
        'pending_teachers': pending_teachers,
        'approved_teachers': approved_teachers,
        'salary_sum': salary_sum
    }
    return render(request, 'quiz/admin_teacher.html', context)


def teacherclick_view(request):
    
    if request.user.is_authenticated:
        return HttpResponseRedirect('/afterlogin')
    return render(request, 'teacher/teacherclick.html')


def teacher_signup_view(request):
    userForm = forms.TeacherUserForm()
    teacherForm = forms.TeacherForm()
    if request.method == 'POST':
        userForm = forms.TeacherUserForm(request.POST)
        teacherForm = forms.TeacherForm(request.POST, request.FILES)
        if userForm.is_valid() and teacherForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            teacher = teacherForm.save(commit=False)
            teacher.user = user
            teacher.save()
            group, _ = Group.objects.get_or_create(name='TEACHER')
            group.user_set.add(user)
            return HttpResponseRedirect('teacherlogin')
    return render(request, 'teacher/teachersignup.html', {'userForm': userForm, 'teacherForm': teacherForm})

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    context = {
        'total_course': QMODEL.Course.objects.count(),
        'total_question': QMODEL.Question.objects.count(),
        'total_student': SMODEL.Student.objects.count()
    }
    return render(request, 'teacher/teacher_dashboard.html', context)

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_exam_view(request):
    return render(request, 'teacher/teacher_exam.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_exam_view(request):
    courseForm = QFORM.CourseForm()
    if request.method == 'POST':
        courseForm = QFORM.CourseForm(request.POST)
        if courseForm.is_valid():
            courseForm.save()
            return HttpResponseRedirect('/teacher/teacher-view-exam')
    return render(request, 'teacher/teacher_add_exam.html', {'courseForm': courseForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_exam_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_exam.html', {'courses': courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def delete_exam_view(request, pk):
    QMODEL.Course.objects.filter(id=pk).delete()
    return HttpResponseRedirect('/teacher/teacher-view-exam')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_question_view(request):
    return render(request, 'teacher/teacher_question.html')

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_add_question_view(request):
    questionForm = QFORM.QuestionForm()
    if request.method == 'POST':
        questionForm = QFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            course = QMODEL.Course.objects.get(id=request.POST.get('courseID'))
            question.course = course
            question.save()
            return HttpResponseRedirect('/teacher/teacher-view-question')
    return render(request, 'teacher/teacher_add_question.html', {'questionForm': questionForm})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def teacher_view_question_view(request):
    courses = QMODEL.Course.objects.all()
    return render(request, 'teacher/teacher_view_question.html', {'courses': courses})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def see_question_view(request, pk):
    questions = QMODEL.Question.objects.filter(course_id=pk)
    return render(request, 'teacher/see_question.html', {'questions': questions})

@login_required(login_url='teacherlogin')
@user_passes_test(is_teacher)
def remove_question_view(request, pk):
    QMODEL.Question.objects.filter(id=pk).delete()
    return HttpResponseRedirect('/teacher/teacher-view-question')
