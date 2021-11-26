import sublime
import sublime_plugin
import os
import re


def plugin_loaded():
    # 翻译标记文件
    packages_path = sublime.packages_path()
    mark_file = os.path.join(packages_path, "Default", ".do")

    # 仅当, 不存在"翻译标记文件"时, 进行翻译
    if not os.path.isfile(mark_file):
        # 当前系统平台
        platform = sublime.platform()

        # 默认翻译插件清单
        default_trans_list = ["Default", "Diff", "ZZ-TopMenu"]
        # 获取已安装插件清单
        ins_pack_list = sublime.load_settings("Package Control.sublime-settings").get("installed_packages")
        # 合并之后的插件清单
        trans_list = default_trans_list + ins_pack_list

        # *.sublime-menu.json
        sublime_menu_json_list = sublime.find_resources("*.sublime-menu.json")

        # 开始翻译
        for item in trans_list:
            for f in sublime_menu_json_list:
                if f.startswith("Packages/sublime-text-chinese/" + item):
                    target_file = packages_path + f.replace("Packages/sublime-text-chinese/", "/").replace('.json', '')
                    original_file_res = sublime.load_resource(f)
                    target_dir = os.path.dirname(target_file)
                    if not os.path.exists(target_dir):
                        os.makedirs(target_dir)

                    # OSX 平台 删除快捷键提示
                    if platform == "osx":
                        pattern = re.compile(r"(?<=[\u3000-\u9FFFa-zA-Z])\([A-Za-z]\)", re.M)
                        original_file_res = re.sub(pattern, "", original_file_res)

                    # 写入目标"翻译后菜单文件"
                    open(target_file, "w", encoding='utf8', newline='').write(original_file_res)

        # 翻译结束, 创建"翻译标记文件"
        open(mark_file, "w")


# 重置翻译
class ResetTranslationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if sublime.ok_cancel_dialog("确定更新或重置翻译？现有翻译将被覆盖..."):
            mark_file = os.path.join(sublime.packages_path(), "Default", ".do")
            if os.path.isfile(mark_file):
                os.remove(mark_file)
            plugin_loaded()
            sublime.message_dialog("翻译已更新！")


# 移除中文翻译
class RemoveTranslationCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if sublime.ok_cancel_dialog("确定移除中文翻译？现有翻译将被丢失..."):
            remove_translation()
            sublime.message_dialog("中文翻译已移除！")


def remove_translation():
    packages_path = sublime.packages_path()

    # 默认翻译插件清单
    default_trans_list = ["Default", "Diff", "ZZ-TopMenu"]
    # 获取已安装插件清单
    ins_pack_list = sublime.load_settings("Package Control.sublime-settings").get("installed_packages")
    # 合并之后的插件清单
    trans_list = default_trans_list + ins_pack_list

    # *.sublime-menu.json 资源清单
    sublime_menu_json_list = sublime.find_resources("*.sublime-menu.json")

    # 开始移除中文翻译
    for item in trans_list:
        for f in sublime_menu_json_list:
            if f.startswith("Packages/sublime-text-chinese/" + item):
                target_file = packages_path + f.replace("Packages/sublime-text-chinese/", "/").replace('.json', '')
                if os.path.exists(target_file):
                    os.remove(target_file)
