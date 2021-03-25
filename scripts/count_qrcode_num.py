from collections import defaultdict

qrcodes = defaultdict(set)

for filename in ['bs_regular_zxing_nowrap.txt', 'bs_regular_zxing_wrap.txt', 'bs_regular_boofcv_nowrap.txt', 'bs_regular_boofcv_nowrap_mirror.txt', 'bs_regular_boofcv_wrap.txt', 'bs_regular_boofcv_wrap_mirror.txt']:
    if '_boofcv' in filename:
        continue
    with open(filename) as f:
        for line in f:
            filename, success_str, version, ecl, *code = line.split()
            if success_str != 'success':
                continue
            if not code:
                code = ''
            else:
                code = code[0]
            search_engine, id = filename.split('+')[:2]
            id = int(id.split('-')[0])
            qrcodes[search_engine].add((ecl, code))

search_engines = list(qrcodes.keys())
search_engines.sort(key=lambda s: (0, s) if s.endswith('.en') else (1, s))

fullset = set()
for search_engine in search_engines:
    print('{:12s}'.format(search_engine), '{:-4d}'.format(len(qrcodes[search_engine])))
    fullset |= qrcodes[search_engine]

print('all ', len(fullset))
