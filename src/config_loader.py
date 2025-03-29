import os
import re

def load_config():
    """載入 .env 檔案中的環境變數"""
    # 直接讀取 .env 檔案
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"\'')
    
    api_key = os.getenv("YOUTUBE_API_KEY")
    channel_id = os.getenv("TARGET_CHANNEL_ID")

    if not api_key:
        raise ValueError("請在 .env 檔案中設定 YOUTUBE_API_KEY")
    if not channel_id:
        raise ValueError("請在 .env 檔案中設定 TARGET_CHANNEL_ID")

    return {"api_key": api_key, "channel_id": channel_id}

# --- 或者 ---

# `src/config_loader.py` (如果使用 `config.yaml`)
# import yaml
# from pathlib import Path

# def load_config(config_path="config/config.yaml"):
#     """載入 YAML 設定檔"""
#     path = Path(config_path)
#     if not path.is_file():
#         raise FileNotFoundError(f"找不到設定檔: {config_path}")
#     with open(path, 'r', encoding='utf-8') as f:
#         config = yaml.safe_load(f)

#     if not config.get("api_key"):
#         raise ValueError("請在設定檔中設定 api_key")
#     if not config.get("channel_id"):
#         raise ValueError("請在設定檔中設定 channel_id")

#     return config