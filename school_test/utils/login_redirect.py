from django.shortcuts import render
from django.http import HttpResponse


def redirect_user_to_login_page(
    request,
    message: str,
    current_id: str = "",
    current_password: str = "",
    status_code: int = 401,
) -> HttpResponse:
    return render(
        request,
        "school_test/login.html",
        {
            "error_message": message,
            "current_id": current_id,
            "current_password": current_password,
        },
        status=status_code,
    )
