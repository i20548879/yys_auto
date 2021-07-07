import os
from typing import Counter
import aircv as ac
import uiautomator2 as u2
import random
import time

class ScreenMonitor:
    def __init__(self,serial) -> None:
        global d,serial_num
        serial_num=serial
        #远程连接修改这里
        #d=u2.connect("192.168.15.10:5555")
        if '.' in serial_num:
            #表示是ip地址，远程调试，需要connect
            os.system("adb connect "+serial_num)
        d=u2.connect(serial_num)
        print('连接成功')
        pass
   

    def screenshot(self):
        #获取当前截图
        #涉及两台设备则需要-s {serial},可通过adb devices查看serial
        if serial_num=='':
            os.system("adb shell screencap -p /sdcard/Download/screenshot.jpg")
            os.system("adb pull /sdcard/Download/screenshot.jpg screenshot.jpg > doc.txt")
        else:
            os.system("adb -s %s shell screencap -p /sdcard/Download/screenshot.jpg"%serial_num)
            os.system("adb -s %s pull /sdcard/Download/screenshot.jpg screenshot.jpg > doc.txt"%serial_num)

    def clicktarget(self,imgobj,confidencevalue=0.7):
        #识别目标图片在屏幕中的坐标，并点击
        self.screenshot()
        target_img=ac.imread(imgobj)
        source_img=ac.imread(r"screenshot.jpg")
        match_result = ac.find_template(source_img,target_img,confidencevalue,rgb=True)
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
        source_img=ac.imread(r"./screenshot.jpg")
        match_result = ac.find_template(source_img,target_img,confidencevalue,rgb=True)
        if match_result:
            print(match_result)
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
                    startx=random.randint(1500,1600)
                    starty=random.randint(375,425)
                    endx=random.randint(900,1000)
                    endy=random.randint(375,425)
                    d.swipe(startx,starty,endx,endy)
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
            #检测结算
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
            while(not self.findtarget(r"./match/tiaozhan.png"),0.97):
                wait_count+=1
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
            #防止没点到，再判断5次（如果点到了这几次的时间也正好在刷御魂，应该不会有人几秒秒刷一把御魂吧，不会吧不会吧）
            self.wait_click(r"./match/tiaozhan.png",5)
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
            
    def test(self):
        t1=time.time()
        self.screenshot()
        t2=time.time()
        print(t2-t1)

if __name__ == '__main__':
    print('########## yys_auto v1.0 ##########')
    connectmode=input("[调试模式]：\n1.单设备USB连接\n2.远程调试/多设备USB连接\n")
    if connectmode=='2':
        print('————————————————————')
        serial=input("[连接设备]请输入ip地址(远程调试)或序列号(多USB设备)\n注意：远程调试请先在命令行测试adb connect [ip]是否能连接\n多设备USB连接请在命令行输入adb devices确认序列号\n")
    else:
        serial=''
    bot=ScreenMonitor(serial)
    
    print('————————————————————')
    mode=input("[执行功能]：\n1.探索\n2.御魂：队长模式\n3.御魂：队员模式\n")
    exe_count=input("[执行次数]: ")
    print("若脚本长时间无响应，请自行截图并替换match文件夹下的图片")
    if mode=='1':
        print("开始探索，请选中探索关卡后开启，让脚本自己点击进入")
        bot.tansuo(int(exe_count))
    elif mode=='2':
        print("御魂队长模式，请手动开一把后自动邀请队友，此时在房间开启脚本，让脚本自己点击挑战按钮")
        bot.yuhun_duizhang(int(exe_count))
    elif mode=='3':
        print("御魂队员模式，请手动开一把后点击自动接收邀请，再开启脚本")
        bot.yuhun_duiyou(int(exe_count))
    else:
        print("请输入正确的数字编号")
    
    
    
    
    
