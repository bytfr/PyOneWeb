# Python OneDrive Web (PyOneWeb) 使用方法



[GitHub](https://github.com/bytfr/PyOneWeb) [Gitee](https://gitee.com/grmine/PyOneWeb)

[演示网址](http://pyoneweb.vaiwan.com/)


## 初始化

1. 需要安装Python 3(我使用的是Python 3.9版本)  [点击下载](https://www.python.org/downloads/release/python-390/ )

2. 安装所需模块

   ```shell
   pip3 install flask
   pip3 install requests
   ```

   

3. 进入到 **index.py** 文件中，找到**第九行( class Setthing(): )**，按照格式和注释进行设置

   > ```python
   > self.port = 8080 #这是网站端口，必填，运行前确保端口没有被占用
   > self.host = "0.0.0.0" #网站IP，必填，如果无法访问请先检查IP是否正确
   > self.title = "这里面输入网站标题，可留空"
   > self.name = "这里面输入网站主页面显示的标题，可留空"
   > self.logo_url = "这里输入网页logo链接，可留空，但在指定模板可能会因为格式问题显得难看"
   > self.e_mail = "网页反馈及联系邮箱，可留空"
   > self.template = "网页模板，必填，填写template文件夹下任意模板(文件夹)名，如: neo"
   > self.background_img = "网页背景，可空"
   > self.shared_url = "OneDrive共享链接，必填，不填 共享个 锤子 啊"
   > self.shared_path = "根目录，必填，默认根目录不是OneDrive共享链接根目录，是你OneDrive账号根目录，如下图"
   > ```

   ![image-20220216180345828](https://s4.ax1x.com/2022/02/16/Hh8gV1.png)

   假如你要共享的是“共享”文件夹，那么你要右键"共享"文件夹，然后点击共享，选择""拥有链接的人都可编辑"，复制链接到self.shared_url，并将self.shared_path设置为"共享"



## 运行

在文件夹里启动cmd，并输入python index.py 即可使用
