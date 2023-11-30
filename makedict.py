import json

enc = 'utf-8'
result = open('dict.txt','w',encoding=enc)
files = ['SXMP1902008031.json','NXMP1902008040.json']
ffff = open("1syllable.txt","w",encoding=enc)
def c_noun(file,morph):
    temp = []
    id = -1
    for m in morph:
        # print(m)
        if id == -1 and (m['label'] == 'NNG' or m['label'] == 'NNP'):# 'NNG':
            temp.append(m['form'])
        elif m['word_id'] == id and (m['label'] == 'NNG' or m['label'] == 'NNP'):#'NNG':
            temp.append(m['form'])
        elif m['label'] == 'NNG':
            temp.append(m['form'])
        else:
            flags = False
            if len(temp) > 1:
                # print(temp)
                file.write(' '.join(['S']+temp+['E'])+'\n')
                for tp in temp:
                    if len(tp) == 1:
                        flags = True
                        break
                if flags:
                    ffff.write(' '.join(['S']+temp+['E'])+'\n')
            temp = []
            
        id = m['word_id']
    
def test(file,morph,sentence):
    temp = []
    id = -1
    from collections import defaultdict
    d = defaultdict(list)
    for m in morph:
        d[m["word_id"]].append(m["form"]+"/"+m["label"])
    print(sentence.split())
    print(d)
    exit()

for filename in reversed(files):
    with open(filename,encoding=enc) as f:
        jsons = json.load(f)
        doc = jsons["document"]

        for d in doc:
            for s in d['sentence']:
                morph = s['morpheme']
                if morph is None:
                    continue
                c_noun(result,morph)
                # test(result,morph,s["form"])
ffff.close()
result.close()