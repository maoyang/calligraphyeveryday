#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
從 YouTube 頻道抓取書法影片並整理成 CSV 檔案
格式範例: 趙孟頫 每日一字 1423閶~全集09篇
"""

import re
import csv
import os
from typing import List, Dict, Tuple, Optional
from cihai.core import Cihai

from src.config_loader import load_config
from src.youtube_api import get_channel_videos

def init_cihai() -> Cihai:
    """初始化 Cihai 以獲取漢字部首"""
    c = Cihai()
    if not c.unihan.is_bootstrapped:
        c.unihan.bootstrap()
    return c

def extract_info_from_title(title: str) -> Optional[Dict[str, str]]:
    """
    從影片標題中提取資訊
    
    Args:
        title: 影片標題，例如 "趙孟頫 每日一字 1423閶~全集09篇" 或 "趙孟頫 每日一字 0001一" 或 "趙孟頫 每日一字 0010既~xxxxxx"
        
    Returns:
        包含篇號、序號、中文字的字典，如果不符合格式則返回 None
    """
    # 使用正則表達式匹配標題格式 1: "趙孟頫 每日一字 1423閶~全集09篇"
    pattern1 = r'趙孟頫\s+每日一字\s+(\d+)([^\s~]+)~全集(\d+)篇'
    match1 = re.search(pattern1, title)
    
    if match1:
        sequence_number = match1.group(1)  # 序號，例如 "1423"
        chinese_char = match1.group(2)     # 中文字，例如 "閶"
        volume_number = match1.group(3)    # 篇號，例如 "09"
        
        # 移除前導零
        volume_number = volume_number.lstrip('0')
        
        return {
            'volume': volume_number,
            'sequence': sequence_number,
            'character': chinese_char
        }
    
    # 使用正則表達式匹配標題格式 3: "趙孟頫 每日一字 0010既~xxxxxx"
    pattern3 = r'趙孟頫\s+每日一字\s+(\d+)([^\s~]+)~'
    match3 = re.search(pattern3, title)
    
    if match3:
        sequence_number = match3.group(1)  # 序號，例如 "0010"
        chinese_char = match3.group(2)     # 中文字，例如 "既"
        
        return {
            'volume': '0',  # 對於沒有篇號的影片，設置為 0
            'sequence': sequence_number,
            'character': chinese_char
        }
    
    # 使用正則表達式匹配標題格式 2: "趙孟頫 每日一字 0001一"
    pattern2 = r'趙孟頫\s+每日一字\s+(\d+)([^\s]+)'
    match2 = re.search(pattern2, title)
    
    if match2:
        sequence_number = match2.group(1)  # 序號，例如 "0001"
        chinese_char = match2.group(2)     # 中文字，例如 "一"
        
        return {
            'volume': '0',  # 對於沒有篇號的影片，設置為 0
            'sequence': sequence_number,
            'character': chinese_char
        }
    
    return None

def get_radical(c: Cihai, character: str) -> str:
    """
    獲取漢字的部首編號
    
    Args:
        c: Cihai 實例
        character: 中文字
        
    Returns:
        部首編號字符串
    """
    try:
        query = c.unihan.lookup_char(character)
        if query:
            # 將 Query 物件轉換為列表
            query_list = list(query)
            if query_list:
                # 嘗試獲取 kRSKangXi 字段，其中包含部首信息
                # 檢查 query_list[0] 是否為字典類型
                if isinstance(query_list[0], dict):
                    rs_info = query_list[0].get('kRSKangXi')
                    if rs_info:
                        # kRSKangXi 格式為 "部首.筆畫數"，例如 "門.8"
                        radical_number = rs_info.split('.')[0]
                        # 使用 kRSUnicode 可能更可靠
                        rs_unicode = query_list[0].get('kRSUnicode')
                        if rs_unicode:
                            radical_number = rs_unicode.split('.')[0]
                        
                        # 直接返回部首編號
                        return radical_number
                elif hasattr(query_list[0], '__dict__'):
                    # 如果是對象，嘗試獲取屬性
                    for attr_name in ['kRSKangXi', 'kRSUnicode']:
                        if hasattr(query_list[0], attr_name):
                            rs_info = getattr(query_list[0], attr_name)
                            if rs_info:
                                radical_number = rs_info.split('.')[0]
                                return radical_number
    except Exception as e:
        print(f"獲取部首時發生錯誤: {e}")
            
    # 如果無法獲取部首，返回空字符串
    return ""

def main():
    """主函數"""
    try:
        # 1. 載入設定
        config = load_config()
        api_key = config["api_key"]
        channel_id = config["channel_id"]
        
        # 2. 初始化 Cihai
        print("初始化 Cihai 以獲取漢字部首...")
        c = init_cihai()
        
        # 3. 獲取頻道影片
        print(f"正在從頻道 {channel_id} 獲取影片...")
        videos = get_channel_videos(api_key, channel_id)
        
        if not videos:
            print("無法獲取影片資訊，程式結束。")
            return
        
        # 4. 處理影片資訊
        print("開始處理影片資訊...")
        calligraphy_videos = []
        
        for video in videos:
            video_id = video['id']
            title = video['title']
            info = extract_info_from_title(title)
            
            if info:
                # 獲取漢字部首
                radical = get_radical(c, info['character'])
                
                # 添加到結果列表
                calligraphy_videos.append({
                    'volume': info['volume'],
                    'sequence': info['sequence'],
                    'character': info['character'],
                    'radical': radical,
                    'url': f"https://www.youtube.com/watch?v={video_id}"
                })
        
        # 5. 輸出 CSV 檔案
        if calligraphy_videos:
            output_file = "calligraphy_videos.csv"
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 寫入標題列
                writer.writerow(['篇', '序號', '中文字', '中文字部首', '影片網址'])
                
                # 寫入資料
                for video in calligraphy_videos:
                    writer.writerow([
                        video['volume'],
                        video['sequence'],
                        video['character'],
                        video['radical'],
                        video['url']
                    ])
            
            print(f"成功處理 {len(calligraphy_videos)} 部書法影片，結果已儲存至 {output_file}")
        else:
            print("未找到符合格式的書法影片。")
            
    except Exception as e:
        print(f"處理過程中發生錯誤：{e}")

if __name__ == "__main__":
    main()
