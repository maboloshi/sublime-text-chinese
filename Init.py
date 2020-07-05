import sublime
import sublime_plugin
import os
import shutil

def plugin_loaded():
	os.chdir(os.path.abspath(os.path.dirname(__file__)))
	if (sublime.platform() == 'osx' and
	not os.path.isfile("Main.sublime-menu")):
		shutil.copy("Main (OSX).sublime-menu.json","Main.sublime-menu")
		if not os.path.isdir("../ZZ-TopMenu/"): os.mkdir("../ZZ-TopMenu/")
		shutil.copy("TopMenu (OSX).sublime-menu.json","../ZZ-TopMenu/Main.sublime-menu")

	if (sublime.platform() != 'osx' and
	not os.path.isfile("Main.sublime-menu")):
		shutil.copy("Main.sublime-menu.json","Main.sublime-menu")
		if not os.path.isdir("../ZZ-TopMenu/"): os.mkdir("../ZZ-TopMenu/")
		shutil.copy("TopMenu.sublime-menu.json","../ZZ-TopMenu/Main.sublime-menu")

	if not os.path.isdir("../Diff/"): os.mkdir("../Diff/")
	shutil.copy("Diff-Context.sublime-menu.json","../Diff/Context.sublime-menu")