from django.test import TestCase
from django.test import Client
from .models import Student
from django.urls import reverse


class AcessePagesTestCase(TestCase):
     def setUp(self):
          self.client=Client()
          self.student=Student.objects.create(first_name='Rafael',last_name='Benicio',password='abc123456')

     def test_acesse_login_page(self):
          response=self.client.get(reverse("school_test:login",))
          self.assertEqual(response.status_code,200)

     def test_redirect_to_admin_page(self):
          response=self.client.get("/admin")
          self.assertEqual(response.status_code,301)

     def test_acesse_home_page_without_autentication(self):
          response=self.client.get(reverse("school_test:home"))
          self.assertEqual(response.status_code,401)

     def test_redirect_student_to_home_page(self):
          form={'id_student':str(self.student.id),'password':'abc123456'}
          response=self.client.post(reverse("school_test:validate",),form)
          self.assertEqual(response.status_code,302)
     
     def test_redirect_not_authenticated_acesse_in_result(self):
          response=self.client.get(reverse("school_test:result",))
          self.assertEqual(response.status_code,403)

     def test_redirect_not_authenticated_acesse_in_logout(self):
          response=self.client.get(reverse("school_test:logout",))
          self.assertEqual(response.status_code,302)