# exceeltojson.py
"""
@file exceeltojson.py
@brief 将Excel文件内容批量转换为 output2.json 所需的 output([...]) 格式
@usage python exceeltojson.py lectures.xlsx output2.json
@require pandas, openpyxl
"""

import sys
import pandas as pd
import json

def main():
    if len(sys.argv) != 3:
        print("用法: python exceeltojson.py <输入Excel文件> <输出json文件>")
        return

    excel_file = sys.argv[1]
    output_file = sys.argv[2]

    # 读取Excel
    df = pd.read_excel(excel_file, dtype=str).fillna('null')

    # 转换为字典列表
    records = df.to_dict(orient='records')

    # 处理字符串中的换行符
    for rec in records:
        for k, v in rec.items():
            if isinstance(v, str):
                rec[k] = v.replace('\r\n', '\\n').replace('\n', '\\n').replace('\r', '\\n')
            if v == 'null':
                rec[k] = None

    # 生成output([...])格式字符串
    json_str = json.dumps(records, ensure_ascii=False, separators=(',', ': '))
    output_str = f"output({json_str})"

    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(output_str)

    print(f"已生成 {output_file}，可直接用于 output2.json 替换。")

if __name__ == "__main__":
    main()