# coding:utf-8
import onedrive
from flask import Flask, render_template, request

app = Flask(__name__)


# 设置
class Setthing():
    def __init__(self):
        # 带*表示必填
        # 端口 *
        self.port = 8080
        # IP *
        self.host = "0.0.0.0"
        # 网站标题
        self.title = "PyOneWeb"
        # 网站名
        self.name = "PyOneWeb"
        # 网页logo
        self.logo_url = "https://static-dbbdc8e5-5f50-4106-bc71-b5a5eedf6400.bspapp.com/grmine_logo.png"
        # 邮箱
        self.e_mail = "example@example.com"
        # 模板 *
        self.template = "neo"
        # 背景
        self.background_img = ""
        # OneDrive共享链接 *
        self.shared_url = "https://example.com/"
        # 路径 * (路径从你OneDrive账号主路径开始，而不是共享文件夹链接路径开始)
        self.shared_path = "/"


setthing = Setthing()
OneDriveSDK = onedrive.OneDriveSDK(setthing.shared_url, setthing.shared_path)


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
            file[path].append({"name": i["name"], "download_url": i["@content.downloadUrl"], "size": i["size"],
                               "date": i["fileSystemInfo"]["lastModifiedDateTime"], "url": path + i["name"],
                               "type": "file"})
    return file


# 判断是否为路径
def isDir(path):
    if path[-1] == "/":
        return True
    return False


# 主函数
@app.route('/', methods=['get'])
def main():
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
        print(index_list)
        try:
            file = get_file(index)
            return render_template(setthing.template + '/index.html', up_file=up_file, logo_url=setthing.logo_url,
                                   e_mail=setthing.e_mail, index=index,
                                   name=setthing.name, file=file[index], background_img=setthing.background_img,
                                   title=setthing.title, index_list=index_list)
        except:
            return render_template(setthing.template + '/index.html', up_file=up_file, logo_url=setthing.logo_url,
                                   e_mail=setthing.e_mail, index=index,
                                   name=setthing.name, file=[
                    {"name": "Error 404", "size": "", "date": "", "url": "", "type": "file"}
                ], background_img=setthing.background_img,
                                   title=setthing.title, index_list=index_list)
    else:
        # 下载
        fullfilename = index
        fullfilenamelist = fullfilename.split('/')
        filename = fullfilenamelist[-1]
        filepath = fullfilename.replace('/%s' % filename, '')
        for i in get_file(filepath)[filepath]:
            if i['type'] == 'file' and i['name'] == filename:
                download_url = i['download_url']
                return render_template(setthing.template + '/download.html', download_url=download_url,
                                       title=setthing.title)
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
        except:
            return "Error"
    else:
        fullfilename = index
        fullfilenamelist = fullfilename.split('/')
        filename = fullfilenamelist[-1]
        filepath = fullfilename.replace('/%s' % filename, '')
        for i in get_file(filepath)[filepath]:
            if i['type'] == 'file' and i['name'] == filename:
                download_url = i['download_url']
                return {"download_url": download_url}
        return "Error 404"


if __name__ == '__main__':
    app.run(debug=True, port=setthing.port, host=setthing.host)
