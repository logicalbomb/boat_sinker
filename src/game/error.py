from django.shortcuts import render


def handle_create_error(request, error_text):
    # Go back to the index and show an error
    context = {
        "error_message": error_text,
    }
    return render(request, "game/create.html", context)
