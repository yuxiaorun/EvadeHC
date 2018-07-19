import get_file as f
import morpher as m
import tester as t
import detector
import get_file
import time
import os
from multiprocessing import Pool, Manager
manager=Manager()

d=detector.detector()
path_len=20
q1=20
q2=q1/5

def EvadeHC():
    clean_temp()
    C=[]
    bytes=get_file.get_bytes_batch()
    print(len(bytes))
    for bytez in bytes:
        clean_temp()
        ti=time.time()
        f = open('temp/' + str(ti) , 'wb+')
        filename='temp/' + str(ti)
        f.write(bytez)
        f.close()
        C=[(100, bytez)]
        v0=90
        C_q2=[]
        paths=[[] for x in range(q1)]
        while v0 >= 70:
            C_q2, paths_q2=get_score_nolessv0(C,v0,paths, q2)
            while len(C_q2)<q2:
                if(len(C_q2)==0):
                    c, p = get_score_nolessv0(C, v0, paths, q2 - len(C_q2))
                else:
                    c,p=get_score_nolessv0(C_q2, v0, paths, q2 - len(C_q2))
                C_q2.extend(c)
                paths_q2.extend(p)

            C_q2.sort(key=lambda x:x[0])
            print("get " + str(len(C_q2)) + " samples that has score <= " + str(v0))
            v0-=5
            C=C_q2[:]
            paths=paths_q2
        print('get C q2 len:',len(C_q2))
        # C_q2=[]
        # paths_q2=[]
        # while len(C_q2) == 0:
        #     C_q2,paths_q2=get_score_nolessv0(C, v0, paths, 2)
        for i in range(len(C_q2)):
            success_samples=C_q2[i][1]
            name=str(int(time.time()))+str(i)
            f=open('success/'+name, 'wb+')
            f.write(success_samples)
            f.close()
            print(paths)
        print("successful evadasion, store sample")
        clean_temp()




def clean_temp():
    path = 'temp'
    for i in os.listdir(path):
        path_file = os.path.join(path, i)
        if os.path.isfile(path_file):
            os.remove(path_file)


    # return result


def binary_search(files):
    if t.submit_query_report(files[0])==False:
        return -1
    if t.submit_query_report(files[-1])==True:
        return len(files)
    size=len(files)
    left=0
    right=size-1
    while(left!=right):
        mid=int((left+right)/2)
        if(t.submit_query_report(files[mid]) is False):
            right=mid
        else:
            left=mid+1
    return left

def get_score_nolessv0(C, v0, paths, num):
    C_m=manager.list()
    paths_q2=manager.list()
    pool = Pool()
    for i in range(len(C)):
        C_q1,p=generate_q1_paths(C[i][1])
        j = 0
        while (j < len(C_q1)):
            pool.apply_async(determine_single, args=(C_q1[j], v0, j, C_m, paths, paths_q2, p,num,))
            j += 1
    pool.close()
    pool.join()
    clean_temp()

    index=0
    tmp=C_m[:]
    tmp.sort(key=lambda x:x[0])
    for i in range(len(tmp)):
        print(tmp[i][0])
        if tmp[i][0] > v0:
            index=i
            break
    tmp=tmp[:index]
    print("get " + str(len(tmp)) + " samples that has score <= " + str(v0))
    return tmp, paths_q2

def determine_single(C, v0, j, C_q2, paths, paths_q2, p, num):
    files = []
    n = 0
    ti = int(time.time())
    for byte in C:
        f = open("temp/" + str(ti) + str(j)+ "_" + str(n), 'wb+')
        f.write(byte)
        f.close()
        files.append(str("temp/" + str(ti) + str(j)+ "_" + str(n)))
        n += 1
    mx = binary_search(files)

    if mx >= 2:
        r0 = target_r(mx, 1)

        if r0 < path_len:
            score=d.submit_report(files[r0])
            C_q2.append((score,open(files[r0], 'rb').read()))
            new_path = paths[j][:]
            new_path.extend(p[j][:int(mx / 2) + 1])
            paths_q2.append(new_path)
            print("find 1 score: "+str(score))
    print('tasks %s ended.'%(j))

def generate_q1_paths(bytez):
    C_q1=[]
    paths=[]
    for x in range(q1):  # generate q1 paths stored in C_q1
        bytezs,path = m.modify_without_breaking(bytez, m.generate_random_actions(path_len))
        C_q1.append(bytezs)
        paths.append(path)
    return C_q1,paths

def target_r(mx,v0):
    return mx-v0

EvadeHC()
# def test():
#     bytes=get_file.get_bytes_batch()
#     bytes=bytes[0:1]
#     record=open('record.txt','w')
#     for bytez in bytes:
#         ti=time.time()
#         f = open('temp/' + str(ti) , 'wb+')
#         filename='temp/' + str(ti)
#         f.write(bytez)
#         f.close()
#         if t.submit_query_report(filename) is False:
#             print("is not malicious! skip.")
#             continue
#         P=generate_q1_paths(bytez)
#         for p in P:
#             test_result=[]
#             detector_result=[]
#             files=[]
#             n=0
#             for b in p:
#                 f = open("temp/" + str(ti) + "_" + str(n), 'wb+')
#                 f.write(b)
#                 f.close()
#                 files.append(str("temp/" + str(ti) + "_" + str(n)))
#                 n += 1
#             for f in files:
#                 detector_result.append(d.submit_report(f))
#                 test_result.append(t.submit_query_report(f))
#             record.write(str(test_result))
#             record.write(str(detector_result))
#     record.close()


# file_list=get_file.get_available_sha256()
# print(len(file_list))
# mal_list=[]
# for file in file_list:
#     bytes=get_file.fetch_file(file)
#     ti=time.time()
#     filename='temp/' + str(ti)
#     f = open(filename , 'wb+')
#     f.write(bytes)
#     f.close()
#     if t.submit_query_report(filename) is True:
#         mal_list.append(file)
# f=open('mal.txt', 'w')
# f.write(str(mal_list))
# f.close()
