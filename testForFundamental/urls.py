
from django.contrib import admin
from django.urls import path,include
import school_test.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("school_test/", include("school_test.urls")),
    path("", school_test.views.login),
]
