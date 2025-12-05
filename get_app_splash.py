import aiohttp
import asyncio
import orjson
import os
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

async def fetch_data(session):
    """获取API数据"""
    url = "http://app.bilibili.com/x/v2/splash/brand/list"
    params = {
        "appkey": "1d8b6e7d45233436",
        "ts": "0",
        "sign": "78a89e153cd6231a4a4d55013aa063ce"
    }
    
    async with session.get(url, params=params) as response:
        if response.status == 200:
            return orjson.loads(await response.read())
        else:
            print(f"请求失败，状态码: {response.status}")
            return None

async def download_image(session, url, save_path):
    """下载单张图片"""
    try:
        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await response.read())
                return True
            else:
                print(f"下载图片失败: {url}, 状态码: {response.status}")
                return False
    except Exception as e:
        print(f"下载图片出错: {url}, 错误: {e}")
        return False

def load_hash_data(hash_file):
    """加载现有的hash数据"""
    if hash_file.exists():
        try:
            with open(hash_file, 'rb') as f:
                return orjson.loads(f.read())
        except Exception as e:
            print(f"读取hash.json文件出错: {e}")
            return {"last_execution_time": "", "images": []}
    else:
        return {"last_execution_time": "", "images": []}

def save_hash_data(hash_file, hash_data):
    """保存hash数据到文件"""
    try:
        with open(hash_file, 'wb') as f:
            f.write(orjson.dumps(hash_data, option=orjson.OPT_INDENT_2))
        return True
    except Exception as e:
        print(f"保存hash.json文件出错: {e}")
        return False

async def main():
    """主函数"""
    # 获取中国标准时间（CST，UTC+8）
    cst_tz = ZoneInfo('Asia/Shanghai')
    now = datetime.now(cst_tz)
    
    # 创建主保存目录
    app_splash_dir = Path("app_splash")
    app_splash_dir.mkdir(exist_ok=True)
    
    # hash文件路径
    hash_file = app_splash_dir / "hash.json"
    
    # 加载现有hash数据
    hash_data = load_hash_data(hash_file)
    existing_hashes = {img["thumb_hash"]: img["thumb_name"] for img in hash_data.get("images", [])}
    
    # 模拟浏览器的请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Cache-Control": "max-age=0"
    }
    
    # 创建aiohttp会话，添加浏览器请求头
    async with aiohttp.ClientSession(headers=headers) as session:
        # 获取数据
        data = await fetch_data(session)
        if not data or data.get("code") != 0:
            print("获取数据失败")
            return
        
        # 提取图片列表
        image_list = data.get("data", {}).get("list", [])
        if not image_list:
            print("没有找到图片数据")
            # 更新执行时间，即使没有图片数据
            hash_data["last_execution_time"] = now.strftime("%Y-%m-%d %H:%M:%S %Z")
            save_hash_data(hash_file, hash_data)
            return
        
        # 收集当前API返回的所有图片信息（用于更新hash.json）
        current_images = []
        for item in image_list:
            thumb_name = item.get("thumb_name", "unknown")
            thumb_hash = item.get("thumb_hash")
            if thumb_hash:
                current_images.append({
                    "thumb_name": thumb_name,
                    "thumb_hash": thumb_hash
                })
        
        # 收集需要下载的图片任务
        download_tasks = []
        for item in image_list:
            thumb_url = item.get("thumb")
            thumb_name = item.get("thumb_name", "unknown")
            thumb_hash = item.get("thumb_hash")
            
            if not thumb_url or not thumb_hash:
                continue
            
            # 检查hash是否已存在
            if thumb_hash in existing_hashes:
                print(f"图片已存在，跳过下载: {thumb_name}")
                continue
            
            # 添加到下载任务列表
            download_tasks.append({
                "thumb_url": thumb_url,
                "thumb_name": thumb_name,
                "thumb_hash": thumb_hash
            })
        
        # 如果没有需要下载的图片，直接更新hash.json并结束
        if not download_tasks:
            print("所有图片都已存在，无需下载")
            # 更新hash.json：只保留当前API返回的图片信息，更新执行时间
            new_hash_data = {
                "last_execution_time": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
                "images": current_images
            }
            save_hash_data(hash_file, new_hash_data)
            return
        
        # 创建子目录，使用中国标准时间命名（只有需要下载时才创建）
        save_dir = app_splash_dir / now.strftime("%Y%m%d_%H%M%S")
        save_dir.mkdir(exist_ok=True)
        
        # 创建链接保存文件
        links_file = save_dir / "image_links.txt"
        
        # 执行下载任务
        tasks = []
        task_info = []
        
        for task_data in download_tasks:
            thumb_url = task_data["thumb_url"]
            thumb_name = task_data["thumb_name"]
            thumb_hash = task_data["thumb_hash"]
            
            # 生成文件名，处理可能的特殊字符
            safe_thumb_name = "".join(c for c in thumb_name if c.isalnum() or c in (' ', '_', '-', '.'))
            file_ext = Path(thumb_url).suffix or ".png"
            file_name = f"{safe_thumb_name}_{now.strftime('%Y%m%d_%H%M%S')}{file_ext}"
            save_path = save_dir / file_name
            
            # 添加到异步任务列表
            tasks.append(download_image(session, thumb_url, save_path))
            task_info.append({
                "thumb_name": thumb_name,
                "thumb_hash": thumb_hash,
                "file_name": file_name,
                "thumb_url": thumb_url
            })
        
        # 等待所有下载完成
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 处理下载结果
        success_count = 0
        
        for i, result in enumerate(results):
            info = task_info[i]
            
            if result is True:
                success_count += 1
                # 保存文件名和链接到文件
                with open(links_file, 'a', encoding='utf-8') as f:
                    f.write(f"{info['file_name']}\t{info['thumb_url']}\n")
            elif isinstance(result, Exception):
                print(f"下载图片出错: {info['thumb_url']}, 错误: {result}")
        
        print(f"下载完成！成功: {success_count}, 总数: {len(tasks)}")
        print(f"保存目录: {save_dir}")
        
        # 只保留当前API返回的图片信息，更新执行时间
        # 这样可以避免hash.json无限增长，只保留当前有效的图片hash
        new_hash_data = {
            "last_execution_time": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "images": current_images
        }
        
        # 保存hash数据
        if save_hash_data(hash_file, new_hash_data):
            print(f"hash数据已更新到: {hash_file}")

if __name__ == "__main__":
    asyncio.run(main())
