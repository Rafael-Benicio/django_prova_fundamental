from django.test import TestCase
from django.test import Client
from .models import Student,Question,ReadyTest,TestQuestions,TestToDo
from django.urls import reverse
from http.cookies import SimpleCookie


class AcessePagesTestCase(TestCase):
     def setUp(self):
          self.client=Client()
          self.student=Student.objects.create(first_name='Rafael',last_name='Benicio',password='abc123456')
          self.student_2=Student.objects.create(first_name='Lucas',last_name='Germania',password='123abcdef')
          self.question=Question.objects.create(question_text='Em Python, qual dos seguintes métodos é usado para converter um objeto em uma string?',question_subject='Python',difficulty_level=2,op1='to_string()',op2='str()',op3='convert_str()',op4='stringify()',answer=2)
          self.test=ReadyTest.objects.create(test_name='Prova de Python',subject='Python',test_descripition='Quero saber o quanto você sabe de Python')
          self.test_question=TestQuestions.objects.create(id_question=self.question,id_test=self.test)
          self.test_to_do=TestToDo.objects.create(id_test=self.test,id_student=self.student)


     def test_acesse_login_page(self):
          response=self.client.get(reverse("school_test:login",))
          self.assertEqual(response.status_code,200)

     def test_redirect_to_admin_page(self):
          response=self.client.get('/admin')
          self.assertEqual(response.status_code,301)

     def test_acesse_home_page_without_autentication(self):
          response=self.client.get(reverse('school_test:home'))
          self.assertEqual(response.status_code,401)

     def test_acesse_home_page_with_autentication(self):
          self.client.cookies=SimpleCookie({'id_student_cookie': str(self.student.id)})
          response=self.client.get(reverse('school_test:home'))
          self.assertEqual(response.status_code,200)

     def test_redirect_student_with_right_password_to_home_page(self):
          form={'id_student':str(self.student.id),'password':'abc123456'}
          response=self.client.post(reverse("school_test:validate",),form)
          self.assertEqual(response.status_code,302)

     def test_redirect_student_with_wrong_password_to_login_page(self):
          form={'id_student':str(self.student.id),'password':'abc123459'}
          response=self.client.post(reverse("school_test:validate",),form)
          self.assertEqual(response.status_code,401)

     def test_acesse_test_page_with_autentication(self):
          self.client.cookies=SimpleCookie({'id_student_cookie': str(self.student.id)})
          response=self.client.get(reverse('school_test:test', args=[self.test.id,]))
          self.assertEqual(response.status_code,200)

     def test_access_test_page_with_authentication_but_not_having_to_do_the_test(self):
          self.client.cookies=SimpleCookie({'id_student_cookie': str(self.student_2.id)})
          response=self.client.get(reverse('school_test:test', args=[self.test.id,]))
          self.assertEqual(response.status_code,302)

     def test_acesse_test_page_without_autentication(self):
          response=self.client.get(reverse('school_test:test', args=[self.test.id,]))
          self.assertEqual(response.status_code,401)

     def test_redirect_not_expected_acesse_in_result_path(self):
          response=self.client.get(reverse('school_test:result',))
          self.assertEqual(response.status_code,403)

     def test_redirect_expected_acesse_in_result_path(self):
          form={'id_student':str(self.student.id),'id_test':str(self.test.id),str(self.question.id):'2'}
          response=self.client.post(reverse("school_test:result",),form)
          self.assertEqual(response.status_code,302)

     def test_redirect_not_authenticated_acesse_in_logout(self):
          response=self.client.get(reverse('school_test:logout',))
          self.assertEqual(response.status_code,302)