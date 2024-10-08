import requests
import json

# Updated Google Apps Script Web application URL
GAS_URL = "https://script.google.com/macros/s/AKfycbzM25TfIKZBLjFceKVzuNnJ3ONTDsjvDmaqP8JsCY7sSZVLujoSffQ0U_oNiHuSfXqo/exec"

# データを取得
response = requests.get(GAS_URL)
data = response.json()

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

# JSON形式に変換（整形）
json_data = json.dumps(formatted_data, ensure_ascii=False, indent=2)

# JSONファイルに保存
with open('public/poster_data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)

print(f"Data has been updated and saved to poster_data.json. Total items: {len(formatted_data)}")