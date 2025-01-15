from textnode import TextNode, TextType
import os
import shutil
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

def copy_static_to_public(path, delete=False):
	if delete:
		delete_old_files("./public")
	files = os.scandir(path)
	for file in files:
		if file.is_dir():
			os.mkdir(path.replace("static","public")+"/"+file.name)
			copy_static_to_public(path+"/"+file.name)
		elif file.is_file():
			filepath = path+"/"+file.name
			newpath = path.replace("static", "public")+"/"+file.name
			print(f"copying file from {filepath} to {newpath}")
			shutil.copyfile(filepath, newpath)

def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")

	md_file = open(from_path, "r")
	template_file = open(template_path, "r")
	dest_file = open(dest_path, "w")

	markdown = md_file.read()
	template = template_file.read()

	html_str = md_to_html_node(markdown).to_html()
	title = extract_title(markdown)

	dest_file.write(template.replace("{{ Title }}", title).replace("{{ Content }}", html_str))

def main():
	copy_static_to_public("./static", True)
	generate_page("./content/index.md", "./template.html", "./public/index.html")

if __name__ == "__main__":
	main()