import os,shutil
from pathlib import Path
from converter import markdown_to_html_node,extract_title

def update_content(src: str = "static",dest: str = "public"):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    for p in os.listdir(src):
        p_src = os.path.join(src,p)
        target = os.path.join(dest,os.path.basename(os.path.normpath(p)))
        if os.path.isfile(p_src):
            shutil.copy(p_src,target)
            continue
        update_content(p_src,target)

def generate_page(from_path, template_path, dest_path, b_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    md_fd = open(from_path,"r")
    md = md_fd.read()

    tmplt_fd = open(template_path,"r")
    template = tmplt_fd.read()

    html = markdown_to_html_node(md)
    title = extract_title(md)

    template = template.replace("{{ Content }}",html.to_html())
    template = template.replace("{{ Title }}",title).replace("href=\"/",f"href=\"{b_path}").replace("src=\"/",f"src=\"{b_path}")

    target_path = os.path.dirname(dest_path)    
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    
    out = open(dest_path,"w")
    out.write(template)
    tmplt_fd.close()
    md_fd.close()
    out.close()

def generate_page_recursive(dir_path_content,template_path, dest_dir_path, b_path):
    for p in os.listdir(dir_path_content):
        if p[-3:] == ".md":
                generate_page(os.path.join(dir_path_content,p),template_path,os.path.join(dest_dir_path,p[:-3]+".html"),b_path)
                continue
        if os.path.isdir(os.path.join(dir_path_content,p)):
            generate_page_recursive(os.path.join(dir_path_content,p),template_path,os.path.join(dest_dir_path,p),b_path)