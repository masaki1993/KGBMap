import xml.etree.ElementTree as ET
import pandas as pd
import os

# ダウンロードしたKMLファイルのパスを指定
kml_file = 'downloaded_kml.kml'

# KMLファイルを読み込む
tree = ET.parse(kml_file)
root = tree.getroot()

# KMLの名前空間
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

# Placemarkを取得
placemarks = root.findall('.//kml:Placemark', namespace)

# データを格納するリスト
data = []

# Placemarkから名前と座標を取得
for placemark in placemarks:
    name_element = placemark.find('kml:name', namespace)
    coordinates_element = placemark.find('.//kml:coordinates', namespace)
    
    if name_element is not None and coordinates_element is not None:
        name = name_element.text
        coordinates = coordinates_element.text.strip()
        lon, lat, _ = coordinates.split(',')
        data.append({'Name': name, 'Latitude': lat, 'Longitude': lon})

# データフレームを作成
df = pd.DataFrame(data)

# スプレッドシートに出力するためのCSVファイルとして保存
csv_file = 'ポスター掲示場.csv'
df.to_csv(csv_file, index=False)

print(f"CSVファイルが保存されました: {csv_file}")