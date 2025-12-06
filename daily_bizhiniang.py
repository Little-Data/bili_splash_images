import os
import random
import shutil

def main():
    # 源目录和目标目录（相对于仓库根目录）
    source_dir = "bizhiniang"
    target_dir = "today"

    # 确保目标目录存在（若不存在则自动创建）
    os.makedirs(target_dir, exist_ok=True)

    # 遍历源目录，收集所有非 txt 文件
    all_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if not file.endswith(".txt"):
                # 构建完整路径（自动处理含空格的文件名/目录名）
                full_path = os.path.join(root, file)
                all_files.append(full_path)

    # 随机选择 3 个文件（若不足 3 个则全部选择）
    if len(all_files) >= 3:
        selected_files = random.sample(all_files, 3)
    else:
        selected_files = all_files

    # 复制并按规则重命名文件
    for idx, src_path in enumerate(selected_files, 1):
        # 目标文件名：bizhiniang_1.png, bizhiniang_2.png, ...
        dst_name = f"bizhiniang_{idx}.png"
        dst_path = os.path.join(target_dir, dst_name)
        
        # 复制文件（保留元数据，自动处理含空格的路径）
        shutil.copy2(src_path, dst_path)
        print(f"已复制：{src_path} → {dst_path}")

    # 提示信息（若文件不足 3 个）
    if len(selected_files) < 3:
        print(f"仅找到 {len(all_files)} 个文件，已全部复制")

if __name__ == "__main__":
    main()
