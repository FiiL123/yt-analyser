import os

import orjson as json
from django.shortcuts import redirect, render

from web import settings as web_settings
from web.analyser.models import Creator, VideoRecord

from .forms import UploadFileForm


def home(request):
    context = {
        "videos_count": VideoRecord.objects.count(),
        "videos": VideoRecord.objects.all(),
        "creator_count": Creator.objects.count(),
    }

    return render(request, "home.html", context)


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        # print(request.FILES["file"])
        if form.is_valid():
            path = handle_uploaded_file(request.FILES["file"])
            process_history_json(path)
            return redirect("home")
    else:
        form = UploadFileForm()
    return render(request, "upload.html", {"form": form})


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
    Creator.objects.all().delete()
    VideoRecord.objects.all().delete()
    with open(file_path, "r") as f:
        data = json.loads(f.read())
        print(len(data))
        for record in data:
            if "subtitles" in record:
                title = record["title"][8:]
                creator_name = record["subtitles"][0]["name"]
                if c := Creator.objects.filter(name=creator_name):
                    creator = c.get()
                    creator.times_watched = creator.times_watched + 1
                else:
                    creator = Creator.create(creator_name, record["subtitles"][0]["url"])
                creator.save()
                time_watched = record["time"]
                url = "missing"
                if "titleUrl" in record:
                    url = record["titleUrl"]

                video = VideoRecord.create(title, creator, time_watched, url)
                if video is not None:
                    video.save()
