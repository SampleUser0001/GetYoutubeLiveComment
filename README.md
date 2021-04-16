# Get Youtube live comment

YoutubeのLive中のコメントを取得する。

## 準備

app/.envファイルを作成する。

``` env
# [Youtube]
YoutubeAPIKey=<APIキー>
LiveID=<取得したい配信のID>
```

## 実行

``` sh
docker-compose up
```

## 実行結果

```app/oputput```配下に```comments_${配信ID}_${実行時_年月日_時分秒}.json```ファイルが作成される。

## 備考

絵文字がうまく取得できない。

### API

``` sh
GOOGLE_API_KEY=${GoogleAPIのキー}
YOUTUBE_LIVE_ID=${配信ID}
curl -X GET https://www.googleapis.com/youtube/v3/videos?key=${GOOGLE_API_KEY}\&id=${YOUTUBE_LIVE_ID}\&part=liveStreamingDetails

YOUTUBE_LIVE_CHAT_ID=${activeLiveChatIDの値}
curl https://www.googleapis.com/youtube/v3/liveChat/messages?key=${GOOGLE_API_KEY}\&id=${YOUTUBE_LIVE_CHAT_ID}\&part=id,snippet,authorDetails
```
