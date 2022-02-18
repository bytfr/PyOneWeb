# Python OneDrive Web (PyOneWeb) 使用方法



[GitHub](https://github.com/bytfr/PyOneWeb) [Gitee](https://gitee.com/grmine/PyOneWeb)

[演示网址](http://pyoneweb.vaiwan.com/)

## 视频教程
https://www.bilibili.com/video/BV1Sa411k71c


## 初始化

1. 需要安装Python 3(我使用的是Python 3.9版本)  [点击下载](https://www.python.org/downloads/release/python-390/ )

2. 安装所需模块

   ```shell
   pip3 install flask
   pip3 install requests
   ```

3. 运行

   在文件夹里启动cmd，并输入python index.py 即可运行
   
4. 配置

   在第一次使用，网页会自动跳转到安装页面，按照提示进行配置。

   管理员登录面板：网址+/login

   如果主页面出现了404或报错无法访问的情况下，请进入管理员面板检查配置是否出错，如果连管理员面板也无法进入，请编辑或删除setthing.json文件。



# 警告！

### 请不要因为任何情况将setthing.json泄露给任何人，这可能会影响你的OneDrive账号安全，如果已经泄露请更改后台密码并更改OneDrive共享链接

