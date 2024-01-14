from ..models import Question, ReadyTest, TestQuestions, TestToDo


def calculate_test_grade(id_question_and_choice: dict) -> float:
    weight = 10 / len(id_question_and_choice)
    right_answers = 0

    for id_question in id_question_and_choice:
        asw = Question.objects.get(id=id_question).answer
        if asw == int(id_question_and_choice[id_question]):
            right_answers += 1

    return right_answers * weight


def regist_student_test_grade(test_form: dict, grade: float) -> None:
    student_test = TestToDo.objects.get(
        id_test=int(test_form["id_test"]), id_student=int(test_form["id_student"])
    )
    if not (student_test.was_done):
        student_test.grade = grade
        student_test.was_done = True
        student_test.save()


def enable_student_to_make_the_test(test_form: dict) -> None:
    student_test = TestToDo.objects.get(
        id_test=int(test_form["id_test"]), id_student=int(test_form["id_student"])
    )
    if not (student_test.was_done):
        student_test.was_done = True
        student_test.save()


def remove_identification_data(test_form: dict) -> dict:
    return {
        field_name: test_form[field_name]
        for field_name in test_form
        if field_name != "id_student"
        and field_name != "csrfmiddlewaretoken"
        and field_name != "id_test"
    }
