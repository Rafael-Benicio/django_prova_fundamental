from django.urls import path

import school_test.views

app_name="school_test"

urlpatterns = [
    path("", school_test.views.login, name="login"),
    path("logout/", school_test.views.user_logout, name="logout"),
    path("validate_user/", school_test.views.user_login_validate, name="validate"),
    path("result/", school_test.views.result_calculate, name="result"),
    path("home/", school_test.views.home, name="home"),
    path("home/prova/<int:id_test>", school_test.views.student_test, name="test"),
    # path("<int:id_student>/test/", school_test.views.home, name="home"),
]