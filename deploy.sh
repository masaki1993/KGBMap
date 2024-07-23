#!/bin/bash

# GASからCSVをダウンロード
curl -L "https://script.google.com/macros/s/AKfycbw38DeRxTrQAHnOoU3do7931AGSpBHIxOgP_LDatjOlm0trFCzYjG9vFwhLvWH5Wx5mOQ/exec" -o public/poster_data.csv

# PythonでCSVをJSONに変換
python3 <<EOF
import pandas as pd
import json

# CSVを読み込む
df = pd.read_csv('public/poster_data.csv')

# JSONに変換して保存
df.to_json('public/poster_data.json', orient='records', force_ascii=False)
EOF

# Netlifyにデプロイ
netlify deploy --dir=public --prod