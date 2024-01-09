from django.contrib import admin

from .models import *
# Register your models here.
class TestQuestionsInline(admin.StackedInline):
    model = TestQuestions

class StudentClassInline(admin.TabularInline):
    model = StudentClass
    extra = 1
    
class TestToDoInline(admin.TabularInline):
    model = TestToDo
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Student Infos", {"fields": ["first_name","last_name","password"]}),
    ]
    inlines = [StudentClassInline,TestToDoInline]

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main Infos", {"fields": ["question_text","question_subject","difficulty_level"]}),
        ("Option to Choice",{"fields":["op1","op2","op3","op4"]}),
        ("Answer",{"fields":["answer"]}),
    ]
    list_display = ["question_text","question_subject","create_date",]

class ReadyTestAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Main Infos", {"fields": ["test_name","subject","test_descripition"]}),
    ]
    inlines = [TestQuestionsInline]
    list_display = ["test_name","subject"]

class TestToDoAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Student and Test", {"fields": ["id_student","id_test",]}),
        ("Results", {"fields": ["was_done","grade",]}),
    ]
    list_display = ["id_student","was_done","grade"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(ReadyTest, ReadyTestAdmin)
admin.site.register(Student,StudentAdmin)
admin.site.register(TestToDo,TestToDoAdmin)