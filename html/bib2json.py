import bibtexparser
import json

# 读取BibTeX文件
with open('你的bib文件夾路徑', 'r', encoding='utf-8') as bib_file:
    bib_database = bibtexparser.load(bib_file)

# 将BibTeX对象转换为JSON格式
json_data = json.dumps(bib_database.entries, indent=2)

# 将JSON数据写入文件
with open('output.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)