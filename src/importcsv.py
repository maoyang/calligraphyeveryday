import pandas as pd
from supabase import create_client
from dotenv import load_dotenv
import os
from pathlib import Path

# 獲取專案根目錄
ROOT_DIR = Path(__file__).parent.parent
print(f"專案根目錄: {ROOT_DIR}")

# 載入環境變數
env_path = ROOT_DIR / '.env'
print(f"正在讀取環境變數文件: {env_path}")
print(f"環境變數文件是否存在: {env_path.exists()}")

# 先清除現有的環境變數
os.environ.pop('SUPABASE_URL', None)
os.environ.pop('SUPABASE_KEY', None)

# 重新載入環境變數
load_dotenv(env_path, override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

print(f"SUPABASE_URL: {SUPABASE_URL}")
print(f"SUPABASE_KEY: {SUPABASE_KEY[:10]}...")  # 只顯示前10個字元

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("請確保 .env 文件中設置了 SUPABASE_URL 和 SUPABASE_KEY")

print(f"正在連接到 Supabase: {SUPABASE_URL}")

# 建立 Supabase 客戶端
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 測試連接
try:
    print("測試 Supabase 連接...")
    response = supabase.table("characters").select("*").limit(1).execute()
    print("連接成功！")
except Exception as e:
    print(f"連接失敗：{str(e)}")
    raise

# 清空資料表
print("正在清空資料表...")
try:
    supabase.table("characters").delete().neq("id", 0).execute()
    print("資料表已清空")
except Exception as e:
    print(f"清空資料表失敗：{str(e)}")
    raise

# 讀取 CSV 資料
csv_path = ROOT_DIR / "calligraphy_videos.csv"
print(f"正在讀取 CSV 文件: {csv_path}")
try:
    df = pd.read_csv(csv_path)
    print(f"成功讀取 CSV，共 {len(df)} 筆資料")
except Exception as e:
    print(f"讀取 CSV 失敗：{str(e)}")
    raise

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
print("\n資料預覽：")
print(df.head())

# 上傳資料到 Supabase
data = df.to_dict(orient="records")
print(f"\n準備上傳 {len(data)} 筆資料...")

# 逐筆插入 Supabase 資料表
success_count = 0
error_count = 0

for i, item in enumerate(data, 1):
    try:
        res = supabase.table("characters").insert(item).execute()
        success_count += 1
        if i % 100 == 0:  # 每100筆顯示一次進度
            print(f"已成功上傳 {success_count} 筆資料...")
    except Exception as e:
        error_count += 1
        print(f"上傳第 {i} 筆資料失敗：{str(e)}")

print(f"\n上傳完成！成功：{success_count} 筆，失敗：{error_count} 筆")
