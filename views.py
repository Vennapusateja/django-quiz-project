
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Question, Choice, Submission


@login_required
def submit(request):
    """
    Handles exam submission.
    Expects POST data with selected choices keyed by question id:
    e.g., choice_<question_id> = <choice_id>
    """
    if request.method == 'POST':
        questions = Question.objects.all()
        correct_count = 0
        total_score = 0

        for question in questions:
            choice_key = f"choice_{question.id}"
            choice_id = request.POST.get(choice_key)

            if not choice_id:
                continue

            selected_choice = Choice.objects.get(id=choice_id)
            is_correct = selected_choice.is_correct

            Submission.objects.create(
                user=request.user,
                question=question,
                selected_choice=selected_choice,
                is_correct=is_correct
            )

            if is_correct:
                correct_count += 1
                total_score += question.grade

        request.session['correct_count'] = correct_count
        request.session['total_score'] = total_score
        request.session['total_questions'] = questions.count()

        messages.success(request, "Exam submitted successfully!")
        return redirect('show_exam_result')

    questions = Question.objects.prefetch_related('choices').all()
    return render(request, 'exam.html', {'questions': questions})


@login_required
def show_exam_result(request):
    """
    Displays exam result summary.
    """
    correct_count = request.session.get('correct_count', 0)
    total_score = request.session.get('total_score', 0)
    total_questions = request.session.get('total_questions', 0)

    context = {
        'correct_count': correct_count,
        'total_score': total_score,
        'total_questions': total_questions
    }

    return render(request, 'exam_result.html', context)
