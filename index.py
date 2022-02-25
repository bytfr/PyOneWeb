# coding:utf-8
from flask import Flask, render_template, request, session, redirect

import json
import onedrive
import os
import requests
import time

app = Flask(__name__)


# 设置
class Setthing:
    def __init__(self):
        self.install = False
        self.title = "PyOneWeb"
        self.name = "PyOneWeb"
        self.logo_url = "https://static-dbbdc8e5-5f50-4106-bc71-b5a5eedf6400.bspapp.com/grmine_logo.png"
        self.e_mail = "example@example.com"
        self.template = "neo"
        self.background_img = ""
        self.shared_url = ""
        self.shared_path = ""
        self.password = "123456"
        self.time = None

    def get_config(self):
        global OneDriveSDK
        with open("./setthing.json", "r") as config:
            set = json.loads(config.read().replace("'", '"'))
            self.title = set['title']
            self.name = set['name']
            self.logo_url = set['logo_url']
            self.e_mail = set['e_mail']
            self.template = set['template']
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
            except:
                pass
            config.close()

    def write_config(self):
        config = {"title": self.title, "name": self.name, "logo_url": self.logo_url,
                  "e_mail": self.e_mail, "template": self.template, "background": self.background_img,
                  "shared_url": self.shared_url, "shared_path": self.shared_path, "password": self.password,
                  "install": str(self.install)}
        with open("./setthing.json", "w") as s:
            s.write(str(config).replace("'", '"'))
            s.close()


setthing = Setthing()

if not os.path.exists("./setthing.json"):
    setthing.write_config()

setthing.get_config()

if setthing.install:
    try:
        OneDriveSDK = onedrive.OneDriveSDK(setthing.shared_url, setthing.shared_path)
        setthing.time = time.time()
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
    if size >= gb:
        return "%.1f GB" % float(size / gb)
    if size >= mb:
        return "%.1f MB" % float(size / mb)
    if size >= kb:
        return "%.1f KB" % float(size / kb)


# 获取文件列表
def get_file(path):
    global setthing
    if path != "" and path[-1] == "/":
        path1 = path[:-1]
    else:
        path1 = path
    file = {}
    file1 = OneDriveSDK.get_folder_file(path1)
    file[path] = []
    file["download_url"]={}
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
    return file


