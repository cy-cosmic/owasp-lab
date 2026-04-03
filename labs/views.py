from django.db import connection
from django.http import Http404, JsonResponse
from django.shortcuts import render

from polls.views import lab_entry


# Create your views here.
def index(request):
    lab_entry(request)
    return render(request, "labs/index.html", locals())


def broken_access_control(request):
    return render(request, "labs/baccess.html", locals())


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
