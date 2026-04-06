from django.shortcuts import render
from django.urls import path
from labs import views

app_name = "labs"
urlpatterns = [
    path("", views.index, name="index"),
    path("baccess/", views.broken_access_control, name="bac"),
    path("baccess/polls/detail/<int:id>/", views.sandbox_polls_detail, name="sandbox_polls_detail"),
    path("cryptfail/", views.cryptographic_failures, name="cryptfail"),
    path("sqli/", views.sql_injection, name="sqli"),
    path('sqli/sqlajax/', views.sqlajax, name='sqlajax'),
    path("idesign/", views.insecure_design, name="idesign"),
    path("secmisconf/", views.security_misconfiguration, name="secmisconf"),
    path("vulncomp/", views.vulnerable_and_outdated_components, name="vulncomp"),
    path("idauthfail/", views.identification_and_auth_failures, name="idauthfail"),
    path("dtintegrityfail/", views.software_and_data_integrity_failures, name="dtintegrityfail"),
    path("seclogmonfail/", views.security_logs_and_monitoring_failures, name="seclogmonfail"),
    path("ssrf/", views.server_side_request_forgery, name="ssrf"),
]
