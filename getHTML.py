import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

wcaID = input("Please input the WCA ID: ")

# 目标网址
url = 'https://www.worldcubeassociation.org/persons/'+wcaID+'?event=333'

# 发送请求
response = requests.get(url)
html = response.text

# 解析网页
soup = BeautifulSoup(html, 'html.parser')

# 提取内容（例如所有标题）
titles = soup.find_all('h2')
for title in titles:
    print(title.text.strip())
    
# 找到目标 tbody
tbody = soup.find('tbody', class_='event-333')

# 提取所有行
rows = tbody.find_all('tr')[1:]  # 从第二个开始取
ignore_classes = {'competition', 'round', 'place', 'regional-single-record', 'regional-average-record'}

filename = title.text.strip()+'_333'+'.csv'
column_names = ['Single', 'Average', 'Attempt1', 'Attempt2', 'Attempt3', 'Attempt4', 'Attempt5']
with open(filename, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)

    writer.writerow(column_names)
    for row in rows:
        cols = row.find_all('td')
        filtered = [
            td.get_text(strip=True)
            for td in cols
            if not ignore_classes.intersection(td.get('class', []))
        ]
        writer.writerow(filtered)

print("Data saved to "+filename)

# 打开 CSV 文件
df = pd.read_csv(filename)
target_columns = ['Average', 'Single']
for col in target_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')
    
# 提取前10行（如果不够就取全部）
sample = df.head(10)

selected = sample[target_columns]

print(selected)

# 创建一个结果表格
stats = pd.DataFrame({
    'Mean': selected.mean(),
    'SD': selected.std()
})

# 显示结果
print('Result:')
print(stats)