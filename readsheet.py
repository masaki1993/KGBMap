import requests
import json
import pandas as pd

# Google Apps ScriptのURLを設定
url = 'https://script.google.com/macros/s/AKfycbw38DeRxTrQAHnOoU3do7931AGSpBHIxOgP_LDatjOlm0trFCzYjG9vFwhLvWH5Wx5mOQ/exec'
response = requests.get(url)

# レスポンスの内容を確認
print(f"HTTPステータスコード: {response.status_code}")

if response.status_code == 200:
    print(f"レスポンステキスト: {response.text}")
    try:
        data = response.json()
    except json.JSONDecodeError as e:
        print(f"JSONのデコードに失敗しました: {e}")
        data = None

    if data:
        # データフレームに変換
        df = pd.DataFrame(data)

        # JSONファイルとして保存
        df.to_json('poster_data.json', orient='records')

        print("データをJSONファイルに保存しました。")

        # データフレームを表示
        print(df)
    else:
        print("データが空です。")
else:
    print("データを取得できませんでした。")