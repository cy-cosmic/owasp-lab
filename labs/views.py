import random
import secrets
import string
import uuid

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db import connection
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from labs.models import SandboxPoll
from polls.models import User, Poll
from django.http import HttpResponse
from .utils import sign_role, verify_role


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
    # Create unique session_id
    if "lab_session" not in request.session:
        request.session["lab_session"] = str(uuid.uuid4())
    session_id = request.session["lab_session"]

    # CLEANUP: delete old sandbox polls for this session
    SandboxPoll.objects.filter(session_id=session_id).delete()

    # Create fresh sandbox polls
    for poll in Poll.objects.filter(is_production=True):
        SandboxPoll.objects.create(
            original_poll=poll,
            question=poll.question,
            session_id=session_id,
            is_modified=False
        )

    return redirect("labs:index")


def index(request):
    lab_entry(request)

    return render(request, "labs/index.html", locals())


def broken_access_control(request):
    polls = SandboxPoll.objects.filter(session_id=request.session["lab_session"])
    return render(request, "labs/baccess.html", locals())


def sandbox_polls_detail(request, id):
    try:
        poll = SandboxPoll.objects.get(id=id)
    except SandboxPoll.DoesNotExist:
        poll = None
    if request.method == 'POST' and 'edit-poll' in request.POST:
        if request.POST['edit-poll'] != "":
            new_poll_question = request.POST['edit-poll']
            SandboxPoll.objects.filter(id=id).update(question=new_poll_question)
            messages.success(request, f'Poll updated successfully!')
            return redirect('labs:sandbox_polls_detail', id)
        else:
            messages.error(request, 'You did not edit this poll!')
            return redirect('labs:sandbox_polls_detail', id)

    return render(request, 'labs/sandbox-poll-detail.html', locals())


def cryptographic_failures(request):
    return render(request, "labs/cryptfail.html", locals())


def sql_injection(request):
    return render(request, "labs/sqli.html", locals())


def sqlajax(request):
    q = request.GET.get("q", "")
    sql = f"""
            SELECT id, question, category
            FROM polls_poll
            WHERE question LIKE '%{q}%'
        """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    print(rows)
    data = [
        {
            "id": r[0],
            "question": r[1],
            "category": r[2],
        }
        for r in rows
    ]

    return JsonResponse({"results": data})


def insecure_design(request):
    return render(request, "labs/idesign.html", locals())


def security_misconfiguration(request):
    return render(request, "labs/secmisconf.html", locals())


def vulnerable_and_outdated_components(request):
    return render(request, "labs/vulncomp.html", locals())


def identification_and_auth_failures(request):
    return render(request, "labs/idauthfail.html", locals())


def software_and_data_integrity_failures(request):
    return render(request, "labs/dtintegrityfail.html", locals())


def security_logs_and_monitoring_failures(request):
    return render(request, "labs/seclogmonfail.html", locals())


def server_side_request_forgery(request):
    return render(request, "labs/ssrf.html", locals())


def cryptographic_failures_sandbox(request):
    cookie_name = "lab_auth"
    cookie = request.COOKIES.get(cookie_name)

    role = "guest"
    user_id = 101
    panel_title = "Sandbox Environment"
    message = "You are currently browsing with limited privileges."
    restricted_notice = "Administrative features are restricted."
    flag = None
    response = None
    # create guest cookie if none exists
    if not cookie:
        payload = {
            "user_id": 101,
            "role": "guest"
        }
        cookie = sign_role(payload)
        response = render(
            request,
            "labs/cryptfailsandbox.html",
            {
                "user_id": user_id,
                "role": role,
                "panel_title": panel_title,
                "message": message,
                "restricted_notice": restricted_notice,
                "flag": flag
            }
        )

        response.set_cookie(
            cookie_name,
            cookie,
            httponly=False  # visible in DevTools intentionally
        )

        return response

    # cookie exists → evaluate role
    try:
        data = verify_role(cookie)
        if data.get("role") == "admin":
            user_id = user_id
            role = "admin"
            panel_title = "Admin Control Panel"
            message = "Elevated privileges detected."
            restricted_notice = "Full administrative functionality enabled."
            flag = "crypto_privilege_escalation_success"

    except Exception:
        panel_title = "Invalid Session"
        message = "The session cookie could not be verified."
        restricted_notice = "Try generating a new session."

    return render(
        request,
        "labs/cryptfailsandbox.html",
        {
            "user_id": user_id,
            "role": role,
            "panel_title": panel_title,
            "message": message,
            "restricted_notice": restricted_notice,
            "flag": flag
        }
    )


def insecure_design_profile_sandbox(request):
    user = User.objects.first()  # demo_user is the only user
    # generate OTP
    if request.method == "POST" and request.POST.get("send-otp") == "sendotp":
        otp = str(random.randint(1000, 6999))
        request.session["password_reset_otp"] = otp
        request.session["otp_user"] = user.username
        send_mail(
            subject="Your password reset token",
            message=f"""
            Hello {user.username}
            Your password reset token is: {otp}.
            If you did not request this, ignore this email.""",
            from_email=None,
            recipient_list=[user.email], )
        messages.success(request,
                         "A password reset token was sent to your email. Enter it in the input below to reset your password."
                         )

        return redirect("labs:idesign_profile_sandbox")
    # verify OTP (vulnerable)
    if request.method == "POST" and request.POST.get("verify-otp"):
        submitted_otp = request.POST.get("otp")
        if submitted_otp == request.session.get("password_reset_otp"):
            messages.success(request, "OTP verified successfully. Password changed.")
        else:
            messages.error(request, "Invalid OTP")
        return redirect("labs:idesign_profile_sandbox")
    return render(request, "labs/idesign-profile.html", locals())


