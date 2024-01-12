from argon2 import PasswordHasher
import datetime

from django.db import models
from django.utils.timezone import now
from django.db.models.signals import pre_save


# Questao(Id_Questão,Texto, Op1, Op2, Op3, Op4, Materia, data, Dificuldade, Resposta)
class Question(models.Model):
    question_text = models.CharField(max_length=2000, null=False)
    create_date = models.DateTimeField(default=now, editable=False)

    op1 = models.CharField(max_length=500, null=False)
    op2 = models.CharField(max_length=500, null=False)
    op3 = models.CharField(max_length=500, null=False)
    op4 = models.CharField(max_length=500, null=False)

    question_subject = models.CharField(max_length=10, null=False)
    difficulty_level = models.IntegerField(null=False)
    answer = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.question_text} | {self.question_subject} |Dif {self.difficulty_level}"


# Aluno (Id_Aluno,Nome_Aluno, Sobrenome_Aluno,Senha, Id_Classe)
class Student(models.Model):
    first_name = models.CharField(max_length=20, null=False)
    last_name = models.CharField(max_length=20, null=False)
    password = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"ID : {self.id} | Aluno : {self.first_name} {self.last_name}"


# Prova(Id_Prova, Nome_Prova ,Materia)
class ReadyTest(models.Model):
    test_name = models.CharField(max_length=200, null=False)
    subject = models.CharField(max_length=10, null=False)
    test_descripition = models.CharField(max_length=500)

    def __str__(self):
        return f"Prova : {self.test_name}"


class TestQuestions(models.Model):
    id_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    id_test = models.ForeignKey(ReadyTest, on_delete=models.CASCADE)

    def __str__(self):
        return f"Questão : {self.id_question} → {self.id_test}"


# Classes (Id_Classe, Id_Aluno ,Ano, Turma )
class StudentClass(models.Model):
    id_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.IntegerField(null=False)
    class_group = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.id_student} | Classe : {self.year}.{self.class_group}"


# ParaFazer(Id_Aluno, Id_Prova)
class TestToDo(models.Model):
    id_student = models.ForeignKey(Student, on_delete=models.CASCADE)
    id_test = models.ForeignKey(ReadyTest, on_delete=models.CASCADE)
    was_done = models.BooleanField(null=False, default=False)
    grade = models.FloatField(null=False, default=0)

    def __str__(self):
        return f"{self.id_student} → {self.id_test}"


def make_password_hasher(sender, instance, **kwargs):
    ph = PasswordHasher()
    if not instance.id:
        hash = ph.hash(instance.password)
        instance.password = hash
    else:
        current_instance = sender.objects.get(id=instance.id)
        if current_instance.password != instance.password:
            hash = ph.hash(instance.password)
            instance.password = hash


# Conecta a função ao sinal pre_save
pre_save.connect(make_password_hasher, sender=Student)
