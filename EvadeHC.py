import get_file as f
import morpher as m
import tester as t
import detector
import get_file
import time
import os
d=detector.detector()
p=10
q1=20
q2=q1/20
def EvadeHC():
    C=[]
    bytes=get_file.get_bytes_batch()
    print(len(bytes))
    for bytez in bytes:
        ti=time.time()
        f = open('temp/' + str(ti) , 'wb+')
        filename='temp/' + str(ti)
        f.write(bytez)
        f.close()
        if t.submit_query_report(filename) is False:
            print("is not malicious! skip.")
            continue
        C=[bytez]
        v0=-1
        C_q2=[]
        paths=[[]]
        while v0 < 1:
            C_q2, paths_q2=get_score_nolessv0(C,v0,paths)
            while len(C_q2)<q2:
                c,p=get_score_nolessv0(C, v0, paths, q2 - len(C_q2))
                C_q2.extend(c)
                paths_q2.extend(p)
            print("get " + str(len(C_q2)) + " samples that has score >= " + str(v0))
            v0+=2
            C=C_q2[:]
            paths=paths_q2
        C_q2=[]
        paths_q2=[]
        while len(C_q2) == 0:
            C_q2,paths_q2=get_score_nolessv0(C, v0, paths)

        success_samples=C_q2[0]
        name=str(int(time.time()))
        f=open('success/'+name, 'wb+')
        f.write(success_samples)
        f.close()
        f=open('success/'+name+'_path','w+')
        f.write(str(paths_q2[0]))
        f.close()
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
        print("malicious disapear at beginning.")
        return -1
    if t.submit_query_report(files[-1])==True:
        return len(files)
    size=len(files)
    left=0
    right=size-1
    while(left!=right):
        mid=int((left+right)/2)
        print(mid)
        if(t.submit_query_report(files[mid]) is False):
            right=mid
        else:
            left=mid+1
    return left

def get_score_nolessv0(C, v0, paths=[], num=q2):
    C_q2=[]
    paths_q2=[]
    for i in range(len(C)):
        C_q1,p=generate_q1_paths(C[i])
        j = 0
        while (j < len(C_q1)):
            files = []
            n = 0
            ti = int(time.time())
            for byte in C_q1[j]:
                f = open("temp/" + str(ti) + "_" + str(n), 'wb+')
                f.write(byte)
                f.close()
                files.append(str("temp/" + str(ti) + "_" + str(n)))
                n += 1
            mx = binary_search(files)
            print(mx)
            if mx >= 1:
                r0 = target_r(mx, v0)

                if r0<10 and d.submit_report(files[r0]) is False:
                    if v0>=1:
                        print("evading Success!")
                        C_q2.append(open(files[r0], 'rb').read())
                        new_path = paths[i][:]
                        new_path.extend(p[j][:int(mx / 2) + 1])
                        paths_q2.append(new_path)
                        return C_q2, paths_q2
                    C_q2.append(open(files[int(mx / 2)], 'rb').read())  # C_q2 store whose score no less than v0
                    new_path=paths[i][:]
                    new_path.extend(p[j][:int(mx / 2) + 1])
                    paths_q2.append(new_path)
                    if len(C_q2)>=num:
                        return C_q2, paths_q2
            j += 1

    return C_q2, paths_q2



def generate_q1_paths(bytez):
    C_q1=[]
    paths=[]
    for x in range(q1):  # generate q1 paths stored in C_q1
        bytezs,path = m.modify_without_breaking(bytez, m.generate_random_actions(10))
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