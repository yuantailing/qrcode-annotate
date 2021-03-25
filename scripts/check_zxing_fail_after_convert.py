detected_1 = set()

with open('zxing_detect_nowrap.txt') as f:
    for line in f:
        name, success_str, res = line.split()
        if success_str == 'success':
            search_engine, second_part = name.split('+')[:2]
            id = int(second_part.split('-')[0])
            detected_1.add(f'{search_engine}/{id}')

detected_2 = set()

with open('zxing_direct_decode.txt') as f:
    for line in f:
        search_engine, id, res = line.split()
        if not res.startswith('com.google.zxing'):
            detected_2.add(f'{search_engine}/{id}')

print(len(detected_1))
print(len(detected_2))
print(detected_2 - detected_1)

cates = {s.split('/')[0] for s in detected_1}
for cate in sorted(cates):
    print(cate, len([s for s in detected_1 if s.startswith(cate + '/')]))
