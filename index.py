# coding:utf-8
import flask
from flask import Flask, render_template, request, session, redirect

import json
import os
import time
import onedrive

try:
    from flask_cors import *
    import requests
except Exception:
    pass


# ======= 函数、类、全局变量声明 ======= #

# 设置类
class Setthing:
    def __init__(self):
        # 是否第一次安装
        self.install = False
        # 默认网站标题
        self.title = "PyOneWeb"
        # 默认网站名
        self.name = "PyOneWeb"
        # 默认Logo
        self.logo_url = "https://static-dbbdc8e5-5f50-4106-bc71-b5a5eedf6400.bspapp.com/grmine_logo.png"
        # 默认邮箱
        self.e_mail = "example@example.com"
        # 默认模板
        self.template = "neo"
        # 背景图
        self.background_img = ""
        # OneDrive 共享链接
        self.shared_url = ""
        # 共享路径
        self.shared_path = ""
        # 初始密码
        self.password = "123456"
        # 刷新纪录时间
        self.time = None

    # 读取设置
    def get_config(self):
        global OneDriveSDK
        with open("./setthing.json", "r") as config:
            set = json.loads(config.read().replace("'", '"'))
            self.title = set['title']
            self.name = set['name']
            self.logo_url = set['logo_url']
            self.e_mail = set['e_mail']
            self.template = str(set['templates'])
            self.background_img = set['background']
            self.shared_url = set['shared_url']
            self.shared_path = set['shared_path']
            self.password = set['password']
            if set['install'] == "True":
                self.install = True
            else:
                self.install = False
            try:
                OneDriveSDK = onedrive.OneDriveSDK(self.shared_url, self.shared_path)
                self.time = time.time()
            except Exception:
                pass
            config.close()

    # 保存设置
    def write_config(self):
        config = {"title": self.title, "name": self.name, "logo_url": self.logo_url,
                  "e_mail": self.e_mail, "templates": str(self.template), "background": self.background_img,
                  "shared_url": self.shared_url, "shared_path": self.shared_path, "password": self.password,
                  "install": str(self.install)}
        with open("./setthing.json", "w") as s:
            s.write(str(config).replace("'", '"'))
            s.close()

    # 初始化
    def init(self):
        # 判断设置(setthing.json)文件是否存在
        if not os.path.exists("./setthing.json"):
            self.write_config()

        # 获取设置
        self.get_config()

        # 判断是否第一次安装
        if self.install:
            try:
                self.time = time.time()
                return onedrive.OneDriveSDK(self.shared_url, self.shared_path)
            except Exception:
                pass


# 获取上一路径
def get_up_file(path):
    if path != "/":
        path = path[:-1]
        path2 = ""
        sum = path.split("/")
        sum.pop()
        sum.pop(0)
        for i in sum:
            path2 += "/" + i
        return "?" + path2 + "/"
    return "/"


# 大小计算
def covertFukeSize(size):
    kb = 1024
    mb = kb * 1024
    gb = mb * 1024
    tb = gb * 1024

    if size >= tb:
        return "%.1f TB" % float(size / tb)
    elif size >= gb:
        return "%.1f GB" % float(size / gb)
    elif size >= mb:
        return "%.1f MB" % float(size / mb)
    elif size >= kb:
        return "%.1f KB" % float(size / kb)
    elif size < kb:
        return "%.1f B" % size


# 获取文件列表
def get_file(path):
    global set
    if path != "" and path[-1] == "/":
        path1 = path[:-1]
    else:
        path1 = path
    file = {}
    file1 = OneDriveSDK.get_folder_file(path1)
    file[path] = []
    file["download_url"] = {}
    for i in file1:
        if covertFukeSize(i["size"]) is None:
            i["size"] = "0 KB"
        else:
            i["size"] = covertFukeSize(i["size"])
        i["fileSystemInfo"]["lastModifiedDateTime"] = i["fileSystemInfo"]["lastModifiedDateTime"].replace("T",
                                                                                                          " ").replace(
            "Z", " ")
        if "folder" in i:
            file[path].append(
                {"name": i["name"], "size": i["size"], "date": i["fileSystemInfo"]["lastModifiedDateTime"],
                 "url": path + i["name"] + "/", "type": "path"})
        else:
            file[path].append({"name": i["name"], "size": i["size"],
                               "date": i["fileSystemInfo"]["lastModifiedDateTime"], "url": path + i["name"],
                               "type": "file"})
            file["download_url"][i["name"]] = i["@content.downloadUrl"]
    print(file)
    return file


# 判断是否为路径
def isDir(path):
    if path[-1] == "/":
        return True
    return False


set = Setthing()

# 初始化
OneDriveSDK = set.init()

# ======= 函数、类、全局变量声明 ======= #

# ======= 网页 ======= #

app = Flask(__name__)
app.secret_key = 'QWERTYUIOP'
CORS(app, supports_credentials=True)


