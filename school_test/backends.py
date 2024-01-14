from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class StudentBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            student = User.objects.get(username=username)
        except User.DoesNotExist:
            return None

        if student.password == password:
            return student

        return None
