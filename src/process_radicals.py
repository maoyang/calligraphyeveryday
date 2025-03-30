import pandas as pd
from cihai.core import Cihai
from supabase import create_client
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 初始化 Cihai
c = Cihai()
if not c.unihan.is_bootstrapped:
    c.unihan.bootstrap()

# 初始化 Supabase 客戶端
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# 定義部首映射表（包含筆劃數）
radical_map = {
    "一": {"number": 1, "strokes": 1},
    "丨": {"number": 2, "strokes": 1},
    "丶": {"number": 3, "strokes": 1},
    "丿": {"number": 4, "strokes": 1},
    "乙": {"number": 5, "strokes": 1},
    "亅": {"number": 6, "strokes": 1},
    "二": {"number": 7, "strokes": 2},
    "亠": {"number": 8, "strokes": 2},
    "人": {"number": 9, "strokes": 2},
    "儿": {"number": 10, "strokes": 2},
    "入": {"number": 11, "strokes": 2},
    "八": {"number": 12, "strokes": 2},
    "冂": {"number": 13, "strokes": 2},
    "冖": {"number": 14, "strokes": 2},
    "冫": {"number": 15, "strokes": 2},
    "几": {"number": 16, "strokes": 2},
    "凵": {"number": 17, "strokes": 2},
    "刀": {"number": 18, "strokes": 2},
    "力": {"number": 19, "strokes": 2},
    "勹": {"number": 20, "strokes": 2},
    "匕": {"number": 21, "strokes": 2},
    "匚": {"number": 22, "strokes": 2},
    "匸": {"number": 23, "strokes": 2},
    "十": {"number": 24, "strokes": 2},
    "卜": {"number": 25, "strokes": 2},
    "卩": {"number": 26, "strokes": 2},
    "厂": {"number": 27, "strokes": 2},
    "厶": {"number": 28, "strokes": 2},
    "又": {"number": 29, "strokes": 2},
    "口": {"number": 30, "strokes": 3},
    "囗": {"number": 31, "strokes": 3},
    "土": {"number": 32, "strokes": 3},
    "士": {"number": 33, "strokes": 3},
    "夂": {"number": 34, "strokes": 3},
    "夊": {"number": 35, "strokes": 3},
    "夕": {"number": 36, "strokes": 3},
    "大": {"number": 37, "strokes": 3},
    "女": {"number": 38, "strokes": 3},
    "子": {"number": 39, "strokes": 3},
    "宀": {"number": 40, "strokes": 3},
    "寸": {"number": 41, "strokes": 3},
    "小": {"number": 42, "strokes": 3},
    "尢": {"number": 43, "strokes": 3},
    "尸": {"number": 44, "strokes": 3},
    "屮": {"number": 45, "strokes": 3},
    "山": {"number": 46, "strokes": 3},
    "巛": {"number": 47, "strokes": 3},
    "工": {"number": 48, "strokes": 3},
    "己": {"number": 49, "strokes": 3},
    "巾": {"number": 50, "strokes": 3},
    "干": {"number": 51, "strokes": 3},
    "幺": {"number": 52, "strokes": 3},
    "广": {"number": 53, "strokes": 3},
    "廴": {"number": 54, "strokes": 3},
    "廾": {"number": 55, "strokes": 3},
    "弋": {"number": 56, "strokes": 3},
    "弓": {"number": 57, "strokes": 3},
    "彐": {"number": 58, "strokes": 3},
    "彡": {"number": 59, "strokes": 3},
    "彳": {"number": 60, "strokes": 3},
    "心": {"number": 61, "strokes": 4},
    "戈": {"number": 62, "strokes": 4},
    "戶": {"number": 63, "strokes": 4},
    "手": {"number": 64, "strokes": 4},
    "支": {"number": 65, "strokes": 4},
    "攴": {"number": 66, "strokes": 4},
    "文": {"number": 67, "strokes": 4},
    "斗": {"number": 68, "strokes": 4},
    "斤": {"number": 69, "strokes": 4},
    "方": {"number": 70, "strokes": 4},
    "无": {"number": 71, "strokes": 4},
    "日": {"number": 72, "strokes": 4},
    "曰": {"number": 73, "strokes": 4},
    "月": {"number": 74, "strokes": 4},
    "木": {"number": 75, "strokes": 4},
    "欠": {"number": 76, "strokes": 4},
    "止": {"number": 77, "strokes": 4},
    "歹": {"number": 78, "strokes": 4},
    "殳": {"number": 79, "strokes": 4},
    "毋": {"number": 80, "strokes": 4},
    "比": {"number": 81, "strokes": 4},
    "毛": {"number": 82, "strokes": 4},
    "氏": {"number": 83, "strokes": 4},
    "气": {"number": 84, "strokes": 4},
    "水": {"number": 85, "strokes": 4},
    "火": {"number": 86, "strokes": 4},
    "爪": {"number": 87, "strokes": 4},
    "父": {"number": 88, "strokes": 4},
    "爻": {"number": 89, "strokes": 4},
    "爿": {"number": 90, "strokes": 4},
    "片": {"number": 91, "strokes": 4},
    "牙": {"number": 92, "strokes": 4},
    "牛": {"number": 93, "strokes": 4},
    "犬": {"number": 94, "strokes": 4},
    "玄": {"number": 95, "strokes": 5},
    "玉": {"number": 96, "strokes": 5},
    "瓜": {"number": 97, "strokes": 5},
    "瓦": {"number": 98, "strokes": 5},
    "甘": {"number": 99, "strokes": 5},
    "生": {"number": 100, "strokes": 5},
    "用": {"number": 101, "strokes": 5},
    "田": {"number": 102, "strokes": 5},
    "疋": {"number": 103, "strokes": 5},
    "疒": {"number": 104, "strokes": 5},
    "癶": {"number": 105, "strokes": 5},
    "白": {"number": 106, "strokes": 5},
    "皮": {"number": 107, "strokes": 5},
    "皿": {"number": 108, "strokes": 5},
    "目": {"number": 109, "strokes": 5},
    "矛": {"number": 110, "strokes": 5},
    "矢": {"number": 111, "strokes": 5},
    "石": {"number": 112, "strokes": 5},
    "示": {"number": 113, "strokes": 5},
    "禸": {"number": 114, "strokes": 5},
    "禾": {"number": 115, "strokes": 5},
    "穴": {"number": 116, "strokes": 5},
    "立": {"number": 117, "strokes": 5},
    "竹": {"number": 118, "strokes": 6},
    "米": {"number": 119, "strokes": 6},
    "糸": {"number": 120, "strokes": 6},
    "缶": {"number": 121, "strokes": 6},
    "网": {"number": 122, "strokes": 6},
    "羊": {"number": 123, "strokes": 6},
    "羽": {"number": 124, "strokes": 6},
    "老": {"number": 125, "strokes": 6},
    "而": {"number": 126, "strokes": 6},
    "耒": {"number": 127, "strokes": 6},
    "耳": {"number": 128, "strokes": 6},
    "聿": {"number": 129, "strokes": 6},
    "肉": {"number": 130, "strokes": 6},
    "臣": {"number": 131, "strokes": 6},
    "自": {"number": 132, "strokes": 6},
    "至": {"number": 133, "strokes": 6},
    "臼": {"number": 134, "strokes": 6},
    "舌": {"number": 135, "strokes": 6},
    "舛": {"number": 136, "strokes": 6},
    "舟": {"number": 137, "strokes": 6},
    "艮": {"number": 138, "strokes": 6},
    "色": {"number": 139, "strokes": 6},
    "艸": {"number": 140, "strokes": 6},
    "虍": {"number": 141, "strokes": 6},
    "虫": {"number": 142, "strokes": 6},
    "血": {"number": 143, "strokes": 6},
    "行": {"number": 144, "strokes": 6},
    "衣": {"number": 145, "strokes": 6},
    "襾": {"number": 146, "strokes": 6},
    "見": {"number": 147, "strokes": 7},
    "角": {"number": 148, "strokes": 7},
    "言": {"number": 149, "strokes": 7},
    "谷": {"number": 150, "strokes": 7},
    "豆": {"number": 151, "strokes": 7},
    "豕": {"number": 152, "strokes": 7},
    "豸": {"number": 153, "strokes": 7},
    "貝": {"number": 154, "strokes": 7},
    "赤": {"number": 155, "strokes": 7},
    "走": {"number": 156, "strokes": 7},
    "足": {"number": 157, "strokes": 7},
    "身": {"number": 158, "strokes": 7},
    "車": {"number": 159, "strokes": 7},
    "辛": {"number": 160, "strokes": 7},
    "辰": {"number": 161, "strokes": 7},
    "辵": {"number": 162, "strokes": 7},
    "邑": {"number": 163, "strokes": 7},
    "酉": {"number": 164, "strokes": 7},
    "釆": {"number": 165, "strokes": 7},
    "里": {"number": 166, "strokes": 7},
    "金": {"number": 167, "strokes": 8},
    "長": {"number": 168, "strokes": 8},
    "門": {"number": 169, "strokes": 8},
    "阜": {"number": 170, "strokes": 8},
    "隶": {"number": 171, "strokes": 8},
    "隹": {"number": 172, "strokes": 8},
    "雨": {"number": 173, "strokes": 8},
    "靑": {"number": 174, "strokes": 8},
    "非": {"number": 175, "strokes": 8},
    "面": {"number": 176, "strokes": 9},
    "革": {"number": 177, "strokes": 9},
    "韋": {"number": 178, "strokes": 9},
    "韭": {"number": 179, "strokes": 9},
    "音": {"number": 180, "strokes": 9},
    "頁": {"number": 181, "strokes": 9},
    "風": {"number": 182, "strokes": 9},
    "飛": {"number": 183, "strokes": 9},
    "食": {"number": 184, "strokes": 9},
    "首": {"number": 185, "strokes": 9},
    "香": {"number": 186, "strokes": 9},
    "馬": {"number": 187, "strokes": 10},
    "骨": {"number": 188, "strokes": 10},
    "高": {"number": 189, "strokes": 10},
    "髟": {"number": 190, "strokes": 10},
    "鬥": {"number": 191, "strokes": 10},
    "鬯": {"number": 192, "strokes": 10},
    "鬲": {"number": 193, "strokes": 10},
    "鬼": {"number": 194, "strokes": 10},
    "魚": {"number": 195, "strokes": 11},
    "鳥": {"number": 196, "strokes": 11},
    "鹵": {"number": 197, "strokes": 11},
    "鹿": {"number": 198, "strokes": 11},
    "麥": {"number": 199, "strokes": 11},
    "麻": {"number": 200, "strokes": 11},
    "黃": {"number": 201, "strokes": 12},
    "黍": {"number": 202, "strokes": 12},
    "黑": {"number": 203, "strokes": 12},
    "黹": {"number": 204, "strokes": 12},
    "黽": {"number": 205, "strokes": 13},
    "鼎": {"number": 206, "strokes": 13},
    "鼓": {"number": 207, "strokes": 13},
    "鼠": {"number": 208, "strokes": 13},
    "鼻": {"number": 209, "strokes": 14},
    "齊": {"number": 210, "strokes": 14},
    "齒": {"number": 211, "strokes": 15},
    "龍": {"number": 212, "strokes": 16},
    "龜": {"number": 213, "strokes": 16},
    "龠": {"number": 214, "strokes": 17}
}

def process_radicals():
    """將部首映射表寫入資料庫"""
    # 清空資料表
    print("正在清空 radical 資料表...")
    try:
        supabase.table('radical').delete().neq('id', 0).execute()
        print("資料表已清空")
    except Exception as e:
        print(f"清空資料表失敗：{str(e)}")
        raise

    # 處理每個部首
    for char, info in radical_map.items():
        try:
            # 檢查部首是否已經存在
            existing = supabase.table('radical').select('id').eq('radicalnumber', info['number']).execute()
            
            if not existing.data:
                # 創建部首記錄
                radical_record = {
                    'char': char,
                    'radicalnumber': info['number'],
                    'stroke_count': info['strokes']
                }
                supabase.table('radical').insert(radical_record).execute()
                print(f"已新增部首: {char} (編號: {info['number']}, 筆劃: {info['strokes']})")
            else:
                print(f"部首已存在: {char} (編號: {info['number']}, 筆劃: {info['strokes']})")
        except Exception as e:
            print(f"處理部首 {char} 時發生錯誤: {str(e)}")

if __name__ == "__main__":
    process_radicals()