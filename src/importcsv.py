import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import os

# 載入環境變數
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 建立 Supabase 客戶端
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 清空資料表
print("正在清空資料表...")
supabase.table("characters").delete().neq("id", 0).execute()
print("資料表已清空")

# 讀取 CSV 資料
df = pd.read_csv("calligraphy_videos.csv")  # CSV 檔案在專案根目錄

# 將 DataFrame 欄位名稱轉為英文，符合資料庫欄位
df.rename(columns={
    "篇": "chapter",
    "序號": "serial",
    "中文字": "character",
    "中文字部首": "radical",
    "影片網址": "video_url"
}, inplace=True)

# 清理數據：將 nan 值替換為 None
df = df.where(pd.notnull(df), None)

# 將 radical 欄位轉換為整數，無效值設為 None
df['radical'] = pd.to_numeric(df['radical'], errors='coerce').astype('Int64')

# 檢查一下資料是否正確
print(df.head())

# 上傳資料到 Supabase
data = df.to_dict(orient="records")

# 逐筆插入 Supabase 資料表
for item in data:
    res = supabase.table("characters").insert(item).execute()
    print(f"Inserted: {res.data}")

print("資料已全部上傳完成！")
