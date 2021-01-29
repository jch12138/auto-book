import requests
import re
import time
import yaml
import os

class Seat :

    def __init__(self,account,password,roomId,seatNum,startTime,endTime):
       
        self.account = account
        self.password = password
        #requests.adapters.DEFAULT_RETRIES = 5 # 增加重连次数
        self.client = requests.Session()
        self.client.keep_alive = False # 关闭多余连接
        self.roomId = roomId
        self.seatNum = seatNum
        self.seatid = 0
        self.startTime = startTime
        self.endTime = endTime

    def notice(self,tile, text):
        requests.get('https://sc.ftqq.com/SCU114947T9322fe437e3e5df900c245a41dfe6b5f6a127ec763.send?text={}&desp={}![logo](http://baldstudio.cn/da-call.png)'.format(tile, text))

    def login(self):
    # 登陆
        url = "https://passport2.chaoxing.com/fanyalogin"

        payload = {
            "uname":  self.account,
            "password": self.password
        }

        headers = {
            'Host': 'passport2.chaoxing.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E14 Safari/604.1 Edg/5.0.413.3',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-',
            'Origin': 'https://passport2.chaoxing.com',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://passport2.chaoxing.com/login?fid=&newversion=true&refer=http%3A%2F%2Fi.chaoxing.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.,en-GB;q=0.7,en-US;q=0.6',
        }

        response = self.client.post(url, headers=headers, data = payload)

        print(response.text)
    def logout(self):
        url = "http://office.chaoxing.com/front/user/login/logout"

        payload = {}
        headers = {
            'Host': 'office.chaoxing.com',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E14 Safari/604.1 Edg/5.0.413.121',
            'Referer': 'http://office.chaoxing.com/front/third/apps/seat/index',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.,en-GB;q=0.7,en-US;q=0.6',
            #'Cookie': 'lv=3; fid=2149; _uid=94530449; uf=da03eb5260151e329e20e4fadaee49d39077ae9c64d294556b0bf3221ea7b1b27203e7696cd03d4444e4d23fcfc49d67c0c30ca5047c5a963e5f11099aa37f6591399cc56ce71fc6e5943dd376a3f97742b319326fb9db2ad12d2a3cd25a207f42725; _d=1600063733452; UID=94530449; vc=3DCC55BAFC00AA5D673D76ED55B220; vc2=9CAF720735149A4707AD03CB5AE2D; vc3=XVM6PFRS4ynVdDEQE1j9m94qAi2E54Kv069eD2N%2BN4J5yn3GpyDaUQRiKUHRWcTuf2FsKjQtZZXibA4d05SkHvYVa9fSEB45tPkpKVhYJU2znehoKtBumfRwv2%2Bm4QJL6VAAwQahQg71Zjxl5h4b3rH%2FDYJE1o6olTTq6z%2BM%3D9d006ede1534c55950d550f3ffd2db7; xxtenc=e774bda6ede5c24dcfc761f0ec70a219; DSSTASH_LOG=C_3-UN_666-US_94530449-T_1600063733454; route=6b5f9c5cf712c012a6021ee235d6b97'
        }

        res = self.client.get(url, headers=headers, data = payload)

        print(res.text.encode('utf'))

    def get_token(self):

        # 获取 token
        url = "http://office.chaoxing.com/front/third/apps/seat/select"

        payload = {}
        headers = {
            'Host': 'office.chaoxing.com',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E14 Safari/604.1 Edg/5.0.413.3',
            'Referer': 'http://office.chaoxing.com/front/third/apps/seat/select?id=170&day=2020-09-14&seatNum=05&backLevel=1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.,en-GB;q=0.7,en-US;q=0.6',
        }
        response = self.client.get( url, headers=headers, data = payload)

        pattern = re.compile(r'token: (.*\')')

        try:
            token = re.search(pattern,response.text,flags=0).group().split("'")[1]
        except:
            token = None

        print("Token: {}".format(token))

        self.token = token
        #return token

    def submit(self):
        # 提交
        url = "http://office.chaoxing.com/data/apps/seat/submit?roomId={}&startTime={}&endTime={}&day={}&seatNum={}&token={}"

        headers = {
            'Host': 'office.chaoxing.com',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E14 Safari/604.1 Edg/5.0.413.3',
            'Referer': 'http://office.chaoxing.com/front/third/apps/seat/select?id=99&day=2020-09-14&backLevel=2',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.,en-GB;q=0.7,en-US;q=0.6',
            # 'Cookie': 'oa_uid=94530449; oa_name=%E5%B0%9A%E5%F%AF%E5%BF%3; source=""; lv=3; fid=2149; _uid=94530449; uf=da03eb5260151e329e20e4fadaee49d39077ae9c64d294556b0bf3221ea7b1b27203e7696cfa0530dc0be32fac49d67c0c30ca5047c5a963e5f11099aa37f6591399cc56ce71fc6e5943dd376a3f97742b31932ce7437aa21b322cabd620a766541040; _d=1600062909547; UID=94530449; vc=3DCC55BAFC00AA5D673D76ED55B220; vc2=9CAF720735149A4707AD03CB5AE2D; vc3=d%2BLllQ4vL0rs2BrGIgSRB5wlDb6bt6SpRWjT%2BRz25EKZqsofiztEqyrlzsL9fiqO5P1TVHlE2nosfPdAQRteo5y4ixRP3KUoXNTWrZGlVWiaiDOgWq9R2OrZ7OmKUlFbkzgZr%2BXY46yA%2Br3YWNr%2FYzrNYDwiUnWA3C4%3D6acb1259525b0ec6312e050dac6d67; xxtenc=e774bda6ede5c24dcfc761f0ec70a219; DSSTASH_LOG=C_3-UN_666-US_94530449-T_1600062909549; spaceFid=2149; JSESSIONID=A4FE150607B205CA00CABB2ED531679.reserve_web_126; oa_deptid=29170; oa_enc=cb50f900c4fefb4a7e3efcb1525f370; route=af71b26362ce1457b3e61b7eb523ec'
        }

        url = url.format(self.roomId,self.startTime,self.endTime,self.day,self.seatNum,self.token)
        print(url)

        response = self.client.get(url, headers=headers, data = None)

        if(response.json()['success']):
            print('预约成功')
            return True
        else:
            print('预约失败')
            print(response.text)
            return False

    def get_time(self):
        localtime = time.localtime(time.time()+86400)
        year = localtime[0]
        month = localtime[1]
        day = localtime[2]
        date = '{:0>4d}-{:0>2d}-{:0>2d}'.format(year,month,day)
        print(date)
        self.day = date
        #eturn date
    
    def delete(self):
        self.client.close()
    
    def check_seat(self):
        url = "http://office.chaoxing.com/data/apps/seat/index"

        payload = {}
        headers = {
            'Host': 'office.chaoxing.com',
            #'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/85.0.4183.121',
            'Referer': 'http://office.chaoxing.com/front/third/apps/seat/index',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            #'Cookie': 'lv=3; fid=2149; _uid=94530449; uf=da0883eb5260151e3298e20e4fadaee49d39077ae9c64d29848556b0bf3221ea7b1b827203e7696cd03d4444e4d23fcfc49d67c0c30ca5047c5a963e85f11099aa37f6591399cc56ce71fc6e59483dd376a3f97742b319326fb9db2ad12d2a3c8d25a207f4287285; _d=1600063733452; UID=94530449; vc=38DCC55BAFC00AA5D673D76E8D55B220; vc2=9CAF720735149A4707A8D03C8B5A8E2D; vc3=XVM6PFRS4ynVdDEQE1j9m984qAi2E54Kv069eD2N%2BN4J5yn3GpyDaUQRiKUHRWcTuf2FsKjQtZZXibA4d05SkHvYVa9fSEB45tPkpKVhYJU2zneh8oKtBumfRwv2%2Bm4QJL6VAAwQahQg71Zjxl5h4b3rH%2FDYJE1o6olT8Tq6z%2BM%3D9d006ede15834c55950d550f3ffd2db7; xxtenc=e774bda6ede5c24dcfc761f0ec70a219; DSSTASH_LOG=C_38-UN_666-US_94530449-T_1600063733454; route=710ce7dd3f4dfc1c1692f919f3ebcc34'
        }

        res = self.client.get(url, headers=headers, data = payload).json()
        if res['success']:
            self.seatId  = res['data']['curReserves'][0]['id']
            self.roomId = res['data']['curReserves'][0]['roomId']
            self.seatNum = res['data']['curReserves'][0]['seatNum']
            print(self.seatId,self.roomId,self.seatNum)

        #print(res.json())

    def get_id(self):

        url = "http://office.chaoxing.com/data/apps/seat/reserve/info?id={}&seatNum={}".format(self.roomId,int(self.seatNum))

        payload = {}
        headers = {
            'Host': 'office.chaoxing.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/85.0.4183.102',
            'Referer': 'http://office.chaoxing.com/front/third/apps/seat/code?id=977&seatNum=60',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        response = self.client.get(url, headers=headers, data = payload)
        print(response.text)
        seatId = response.json()['data']['seatReserve']['id']
        print('座位 id : {}'.format(seatId))
        self.seatId = seatId
        #return seatId

    def signin(self):
        url = 'http://office.chaoxing.com/data/apps/seat/sign?id={}'.format(self.seatId) #小in专座

        payload = {}
        headers = {
            'Host': 'office.chaoxing.com',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/85.0.4183.102',
            'Referer': 'http://office.chaoxing.com/front/third/apps/seat/code?id=977&seatNum=60',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        response = self.client.get(url, headers=headers, data = payload)

        if(response.json()['success']==True):
            print('签到成功!')
            print(response.text)

        else:
            print('签到失败!')
            print(response.text)

    def signout(self):

        url = "http://office.chaoxing.com/data/apps/seat/signback?id={}".format(self.seatId)

        payload = {}
        headers = {
            'Host': 'office.chaoxing.com',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'DNT': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/85.0.4183.102',
            'Referer': 'http://office.chaoxing.com/front/third/apps/seat/index?appId=1000&fidEnc=321a0e36ee4a9fd1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        }

        response = self.client.get(url, headers=headers, data=payload)

        if(response.json()['success'] == True):
            print('成功签退!')
            return True
        else:
            print('签退失败')
            print(response.text)
            return False

def parse_config():
        filePath = os.path.dirname(__file__)
        fileNamePath = os.path.split(os.path.realpath(__file__))[0]
        yamlPath = os.path.join(fileNamePath,'config.yaml')
        f = open(yamlPath,'r',encoding='utf-')
        config_file = f.read()

        config = yaml.load(config_file)
        if(config):
            config = config['record']
            return config
        else:
            print('Config file has problem!')
            return None
