from ..models import Student, TestToDo, ReadyTest,Question, TestQuestions

def build_list_of_tests(id_student:int)-> list[dict]:
     student_and_associated_tests={'name_student':'','associated_tests':[]}
     
     student=Student.objects.get(id=id_student)
     student_and_associated_tests['name_student']=f"{student.first_name} {student.last_name}"

     id_from_student_and_readytests=TestToDo.objects.filter(id_student=id_student)
     for testtodo_object in id_from_student_and_readytests:
          test_entity=(ReadyTest.objects.get(id=testtodo_object.id_test.id))

          test_object={"test_name":test_entity.test_name}
          test_object["subject"]=test_entity.subject
          test_object["id"]=test_entity.id
          test_object["grade"]=testtodo_object.grade
          test_object["was_done"]=testtodo_object.was_done

          student_and_associated_tests['associated_tests'].append(test_object)

     return student_and_associated_tests

def build_student_test(id_student:int,id_test:int)->dict:
     questions=[]
     student_test=ReadyTest.objects.get(id=int(id_test))
     student=Student.objects.get(id=id_student)

     id_from_question_and_readytest=TestQuestions.objects.filter(id_test=id_test)
     for testquestion_object in id_from_question_and_readytest:
          questions.append(Question.objects.get(id=testquestion_object.id_question.id))

     test={'name':student_test.test_name, }
     test['id_student']=id_student
     test['id_test']=id_test
     test['name_student']=f"{student.first_name} {student.last_name}"
     test['subject']=student_test.subject
     test['questions']=questions
     return test