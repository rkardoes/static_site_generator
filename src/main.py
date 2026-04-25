import os
import shutil
import sys
from htmlnode import markdown_to_html_node
from markdownfuncs import extract_title

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

def regen_static(src, dest):
    src_path = os.path.abspath(src) 
    dest_path = os.path.abspath(dest)
    print(f"src = {src_path}")
    print(f"dest = {dest_path}")
    empty_directory(dest_path)
    copy_directory(src_path, dest_path)

def generate_page(src_path, template_path, dest_path, basepath):
    print(f"Generating page from {src_path} to {dest_path} using template at {template_path}")
    if not os.path.exists(src_path):
        raise Exception("src path does not exist")
    if not os.path.exists(template_path):
        raise Exception("template path does not exist")
    with open(src_path) as file:
        md = file.read()
    with open(template_path) as file:
        template = file.read()
    html = markdown_to_html_node(md).to_html()
    title = extract_title(md)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html).replace("href=\"/", f"href\"={basepath}").replace("src=\"/", f"src=\"{basepath}")
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    with open(dest_path, "w") as file:
        file.write(page)
    return

def generate_pages_recursive(src_dir, template_path, dest_dir, basepath):
    if not os.path.exists(src_dir):
        raise Exception("src directory does not exist")
    if not os.path.exists(template_path):
        raise Exception("template path does not exist")
    contents = os.listdir(src_dir)
    for content in contents:
        src_path = os.path.join(src_dir, content)
        dest_path = os.path.join(dest_dir, content)
        if os.path.isfile(src_path):
            dest_path = dest_path.rstrip(".md") + ".html"
            generate_page(src_path, template_path, dest_path, basepath)
        if os.path.isdir(src_path):
            os.mkdir(dest_path)
            print(f"made dir: {dest_path}")
            generate_pages_recursive(src_path, template_path, dest_path, basepath)

def main():
    basepath = sys.argv[1] if 1 < len(sys.argv) else "/" 
    regen_static("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()