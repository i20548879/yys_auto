<<<<<<< HEAD
﻿yys_auto  
=======
yys_auto  
>>>>>>> 8c3ec1a51802c0ae9e5aa7d5277c029d2f508112
懂的都懂

####说明####  
原理：adb命令截图并pull到本地，使用aircv进行图色识别对照获取图片坐标，使用uiautomator2随机点击图片坐标点  
  
####安装####  
1.python3  
2.adb  
3.pip install -r requirement.txt  
  
####使用####  
1.需使用数据线连接电脑，并在开发者模式下打开adb调试、USB安装
2.可通过同一局域网远程adb调试（修改connect，加入参数{ip}:{port}即可）  
若要远程不连线手机，执行操作：2.1打开开发者模式 2.2打开wifi调试 2.3先连接数据线，输入adb tcpip 5555 2.4拔线测试，adb connect {ip}  
3.测试手机尺寸2400x1080。若无法正常识别请自行截图并替换match文件夹下面的图片（注意图片大小与屏幕中大小保持一致）  
4.在main函数中设定指定任务和次数  
5.当前目录下命令行运行python yys_auto.py  
tips:双开请重新建个文件夹，把所有东西放里面，启两个命令行即可  
  
####更新####  
1.0 支持探索、御魂队长/队员模式  
探索由于怪物在动容易找不到，加入了处理机制，但还是会比较慢  
1.01 修复队友未进入房间，队长仍然点击灰色挑战的问题;增加引导界面;
