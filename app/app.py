# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
import settings
import requests
import locale
import json

# 動画情報を取得するAPI。ActiveLiveChatIDを取得するために使う。
VIDEO_API_URL='https://www.googleapis.com/youtube/v3/videos'

# コメントを取得するAPI。
LIVE_CHAT_API_URL='https://www.googleapis.com/youtube/v3/liveChat/messages'

# envのキーを読み込む。
keyIndex = 0
ENV_KEY_YOUTUBE_KEY = settings.ENV_KEYS[keyIndex]; keyIndex = keyIndex + 1;
ENV_KEY_LIVE_ID = settings.ENV_KEYS[keyIndex]; keyIndex = keyIndex + 1;


def getActiveLiveChatID():
    """ ActiveLiveChatIDを取得する関数。
    取得できなかった場合はNoneを返す。
    """
    params = {
        'key':settings.ENV_DIC[ENV_KEY_YOUTUBE_KEY],
        'id':settings.ENV_DIC[ENV_KEY_LIVE_ID],
        'part':'liveStreamingDetails'}
    result = requests.get(VIDEO_API_URL, params=params).json()

    KEY = 'activeLiveChatId'
    if KEY in result['items'][0]['liveStreamingDetails'].keys():
        return result['items'][0]['liveStreamingDetails'][KEY]
    else:
        print(KEY, 'is None')
        return None

def getLiveComments(liveChatId):
    """ コメントを取得する関数。
    liveChatIdにはgetActiveLiveChatID関数で取得したactiveLiveChatIDを渡す。
    liveChatIdがNoneの場合、Noneを返す。
    また、コメントが取得できなかった場合もNoneを返す。
    """
    if(liveChatId is not None):
        params = {
            'key':settings.ENV_DIC[ENV_KEY_YOUTUBE_KEY],
            'liveChatId':liveChatId,
            'part':'id,snippet,authorDetails'
        }
        return requests.get(LIVE_CHAT_API_URL, params=params).json()
    else:
        print('Cannot get live comments.')
        return None

# コメント取得。
liveComments = getLiveComments(getActiveLiveChatID())

if liveComments is not None:
    # コメントが取得できた場合、ファイルに書き込む。

    # 書き込みファイルのファイル名を生成する。
    DATE_FORMAT='%Y%m%d_%H%M%S'
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST).strftime(DATE_FORMAT)
    COMMENTS_FILE='output/comments_' + now + '.json'

    # コメント出力先ファイルパスを標準出力する。…え？書き方がダサい？
    print('filename:', 'app/' + COMMENTS_FILE)

    # エンコード回避しないならencodingの記載は不要
    with open(COMMENTS_FILE, mode='w', encoding='utf-8') as f:
        # エンコード回避
        f.write(json.dumps(liveComments, ensure_ascii=False))

