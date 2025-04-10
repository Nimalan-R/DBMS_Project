from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Quiz, Question, Answer, Result, ResultDetail, Subject, UserProgress
import random
from datetime import datetime

def quiz_list(request):
    subject_id = request.GET.get('subject')
    subjects = Subject.objects.all()

    if subject_id:
        quizzes = Quiz.objects.filter(subject_id=subject_id)
    else:
        quizzes = Quiz.objects.all()

    return render(request, 'quiz_list.html', {'quizzes': quizzes, 'subjects': subjects, 'selected_subject': subject_id})

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = list(quiz.questions.all())
    selected_questions = random.sample(questions, min(quiz.total_questions, len(questions)))
    request.session['start_time'] = str(datetime.now())
    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': selected_questions})

@login_required
def submit_quiz(request, quiz_id):
    if request.method != 'POST':
        return redirect('quiz_list')

    quiz = get_object_or_404(Quiz, id=quiz_id)
    user = request.user
    score = 0
    total = 0
    details = []

    start_time = datetime.fromisoformat(request.session.get('start_time'))
    end_time = datetime.now()
    time_taken = (end_time - start_time).total_seconds()

    for key, value in request.POST.items():
        if key.startswith('question_'):
            qid = int(key.split('_')[1])
            question = get_object_or_404(Question, id=qid)
            selected_answer = get_object_or_404(Answer, id=int(value))
            correct = selected_answer.is_correct
            if correct:
                score += 1
            total += 1
            details.append((question, selected_answer, correct))

    result = Result.objects.create(user=user, quiz=quiz, score=score)
    for question, selected_answer, correct in details:
        ResultDetail.objects.create(result=result, question=question, selected_answer=selected_answer, is_correct=correct)

    # Update progress
    progress, created = UserProgress.objects.get_or_create(user=user)
    progress.total_quizzes_taken += 1
    progress.total_score += score
    progress.total_time_seconds += int(time_taken)
    progress.average_score = progress.total_score / progress.total_quizzes_taken
    progress.save()

    return redirect('view_result', result_id=result.id)

@login_required
def profile_view(request):
    user = request.user
    progress = getattr(user, 'progress', None)
    results = Result.objects.filter(user=user).order_by('-timestamp')

    return render(request, 'profile.html', {
        'progress': progress,
        'results': results
    })

@login_required
def view_result(request, result_id):
    result = get_object_or_404(Result, id=result_id, user=request.user)
    return render(request, 'view_result.html', {'result': result})

@login_required
def view_progress(request):
    progress = getattr(request.user, 'progress', None)
    return render(request, 'user_progress.html', {'progress': progress})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})