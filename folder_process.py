import os
import shutil
import datetime


class FolderProcess:
    @classmethod
    def folder_move(cls, src_dir, dst_dir):
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
            print(f'未找到目录{dst_dir},已自动创建')

        if os.path.exists(src_dir) and os.path.basename(src_dir) not in os.listdir(dst_dir):
            shutil.move(src=str(src_dir), dst=os.path.join(str(dst_dir), os.path.basename(str(src_dir))))
            print(f'已将{os.path.basename(src_dir)}移动至{dst_dir}')
        elif not os.path.exists(src_dir):
            print(f'未找到{src_dir}，请输入正确的文件路径!')
        elif os.path.basename(src_dir) in os.listdir(dst_dir):
            print(f'{dst_dir}路径下已存在{os.path.basename(src_dir)}')

    @classmethod
    def folder_add_time(cls, src_dir):
        if os.path.exists(src_dir):
            now = datetime.datetime.now()
            now_str = now.strftime('%Y-%m-%d %H_%M_%S')
            dst_name = os.path.basename(src_dir) + ' ' + now_str
            print(dst_name)
            directory, filename = os.path.split(src_dir)
            dst_path = os.path.join(directory, dst_name)
            os.rename(src_dir, dst_path)
            print(f'已将{filename}修改为{dst_name}')
        elif not os.path.exists(src_dir):
            print(f'未找到{src_dir}，请输入正确的文件路径!')


if __name__ == '__main__':
    source_path = "D:\\Code\\src"
    target_dir = "D:\\Code\\dst1"
    FolderProcess.folder_move(source_path, target_dir)
