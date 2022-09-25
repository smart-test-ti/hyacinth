## 1. APP相关接口

#### 上传版本文件
- Curl
```
curl -X POST \
  http://{ip}:{port}/package/api/file/create \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'content-type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW' \
  -F file=@/Users/xx/xx/demo-release.apk \
  -F key=tpONqU3jnv \
  -F version=1.12.00 \
  -F build_num=1
```
- Python
```python
import requests
url = "http://{ip}:{port}/package/api/file/create"
files = {'file':open('{file_path}','rb')}
data = {
    "key": "dhT6Gji90ds", #app密钥，创建app会有
    "version": '1.0.0',   #版本
    "build_num": 1,       #构建号
}
response = requests.post(url=url, files=files, data=data)

```
- 返回结果
```
{
    "status": 1,
    "msg": "success",
    "download_path": "http://{ip}:{host}/static/apk/{app}/{version}/{filename}"
}
```