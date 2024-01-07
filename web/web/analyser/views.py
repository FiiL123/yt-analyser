import os
import time
from concurrent.futures import ThreadPoolExecutor

import orjson as json
from django.db.models import Count
from django.shortcuts import redirect, render
from yt_dlp import YoutubeDL

from web import settings as web_settings
from web.analyser.models import Creator, VideoRecord

from .empyLogger import Logger
from .forms import DataFilterForm, UploadFileForm

ydl_opts = {
    "logger": Logger(),
    "ignoreerrors": True,
    "extractor_args": {
        "youtube": {"skip": ["translated_subs", "hls", "dash"], "player_skip": ["configs", "webpage", "js"]}
    },
}
ydls = []
for _ in range(32):
    ydls.append(YoutubeDL(ydl_opts))

yd_counter = 0


def home(request):
    if request.method == "POST":
        form = DataFilterForm(request.POST)
        if form.is_valid():
            pass
    else:
        pass
    form = DataFilterForm()

    top_creators = Creator.objects.order_by("-times_watched")[:10]
    top_videos = (
        VideoRecord.objects.values("title", "categories")
        .annotate(times_watched=Count("title"))
        .order_by("-times_watched")[:10]
    )
    top_categories = (
        VideoRecord.objects.values("categories")
        .annotate(times_watched=Count("categories"))
        .order_by("-times_watched")[:10]
    )
    context = {
        "videos_count": VideoRecord.objects.count(),
        "videos": VideoRecord.objects.all(),
        "creator_count": Creator.objects.count(),
        "creators": Creator.objects.all(),
        "top_creators": top_creators,
        "top_videos": top_videos,
        "top_categories": top_categories,
        "form": form,
    }

    return render(request, "home.html", context)


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
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
    with open(file_path, "r") as f:
        data = json.loads(f.read())
        with ThreadPoolExecutor(max_workers=32) as executor:
            executor.map(process_record, data)


def process_record(record):
    start = time.time()
    if "subtitles" in record:
        title = record["title"][8:]
        creator_name = record["subtitles"][0]["name"]
        time_watched = record["time"]
        if VideoRecord.objects.filter(title=title, time_watched=time_watched).count() == 0:
            if c := Creator.objects.filter(name=creator_name):
                creator = c.get()
                creator.times_watched = creator.times_watched + 1
            else:
                creator = Creator.create(creator_name, record["subtitles"][0]["url"])
            creator.save()
            url = "missing"
            if "titleUrl" in record:
                url = record["titleUrl"]
            metadata = get_metadata(url)
            video = VideoRecord.create(
                title,
                creator,
                time_watched,
                url,
                metadata["duration"],
                ",".join(metadata["categories"]),
                ",".join(metadata["tags"]),
            )
            if video is not None:
                video.save()
        end = time.time()
        dur = end - start
        print(f"Just processed {dur} [{creator_name}]{title} from {time_watched}.")


def get_metadata(url):
    global yd_counter
    ydl = ydls[yd_counter % 32]
    yd_counter += 1
    try:
        info_dict = ydl.extract_info(url, download=False, process=False)
        ret = {"duration": info_dict["duration"], "categories": info_dict["categories"], "tags": info_dict["tags"]}
        return ret
    except Exception:
        print("FAILED GETTING METADATA")
        ret = {"duration": 0, "categories": [], "tags": []}
        return ret
