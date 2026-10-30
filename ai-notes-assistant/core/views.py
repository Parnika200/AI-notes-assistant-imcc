from django.http import HttpResponse


def home(request):
    return HttpResponse(
        """
        <h1>AI Notes Assistant</h1>
        <p>Your project is running with Django and SQLite.</p>
        """
    )