# Python OneDrive Web

一个使用OneDrive网盘来快速共享文件下载的网页



[GitHub](https://github.com/bytfr/PyOneWeb) [Gitee](https://gitee.com/grmine/PyOneWeb)

[演示网址 (我自己在家搭建)](http://download2.grmine.cn/)

[演示网址 (腾讯云搭建)](http://110.42.148.82/)



- 文件共享

![](https://s4.ax1x.com/2022/02/21/Hjsf39.png)



在线预览

![](https://s4.ax1x.com/2022/02/22/HzrRbt.png)

![](https://s4.ax1x.com/2022/02/22/Hzr2DI.png)

## 视频教程

https://www.bilibili.com/video/BV1Sa411k71c


## 初始化

1. 需要安装Python 3(我使用的是Python 3.9版本)  [点击下载](https://www.python.org/downloads/release/python-390/ )

2. 安装所需模块 (有些电脑或系统要把pip改为pip3)

   ```shell
   pip install flask
   pip install requests
   pip install flask-cors
   ```

3. 运行

   在文件夹打开cmd输入 python index.py (有些电脑或系统要把python改为python3 如果会使用gunicorn最好)

4. 配置

   在第一次使用，网页会自动跳转到安装页面，按照提示进行配置。

   管理员登录面板：网址+/login

   如果主页面出现了404或报错无法访问的情况下，请进入管理员面板检查配置是否出错，如果连管理员面板也无法进入，请尝试编辑或删除setthing.json文件，若仍然没有得到解决，请使用QQ联系我。
   QQ:2678509244



# 警告！

### 请不要因为任何情况将setthing.json泄露给任何人，这可能会影响你的OneDrive账号安全，如果已经泄露请更改后台密码并更改OneDrive共享链接

