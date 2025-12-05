import requests
import os
import json
from bs4 import BeautifulSoup
from datetime import datetime, UTC
from zoneinfo import ZoneInfo


# bilibili网址
URL = 'https://www.bilibili.com/'

# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
}

# 配置：链接记录最大数量，超过则只保留最新的N条
MAX_LINK_RECORDS = 100  # 可根据实际需求调整


def main():
    # 创建会话对象，复用TCP连接
    with requests.Session() as session:
        session.headers.update(headers)
        
        # 获取网页源码
        res = session.get(URL)
        res.encoding = 'utf-8'  # 确保编码正确
        
        # 解析网页获取图片URL
        soup = BeautifulSoup(res.text, 'html.parser')
        picture = soup.find("picture", class_="banner-img")
        if not picture:
            raise ValueError("未找到图片容器")
            
        img = picture.find("source", type="image/webp")
        if not img or 'srcset' not in img.attrs:
            raise ValueError("未找到图片源")
            
        # 处理图片URL
        img_url = img['srcset']
        full_url = "https:" + img_url.split('@', 1)[0]
        
        # 准备基础目录
        base_dir = os.path.join(os.path.abspath('.'), 'bili_web_header')
        os.makedirs(base_dir, exist_ok=True)
        
        # 图片链接记录文件路径
        links_file = os.path.join(base_dir, 'image_links.json')
        
        # 准备时间信息（用于执行时间记录和文件命名）
        utc_time = datetime.now(UTC)
        cst_time = utc_time.astimezone(ZoneInfo("Asia/Shanghai"))
        current_execution_time = cst_time.isoformat()  # ISO格式时间，包含时区
        
        # 读取已存在的链接记录和执行时间
        data = {
            "last_executed": "",  # 上一次执行时间
            "links": []           # 已下载的图片链接列表
        }
        
        if os.path.exists(links_file):
            with open(links_file, 'r', encoding='utf-8') as f:
                try:
                    loaded_data = json.load(f)
                    # 合并加载的数据，确保结构完整
                    data["last_executed"] = loaded_data.get("last_executed", "")
                    data["links"] = loaded_data.get("links", [])
                except json.JSONDecodeError:
                    # 解析错误时使用默认结构
                    data = {"last_executed": "", "links": []}
        
        # 检查链接是否已存在
        if full_url in data["links"]:
            print(f"图片链接已存在，不进行下载：{full_url}")
            # 更新执行时间（即使未下载，也要记录程序执行时间）
            data["last_executed"] = current_execution_time
            # 写入更新后的执行时间
            with open(links_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return None
        
        # 生成日期目录名（年-月-日）
        date_dir = cst_time.strftime("%Y-%m-%d")
        # 生成文件名（时-分-秒.png）
        file_name = cst_time.strftime("%H-%M-%S.png")
        # 生成链接文件名
        url_file_name = cst_time.strftime("%H-%M-%S.txt")
        
        # 准备保存路径
        save_dir = os.path.join(base_dir, date_dir)
        os.makedirs(save_dir, exist_ok=True)
        
        # 图片保存路径
        file_path = os.path.join(save_dir, file_name)
        # 链接保存路径
        url_file_path = os.path.join(save_dir, url_file_name)
        
        # 下载图片（使用流式读取减少内存占用）
        try:
            # 保存图片
            with session.get(full_url, stream=True) as img_res, \
                 open(file_path, 'wb') as f:
                for chunk in img_res.iter_content(chunk_size=1024):
                    if chunk:  # 过滤空块
                        f.write(chunk)
            
            # 保存图片链接到txt文件
            with open(url_file_path, 'w', encoding='utf-8') as f:
                f.write(full_url)
            
            # 更新记录：添加新链接（添加到列表开头，保持最新的在前面）
            data["links"].insert(0, full_url)
            
            # 限制链接数量，只保留最新的MAX_LINK_RECORDS条
            if len(data["links"]) > MAX_LINK_RECORDS:
                data["links"] = data["links"][:MAX_LINK_RECORDS]
            
            # 更新执行时间
            data["last_executed"] = current_execution_time
            
            # 写入更新后的记录到JSON文件
            with open(links_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"操作错误：{repr(e)}")
            return None
            
        return file_path


if __name__ == '__main__':
    file_path = main()
    if file_path:
        print(f"图片已保存至：{file_path}")
        print(f"图片链接已保存至同目录下的txt文件和image_links.json")
