from textnode import TextNode, TextType
import os
import shutil
import sys
from utils import *
from md_to_htmlnode import md_to_html_node

def delete_old_files(path):
	files = os.scandir(path)
	for file in files:
		if file.is_dir():
			delete_old_files(path+"/"+file.name)
			os.rmdir(path+"/"+file.name)
		elif file.is_file():
			os.remove(path+"/"+file.name)

def copy_static_to_docs(path, delete=False):
	if delete:
		delete_old_files("./docs")
	files = os.scandir(path)
	for file in files:
		if file.is_dir():
			os.mkdir(path.replace("static","docs")+"/"+file.name)
			copy_static_to_docs(path+"/"+file.name)
		elif file.is_file():
			filepath = path+"/"+file.name
			newpath = path.replace("static", "docs")+"/"+file.name
			print(f"copying file from {filepath} to {newpath}")
			shutil.copyfile(filepath, newpath)

def generate_page(basepath, from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")

	md_file = open(from_path, "r")
	template_file = open(template_path, "r")
	dest_file = open(dest_path, "w")

	markdown = md_file.read()
	template = template_file.read()

	html_str = md_to_html_node(markdown).to_html()
	title = extract_title(markdown)

	dest_file.write(template
				 .replace("{{ Title }}", title)
				 .replace("{{ Content }}", html_str)
				 .replace("href=\"/", f"href=\"{basepath}")
				 .replace("src=\"/", f"src=\"{basepath}")
			)

def generate_page_recursive(basepath, dir_path_content, template_path, dest_dir_path):
	files = os.scandir(dir_path_content)
	for file in files:
		if file.is_dir():
			os.mkdir(dest_dir_path+"/"+file.name)
			generate_page_recursive(basepath, dir_path_content+"/"+file.name, template_path, dest_dir_path+"/"+file.name)
		elif file.is_file() and file.name.endswith(".md"):
			generate_page(basepath, dir_path_content+"/"+file.name, template_path, dest_dir_path+"/"+file.name.replace(".md", ".html"))

def main():
	basepath = sys.argv[1] if sys.argv[1] else '/'
	copy_static_to_docs("./static", True)
	generate_page_recursive(basepath, "./content", "./template.html", "./docs")

if __name__ == "__main__":
	main()