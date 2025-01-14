from textnode import TextNode, TextType
import os
import shutil

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

def main():
	copy_static_to_public("./static", True)

if __name__ == "__main__":
	main()