import os
import shutil
import datetime


class FolderProcess:
    @classmethod
    def folder_move(cls, src_dir, dst_dir):
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir, exist_ok=True)

        if os.path.exists(src_dir) and os.path.basename(src_dir) not in os.listdir(dst_dir):
            shutil.move(src=str(src_dir), dst=os.path.join(str(dst_dir), os.path.basename(str(src_dir))))
            print(f'已将{src_dir}移动至{dst_dir}！')
        elif not os.path.exists(src_dir):
            print(f'未找到{src_dir}，请输入正确的文件路径!')
        elif os.path.basename(src_dir) in os.listdir(dst_dir):
            if os.path.isdir(src_dir):
                for file in os.listdir(src_dir):
                    src_path = os.path.join(src_dir, file)
                    FolderProcess.folder_move(src_path, os.path.join(dst_dir, os.path.basename(src_dir)))
                os.rmdir(src_dir)
                print(f'已删除空文件夹{src_dir}！')
            else:
                file = os.path.basename(src_dir)
                dst_name = f'{file.replace(f'.{file.split('.')[-1]}', '')}(1).{file.split('.')[-1]}'
                dst_path = os.path.join(dst_dir, dst_name)
                shutil.move(src=src_dir, dst=dst_path)
                print(f'已将{src_dir}移动至{dst_dir}！')

    @classmethod
    def folder_add_time(cls, src_dir):
        if os.path.exists(src_dir):
            now = datetime.datetime.now()
            now_str = now.strftime('%Y-%m-%d %H_%M')
            directory, filename = os.path.split(src_dir)
            if os.path.isdir(src_dir):
                new_name = filename + ' ' + now_str
                new_path = os.path.join(directory, new_name)
                for file in os.listdir(src_dir):
                    src_path = os.path.join(src_dir, file)
                    FolderProcess.folder_add_time(src_path)
                os.rename(src_dir, new_path)

            else:
                suffix = f'.{filename.split('.')[-1]}'
                new_name = filename.replace(suffix, '') + ' ' + now_str + suffix
                new_path = os.path.join(directory, new_name)
                os.rename(src_dir, new_path)
            print(f'已将{src_dir}修改为{new_path}')
        else:
            print(f'未找到{src_dir}，请输入正确的文件路径!')


if __name__ == '__main__':
    source_path = "D:\\Code\\src"
    target_dir = "D:\\Code\\dst"
    FolderProcess.folder_move(source_path, target_dir)