# 404错误
@app.errorhandler(404)
def Error_notfound(e):
    return render_template(setthing.template + '/index.html', up_file="/", logo_url=setthing.logo_url,
                           e_mail=setthing.e_mail, index="Error",
                           name=setthing.name, file=[
            {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"},
            {"name": "NotFound 没有这个文件或路径", "size": "", "date": "", "url": "", "type": "file"}
        ], background_img=setthing.background_img,
                           title=setthing.title, index_list=["Error",""])


@app.errorhandler(500)
def Error_500(e):
    return render_template(setthing.template + '/index.html', up_file="/", logo_url=setthing.logo_url,
                           e_mail=setthing.e_mail, index="Error",
                           name=setthing.name, file=[
            {"name": "Error 500 服务器内部错误", "size": "", "date": "", "url": "", "type": "file"},
            {"name": "如果你是用户，请联系网页搭建者"+setthing.e_mail, "size": "", "date": "", "url": "mailto:"+setthing.e_mail, "type": "file"},
            {"name": "如果你是开发者，请联系邮箱2678509244@qq.com", "size": "", "date": "", "url": "mailto:"+setthing.e_mail, "type": "file"}
        ], background_img=setthing.background_img,
                           title=setthing.title, index_list=["Error",""])

# 判断是否为路径
def isDir(path):
    if path[-1] == "/":
        return True
    return False


@app.route('/install', methods=['get', 'post'])
def install():
    global setthing
    if setthing.install:
        return redirect("/")
    page = request.values.get("page")
    if page == "1":
        if request.method == 'POST':
            setthing.shared_url = request.form.get("shared_url")
            return redirect("/install?page=2")
        else:
            return render_template("install/1.html")
    if page == "2":
        setthing.install = True
        setthing.write_config()
        setthing.get_config()
        return render_template("install/2.html")
    else:
        return redirect("/install?page=1")


# 主函数
@app.route('/', methods=['get', 'post'])
def main():
    global OneDriveSDK
    if not setthing.install:
        return redirect("/install?page=1")
    try:
        if time.time() - setthing.time >= 1800:
            OneDriveSDK = onedrive.OneDriveSDK(setthing.shared_url, setthing.shared_path)
    except Exception:
        pass
    list = []
    for r in request.values:
        list.append(r)
    if not list:
        list.append("/")
    index = list[0]
    # 判断是否为路径
    if isDir(index):
        # 获取文件
        up_file = get_up_file(index)
        index_list = index.split("/")
        index_list.pop(0)
        try:
            file = get_file(index)
            return render_template(setthing.template + '/index.html', up_file=up_file, logo_url=setthing.logo_url,
                                   e_mail=setthing.e_mail, index=index,
                                   name=setthing.name, file=file[index], background_img=setthing.background_img,
                                   title=setthing.title, index_list=index_list)
        except Exception as Error_text:
            return render_template(setthing.template + '/index.html', up_file=up_file, logo_url=setthing.logo_url,
                                   e_mail=setthing.e_mail, index=index,
                                   name=setthing.name, file=[
                    {"name": Error_text, "size": "", "date": "", "url": "", "type": "file"}
                ], background_img=setthing.background_img,
                                   title=setthing.title, index_list=index_list)
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
            return render_template(setthing.template + '/index.html', up_file="/", logo_url=setthing.logo_url,
                                   e_mail=setthing.e_mail, index=index,
                                   name=setthing.name, file=[
                    {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}
                ], background_img=setthing.background_img,
                                   title=setthing.title, index_list=["Error"])
        except Exception:
            return render_template(setthing.template + '/index.html', up_file="/", logo_url=setthing.logo_url,
                                   e_mail=setthing.e_mail, index=index,
                                   name=setthing.name, file=[
                    {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}
                ], background_img=setthing.background_img,
                                   title=setthing.title, index_list=["Error"])


# api函数
@app.route('/api', methods=['get'])
def api():
    global file, yu_load_isok
    list = []
    for r in request.values:
        list.append(r)
    if not list:
        list.append("/")
    index = list[0]
    if isDir(index):
        try:
            file = get_file(index)
            return str(file[index])
        except Exception:
            return "Error"
    else:
        try:
            fullfilename = index
            fullfilenamelist = fullfilename.split('/')
            filename = fullfilenamelist[-1]
            filepath = fullfilename.replace('/%s' % filename, '')
            download_url = get_file(filepath)["download_url"]
            if filename in download_url:
                download_url = download_url[filename]
                return {"download_url": download_url}
            return "Error 404"
        except Exception:
            return "Error 404"


app.secret_key = 'QWERTYUIOP'


@app.route('/login', methods=['get', 'post'])
def login():
    if request.method == 'GET':
        return render_template('admin/index.html', title=setthing.title)
    user = request.form.get('user')
    pwd = request.form.get('pwd')
    if user == 'admin' and pwd == setthing.password:  # 这里可以根据数据库里的用户和密码来判断，因为是最简单的登录界面，数据库学的不是很好，所有没用。
        session['user_info'] = user
        return redirect('/admin')
    else:
        return render_template('admin/index.html', msg='用户名或密码输入错误', title=setthing.title)


@app.route('/admin', methods=['get', 'post'])
def admin():
    global setthing
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    if request.method == 'POST':
        setthing.title = request.form.get('title')
        setthing.name = request.form.get('name')
        setthing.logo_url = request.form.get('logo_url')
        setthing.e_mail = request.form.get('e_mail')
        setthing.template = request.form.get('template')
        setthing.background_img = request.form.get('background')
        setthing.shared_url = request.form.get('shared_url')
        setthing.shared_path = request.form.get('shared_path')
        setthing.password = request.form.get('password')
        setthing.write_config()
        setthing.get_config()
        return render_template('admin/admin.html', title=setthing.title,
                               name=setthing.name, logo_url=setthing.logo_url, e_mail=setthing.e_mail,
                               template=setthing.template, background=setthing.background_img,
                               shared_url=setthing.shared_url, shared_path=setthing.shared_path,
                               password=setthing.password, msg="修改成功")
    else:
        return render_template('admin/admin.html', title=setthing.title,
                               name=setthing.name, logo_url=setthing.logo_url, e_mail=setthing.e_mail,
                               template=setthing.template, background=setthing.background_img,
                               shared_url=setthing.shared_url, shared_path=setthing.shared_path,
                               password=setthing.password)


@app.route('/preview/<path:p>/<string:file>')
def preview(p, file):
    try:
        filename = file
        filepath = "/" + p
        index_list = (p + "/" + filename).split("/")
        index_list.append("")
        type = filename.split(".")[-1]
        url = "/?" + filepath + "/" + filename
        download_url = get_file(filepath)["download_url"]
        if filename in download_url:
            download_url = download_url[filename]
            text = ""
            if type in ["txt", "json", "html", "md"]:
                text = requests.get(download_url).text
            return render_template(setthing.template + '/preview.html', text=text, up_file=filepath,type=type,
                                   download_url=download_url, logo_url=setthing.logo_url,
                                   e_mail=setthing.e_mail, index=filepath,
                                   name=setthing.name, background_img=setthing.background_img,
                                   title=setthing.title, index_list=index_list, url=url)
        return render_template(setthing.template + '/preview.html', up_file="/", logo_url=setthing.logo_url,
                               e_mail=setthing.e_mail, index=filepath,
                               name=setthing.name, file=[
                {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}
            ], background_img=setthing.background_img,
                               title=setthing.title, index_list=["Error"])
    except Exception:
        return render_template(setthing.template + '/preview.html', up_file="/", logo_url=setthing.logo_url,
                               e_mail=setthing.e_mail, index="/" + p,
                               name=setthing.name, file=[
                {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}
            ], background_img=setthing.background_img,
                               title=setthing.title, index_list=["Error"])


@app.route('/logout')
def logout_():
    del session['user_info']
    return redirect('login')


if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")
