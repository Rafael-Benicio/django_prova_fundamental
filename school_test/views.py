from argon2 import PasswordHasher
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from .models import Student

from .asset import build_data_of_pages as build_data
from .asset import calculate_test_result as calculate_test

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
          return render(request,"school_test/login.html",{"error_message": "Seu Id ou Senha estão errados","current_id":request.POST["id_student"],"current_password":request.POST["password"]},status=401)
     else:
          response= HttpResponseRedirect(reverse("school_test:home",))
          response.set_cookie('id_student_cookie', request.POST['id_student'])
          return response

def home(request)->HttpResponse:
     try:
          id_student= int(request.COOKIES['id_student_cookie'])
     except KeyError as err:
          print(f' Erro, Cookie : {err} not finded')
          return render(request,"school_test/login.html",{"error_message": "Ocorreu algum erro com seu acesso","current_id":'',"current_password":''},status=401)
     else:
          context = {"student_tests": build_data.build_list_of_tests(id_student)}
          return render(request,"school_test/home.html",context)

def student_test(request,id_test:int)->HttpResponse:
     try:
          id_student= int(request.COOKIES['id_student_cookie'])
     except KeyError as err:
          print(f' Erro, Cookie : {err} not finded')
          return HttpResponseRedirect(reverse("school_test:login",))
     else:
          context = {"test": build_data.build_student_test(id_student,id_test)}
          return render(request,"school_test/test.html",context)
     

def result_calculate(request)->HttpResponse:
     try: 
          grade=calculate_test.calculate_test_grade(calculate_test.remove_identification_data(request.POST))
          calculate_test.regist_student_test_grade(request.POST,grade)
          return HttpResponseRedirect(reverse("school_test:home",))
     except:
          return render(request,"school_test/login.html",{"error_message": "Ocorreu algum erro com seu acesso","current_id":'',"current_password":''},status=403)

def user_logout(request)->HttpResponse:
     response= HttpResponseRedirect(reverse("school_test:login",))
     response.delete_cookie('id_student_cookie')
     return response

