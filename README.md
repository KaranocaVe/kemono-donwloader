# kemono-donwloader

Use this handy script to download images from [kemono.su](https://kemono.su/)~

## How to use  使用说明

1. Download Edge webdriver from [here](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)

从[此处](https://developer.microsoft.com/zh-cn/microsoft-edge/tools/webdriver/)下载Edge浏览器的webdriver

```shell
wget https://msedgedriver.azureedge.net/126.0.2592.87/edgedriver_win32.zip
```
2.  Install the required packages 安装所需的包
```shell
pip install -r requirements.txt
```
3. Run the script 运行脚本
```shell
python run.py
```

## Function 功能

- [x] download static images 下载静态图片
- [x] multi-threading 多线程下载
- [ ] break-point resume 断点续传