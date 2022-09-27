<p align="center">
  <a>中文</a> | <a href="./README.EN.md">English</a>
</p>

<p align="center">
<a><img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1662542175003-cb28ac22-b457-4d23-bc1b-8920f88cf4f9.png" alt="Hyacinth" width="100"></a>
<br>
<br>

## 风信子
风信子是一个轻量、免费的APP包内测平台，并且支持病毒扫描、安全加固等功能。开放式API可以有助你构建到CI/CD流程中，美观的UI、便捷的安装方式可以更好的给团队内部分发内测包。

<img src="https://cdn.nlark.com/yuque/0/2022/png/153412/1664101122085-064d6607-3a25-4097-9c63-71ddb62a643b.png?x-oss-process=image%2Fresize%2Cw_1500%2Climit_0"  width="100%">

<br>
<br>

<a href="./doc.md">使用文档</a>

## 初始化
```bash
git clone git@github.com:smart-test-ti/hyacinth.git

sh initialize.sh
```
## 部署
#### uWSGI
```bash
pip3 install uwsgi

uwsgi --ini uwsgi.ini
```
#### nohup
```bash
nohup python3 manage.py runserver 0.0.0.0:60006 >run.log 2>&1 &
```

## 本地运行
```bash-m '
sh startup.sh
```

## 支持平台
PC和H5
