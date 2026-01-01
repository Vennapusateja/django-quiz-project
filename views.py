from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Course, Question, Choice, Submission

@login_required
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = Submission.objects.create(
        user=request.user,
        course=course
    )

    for key, value in request.POST.items():
        if key.startswith('choice_'):
            choice = Choice.objects.get(id=value)
            submission.choices.add(choice)

    return show_exam_result(request, course_id, submission.id)

@login_required
def show_exam_result(request, course_id, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    questions = Question.objects.filter(course_id=course_id)

    total_score = 0
    possible_score = 0

    for question in questions:
        possible_score += question.grade
        if question.is_get_score(submission):
            total_score += question.grade

    context = {
        'grade': total_score,
        'possible_grade': possible_score
    }

    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
