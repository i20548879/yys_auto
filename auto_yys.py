import os
import sys
from typing import Counter
import aircv as ac
import uiautomator2 as u2
import random
import time

class ScreenMonitor:
    def __init__(self) -> None:
        global d
        #远程连接修改这里
        d=u2.connect("192.168.137.131:5555")
        pass
   

    def screenshot(self):
        #获取当前截图
        #涉及两台设备则需要-s {serial},可通过adb devices查看serial
        os.system("adb -s 192.168.137.131:5555 shell screencap -p /sdcard/Download/now.png")
        os.system("adb -s 192.168.137.131:5555 pull /sdcard/Download/now.png screenshot/now.png >doc.txt 2>&1")

    def clicktarget(self,imgobj,confidencevalue=0.7):
        #识别目标图片在屏幕中的坐标，并点击
        self.screenshot()
        target_img=ac.imread(imgobj)
        source_img=ac.imread("screenshot/now.png")
        match_result = ac.find_template(source_img,target_img,confidencevalue)
        if match_result:
            #获取四个点的坐标
            zs,zx,ys,yx=match_result['rectangle']    
            x=random.randint(zs[0],ys[0])
            y=random.randint(zs[1],zx[1])
            d.click(x,y)
            return 0
        else:
            return -1

    def findtarget(self,imgobj,confidencevalue=0.7):
        #在屏幕中找寻对应图片，找到返回True，找不到返回false
        self.screenshot()
        target_img=ac.imread(imgobj)
        source_img=ac.imread(r"./screenshot/now.png")
        match_result = ac.find_template(source_img,target_img,confidencevalue)
        if match_result:
            return True
        else:
            return False

    def wait_click(self,imgobj,confidencevalue=0.7,wait_count=-1):
        #持续等待某个图，直到出现,然后点击它,wait_count代表几次等待不到后就退出,-1为无限等
        while(not self.findtarget(imgobj,confidencevalue) and wait_count!=0):
            wait_count-=1
            time.sleep(5)
        if wait_count!=0:
            self.clicktarget(imgobj,confidencevalue)

    def tansuo(self,exe_times):
        #探索：选完探索章节在探索框处打开（让脚本自己点探索），固定阵容，怪物移动太快了可能点不到，有处理机制不过有点慢
        exe_count=0
        while(exe_count<exe_times):
            self.wait_click(r"./match/tansuo_tansuo.png")
            time.sleep(5)
            print('开始找怪')
            slide_count=0
            while (not self.findtarget(r"./match/tansuo_boss.png")):
                #如果没找到boss就接着找怪打
                while(not self.findtarget(r"./match/tansuo_xiaoguai.png") and slide_count<5):
                    #找不到小怪则滑动
                    slide_count+=1
                    print('没找到怪物，第%i滑动'%slide_count)
                    d.swipe_ext("left",2)
                if (slide_count<5):
                    slide_count=0
                    print('找到小怪，攻击')
                    self.clicktarget(r"./match/tansuo_xiaoguai.png")
                    print('等待战斗结束')
                    self.wait_click(r"./match/jiesuan.png",wait_count=5)
                else:
                    print('滑动次数超过5次，重新检查是否有boss')
            print('攻击Boss')
            self.clicktarget(r"./match/tansuo_boss.png")
            print('等待战斗结束')
            self.wait_click(r"./match/jiesuan.png")
            self.wait_click(r"./match/back.png")
            self.wait_click(r"./match/confirm.png",5)
            print("探索：完成%i/%i"%(exe_count,exe_times))

    def yuhun_duiyou(self,exe_times):
        #御魂 队友模式 先开一把，然后自动同意邀请后开启（也就是队友模式只会管结算界面）
        exe_count=0
        while(exe_count<exe_times):
            while(not self.findtarget(r"./match/shengli.png")):
                if self.findtarget(r"./match/jiesuan.png"):
                    break
                else:
                    time.sleep(1)
                    continue
                #每2秒检测一次
            #没找到胜利界面就会循环
            print("结算中")
            x=random.randint(1700,2200)
            y=random.randint(880,1000)
            d.click(x,y)
            d.click(x,y)
            time.sleep(3)
            x=random.randint(1700,2200)
            y=random.randint(880,1000)
            d.click(x,y)
            d.click(x,y)
            exe_count+=1
            print("御魂：完成%i/%i"%(exe_count,exe_times))
            time.sleep(20)

    def yuhun_duizhang(self,exe_times):
        #御魂 队长模式 先开一把，然后自动邀请队友后开启(会点开始和结算)
        exe_count=0
        while(exe_count<exe_times):
            wait_count=0
            while(not self.findtarget(r"./match/tiaozhan.png")):
                wait_count+=1
                time.sleep(1)
                if wait_count>=20:
                    #重新邀请
                    print("长时间无响应，重新邀请")
                    self.clicktarget(r"./match/yaoqing_jiahao.png")
                    time.sleep(2)
                    self.clicktarget(r"./match/yaoqing_zuijin.png")
                    x=random.randint(780,1150)
                    y=random.randint(270,400)
                    d.click(x,y)
                    self.clicktarget(r"./match/yaoqing_yaoqing.png")
            print("点击挑战")
            self.clicktarget(r"./match/tiaozhan.png")
            time.sleep(15)
            while(not self.findtarget(r"./match/shengli.png")):
                if self.findtarget(r"./match/jiesuan.png"):
                    break
                else:
                    #time.sleep(1)
                    continue
                #每秒检测一次
            #没找到胜利界面就会循环
            print("结算中")
            x=random.randint(1700,2200)
            y=random.randint(880,1000)
            d.click(x,y)
            d.click(x,y)
            time.sleep(3)
            x=random.randint(1700,2200)
            y=random.randint(880,1000)
            d.click(x,y)
            d.click(x,y)
            exe_count+=1
            print("御魂：完成%i/%i"%(exe_count,exe_times))
            


if __name__ == '__main__':
    bot=ScreenMonitor()
    bot.yuhun_duiyou(100)
    #bot.screenshot()
