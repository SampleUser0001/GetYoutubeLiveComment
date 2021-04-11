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

```app/oputput```配下に```comments_${実行時_年月日_時分秒}.json```ファイルが作成される。

## 備考

絵文字がうまく取得できない。
