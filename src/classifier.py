import re # 可以用正規表達式進行更複雜的匹配

def classify_video_by_title(title: str) -> str:
    """
    根據影片標題進行分類。

    Args:
        title: 影片標題字串。

    Returns:
        分類名稱 (字串)，如果無法分類則返回 "未分類"。
    """
    title_lower = title.lower() # 轉換成小寫方便比對

    # --- 在這裡定義你的分類規則 ---
    # 範例：
    if "開箱" in title_lower or "unboxing" in title_lower:
        return "開箱評測"
    elif "教學" in title_lower or "tutorial" in title_lower or "怎麼做" in title_lower:
        return "教學技巧"
    elif re.search(r'vlog|日常|生活', title_lower): # 使用正規表達式
        return "生活紀錄"
    elif "遊戲" in title_lower or "gameplay" in title_lower:
        return "遊戲實況"
    # --- 規則結束 ---

    return "未分類" # 預設分類

# (進階想法) 你也可以從 categories.yaml 讀取規則
# import yaml
# from pathlib import Path

# def load_categories(config_path="config/categories.yaml"):
#     # ... 讀取 yaml 檔案，裡面定義關鍵字和對應分類 ...
#     pass

# def classify_video_with_rules(title: str, rules: dict) -> str:
#     title_lower = title.lower()
#     for category, keywords in rules.items():
#         if any(keyword.lower() in title_lower for keyword in keywords):
#             return category
#     return "未分類"