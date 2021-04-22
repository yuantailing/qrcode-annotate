with open('zxing_detect_cjig_not_converted.txt') as f, open('zxing_detect_cjig.txt', 'w') as fw:
    for line in f:
        search_engine, image_id, res = line.split()
        if not res.startswith('com.google.zxing'):
            fw.write(f'{search_engine}+{image_id}-orig.png ')
            fw.write(f'success {res}\n')
