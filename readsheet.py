import requests
import json
import sys

# Updated Google Apps Script Web application URL for version 2
GAS_URL = "https://script.google.com/macros/s/AKfycbxiq0DkAeoJWxctvpSE-2EC9wZDOPn8voUnZ87bwYcsxgGOJSqic1sLoTPqz7Q0PU1edA/exec"

print("Starting data fetch from Google Apps Script...")

try:
    # データを取得
    response = requests.get(GAS_URL)
    response.raise_for_status()  # This will raise an exception for HTTP errors
    data = response.json()
    print(f"Data fetched successfully. Number of items: {len(data)}")
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}", file=sys.stderr)
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

print(f"Data formatted. Number of formatted items: {len(formatted_data)}")

# JSON形式に変換（整形）
json_data = json.dumps(formatted_data, ensure_ascii=False, indent=2)

# JSONファイルに保存
try:
    with open('public/poster_data.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
    print("Data has been successfully written to poster_data.json")
except IOError as e:
    print(f"Error writing to file: {e}", file=sys.stderr)
    sys.exit(1)

print(f"Data update process completed. Total items: {len(formatted_data)}")