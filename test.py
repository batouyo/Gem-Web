
import io
with io.open('papers_info_2026-01-12_18-47-12.json','r',encoding='utf-8') as r, \
     io.open('html/papers_info.js','w',encoding='utf-8') as w:
    w.write('window.PAPERS_JSON = ')
    w.write(r.read())
    w.write(';')
print('wrote html/papers_info.js')