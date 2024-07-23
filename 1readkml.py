import requests
import xml.etree.ElementTree as ET
import pandas as pd

# リンク先のURL
url = 'https://www.google.com/maps/d/u/0/kml?forcekml=1&mid=1GPEHJ5ce-7FgpGV0oVpZ0KzZm84MTPI'

# KMLファイルのダウンロード
response = requests.get(url)

# ダウンロードしたKMLファイルを保存
downloaded_kml_file = 'downloaded_kml.kml'
with open(downloaded_kml_file, 'wb') as file:
    file.write(response.content)

print("KMLファイルがダウンロードされました。")

# ダウンロードしたKMLファイルのパスを指定
kml_file = downloaded_kml_file

# KMLファイルを読み込む
tree = ET.parse(kml_file)
root = tree.getroot()

# KMLの名前空間
namespace = {'kml': 'http://www.opengis.net/kml/2.2'}

# Placemarkを取得
placemarks = root.findall('.//kml:Placemark', namespace)

# データを格納するリスト
data = []

# Placemarkから必要な情報を取得
for placemark in placemarks:
    name = placemark.find('kml:name', namespace).text if placemark.find('kml:name', namespace) is not None else ""
    description = placemark.find('kml:description', namespace).text if placemark.find('kml:description', namespace) is not None else ""
    coordinates = placemark.find('.//kml:coordinates', namespace).text.strip() if placemark.find('.//kml:coordinates', namespace) is not None else ""
    
    extended_data = {}
    for data_element in placemark.findall('.//kml:Data', namespace):
        data_name = data_element.attrib['name']
        data_value = data_element.find('kml:value', namespace).text if data_element.find('kml:value', namespace) is not None else ""
        extended_data[data_name] = data_value
    
    if coordinates:
        lon, lat, _ = coordinates.split(',')
        item = {
            'Name': name,
            'Description': description,
            'Latitude': lat,
            'Longitude': lon,
            '投票区': extended_data.get('投票区', ''),
            '住所1': extended_data.get('住所1', ''),
            '住所2': extended_data.get('住所2', ''),
            '緯度': extended_data.get('緯度', lat),
            '経度': extended_data.get('経度', lon)
        }
        data.append(item)

# データフレームを作成
df = pd.DataFrame(data)

# スプレッドシートに出力するためのCSVファイルとして保存
csv_file = 'ポスター掲示場.csv'
df.to_csv(csv_file, index=False)

print(f"CSVファイルが保存されました: {csv_file}")