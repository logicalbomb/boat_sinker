from django.shortcuts import render

import sentry_sdk


sentry_sdk.init("https://61842b75251a4ecbb84748556426aa60@sentry.io/1400606")


def handle_create_error(request, error_text):
    # Go back to the index and show an error
    context = {
        "error_message": error_text,
    }
    return render(request, "game/create.html", context)
