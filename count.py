from collections import defaultdict
import re
enc = 'utf-8'

count_uni = defaultdict(int)
count_bi = defaultdict(int)

count_c_uni = defaultdict(int)
count_c_bi = defaultdict(int)

result_uni = open('unidict.txt','w',encoding=enc)
result_bi = open('bidict.txt','w',encoding=enc)
result_lbi = open('lbidict.txt','w',encoding=enc)
result_c_uni = open('unidict_c.txt','w',encoding=enc)
result_c_bi = open('bidict_c.txt','w',encoding=enc)

line_bi = defaultdict(int)
line_bi_cnt = defaultdict(int)
with open('dict.txt',encoding=enc) as f:
    for l in f:
        l = l.strip()
        # lbi = l.replace("S ","").replace(" E","").replace(" ", " | ").strip()
        # lbi = re.sub(" +"," ",lbi)
        # lbi = lbi.split()
        
        # for i in range(len(lbi)-1):
        #     bi = "".join(lbi[i:i+2]) 
        #     line_bi[bi] += 1
        #     line_bi_cnt[lbi[i]] +=1 
        
        l_c = l#.replace(' ','')
        for l_ in l_c:
            count_c_uni[l_] += 1
        
        for i in range(len(l_c)-1):
            bi = l_c[i:i+2]
            count_c_bi[bi] += 1
 
        l = l.split()

        for l_ in l:
            count_uni[l_] += 1
        
        for i in range(len(l)-1):
            bi = ','.join(l[i:i+2])
            count_bi[bi] += 1
one_syllable_f = defaultdict(int)
one_syllable_b = defaultdict(int)
one_syllable_c = defaultdict(int)
one_syllable_f_cnt = defaultdict(int)
one_syllable_b_cnt = defaultdict(int)
one_syllable_c_cnt = defaultdict(int)

result_1syf = open('1syf.txt','w',encoding=enc)
result_1syb = open('1syb.txt','w',encoding=enc)
result_1syc = open('1syc.txt','w',encoding=enc)
# result_c_1syf = open('1syf_c.txt','w',encoding=enc)
# result_c_1syb = open('1syb_c.txt','w',encoding=enc)
import re
with open('1syllable.txt',encoding=enc) as f:
    for l in f:
        l = l.strip()
        # flag = False
        # if l == "S 팀 분위기 E":
        #     flag = True
        l = l.replace("S ","").replace(" E","")
        # ll = l
     
        # if len(l.split()[0]) == 1:
        temp = l.split()#[1:][:-1]
        l = "S"+temp[0] + " " + re.sub(" +","","".join(temp[1:]))+"E"
        str_f = list(l)
        # if flag:
        #     print(l)   
        for i in range(len(str_f)-2):        
            
            # for i in range(len(str_f)-1):
            fbi = ''.join(str_f[i:i+3])
            # if flag:
            #     print(fbi)
            # fbi = ''.join(str_f[1:1+3])
            # print(fbi)
            # fbi = ''.join(str_f[2:2+3])
            # print(fbi)
            # if flag:
                # print(fbi)
            one_syllable_f[fbi] += 1
            one_syllable_f_cnt[fbi[:-1]] +=1
            
            one_syllable_c[fbi] += 1
            # print(fbi+"<<<<<")
            one_syllable_c_cnt[fbi[0]+fbi[2]] +=1
            # print(temp)
            # print(fbi)
            # rfbi = list(reversed(fbi))
            # # print(fbi,rfbi)
            # rfbi = "r"+"".join(rfbi)
            # one_syllable_f[rfbi] += 1
            # one_syllable_f_cnt[rfbi[1:-1]] +=1
        
        # str_b = list(reversed(temp))
        # l = "S"+temp[0] + "  " + re.sub(" +","","".join(temp[1:]))+"E" 
        l = list(reversed(l))
        str_b = l
        for i in range(len(str_b)-2):
        # if len(str_b[0]) == 1:
            temp = str_b
            # print(temp)
            # print(temp)
              #"".join(temp[:-1]) + temp[-1]
            # l = reversed(l)        
            # str_b = list(l)
            # print(str_b)
            # for i in range(len(str_b)-1):
            bbi = ''.join(str_b[i:i+3])
            # if flag:
            #     print(bbi)
            # print(bbi+"<<<<")
            # print(bbi+"<<<")
            # print(bbi[:-1]+"<<<")
            # exit()
            one_syllable_b[bbi] += 1
            one_syllable_b_cnt[bbi[:-1]] +=1
            
            # rbbi = list(reversed(bbi))
            # # print(fbi,rfbi)
            # rbbi = "r"+"".join(rbbi)
            # one_syllable_b[rbbi] += 1
            # one_syllable_b_cnt[rbbi[1:-1]] +=1


for k,v in one_syllable_c.items():
    result_1syc.write(k+"\t"+str(v)+"\t"+str(v/one_syllable_c_cnt[k[0]+k[2]])+"\n")

for k,v in one_syllable_f.items():
    if k[0] == "r":
        result_1syf.write(k+'\t'+str(v)+'\t'+str(v/one_syllable_f_cnt[k[1:-1]])+'\n')
    else:
        result_1syf.write(k+'\t'+str(v)+'\t'+str(v/one_syllable_f_cnt[k[:-1]])+'\n')
result_1syf.close()

for k,v in one_syllable_b.items():
    # print(k)
    if k[0] == "r":
        result_1syb.write(k+'\t'+str(v)+'\t'+str(v/one_syllable_b_cnt[k[1:-1]])+'\n')
    else:
        result_1syb.write(k+'\t'+str(v)+'\t'+str(v/one_syllable_b_cnt[k[:-1]])+'\n')
result_1syb.close()


for k,v in line_bi.items():
    uni = k.replace("|"," | ").strip()
    uni = uni.split()[0]
    result_lbi.write(k+'\t'+str(v)+"\t"+str(v/line_bi_cnt[uni])+'\n')
result_lbi.close()

for k,v in count_uni.items():
    result_uni.write(k+'\t'+str(v)+'\n')
result_uni.close()

for k,v in count_bi.items():
    result_bi.write(k+'\t'+str(v)+'\t'+str(v/count_uni[k.split(',')[0]])+'\n')
result_bi.close()

for k,v in count_c_uni.items():
    result_c_uni.write(k+'\t'+str(v)+'\n')
result_c_uni.close()

for k,v in count_c_bi.items():
    result_c_bi.write(k+'\t'+str(v)+'\t'+str(v/count_c_uni[k[0]])+'\n')
result_c_bi.close()