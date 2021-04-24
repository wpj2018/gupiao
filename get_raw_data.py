def get_raw_data(file):
    fw = open(file+".txt", 'w+', encoding='utf-8')
    with open(file, 'r',encoding='utf-8') as f:
        line = f.read()
        lst = line.strip().split(')')[:-1]
        for elem in lst:
            name,code = elem.split('(')
            if "ST" in name:
                print(name)
                continue
            fw.write("{}\t{}\n".format(code, name))

dic1 = {}
with open("resource/total.shang.txt", "r", encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        code, name = line.split('\t')
        dic1[code] = 1
with open("resource/shang.txt", "r", encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        code, name = line.split('\t')
        if code not in dic1:
            print(code)
    print('finish')