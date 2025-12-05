# bili_splash_images

![](/today/today_web_header.png)

B站WEB头图和APP开屏图自动下载，使用Actions

[![App 启动图](https://github.com/Little-Data/bili_splash_images/actions/workflows/app_splash.yml/badge.svg)](https://github.com/Little-Data/bili_splash_images/actions/workflows/app_splash.yml) [![Web 首页头图](https://github.com/Little-Data/bili_splash_images/actions/workflows/bili_web_header.yml/badge.svg)](https://github.com/Little-Data/bili_splash_images/actions/workflows/bili_web_header.yml)

<div align="center">
<h1>随机APP启动图</h1>
</div>

<div align="center">
<img height="550px" src="/today/today_app_splash.png" />
</div>

<div align="center">
每日更换一次，有可能重复，有可能是旧图。
</div>

# 一些碎语

随着b站对api的使用越发严格，我不知道能使用多久。

原本想实现壁纸喵更新的，但过于复杂，不如人工更新。

因为api接口数据官方随时会改变，有可能获取不到图片或者图片有误。

# 文件说明

`today文件夹`用来更新该页面的图片。

`bili_web_headerw文件夹`Web 首页头图。
  - `{日期命名的文件夹}`存放程序当天执行成功时获取到的文件。
  - `image_links.json`记录上一次执行的时间，图片链接。后续执行时先检查是否重复下载。

`app_splash文件夹`App 启动图。
  - `{日期时间命名的文件夹}`存放程序当天执行成功时获取到的文件。
  - `hash.json`记录上一次执行的时间，图片名称，图片hash。后续执行时先检查是否重复下载。

`get_app_splash.py`App 启动图获取程序。

`getimg.py`Web 首页头图获取程序。

# 灵感

[bilibili-API-collect](https://github.com/SocialSisterYi/bilibili-API-collect)api接口文档，一切的基础。

[bili_app_splash](https://github.com/zjkwdy/bili_app_splash)代码参考，历史图片提供。

[pyhton 爬虫爬取B站首页头图](https://www.bilibili.com/opus/739912377260048432)Web头图代码参考。

[BiliResourceDownloader](https://github.com/LightQuanta/BiliResourceDownloader)在初期手工收集壁纸喵图片时大大减轻了工作量，感谢。

# license

CC BY-NC-SA 4.0

[署名—非商业性使用—相同方式共享 4.0 协议国际版](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode.zh-hans)


![Star History Chart](https://api.star-history.com/svg?repos=Little-Data/bili_splash_images&type=date&legend=top-left)
