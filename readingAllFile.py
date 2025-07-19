import os

def read_all_files(root_dir):
    """
    遍历 root_dir 目录下所有文件（含子目录），
    返回 (relative_path, content) 的生成器
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in filenames:
            full_path = os.path.join(dirpath, name)           # 绝对路径
            relative_path = os.path.relpath(full_path, root_dir)  # 相对路径
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                yield relative_path, content
            except (UnicodeDecodeError, OSError) as e:
                # 遇到二进制文件或权限问题，跳过或打印提示
                print(f"[WARN] 跳过文件：{relative_path}  ({e})")

if __name__ == "__main__":
    root_dir = r"app001\inputText"   # 改成自己的目录
    for file_name, file_text in read_all_files(root_dir):
        print("=" * 40)
        print("文件名:", file_name)
        print("内容:\n", file_text[:500])  # 只打印前 500 字符，防止刷屏