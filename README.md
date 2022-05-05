# Get Youtube live comment

YoutubeのLive中のコメントを取得する。

## 準備

app/.envファイルを作成する。

``` env
# [Youtube]
YoutubeAPIKey=<APIキー>
```

### YoutubeAPIKeyの確認

取得済みの想定で…確認方法を忘れがちなのでメモ。

1. GoogleCloudPlatform
2. 対象プロジェクト
3. 左上のハンバーガーメニュー
4. APIとサービス
5. 認証情報
6. APIキー

## 実行

``` sh
export LIVE_ID=${動画ID}
docker-compose run -e LiveID=${LIVE_ID} --rm python
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