# 404 错误
@app.errorhandler(404)
def Error_notfound(e):
    return render_template(set.template + '/index.html', up_file="/", logo_url=set.logo_url,
                           e_mail=set.e_mail, index="Error",
                           name=set.name, file=[
            {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"},
            {"name": "NotFound 没有这个文件或路径", "size": "", "date": "", "url": "", "type": "file"}
        ], background_img=set.background_img,
                           title=set.title, index_list=["Error", ""])


# 500 错误
@app.errorhandler(500)
def Error_500(e):
    return render_template(set.template + '/index.html', up_file="/", logo_url=set.logo_url,
                           e_mail=set.e_mail, index="Error",
                           name=set.name, file=[
            {"name": "Error 500 服务器内部错误", "size": "", "date": "", "url": "", "type": "file"},
            {"name": "如果你是用户，请联系网页搭建者" + set.e_mail, "size": "", "date": "", "url": "mailto:" + set.e_mail,
             "type": "file"},
            {"name": "如果你是开发者，请联系邮箱2678509244@qq.com", "size": "", "date": "", "url": "mailto:" + set.e_mail,
             "type": "file"}
        ], background_img=set.background_img,
                           title=set.title, index_list=["Error", ""])


# 安装引导
@app.route('/install', methods=['get', 'post'])
def install():
    global set
    # 判断是否为第一次运行
    if set.install:
        # 返回主页面
        return redirect("/")
    # 获取页数
    page = request.values.get("page")

    if page == "0":
        tj = {"go": True}

        import platform
        if platform.python_version()[0] == "3":
            tj["Python"] = True
        else:
            tj["Python"] = False
            tj["go"] = False

        try:
            import flask as fla
            tj["Flask"] = True
        except Exception:
            tj["Flask"] = False
            tj["go"] = False

        try:
            import requests as req
            tj["requests"] = True
        except Exception:
            tj["requests"] = False
            tj["go"] = False

        try:
            import flask_cors
            tj["flask-cors"] = True
        except Exception:
            tj["flask-cors"] = False
            tj["go"] = False
        return render_template("install/0.html", tj=tj)

    # 页数 1
    if page == "1":
        if request.method == 'POST':
            set.shared_url = request.form.get("shared_url")
            return redirect("/install?page=2")
        else:
            return render_template("install/1.html")

    # 页数 2
    if page == "2":
        set.install = True
        set.write_config()
        set.get_config()
        return render_template("install/2.html")
    # 初始化页数
    else:
        return redirect("/install?page=0")


# 主函数
@app.route('/', methods=['get', 'post'])
def main():
    global OneDriveSDK

    # 判断是否为第一次安装
    if not set.install:
        return redirect("/install?page=0")
    try:
        # 如果距离第一次刷新超过30分钟
        if time.time() - set.time >= 1800:
            # 刷新
            OneDriveSDK = onedrive.OneDriveSDK(set.shared_url, set.shared_path)
    except Exception:
        pass
    list = []
    for r in request.values:
        list.append(r)
    if not list:
        list.append("/")
    index = list[0]
    '''
    致改源码的你
    print("wdnmd")
    '''
    # 判断是否为路径
    if isDir(index):
        # 获取文件
        up_file = get_up_file(index)
        index_list = index.split("/")
        index_list.pop(0)
        try:
            file = get_file(index)
            return render_template(set.template + '/index.html', up_file=up_file, logo_url=set.logo_url,
                                   e_mail=set.e_mail, index=index,
                                   name=set.name, file=file[index], background_img=set.background_img,
                                   title=set.title, index_list=index_list)
        except Exception as Error_text:
            return render_template(set.template + '/index.html', up_file=up_file, logo_url=set.logo_url,
                                   e_mail=set.e_mail, index=index,
                                   name=set.name, file=[
                    {"name": Error_text, "size": "", "date": "", "url": "", "type": "file"}
                ], background_img=set.background_img,
                                   title=set.title, index_list=index_list)
    else:
        # 下载
        try:
            fullfilename = index
            fullfilenamelist = fullfilename.split('/')
            filename = fullfilenamelist[-1]
            filepath = fullfilename.replace('/%s' % filename, '')
            download_url = get_file(filepath)["download_url"]
            if filename in download_url:
                download_url = download_url[filename]
                return redirect(download_url)
            return render_template(set.template + '/index.html', up_file="/", logo_url=set.logo_url,
                                   e_mail=set.e_mail, index=index,
                                   name=set.name, file=[
                    {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}
                ], background_img=set.background_img,
                                   title=set.title, index_list=["Error"])
        except Exception:
            return render_template(set.template + '/index.html', up_file="/", logo_url=set.logo_url,
                                   e_mail=set.e_mail, index=index,
                                   name=set.name, file=[
                    {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}
                ], background_img=set.background_img,
                                   title=set.title, index_list=["Error"])


# api函数
@app.route('/api', methods=['get'])
def api():
    global file, yu_load_isok, OneDriveSDK
    list = []
    for r in request.values:
        list.append(r)
    if not list:
        list.append("/")
    index = list[0]
    try:
        # 如果距离第一次刷新超过30分钟
        if time.time() - set.time >= 1800:
            # 刷新
            OneDriveSDK = onedrive.OneDriveSDK(set.shared_url, set.shared_path)
    except Exception:
        pass
    if isDir(index):
        index_list = index.split("/")
        try:
            api_dict = {"file_list": get_file(index)[index], "index": index, "up_file":
                get_up_file(index), "index_list": index_list, "name": set.name, "background_img": set.background_img}
            return api_dict
        except Exception:
            return {"file_list": [{"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}],
                    "index": "Error", "up_file":
                        "/", "name": set.name, "background_img": set.background_img}
    else:
        try:
            fullfilename = index
            fullfilenamelist = fullfilename.split('/')
            filename = fullfilenamelist[-1]
            filepath = fullfilename.replace('/%s' % filename, '')
            download_url = get_file(filepath)["download_url"]
            if filename in download_url:
                download_url = download_url[filename]
                return {"download_url": download_url, "index": index, "up_file": get_up_file(index)}
            return {"file_list": [{"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}],
                    "index": "Error", "up_file":
                        "/", "name": set.name, "background_img": set.background_img}
        except Exception:
            return {"file_list": [{"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}],
                    "index": "Error", "up_file":
                        "/", "name": set.name, "background_img": set.background_img}


# 后台登录
@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'GET':
        return render_template('admin/index.html', title=set.title, tz=0)
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user == 'admin' and pwd == set.password:
        session['user_info'] = user
        return render_template('admin/index.html', msg={"code": 0, "msg": '登录成功'}, title=set.title, tz=1)
    else:
        return render_template('admin/index.html', msg={"code": 1, "msg": '用户名或密码输入错误'}, title=set.title, tz=0)


# 管理员面板
@app.route('/admin', methods=['get', 'post'])
def admin():
    global set
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    if request.method == 'POST':
        set.title = request.form.get('title')
        set.name = request.form.get('name')
        set.logo_url = request.form.get('logo_url')
        set.e_mail = request.form.get('e_mail')
        set.template = request.form.get('template')
        set.background_img = request.form.get('background')
        set.shared_url = request.form.get('shared_url')
        set.shared_path = request.form.get('shared_path')
        set.password = request.form.get('password')
        set.write_config()
        set.get_config()
        return render_template('admin/admin.html', title=set.title,
                               name=set.name, logo_url=set.logo_url, e_mail=set.e_mail,
                               template=set.template, background=set.background_img,
                               shared_url=set.shared_url, shared_path=set.shared_path,
                               password=set.password, msg="修改成功")
    else:
        return render_template('admin/admin.html', title=set.title,
                               name=set.name, logo_url=set.logo_url, e_mail=set.e_mail,
                               template=set.template, background=set.background_img,
                               shared_url=set.shared_url, shared_path=set.shared_path,
                               password=set.password)


# 在线预览
@app.route('/preview/<path:p>/<string:file>')
def preview(p, file):
    try:
        # 文件名
        filename = file
        # 文件路径
        filepath = "/" + p
        # 路径
        index_list = (p + "/" + filename).split("/")
        # 结尾
        index_list.append("")
        # 获取文件类型
        type = filename.split(".")[-1]
        # 下载路径
        url = "/?" + filepath + "/" + filename
        # 下载链接
        download_url = get_file(filepath)["download_url"]
        # 如果文件存在
        if filename in download_url:
            download_url = download_url[filename]
            text = ""
            # 如果文件是纯文本
            if type in ["txt", "json", "html", "md"]:
                # 获取文件内容
                text = requests.get(download_url).text
                # 如果文件是纯文本但有样式
                if type in ["html", "md"]:
                    if type == "md":
                        print(text)
                        text = text.replace("\r\n", r"\n")
                    elif type == "html":
                        return flask.Markup(text)
            print(text)
            return render_template(set.template + '/preview.html', text=text, up_file=filepath, type=type,
                                   download_url=download_url, logo_url=set.logo_url,
                                   e_mail=set.e_mail, index=filepath,
                                   name=set.name, background_img=set.background_img,
                                   title=set.title, index_list=index_list, url=url)
        # 否则返回404
        return render_template(set.template + '/preview.html', up_file="/", logo_url=set.logo_url,
                               e_mail=set.e_mail, index=filepath,
                               name=set.name, file=[
                {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}
            ], background_img=set.background_img,
                               title=set.title, index_list=["Error"])
    except Exception:
        return render_template(set.template + '/preview.html', up_file="/", logo_url=set.logo_url,
                               e_mail=set.e_mail, index="/" + p,
                               name=set.name, file=[
                {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}
            ], background_img=set.background_img,
                               title=set.title, index_list=["Error"])


# 登出
@app.route('/logout')
def logout_():
    del session['user_info']
    return redirect('login')


# ======= 网页 ======= #

# ======= 运行 ======= #

if __name__ == '__main__':
    app.run(debug=True, port=4211, host="0.0.0.0")

# ======= 运行 ======= #
