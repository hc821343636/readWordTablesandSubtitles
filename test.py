from ltp import LTP
if __name__ == '__main__':
    txt="第二条网络信息管理员的目的对网络设备定期检查，确保其正常运行。"
    ltp=LTP("base2")
    res=ltp.pipeline(txt,tasks=['cws','srl'])
    print(res.srl)