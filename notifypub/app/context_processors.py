import os


def site_name(request):
    return {
        "site_name": os.getenv('APP_NAME', "NotifyPub")
    }


def logged_in(request):
    return {
        "logged_in": request.user.is_authenticated
    }
