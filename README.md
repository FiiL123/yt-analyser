# yt-analyser
An app that lets you explore your YouTube watch history data

## Where to get the data
The data must be requested from Google via [Takeout](https://takeout.google.com/) where you only need to select `YouTube and YouTube Music` > `history`(in json format).

## Process
You upload YT watch history data into the app. After upload you can safely go back to the home page. Unfortunatly the way application gets metadata off of videos - [yt-dlp](https://github.com/yt-dlp/yt-dlp) extractor takes quite some time as we do requests for each video individually. With threading I was able to process about 8000 videos per hour.
