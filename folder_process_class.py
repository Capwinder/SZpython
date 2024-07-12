import os
import shutil


class FolderProcess:
    @classmethod
    def folder_move(cls, src_dir, dst_dir):
        if os.path.exists(src_dir) and os.path.basename(src_dir) not in os.listdir(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)
            shutil.move(src=str(src_dir), dst=os.path.join(str(dst_dir), os.path.basename(str(src_dir))))
            print(f'已将{os.path.basename(src_dir)}移动至{dst_dir}')
        elif not os.path.exists(src_dir):
            print(f'未找到{src_dir}，请输入正确的文件路径!')
        elif os.path.basename(src_dir) in os.listdir(dst_dir):
            print(f'{dst_dir}路径下已存在{os.path.basename(src_dir)}')

    @classmethod
    def folder_rename(cls, src_dir, dst_name):
        if os.path.exists(src_dir) and dst_name not in os.listdir(os.path.dirname(src_dir)):
            directory, filename = os.path.split(src_dir)
            dst_path = os.path.join(directory, dst_name)
            os.rename(src_dir, dst_path)
            print(f'已将{filename}修改为{dst_name}')
        elif not os.path.exists(src_dir):
            print(f'未找到{src_dir}，请输入正确的文件路径!')
        elif dst_name in os.listdir(os.path.dirname(src_dir)):
            print(f'{src_dir}路径下已存在{dst_name}')


if __name__ == '__main__':
    source_path = "D:\\Code\\src"
    target_name = "renamed_src"
    revised_path = os.path.join(os.path.dirname(source_path), target_name)
    target_dir = "D:\\Code\\dst"
    FolderProcess.folder_rename(source_path, target_name)
    FolderProcess.folder_move(revised_path, target_dir)
