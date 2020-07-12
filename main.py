import sublime
import sublime_plugin
import os
import shutil

def plugin_loaded():
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
	packages_path=sublime.packages_path()
	for item in os.listdir():
		if os.path.isdir(item):
			#original_dir=item
			#target_dir="../"+ item
			original_dir=os.path.abspath(item)
			target_dir=os.path.join(packages_path, item)
			if not os.path.isdir(target_dir): os.mkdir(target_dir)
			for file in os.listdir(item):
				#if file.endswith('.json'):
				target_file=file.replace('.json','')
				shutil.copy(os.path.join(original_dir, file),os.path.join(target_dir, target_file))
			# OSX 平台 使用无快捷键提示版本
			osx_menu_file="Main (OSX).sublime-menu"
			target_file="Main.sublime-menu"
			if (sublime.platform() == 'osx' and
				os.path.isfile(os.path.join(target_dir, osx_menu_file))):
				shutil.move(os.path.join(target_dir, osx_menu_file), os.path.join(target_dir, target_file))
