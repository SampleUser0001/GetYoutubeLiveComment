# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, timezone
import settings
import requests
import locale
import json
import time

# 動画情報を取得するAPI。ActiveLiveChatIDを取得するために使う。
VIDEO_API_URL='https://www.googleapis.com/youtube/v3/videos'

# コメントを取得するAPI。
LIVE_CHAT_API_URL='https://www.googleapis.com/youtube/v3/liveChat/messages'

# 待ち時間取得キー
KEY_POLLING_INTERVAL_MILLIS='pollingIntervalMillis'

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
        print(result)
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

def writeLiveComments(liveComments):
    """ 取得したLiveのコメントをファイルに書き込む。
    書き込んだファイルのファイルパスを返す。
    ファイルパスはapp/comments_${LiveID}_%Y%m%d_%H%M%S.json
    引数がNoneの場合、何もせずにNoneを返す。
    """
    json_file_path = None
    
    if liveComments is not None:
        # コメントが取得できた場合、ファイルに書き込む。
    
        # 書き込みファイルのファイル名を生成する。
        DATE_FORMAT='%Y%m%d_%H%M%S'
        JST = timezone(timedelta(hours=+9), 'JST')
        now = datetime.now(JST).strftime(DATE_FORMAT)
        COMMENTS_FILE='output/comments_' + settings.ENV_DIC[ENV_KEY_LIVE_ID] + '_' + now + '.json'
    
        json_file_path = 'app/' + COMMENTS_FILE
    
        # エンコード回避しないならencodingの記載は不要
        with open(COMMENTS_FILE, mode='w', encoding='utf-8') as f:
            # エンコード回避
            f.write(json.dumps(liveComments, ensure_ascii=False))
    
    return json_file_path

if __name__ == '__main__':
    live_chat_id = getActiveLiveChatID()
    if live_chat_id is not None:
        while True:
            # コメント取得。
            liveComments = getLiveComments(live_chat_id)
            
            # ファイル書き込み
            json_file_path = writeLiveComments(liveComments)

            # コメント出力先ファイルパスを標準出力する。
            print('filename:', json_file_path , flush=True)
            try:
#                sleeptime = float(liveComments[KEY_POLLING_INTERVAL_MILLIS])
                sleeptime = 8000
            except TypeError:
                print("{} is not found.".format(KEY_POLLING_INTERVAL_MILLIS))
#                sleeptime = float(4500)
            time.sleep(sleeptime/1000)
