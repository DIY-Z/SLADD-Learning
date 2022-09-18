#删除空目录
import os

def del_empty_folder(path_data):
    for root, dirs, files in os.walk(path_data, topdown=False):
        if not files and not dirs:  #如果该目录下既没有文件也没有子目录,则删掉
            os.rmdir(root)

del_empty_folder('D:\\ProjectDevelop\\SLADD-Learning\\data\\FF')
