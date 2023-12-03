import copy
import os
root = os.environ["HT"] + "/" + "korean_compound_noun_decomposer"
from collections import defaultdict

enc = "utf-8"
max_ngram = 3
def read_dic(file=root+"/unidict.txt"):
    dic = []
    onedic = []
    with open(file,encoding=enc) as dic_file:
        for l in dic_file:
            l = l.strip()
            l = l.split("\t")
            c = int(l[1])
            l = l[0]
            if len(l) >= 1:
                dic.append(l)
            if len(l) == 1:
                onedic.append(l)
            # elif c > 50:
            #     dic.append(l)
    
    return dic,onedic

def read_biw(file=root+"/bidict.txt"):
    wbidic = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            wbidic[l[0]] = float(l[-1])
    
    return wbidic

def read_bic(file=root+"/bidict_c.txt"):
    cbidic = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            cbidic[l[0]] = float(l[-1])
    
    return cbidic

def read_biw(file=root+"/bidict.txt"):
    bidic = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            bidic[l[0]] = float(l[-1])
    
    return bidic

def read_lbi(file=root+"/lbidict.txt"):
    lbidic = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            lbidic[l[0]] = float(l[-1])
    
    return lbidic

def read_1syf(file=root+"/1syf.txt"):
    one_syf = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            one_syf[l[0]] = float(l[-1])
    
    return one_syf

def read_1syb(file=root+"/1syb.txt"):
    one_syb = {}
    
    with open(file,encoding=enc) as bi_dic_file:
        for l in bi_dic_file:
            l = l.strip()
            l = l.split("\t")
            one_syb[l[0]] = float(l[-1])
    
    return one_syb

def read_1syc(file=root+"/1syc.txt"):
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
dic,onedic = read_dic()
biwords = read_biw()
bichars = read_bic()
onesyl=True
def check(d, tri):
    try:
        return d[tri]
    except KeyError:
        print(tri,"없어")
        return 1e-9
    
def syl_chk_point(ft,ct,bt):
    return (check(c,ct) * 0.1  + check(f,ft) * 0.35+ check(b,bt) * 0.35 )# / 3

def candidate(text):
    c = 0
    words = defaultdict(list)
    
    for j in range(1,max_ngram):
        c = 0
        for i in range(len(text)-j):
            if text[i:i+j+1] in dic:
                c+=1
                words[i].append([c,i,i+j+1,text[i:i+j+1]])
    # print(words)
    words[0] = [[1,0,1,text[0]]] + words[0]
    words[len(text)-1].append([len(text),len(text)-1,len(text)-1+1+1,text[-1]])
    # print(words)
    return words

def iterative_dfs(start_v, token_list,text):
    discovered = []
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
        if bistr in biwords:
            words_point += biwords[bistr] 
    length = len(candidate_word_arr)-1 
    if length == 0:
        return -1.0
    return words_point / length

def calc_char_point(candidate_word):
    chars_point = 0.0
    for c in range(len(candidate_word)-1):
        bic = candidate_word[c:c+2] 
        if bic in bichars:
            chars_point += bichars[bic]
    return chars_point / (len(candidate_word)-1)

def main(text):
    cnouns = None
    temp = 0
    words = candidate(text)
    st = [[] for i in range(10)]
    curr = 0

    for i in words[0]:
        candi = iterative_dfs(i,words,text)
        # print(candi)
        if len(candi) > 0:
            for cdw in candi:
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
                
                firs_1 = False
                last_1 = False
                
                if len(cdw_arr[1]) == 1:
                    first_1 = True
                if len(cdw_arr[-1]) == 1:
                    last_1 = True

                cnouns = max(cnouns,[cdw_arr,point],key=lambda x: x[1])
    return cnouns

def one_syl(text):
    cnouns = []
    if text[0] in onedic and text[1:] in dic:
        # first = ['S'] + [text[0]] + [text[1:]] + ['E']
        first = [text[0]] + [text[1:]]
        
        chars_point = calc_char_point(' '.join(first))
        words_point = calc_word_point(first)

        point = ((words_point * 0.8) + (chars_point * 0.2))

        cnouns.append([first,point])
    if text[-1] in onedic and text[:-1] in dic:
        # ends = ['S'] + [text[:-1]] + [text[-1]] + ['E']
        ends = [text[:-1]] + [text[-1]]

        chars_point = calc_char_point(' '.join(ends))
        words_point = calc_word_point(ends)

        point = ((words_point * 0.8) + (chars_point * 0.2))

        cnouns.append([ends,point])
    # texts = ['S'] + [text] + ['E']
    texts = [text]
    chars_point = calc_char_point(' '.join(texts))
    words_point = calc_word_point(texts)

    point = ((words_point * 0.8) + (chars_point * 0.2))

    cnouns.append([texts,point])

    return max(cnouns,key=lambda x: x[1])#[0][1:-1]
def cnoun(text):
    res = main(text)
    # print(res)
    if res is None:
        res1 = main(text[:-1])#+[text[-1]])
        res2 = main(text[1:])

        t = []
        if res1 != None:
            res1[0] = res1[0][1:-1] + [text[-1]]
            t.append(res1)

        if res2 != None:
            res2[0] = [text[0]] + res2[0][1:-1]
            t.append(res2)

        if not res1 and not res2:
            return [text]
        else:
            return max(t,key=lambda x: x[1])[0]
    
    result = []
    for r in res[0][1:-1]:
        if onesyl and len(r) > 2:
            result_tmp = []
            three_check_ori = ['S'] + [r] #+ ['E']
            chars_point = calc_char_point(' '.join(three_check_ori))
            words_point = calc_word_point(three_check_ori)
            point = ((words_point * 0.8) + (chars_point * 0.2))
            result_tmp.append([three_check_ori,point])

            one_tk = one_syl(r)

            result_tmp.append(one_tk)
            for tk in max(result_tmp,key=lambda x: x[1])[0][1:]:
                result.append(tk)

        else:

            result.append(r)

    return result

# head = ["전","총"]
# tail = ["역","실","사","부"]
if __name__ == "__main__":
    while True:
        text = input("복합명사: ")
        print(cnoun(text))
        # print()
