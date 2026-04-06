import secrets
import string

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from polls.models import Poll, Choice


def index(request):
    return render(request, "polls/index.html")


def lab_entry(request):
    # already logged in? continue normally
    # if first time after logout, delete previous session
    # if login in, create new user session
    # if new session, populate sandbox polls to interact with
    if request.user.is_authenticated:
        return redirect('polls')

    username = "demo_user"
    alphabet = string.ascii_letters + string.digits
    random_password = ''.join(secrets.choice(alphabet) for _ in range(16))

    user, created = User.objects.get_or_create(username=username)

    if created:
        user.password = make_password(random_password)
        user.save()

    login(request, user)

    return redirect('polls')


def polls(request):
    lab_entry(request) # enter lab as a demo user
    polls = Poll.objects.all()
    return render(request, 'polls/polls.html', {'polls': polls})


def detail(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/detail.html', {'poll': poll})


@login_required()
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    try:
        choice_id = request.POST['choice']
        selected_choice = get_object_or_404(Choice, pk=choice_id)
        selected_choice.votes += 1
        selected_choice.save()
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'poll': poll, "error_message": "must select a choice"})
    return redirect('results', poll.id)


def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    return render(request, 'polls/results.html', {"poll": poll})
