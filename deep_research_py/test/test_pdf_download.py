import requests
import os
from urllib.parse import urlparse

def download_pdf(url, parent_dir):
    """
    检查 URL 是否为 PDF 文件，如果是，则下载到指定父目录。
    
    参数:
    - url: 要检查和下载的 URL 字符串
    - parent_dir: 保存 PDF 文件的父目录路径
    """
    try:
        # 确保父目录存在，如果不存在则创建
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

        # 发送 HEAD 请求检查文件类型（避免直接下载整个文件）
        response = requests.head(url, allow_redirects=True)
        content_type = response.headers.get('Content-Type', '').lower()

        # 检查是否为 PDF 类型
        if 'application/pdf' in content_type or url.lower().endswith('.pdf'):
            print(f"检测到 PDF 文件: {url}")
            
            # 获取文件名（从 URL 中提取，或使用默认名）
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename:
                filename = 'downloaded_file.pdf'  # 默认文件名
            elif not filename.lower().endswith('.pdf'):
                filename += '.pdf'

            # 构建保存路径
            save_path = os.path.join(parent_dir, filename)

            # 下载文件
            print(f"正在下载到: {save_path}")
            response = requests.get(url, stream=True)  # 使用流模式下载大文件
            response.raise_for_status()  # 检查请求是否成功

            # 以二进制写入文件
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):  # 分块写入
                    if chunk:
                        f.write(chunk)
            print(f"下载完成: {save_path}")
        else:
            print(f"URL 不是 PDF 文件: {url} (Content-Type: {content_type})")

    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

# 示例用法
if __name__ == "__main__":
    # 示例 URL 和保存路径
    url = "https://pic.bankofchina.com/bocappd/rareport/202501/P020250108516286149745.pdf"  # 替换为实际 URL
    parent_dir = "PDFs"  # 替换为你的保存路径

    download_pdf(url, parent_dir)