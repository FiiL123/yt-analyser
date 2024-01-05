import json
import os

from django.shortcuts import redirect, render

from web import settings as web_settings

from .forms import UploadFileForm


def home(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        # print(request.FILES["file"])
        if form.is_valid():
            path = handle_uploaded_file(request.FILES["file"])
            process_history_json(path)
            return redirect("home")
    else:
        form = UploadFileForm()
    return render(request, "home.html", {"form": form})


def handle_uploaded_file(uploaded_file):
    # Define the upload path
    upload_path = os.path.join(web_settings.MEDIA_ROOT, "uploads", uploaded_file.name)
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    # Save the file to the server
    with open(upload_path, "wb+") as destination:

        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return upload_path


def process_history_json(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
        for record in data:
            print(record["title"])
