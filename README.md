# bili_splash_images

![](/today/today_web_header.png)

B站web头图和app开屏图自动下载，使用Actions

[![App 启动图](https://github.com/Little-Data/bili_splash_images/actions/workflows/app_splash.yml/badge.svg)](https://github.com/Little-Data/bili_splash_images/actions/workflows/app_splash.yml) [![Web 首页头图](https://github.com/Little-Data/bili_splash_images/actions/workflows/bili_web_header.yml/badge.svg)](https://github.com/Little-Data/bili_splash_images/actions/workflows/bili_web_header.yml)

<div align="center">
<h1>随机APP 启动图</h1>
</div>

<div align="center">
<img height="550px" src="/today/today_app_splash.png" />
</div>

# 文件说明

`today文件夹`用来更新该页面的图片。

`bili_web_headerw文件夹`Web 首页头图。
  - `{日期命名的文件夹}`存放程序当天执行成功时获取到的文件。
  - `image_links.json`记录上一次执行的时间，图片链接。后续执行时先检查是否重复下载。

`app_splash文件夹`App 启动图
  - `{日期时间命名的文件夹}`存放程序当天执行成功时获取到的文件。
  - `hash.json`记录上一次执行的时间，图片名称，图片hash。后续执行时先检查是否重复下载。

`get_app_splash.py`App 启动图获取程序。

`getimg.py`Web 首页头图获取程序。

# 灵感

[bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)api接口文档

[bili_app_splash](https://github.com/zjkwdy/bili_app_splash)代码参考，历史图片提供

[pyhton 爬虫爬取B站首页头图](https://www.bilibili.com/opus/739912377260048432)Web头图代码参考

# license

CC BY-NC-SA 4.0

[署名—非商业性使用—相同方式共享 4.0 协议国际版](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.zh-hans)


![Star History Chart](https://api.star-history.com/svg?repos=Little-Data/bili_splash_images&type=date&legend=top-left)
