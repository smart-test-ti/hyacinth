<p align="center">
  <a>English</a> | <a href="./README.md">中文</a> | <a href="./doc.md">使用文档</a>
</p>

<p align="center">
<a><img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1662542175003-cb28ac22-b457-4d23-bc1b-8920f88cf4f9.png" alt="Hyacinth" width="100"></a>
<br>
<br>

# Hyacinth
Hyacinth is a lightweight, free APP package internal testing platform, and supports virus scanning, security reinforcement and other functions. The open API can help you build into the CI/CD process, and the beautiful UI and convenient installation method can better distribute the internal testing package to the team.

<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1664101122085-064d6607-3a25-4097-9c63-71ddb62a643b.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0"  width="100%">

## Initialization
```bash
git clone git@github.com:smart-test-ti/hyacinth.git

sh initialize.sh
```
## Deploy
#### uWSGI
```bash
pip3 install uwsgi

uwsgi --ini uwsgi.ini
```
#### nohup
```bash
nohup python3 manage.py runserver 0.0.0.0:60006 >run.log 2>&1 &
```

## Run locally
```
sh startup.sh
```

## Supports
```
PC和H5
```