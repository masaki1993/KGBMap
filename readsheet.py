import requests
import json
import sys
from datetime import datetime

# Add this at the beginning of the script
def log_message(message):
    with open('readsheet_log.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()}: {message}\n")

# Updated Google Apps Script Web application URL for version 2
GAS_URL = "https://script.google.com/macros/s/AKfycbxiq0DkAeoJWxctvpSE-2EC9wZDOPn8voUnZ87bwYcsxgGOJSqic1sLoTPqz7Q0PU1edA/exec"

log_message("Starting data fetch from Google Apps Script...")

try:
    # データを取得
    response = requests.get(GAS_URL)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    data = response.json()
    log_message(f"Data fetched successfully. Number of items: {len(data)}")
except requests.exceptions.RequestException as e:
    log_message(f"Error fetching data: {e}")
    sys.exit(1)

# データの検証と整形
formatted_data = []
for item in data:
    formatted_item = {
        "Name": item.get("Name", ""),
        "Latitude": item.get("Latitude", 0),
        "Longitude": item.get("Longitude", 0),
        "投票区": item.get("投票区", ""),
        "住所1": item.get("住所1", ""),
        "住所2": item.get("住所2", ""),
        "ステータス": item.get("ステータス", "未完了"),
        "更新者": item.get("更新者", "")
    }
    formatted_data.append(formatted_item)

log_message(f"Data formatted. Number of formatted items: {len(formatted_data)}")

# JSON形式に変換（整形）
json_data = json.dumps(formatted_data, ensure_ascii=False, indent=2)

# JSONファイルに保存
try:
    with open('public/poster_data.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
    log_message("Data has been successfully written to poster_data.json")
except IOError as e:
    log_message(f"Error writing to file: {e}")
    sys.exit(1)

log_message(f"Data update process completed. Total items: {len(formatted_data)}")