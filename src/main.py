import os
import shutil

def empty_directory(dir):
    if not os.path.exists(dir):
        raise Exception("path doesn't exist")
    contents = os.listdir(dir)
    dirs = []
    for content in contents:
        path = os.path.join(dir, content)
        if os.path.isfile(path):
            print(f"rm {path}")
            os.remove(path)
        if os.path.isdir(path):
            empty_directory(path)
            dirs.append(path)
    for d in dirs:
        print(f"rm {d}")
        os.rmdir(d)
    return 

def copy_directory(src_dir, dest_dir):
    if not os.path.exists(src_dir):
        raise Exception("src dir does not exist")
    if not os.path.exists(dest_dir):
        raise Exception("dest dir does not exist")
    contents = os.listdir(src_dir)
    for content in contents:
        src_path = os.path.join(src_dir, content)
        dest_path = os.path.join(dest_dir, content)
        if os.path.isfile(src_path):
            print(f"copy {src_path}\nto\n{dest_path}")
            shutil.copy(src_path, dest_path)
        if os.path.isdir(src_path):
            os.mkdir(dest_path)
            copy_directory(src_path, dest_path)

def regen_site():
    src_path = os.path.abspath("static") 
    dest_path = os.path.abspath("public")
    print(f"src = {src_path}")
    print(f"dest = {dest_path}")
    empty_directory(dest_path)
    copy_directory(src_path, dest_path)


def main():
    regen_site()

main()