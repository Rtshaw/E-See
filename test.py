# -*-coding: utf-8 -*-

with open('tmp.txt', 'r+', encoding = 'utf-8-sig') as f:
    content = f.read().strip()
    content = content.replace('________________', '')
    print(content)
    f.write('%s' %content)

#print(text)
