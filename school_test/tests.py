from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from .models import Question, ReadyTest, TestQuestions, TestToDo


class AcessePagesTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.student = User.objects.create(
            first_name="Rafael",
            last_name="Benicio",
            password="abc123456",
            username="Rafaelzinho",
        )

        self.student_2 = User.objects.create(
            first_name="Lucas",
            last_name="Germania",
            password="123abcdef",
            username="Luquinhas123",
        )

        self.question = Question.objects.create(
            question_text="Em Python, qual dos seguintes métodos é usado para converter um objeto em uma string?",
            question_subject="Python",
            difficulty_level=2,
            op1="to_string()",
            op2="str()",
            op3="convert_str()",
            op4="stringify()",
            answer=2,
        )
        self.test = ReadyTest.objects.create(
            test_name="Prova de Python",
            subject="Python",
            test_descripition="Quero saber o quanto você sabe de Python",
        )
        self.test_question = TestQuestions.objects.create(
            id_question=self.question, id_test=self.test
        )
        self.test_to_do = TestToDo.objects.create(
            id_test=self.test, id_student=self.student
        )

        self.student.save()
        self.student_2.save()
        self.question.save()
        self.test.save()
        self.test_question.save()
        self.test_to_do.save()

    # login
    def test_acesse_login_page(self):
        response = self.client.get(reverse("school_test:login"))

        self.assertEqual(response.status_code, 200)

    # admin
    def test_redirect_to_admin_page(self):
        response = self.client.get("/admin")

        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, "/admin/")

    def test_redirect_student_with_right_infos_to_home_page(self):
        login_form = {"username": "Rafaelzinho", "password": "abc123456"}

        response = self.client.post(reverse("school_test:validate"), login_form)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("school_test:home"))

    # validade
    def test_redirect_student_with_wrong_password_to_login_page(self):
        login_form = {"username": "Rafaelzinho", "password": "abc1ddd23459"}

        response = self.client.post(reverse("school_test:validate"), login_form)

        self.assertEqual(response.url, reverse("school_test:login"))
        self.assertEqual(response.status_code, 302)

    def test_redirect_student_with_wrong_username_to_login_page(self):
        login_form = {"username": "o", "password": "abc123456"}

        response = self.client.post(reverse("school_test:validate"), login_form)

        self.assertEqual(response.url, reverse("school_test:login"))
        self.assertEqual(response.status_code, 302)

    # home
    def test_redirect_acesse_in_home_page_without_autentication(self):
        response = self.client.get(reverse("school_test:home"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/school_test/login/?next=/school_test/home/")

    def test_acesse_home_page_with_autentication(self):
        login_form = {"username": "Rafaelzinho", "password": "abc123456"}

        self.client.force_login(self.student)
        self.client.post(reverse("school_test:validate"), login_form)

        response = self.client.get(reverse("school_test:home"))

        self.assertEqual(response.status_code, 200)

    # test
    def test_acesse_test_page_with_autentication(self):
        login_form = {"username": "Rafaelzinho", "password": "abc123456"}

        self.client.force_login(self.student)
        self.client.post(reverse("school_test:validate"), login_form)

        response = self.client.get(reverse("school_test:test", args=[self.test.id]))

        self.assertEqual(response.status_code, 200)

    def test_access_test_page_with_authentication_but_not_having_to_do_the_test(self):
        login_form = {"username": "Luquinhas123", "password": "123abcdef"}

        self.client.force_login(self.student_2)
        self.client.post(reverse("school_test:validate"), login_form)

        response = self.client.get(reverse("school_test:test", args=[self.test.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("school_test:home"))

    def test_redirect_acesse_in_test_page_without_autentication(self):
        response = self.client.get(reverse("school_test:test", args=[self.test.id]))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            f"/school_test/login/?next=/school_test/home/prova/{self.test.id}",
        )

    # result
    def test_redirect_not_expected_acesse_in_result_path(self):
        response = self.client.get(reverse("school_test:result"))

        self.assertEqual(response.url, "/school_test/login/?next=/school_test/result/")
        self.assertEqual(response.status_code, 302)

    def test_redirect_expected_acesse_in_result_path_with_right_info(self):
        test_form = {
            "id_student": str(self.student.id),
            "id_test": str(self.test.id),
            str(self.question.id): "2",
        }
        login_form = {"username": "Rafaelzinho", "password": "abc123456"}
        self.client.force_login(self.student)
        self.client.post(reverse("school_test:validate"), login_form)

        response = self.client.post(reverse("school_test:result"), test_form)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("school_test:home"))
        self.assertTrue(
            TestToDo.objects.get(
                id_student=self.student.id, id_test=self.test.id
            ).was_done
        )

    def test_redirect_expected_acesse_in_result_path_but_with_wrong_form_1(self):
        test_form = {
            "id_student": str(self.student.id),
            "id_test": str(self.test.id),
            "wd": "2",
        }
        login_form = {"username": "Rafaelzinho", "password": "abc123456"}

        self.client.force_login(self.student)
        self.client.post(reverse("school_test:validate"), login_form)

        response = self.client.post(reverse("school_test:result"), test_form)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("school_test:home"))
        self.assertFalse(
            TestToDo.objects.get(
                id_student=self.student.id, id_test=self.test.id
            ).was_done
        )

    def test_redirect_expected_acesse_in_result_path_but_with_wrong_form_2(self):
        test_form = {
            "id_student": str(self.student.id),
            "id_test": str(self.test.id),
        }
        login_form = {"username": "Rafaelzinho", "password": "abc123456"}

        self.client.force_login(self.student)
        self.client.post(reverse("school_test:validate"), login_form)

        response = self.client.post(reverse("school_test:result"), test_form)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("school_test:home"))
        self.assertFalse(
            TestToDo.objects.get(
                id_student=self.student.id, id_test=self.test.id
            ).was_done
        )

    def test_redirect_expected_acesse_in_result_path_but_with_wrong_form_3(self):
        test_form = {
            "id_student": str(self.student.id),
            str(self.question.id): "2",
        }
        login_form = {"username": "Rafaelzinho", "password": "abc123456"}
        self.client.force_login(self.student)
        self.client.post(reverse("school_test:validate"), login_form)

        response = self.client.post(reverse("school_test:result"), test_form)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("school_test:home"))
        self.assertFalse(
            TestToDo.objects.get(
                id_student=self.student.id, id_test=self.test.id
            ).was_done
        )

    def test_redirect_expected_acesse_in_result_path_but_with_wrong_form_4(self):
        test_form = {
            "id_test": str(self.test.id),
            str(self.question.id): "2",
        }
        login_form = {"username": "Rafaelzinho", "password": "abc123456"}

        self.client.force_login(self.student)
        self.client.post(reverse("school_test:validate"), login_form)

        response = self.client.post(reverse("school_test:result"), test_form)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("school_test:home"))
        self.assertFalse(
            TestToDo.objects.get(
                id_student=self.student.id, id_test=self.test.id
            ).was_done
        )

    # logout
    def test_redirect_acesse_in_logout_path_and_logout(self):
        login_form = {"username": "Rafaelzinho", "password": "abc123456"}

        self.client.force_login(self.student)
        self.client.post(reverse("school_test:validate"), login_form)

        response_1 = self.client.get(reverse("school_test:home"))
        response_2 = self.client.get(reverse("school_test:logout"))
        response_3 = self.client.get(reverse("school_test:home"))

        self.assertEqual(response_1.status_code, 200)

        self.assertEqual(response_2.status_code, 302)
        self.assertEqual(response_2.url, reverse("school_test:login"))

        self.assertEqual(response_3.status_code, 302)
        self.assertEqual(response_3.url, "/school_test/login/?next=/school_test/home/")
