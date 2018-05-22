
import requests
import time
import get_file
key='d1c94905ed72f6799aad01bff785ef20d19b1a8643b1e2b37cfaabccabd0d989'
class detector(object):

    def isMalicious(self):
        return True

    def upload(self,file):
        url = 'https://www.virustotal.com/vtapi/v2/file/scan'
        params = {'apikey': key}
        files = {'file': ('myfile1.exe', open(str(file),'rb'))}
        response = requests.post(url, files=files, params=params)
        if (response.status_code != 200):
            print("fail to upload file! statuse code:" + str(response.status_code))
        else:
            print(response.json())
            return response.json()['resource']

    # def upload_sequence(self,sequence):


    def get_report(self, resource):
        url = 'https://www.virustotal.com/vtapi/v2/file/report'
        params = {'apikey': key, 'resource': resource}
        response = requests.get(url, params=params)
        if(response.status_code!=200):
            print("fail to get report! statuse code:"+str(response.status_code))
            return -1
        else:
            if response.json()['response_code']==-2:
                print("queued for analysis. try again after 10s")
                return -1
            score=0
            if 'Cylance' in response.json()['scans'] is False:
                print('NO Cylance')
                return response.json()['scans']['Sophos']['result'] is not None
            if 'Cylance' in response.json()['scans'] and response.json()['scans']['Cylance']['result'] is not None:
                score+=1
            if response.json()['scans']['Sophos']['result'] is not None:
                score+=1
            print('score: ',score)
            return score>0

    def submit_report(self,file):
        resource = self.upload(file)
        time.sleep(10)

        result = self.get_report(resource)
        while (result == -1):
            try:
                time.sleep(20)
                result = self.get_report(resource)
            except Exception:
                result==-1
                continue
        return result


