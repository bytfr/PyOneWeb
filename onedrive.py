# coding: utf-8
import json
import os
try:
    import requests
except Exception:
    pass


class OneDriveSDK():
    def __init__(self, url: str, shared_folder: str):
        """
        :param url:str OneDrive共享链接
        :param shared_folder:str 共享路径
        """

        self.url = url
        self.shared_folder = shared_folder
        tenant = self.url.split('/')[2]
        mail = self.url.split('/')[6]

        response = requests.get(self.url)
        self.cookies = response.cookies.get_dict()

        self.url = "https://" + tenant + "/personal/" + mail + "/_api/web/GetListUsingPath(DecodedUrl=@a1)/RenderListDataAsStream?@a1='/personal/" + mail + "/Documents'&RootFolder=/personal/" + mail + "/Documents/&TryNewExperienceSingle=TRUE"

        headers = {
            'Accept': 'application/json;odata=verbose',
            'Content-Type': 'application/json;odata=verbose'
        }

        payload = {
            "parameters": {
                "__metadata": {"type": "SP.RenderListDataParameters"},
                "RenderOptions": 136967,
                "AllowMultipleValueFilterForTaxonomyFields": True,
                "AddRequiredFields": True
            }
        }

        response = requests.post(self.url, cookies=self.cookies, headers=headers, data=json.dumps(payload))

        payload = json.loads(response.text)
        self.token = payload['ListSchema']['.driveAccessToken'][13:]
        self.api_url = payload['ListSchema']['.driveUrl'] + '/'

    # 获取文件夹下所有文件
    def get_folder_file(self, path: str) -> dict:
        """
        :param path:str 路径
        :return dict 返回路径下所有文件
        """

        headers = {
            'Authorization': 'Bearer ' + self.token
        }
        response = requests.get(self.api_url + 'root:/' + self.shared_folder + path + ":/children", headers=headers)
        files = json.loads(response.text)['value']
        return files

    # 获取文件下载链接
    def get_file_downloadurl(self, file_id: str) -> str:
        """
        :param file_id:str 文件ID
        :return str
        """

        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }
        response = requests.get(self.api_url + 'items/' + file_id + '/content', headers=headers, allow_redirects=False)
        download_link = response.headers['Location']
        return download_link

    # 上传文件 (大小最高15GB)
    def file_upload(self, onedrive_path: str, file_path: str):
        """
        :param onedrive_path:str OneDrive路径
        :param file_path:str 上传文件路径
        """

        headers = {
            'Authorization': 'Bearer ' + self.token,
            'Content-Type': 'application/json'
        }

        response = requests.post(
            self.api_url + 'items/root:/' + self.shared_folder + onedrive_path + ':/createUploadSession',
            headers=headers)
        uploadUrl = json.loads(response.text)['uploadUrl']

        file_size = os.path.getsize(file_path)
        with open(file_path, "rb") as file:
            while True:
                data = file.read(1024 * 1024)
                if not data:
                    file_id = json.loads(response.text)['id']
                    break

                headers = {
                    'Content-Length': str(len(data)),
                    'Content-Range': 'bytes ' + str(file.tell() - len(data)) + '-' + str(file.tell() - 1) + '/' + str(
                        file_size)
                }

                response = requests.put(uploadUrl, headers=headers, data=data)
