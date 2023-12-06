import re

from bixin import predict
from ltp import LTP

# 拟用此代码 找出  对己方效果（积极） 和对敌方效果（消极）
if __name__ == '__main__':
    text = "与敌空袭兵作斗争，干扰、阻断及破坏敌空袭兵器所配备火控指导系统作战效能的有效发挥"

    # 出自安德烈·纪德《人间食粮》
    print(predict(text))

    ltp = LTP('base2')
    hc = '电子防空营的战斗任务：（一） 对陆军战役军团作战方向敌机载雷达实施干扰压制，削弱其目标探测能力，破坏其攻击行动，降低敌空袭作战的效能，并积极为火力防空创造条件。（二） 综合运用光电干扰手段，对敌空地激光、红外、电视等精准制导武器实施干扰，诱偏或直接毁伤、致盲敌光电设备，掩护陆军战役军团作战方向重要目标的对空安全。进攻战斗中电子防空的主要任务是：组织对空侦察，及时发现敌空袭征候，为防空作战提供空袭，判定、分析、识别来袭武器电子信号，为对空电子干扰提供情报支援；与敌空袭兵作斗争，干扰、阻断及破坏敌空袭兵器所配备火控指导系统作战效能的有效发挥。'
    word = ltp.pipeline(hc, tasks=['cws', 'pos'])
    """print(word.cws)
    print(word.pos)"""
    sents = re.split(r'[，：；。]',hc)
    for sent in sents:
        word = ltp.pipeline(sent, tasks=['cws', 'pos'])
        vnum = 0
        vsum = 0
        for w, label in zip(word.cws, word.pos):
            if label == 'v':
                #print(w, predict(w))
                vsum += predict(w)
                vnum += 1
        if vnum != 0:
            score = vsum / vnum
            print(score, sent)


"""  for w,label in zip(word.cws,word.pos):
      if label=='v':
          print(w,predict(w))
      else:
          print(w,label)
"""
