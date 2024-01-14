from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import TestToDo
from .utils import build_data_of_pages as build_data
from .utils import calculate_test_result as calculate_test


def user_login(request) -> HttpResponse:
    return render(request, "school_test/login.html")


def user_login_validate(request) -> HttpResponseRedirect:
    try:
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user == None:
            raise Exception("wrong username or passoword")

    except Exception as err:
        print(f"Login Erro : {err}")
        return redirect(reverse("school_test:login"))
    else:
        request.session["user_id"] = user.id
        login(request, user)
        return redirect(reverse("school_test:home"))


@login_required(login_url="/school_test/login/")
def home(request) -> HttpResponse:
    context = {
        "student_tests": build_data.build_list_of_tests(
            request.session.get("user_id", None)
        )
    }
    return render(request, "school_test/home.html", context, status=200)


@login_required(login_url="/school_test/login/")
def student_test(request, id_test: int) -> HttpResponse:
    try:
        id_student = request.session.get("user_id", None)
        student_test = TestToDo.objects.get(id_student=id_student, id_test=id_test)
    except TestToDo.DoesNotExist as cont_not_exist:
        print(f" Erro, student test not finded : {cont_not_exist}")
        return redirect(reverse("school_test:home"))
    else:
        context = {"test": build_data.build_student_test(id_student, id_test)}
        return render(request, "school_test/test.html", context, status=200)


@login_required(login_url="/school_test/login/")
def result_calculate(request) -> HttpResponseRedirect:
    try:
        grade = calculate_test.calculate_test_grade(
            calculate_test.remove_identification_data(request.POST)
        )
        calculate_test.regist_student_test_grade(request.POST, grade)
    except Exception as err:
        print(f"Result Erro : {err}")
        calculate_test.enable_student_to_make_the_test(request.POST, grade)
    finally:
        return redirect(reverse("school_test:home"))


def user_logout(request) -> HttpResponseRedirect:
    logout(request=request)
    return redirect(reverse("school_test:login"))
