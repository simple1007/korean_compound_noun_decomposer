import copy
from collections import defaultdict

# text = "관광버스회사"
# index = []
# index2 = []
# dic = ["백수","혈통","전자","혈","통","통전자","백","수","전","자"]
enc = "utf-8"
max_ngram = 4
def read_dic(file="./unidict.txt"):
    dic = []
    with open(file,encoding=enc) as dic_file:
        for l in dic_file:
            l = l.strip()
            l = l.split("\t")
            c = int(l[1])
            l = l[0]
            if len(l) >= 1:
                dic.append(l)
            # elif c > 50:
            #     dic.append(l)
    
    return dic

def read_biw(file="./bidict.txt"):
    wbidic = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            wbidic[l[0]] = float(l[-1])
    
    return wbidic

def read_bic(file="./bidict_c.txt"):
    cbidic = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            cbidic[l[0]] = float(l[-1])
    
    return cbidic

def read_biw(file="./bidict.txt"):
    bidic = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            bidic[l[0]] = float(l[-1])
    
    return bidic

def read_lbi(file="./lbidict.txt"):
    lbidic = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            lbidic[l[0]] = float(l[-1])
    
    return lbidic

def read_1syf(file="./1syf.txt"):
    one_syf = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            one_syf[l[0]] = float(l[-1])
    
    return one_syf

def read_1syb(file="./1syb.txt"):
    one_syb = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            one_syb[l[0]] = float(l[-1])
    
    return one_syb

def read_1syc(file="./1syc.txt"):
    one_syc = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            one_syc[l[0]] = float(l[-1])
    
    return one_syc

f = read_1syf()
b = read_1syb()
c = read_1syc()
def check(d, tri):
    try:
        return d[tri]
    except KeyError:
        print(tri,"없어")
        return 1e-9
    
def syl_chk_point(ft,ct,bt):
    return (check(c,ct) * 0.1  + check(f,ft) * 0.35+ check(b,bt) * 0.35 )# / 3

# lbi = read_lbi()
# print(lbi["|서울대"]+lbi["|입구"]+lbi["|역"]+lbi["|서울대"]+lbi["|입구|"]+lbi["역|"])
# print(lbi["|서울"]+lbi["|대입"]+lbi["|구역"])
# exit()
# while True:
#     text = input("text: ")
#     ft = "S"+text[0]+" "
#     ct = text[0] + " " + text[2]
#     bt = text[3] + text[2] + " "
#     print(ft,ct,bt)
#     print(syl_chk_point(ft,ct,bt))
    
#     ft = text[-2]+text[-1]+" "
#     ct = text[-2] + " " + text[-1]
#     bt = "E"+text[-1] + " "
#     print(ft,ct,bt)
#     print(syl_chk_point(ft,ct,bt))
# exit()

def candidate(text):
    c = 0
    words = defaultdict(list)

    # for j in range(len(text)):
    for j in range(max_ngram):
        c = 0
        for i in range(len(text)-j):
            if text[i:i+j+1] in dic:
                c+=1
                words[i].append([c,i,i+j+1,text[i:i+j+1]])
    
    return words

def iterative_dfs(start_v, token_list,text):
    discovered = []
    # print(start_v)
    stack = [start_v]
    count = defaultdict(int)
    
    result = []
    while stack:
        v = stack.pop()
        if len(v[3].replace(":","")) == len(text):
            result.append(v[3])
        words_cp = copy.deepcopy(token_list)
        if (v[1],v[2]) not in discovered or count[(v[1],v[2])] < len(token_list[v[2]]):
            count[(v[1],v[2])] += 1
            discovered.append((v[1],v[2]))
            for w in words_cp[v[2]]:
                w[3] = v[3] + ":" + w[3]
                stack.append(w)
    return result

def calc_word_point(candidate_word_arr):
    words_point = 0.0
    for w in range(len(candidate_word_arr)-1):
        bi = candidate_word_arr[w:w+2]
        bistr = ",".join(bi)
        # print(bistr)
        if bistr in biwords:
            words_point += biwords[bistr] 
    length = len(candidate_word_arr)-1 
    # print(words_point,candidate_word_arr)
    if length == 0:
        return -1.0
    return words_point / length

def calc_char_point(candidate_word):
    chars_point = 0.0
    for c in range(len(candidate_word)-1):
        bic = candidate_word[c:c+2] 
        # if candidate_word[c] != ' ':
        #     bic = candidate_word[c] + ' '
        #     # print(bic)
        if bic in bichars:
            chars_point += bichars[bic]
    return chars_point / (len(candidate_word)-1)

def main(text):
    cnouns = None
    temp = 0
    # print(text)
    words = candidate(text)
    # print(words)
    st = [[] for i in range(10)]
    curr = 0

    for i in words[0]:
        candi = iterative_dfs(i,words,text)
        # print(candi)
        if len(candi) > 0:
            for cdw in candi:
                # if ":" not in cdw:
                #     continue

                cdw = 'S ' + cdw.replace(":"," ") + ' E'
                cdw_arr = cdw.split()
                o_nouns = False
                for cdw_ in cdw_arr[2:-2]:
                    if len(cdw_) == 1:
                        o_nouns = True
                if o_nouns:
                    continue
                if cnouns is None:
                    cnouns = [cdw_arr,0.0]
                    
                words_point = calc_word_point(cdw_arr)
                chars_point = calc_char_point(cdw)

                point = ((words_point * 0.8) + (chars_point * 0.2))
                # print(cdw,words_point,chars_point,point)
                
                firs_1 = False
                last_1 = False
                
                if len(cdw_arr[1]) == 1:
                    first_1 = True
                if len(cdw_arr[-1]) == 1:
                    last_1 = True
                # print(cdw_arr[2:-2])


                
                
                # temp = max(o_nouns
                # if temp > o_nouns:
                cnouns = max(cnouns,[cdw_arr,point],key=lambda x: x[1])
    return cnouns

head = ["전","총"]
tail = ["역","실","사","부"]
if __name__ == "__main__":
    dic = read_dic()
    biwords = read_biw()
    bichars = read_bic()
    onesyl=True
    while True:
        text = input("복합명사: ")
        res = main(text)
        if res is None:
            print(text)
            continue
        for r in res[0][1:-1]:
            if onesyl and len(r) > 3 or r[0] in head or r[-1] in tail:
                for tk in main(r)[0][1:-1]:
                    print(tk, end=' ')
            else:
                print(r, end=' ')

        print()