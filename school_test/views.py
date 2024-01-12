from argon2 import PasswordHasher
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from .models import Student,TestToDo

from .asset import build_data_of_pages as build_data
from .asset import calculate_test_result as calculate_test
from .asset import login_redirect as lr

def login(request)->HttpResponse:
     return render(request, "school_test/login.html")

def user_login_validate(request)->HttpResponse:
     ph = PasswordHasher()
     id_student=request.POST["id_student"]
     try:
          student_entity = Student.objects.get(id=int(id_student))
          if not (ph.verify(student_entity.password, request.POST['password'])):
               raise "Wrong Password"
     except:
          return lr.redirect_user_to_login_page(request,"Seu Id ou Senha estão errados",request.POST["id_student"],)
     else:
          response= HttpResponseRedirect(reverse("school_test:home",))
          response.set_cookie('id_student_cookie', request.POST['id_student'])
          return response

def home(request)->HttpResponse:
     try:
          id_student= int(request.COOKIES['id_student_cookie'])
     except KeyError as err:
          print(f' Erro, Cookie : {err} not finded')
          return lr.redirect_user_to_login_page(request,"Ocorreu algum erro com seu acesso")
     else:
          context = {"student_tests": build_data.build_list_of_tests(id_student)}
          return render(request,"school_test/home.html",context,status=200)

def student_test(request,id_test:int)->HttpResponse:
     try:
          id_student= int(request.COOKIES['id_student_cookie'])
          student_test=TestToDo.objects.get(id_student=int(request.COOKIES['id_student_cookie']),id_test=id_test)
     except TestToDo.DoesNotExist as cont_not_exist:
          print(f' Erro, student test not finded : {cont_not_exist}')
          return HttpResponseRedirect(reverse("school_test:home",))
     except KeyError as err:
          print(f' Erro, Cookie : {err} not finded')
          return lr.redirect_user_to_login_page(request,"Ocorreu algum erro com seu acesso")
     else:
          context = {"test": build_data.build_student_test(id_student,id_test)}
          return render(request,"school_test/test.html",context,status=200)
     

def result_calculate(request)->HttpResponse:
     try: 
          grade=calculate_test.calculate_test_grade(calculate_test.remove_identification_data(request.POST))
          calculate_test.regist_student_test_grade(request.POST,grade)
          return HttpResponseRedirect(reverse("school_test:home",))
     except:
          return lr.redirect_user_to_login_page(request,"Ocorreu algum erro com seu acesso",status_code=403)

def user_logout(request)->HttpResponse:
     response= HttpResponseRedirect(reverse("school_test:login",))
     response.delete_cookie('id_student_cookie')
     return response

