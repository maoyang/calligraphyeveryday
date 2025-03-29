from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_channel_videos(api_key: str, channel_id: str):
    """
    獲取指定 YouTube 頻道的所有影片標題和 ID。

    Args:
        api_key: YouTube Data API v3 金鑰。
        channel_id: 目標 YouTube 頻道的 ID。

    Returns:
        一個包含影片資訊 (id, title) 的 list。
        如果發生錯誤則返回 None。
    """
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)

        # 1. 獲取頻道的 uploads playlist ID
        channel_response = youtube.channels().list(
            part='contentDetails',
            id=channel_id
        ).execute()

        if not channel_response.get('items'):
            print(f"錯誤：找不到頻道 ID {channel_id}")
            return None

        uploads_playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        # 2. 分頁獲取播放列表中的所有影片 ID
        video_ids = []
        next_page_token = None
        while True:
            playlist_response = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=uploads_playlist_id,
                maxResults=50, # API 每次最多返回 50 個
                pageToken=next_page_token
            ).execute()

            video_ids.extend([item['contentDetails']['videoId'] for item in playlist_response.get('items', [])])

            next_page_token = playlist_response.get('nextPageToken')
            if not next_page_token:
                break

        # 3. 分批獲取影片的標題 (一次最多請求 50 個影片的詳細資訊)
        all_videos_details = []
        for i in range(0, len(video_ids), 50):
            batch_ids = video_ids[i:i+50]
            videos_response = youtube.videos().list(
                part='snippet', # 我們只需要 snippet 中的 title
                id=','.join(batch_ids)
            ).execute()
            all_videos_details.extend([
                {'id': item['id'], 'title': item['snippet']['title']}
                for item in videos_response.get('items', [])
            ])

        print(f"成功獲取頻道 {channel_id} 的 {len(all_videos_details)} 部影片資訊。")
        return all_videos_details

    except HttpError as e:
        print(f"呼叫 YouTube API 時發生錯誤：{e}")
        return None
    except Exception as e:
        print(f"處理過程中發生預期外的錯誤：{e}")
        return None