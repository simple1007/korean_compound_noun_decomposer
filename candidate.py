cnoun = ['삼','성','삼성','전자','통','합','통합','교육','집행','위원','전','자','집','행']
check = 0
text = '통합교육집행'

temp = []
# while True:
# start = 0
# while check < len(text):
#     temp = []

start = 0
# for j in range(len(text)):
#     start = j
all = []
# while True:
    # start = 0
count = 0
result = []

# index = [0]
stack = [[0]]

# flag = True
while len(stack) > 0:
    index = stack.pop(-1)
    for i in range(index[-1],start,len(text)):
        t = text[start:i+1]
        if t in cnoun:
            index.append(i+1)
            
            if i+1 == len(text):
                break
            else:
                stack.append(index)
    # index = stack.pop(-1)

# for i in range(len(text)):
#     t = text[start:i+1]

#     if t in 

# while True:
#     # stag = 0
#     # start = 0
#     for j in range(len(text)):
#         start = j
#         for i in range(len(text)):
#             val = text[start:i+1]
#             # print(val)
#             if val in cnoun:
#                 # temp.append([[start,i],val])
#                 # start = i+1
#                 # if start[0] == 0:
#                 #     all.append([i+1])

#                 result.append([start,i,val])
#             start = start+1#min(result)
#     # print(result)
#     # result = []
#     # start = all.pop(-1)
#     count+=1
#     if count == 10:
#         break
#     # stag+=1
# temp.sort()
# print(temp)
# result.sort(key=lambda x: x[0] > x[1])
# print(result)