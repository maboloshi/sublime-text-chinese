import sublime
import sublime_plugin
import os
import shutil


def plugin_loaded():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    packages_path = sublime.packages_path()
    default_trans_list = ["Default", "Diff", "ZZ-TopMenu"]
    ins_pack_list = sublime.load_settings("Package Control.sublime-settings").get("installed_packages")
    trans_list = default_trans_list + ins_pack_list
    for item in trans_list:
        if os.path.isdir(item):
            # original_dir = item
            # target_dir = "../"+ item
            original_dir = os.path.abspath(item)
            target_dir = os.path.join(packages_path, item)
            if not os.path.isdir(target_dir):
                os.mkdir(target_dir)
            for file in sorted(os.listdir(item), reverse=True):
                target_file = file.replace('.json', '')

                # OSX 平台 使用无快捷键提示版本
                # 之前使用sorted降序处理, 规避了Main (OSX).sublime-menu被
                # Main.sublime-menu复写的问题
                if file == 'Main (OSX).sublime-menu.json':
                    if sublime.platform() == 'osx':
                        target_file = 'Main.sublime-menu'
                    else:
                        continue

                shutil.copy(os.path.join(original_dir, file), os.path.join(target_dir, target_file))