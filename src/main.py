from src.config_loader import load_config
from src.youtube_api import get_channel_videos
from src.classifier import classify_video_by_title # 或 classify_video_with_rules
# from src.classifier import load_categories # 如果使用 yaml 規則

def main():
    """程式主執行函數"""
    try:
        # 1. 載入設定
        config = load_config()
        api_key = config["api_key"]
        channel_id = config["channel_id"]

        # (可選) 載入分類規則
        # category_rules = load_categories()

        # 2. 獲取頻道影片
        print(f"正在從頻道 {channel_id} 獲取影片...")
        videos = get_channel_videos(api_key, channel_id)

        if not videos:
            print("無法獲取影片資訊，程式結束。")
            return

        # 3. 進行分類
        print("開始分類影片...")
        classified_videos = {} # 使用字典來存放分類結果 { "分類名稱": [影片清單] }

        for video in videos:
            video_id = video['id']
            title = video['title']
            # category = classify_video_with_rules(title, category_rules) # 使用 yaml 規則
            category = classify_video_by_title(title) # 使用寫在程式碼中的規則

            if category not in classified_videos:
                classified_videos[category] = []

            classified_videos[category].append({
                'title': title,
                'id': video_id,
                'url': f"https://www.youtube.com/watch?v={video_id}"
            })

        # 4. 輸出結果
        print("\n--- 分類結果 ---")
        for category, video_list in classified_videos.items():
            print(f"\n分類：{category} ({len(video_list)} 部影片)")
            for i, video_info in enumerate(video_list[:5]): # 只顯示前 5 部範例
                print(f"  - {video_info['title']} ({video_info['url']})")
            if len(video_list) > 5:
                print(f"  ... (還有 {len(video_list) - 5} 部)")

        # (可選) 將結果存檔，例如存成 JSON
        # import json
        # with open('classification_results.json', 'w', encoding='utf-8') as f:
        #     json.dump(classified_videos, f, ensure_ascii=False, indent=4)
        # print("\n分類結果已儲存至 classification_results.json")

    except ValueError as e:
        print(f"設定錯誤：{e}")
    except Exception as e:
        print(f"發生未預期的錯誤：{e}")

if __name__ == "__main__":
    # 確保這個檔案被直接執行時，才呼叫 main()
    main()