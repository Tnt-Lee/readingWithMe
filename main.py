
import readingAllFile 
import readingbook
import os
from concurrent.futures import ProcessPoolExecutor
import readingAllFile
import readingbook

def process_one_file(file_name, file_text):
    """
    包装成独立函数，供子进程调用
    """
    try:
        readingbook.convert_text_to_audio(file_name, file_text)
    except Exception as e:
        # 子进程异常捕获打印，避免静默失败
        print(f"[ERROR] {file_name} -> {e}")

if __name__ == '__main__':
    # 读取文件
    root_dir = r"app001\inputText"   # 改成自己的目录
    max_workers = os.cpu_count() or 4          # 按 CPU 核数并行
    with ProcessPoolExecutor(max_workers=max_workers) as pool:
        for file_name, file_text in readingAllFile.read_all_files(root_dir):
            print("=" * 40)
            print("文件名:", file_name.rsplit('.', 1)[0])
            print("内容:\n", file_text[:500])  # 只打印前 500 字符，防止刷屏
            pool.submit(process_one_file, file_name.rsplit('.', 1)[0], file_text)
    # 把生成