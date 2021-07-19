import sublime
import sublime_plugin
import os
import shutil


def plugin_loaded():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    packages_path = sublime.packages_path()

    # 翻译标记文件
    mark_file = os.path.join(packages_path, "Default", ".do")

    # 不存在翻译标记文件的情况 需要翻译
    if not os.path.isfile(mark_file):

        # 默认翻译插件清单
        default_trans_list = ["Default", "Diff", "ZZ-TopMenu"]
        # 获取已安装插件清单
        ins_pack_list = sublime.load_settings("Package Control.sublime-settings").get("installed_packages")
        # 合并插件清单
        trans_list = default_trans_list + ins_pack_list

        # 开始翻译
        for item in trans_list:
            if os.path.isdir(item):
                # original_dir = item
                # target_dir = "../"+ item
                original_dir = os.path.abspath(item)
                target_dir = os.path.join(packages_path, item)
                if not os.path.isdir(target_dir):
                    os.mkdir(target_dir)
                for file in os.listdir(item):
                    target_file = file.replace('.json', '')

                    # OSX 平台 使用无快捷键提示版本
                    if sublime.platform() == 'osx' and file == 'Main.sublime-menu.json':
                        continue
                    if sublime.platform() == 'osx' and file == 'Main (OSX).sublime-menu.json':
                        target_file = 'Main.sublime-menu'

                    shutil.copy(os.path.join(original_dir, file), os.path.join(target_dir, target_file))
        # 翻译结束 创建标记文件
        open(mark_file, "w")


# 删除翻译标记文件
class RemoveMarkFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        packages_path = sublime.packages_path()
        mark_file = os.path.join(packages_path, "Default", ".do")
        if os.path.isfile(mark_file):
            if sublime.ok_cancel_dialog("确定要删除\"翻译标记文件?\""):
                os.remove(mark_file)
                sublime.message_dialog("\"翻译标记文件\"已删除，请重新启动ST，更新翻译！")
        else:
            sublime.message_dialog("\"翻译标记文件\"已删除，请重新启动ST，更新翻译！")
