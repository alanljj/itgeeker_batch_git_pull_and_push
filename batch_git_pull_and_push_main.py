# -*- coding: utf-8 -*-
###########################################################################
#    Copyright 2023 奇客罗方智能科技 https://www.geekercloud.com
#    ITGeeker.net <alanljj@gmail.com>
############################################################################
import base64
import json
import os
import subprocess
import tempfile
import tkinter as tk
from tkinter import ttk
# import ttkbootstrap as ttk
from tkinter import messagebox
import tkinter.filedialog
from webbrowser import open_new_tab
# from pathlib import Path
# from git import Repo


class GitListFolder(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        # self.label1 = tk.Label(self, text='文件夹列表')
        # self.label1.config(font=('Microsoft YaHei UI', 14))
        # self.label1.grid(row=0, column=0, columnspan=2, ipadx=10, ipady=10)

        self.menu_option = None
        self.label_folder_size = None
        self.label_file_nmb = None
        self.folder_frame = None
        self.start_git_pull = None
        self.browse_button = None
        self.edit_button = None
        self.listbox = None
        self.entry_path = None
        self.add_button = None

        self.list_frame()
        self.select_path_frame()
        self.author_frame()
        # self.menu_frame()

    def on_dropdown_menu_click(self, selected_menu):
        # print('on_dropdown_menu_click: %s' % self.menu_option)
        print('on_dropdown_menu_click selected_menu: %s' % selected_menu)
        if selected_menu == '保存列表':
            print('save folder list')
            val_list = self.get_all_item_list()
            if val_list:
                # right_dir = val_list[0].split(os.sep)[-1]
                dir_l = []
                for index, val in enumerate(val_list):
                    if index < 4 and val.strip():
                        right_dir = val.split('/')[-1]
                        dir_l.append(right_dir)
                dir_three_ma = ' - '.join(x for x in dir_l)
                ffp_save = tk.filedialog.asksaveasfilename(
                    initialdir=".",
                    title="保存当前目录列表",
                    initialfile='Git_Folder_List-' + dir_three_ma + '.json',
                    filetypes=[("json files", "*.json"), ("All files", "*.*")])
                if ffp_save:
                    print('ffp_save: %s' % ffp_save)
                    con_dict = {'folder_list': val_list}
                    try:
                        with open(ffp_save, 'w', encoding='utf-8') as ffp:
                            ffp.write(json.dumps(con_dict, indent=4, ensure_ascii=False))
                    except Exception as err:
                        print('save folder list at menu save config failed: %s' % err)
            else:
                messagebox.showwarning(title="Error Reminder", message="当前没有添加任何目录！")
        else:
            print('load folder list')
            ffp_open = tk.filedialog.askopenfilename(
                initialdir=".",
                title="打开保存的文件列表文件",
                initialfile='',
                filetypes=[("json files", "*.json"), ("All files", "*.*")])
            if ffp_open:
                print('ffp_open: %s' % ffp_open)
                try:
                    with open(ffp_open, 'r', encoding='utf-8') as ffp:
                        dt_dict = json.load(ffp)
                        if 'folder_list' in dt_dict:
                            lines = dt_dict['folder_list']
                            print('folder list to load: %s' % lines)
                            if lines:
                                self.listbox.delete(0, tk.END)
                                for i in range(len(lines)):
                                    lines[i] = lines[i].rstrip("\n")
                                for line in lines:
                                    if line:
                                        self.listbox.insert(tk.END, line)
                except Exception as err:
                    print('open folder list at menu open config failed: %s' % err)
        self.menu_option.set("保存或读取")

    def check_dup_folder(self, fp):
        val_list = self.get_all_item_list()
        if fp in val_list:
            messagebox.showwarning(title="Error Reminder", message="您选择的目录已存在！")
            return True
        else:
            return False

    def add_path(self):
        # item = input("Enter item: ")
        fp = self.entry_path.get()
        if fp == '浏览并选择目录':
            messagebox.showwarning(title="Error Reminder", message="请先选择文件的目录！")
        else:
            dup_f = self.check_dup_folder(fp)
            if not dup_f:
                self.listbox.insert(tk.END, fp.strip())
                self.entry_path.delete(0, tk.END)

    def edit_item(self):
        if self.listbox.curselection():
            for item in self.listbox.curselection():
                print('self.listbox.get(item): ', self.listbox.get(item))
                self.entry_path.delete(0, tk.END)
                self.entry_path.insert(tk.END, self.listbox.get(item))
                self.listbox.delete(item)
                # self.listbox.insert("end", "foo")
        else:
            messagebox.showwarning(title="Error Reminder", message="请先选择想要修改的文字！")

    def get_all_item_list(self):
        values = self.listbox.get(0, tk.END)
        print('values: %s' % type(values))  # <class 'tuple'>
        print('values: %s' % list(values))
        return list(values)

    def pull_all_folders(self, f_list):
        count_f = 0
        for gf in f_list:
            subprocess.run(["git", "pull"], cwd=gf)
            count_f += 1
        return count_f

    # def get_remote_url(self, repo_path):
    #     path = Path(repo_path)
    #     remote_url = None
    #     with open(os.path.join(path, ".git", "config"), "r") as config_file:
    #         for line in config_file:
    #             if line.startswith("	url = "):
    #                 remote_url = line.split(" = ")[1]
    #             # if line.startswith("remote "):
    #             #     remote_name = line.split(" ")[1]
    #             #     if remote_name == "origin":
    #             #         remote_url = line.split(" ")[2]
    #             #         break
    #     print('remote_url: %s' % remote_url)
    #     return remote_url

    def push_all_folders(self, f_list):
        count_f = 0
        for gf in f_list:
            print('gf: %s' % gf)
            try:
                os.chdir(gf)
                # commit_message = 'git push from git python exe.'
                # subprocess.call("git --version")
                # subprocess.call("git status")
                subprocess.call("git add --all .")
                subprocess.call("git commit -m \"git push from git python exe.\"")
                subprocess.call("git push")
                count_f += 1
            except Exception as err:
                print('push %s failed\n -reason: %s' % (gf, err))
                messagebox.showwarning(title="Error Reminder", message='Push%s\n失败原因: %s' % (gf, err))
        return count_f

    # # use gitpython failed
    # def push_all_folders(self, f_list):
    #     count_f = 0
    #     for gf in f_list:
    #         print('gf: %s' % gf)
    #         # subprocess.run(["git", "push"], cwd=gf)
    #         # pip install gitpython
    #         commit_message = 'git push from git python exe.'
    #         try:
    #             repo = Repo(gf)
    #             repo.git.add(update=True)
    #             repo.index.commit(commit_message)
    #             origin = repo.remote(name='origin')
    #             # origin = repo.remote(name='master')
    #             origin.push()
    #             count_f += 1
    #         except Exception as err:
    #             print('push %s\nfailed reason: %s' % (gf, err))
    #             messagebox.showwarning(title="Error Reminder", message='Push%s\n失败原因: %s' % (gf, err))
    #     return count_f

    def start_git_these_folders(self, git_method):
        val_list = self.get_all_item_list()
        if val_list:
            self.save_all_item_to_json(val_list)
        if not val_list:
            messagebox.showwarning(title="Error Reminder", message="请添加包含.git的源码目录！")
        else:
            if git_method == 'pull_bt':
                print('pull_bt')
                finished_nmb = self.pull_all_folders(val_list)
            else:
                print('push_bt')
                finished_nmb = self.push_all_folders(val_list)
            if finished_nmb:
                messagebox.showinfo(title="任务通知", message="任务已圆满完成！共处理了%s个目录。"
                                                              % str(finished_nmb))
            else:
                messagebox.showerror(title="任务错误通知", message="任务完成，但有错误！")

    def generate_json_ffp(self):
        cur_usr_path = os.environ['USERPROFILE']
        print('cur_usr_path: %s' % cur_usr_path)
        git_conf_f = os.path.join(cur_usr_path, 'itgeeker_git_config.json')
        if not os.path.isfile(git_conf_f):
            ffp_d = dict()
            with open(git_conf_f, 'w', encoding='utf-8') as fp:
                fp.write(json.dumps(ffp_d, indent=4, ensure_ascii=False))
        return git_conf_f

    def save_all_item_to_json(self, value_list):
        print("here should to save all")
        ffp_d = dict()
        git_conf_f = self.generate_json_ffp()

        if self.entry_path.get():
            ffp_d['entry_path'] = self.entry_path.get()

        print('ffp_d: ', ffp_d)
        with open(git_conf_f, 'w', encoding='utf-8') as ffp:
            ffp_d['folder_list'] = value_list
            ffp.write(json.dumps(ffp_d, indent=4, ensure_ascii=False))

    def read_all_item_to_list_box(self):
        remove_str_f = self.generate_json_ffp()
        with open(remove_str_f, 'r', encoding='utf-8') as ffp:
            dt_dict = json.load(ffp)
            if 'folder_list' in dt_dict:
                lines = dt_dict['folder_list']
                print('lines: %s' % lines)
                if lines:
                    for i in range(len(lines)):
                        lines[i] = lines[i].rstrip("\n")
                    for line in lines:
                        if line:
                            self.listbox.insert(tk.END, line)
            if 'entry_path' in dt_dict:
                self.entry_path.delete(0, tk.END)
                self.entry_path.insert(0, dt_dict['entry_path'])
                self.folder_info_fram()
                self.count_files(dt_dict['entry_path'])

    def check_is_git_folder(self, directory):
        if os.path.exists(directory):
            if os.path.isdir(os.path.join(directory, ".git")):
                return True
            else:
                return False
        else:
            return False

    def count_files(self, directory):
        """Counts the number of files in the directory."""
        file_count = 0
        total_size = 0
        for root, directories, files in os.walk(directory):
            for file in files:
                file_count += 1
                file_path = os.path.join(root, file)
                total_size += os.path.getsize(file_path)
        self.label_file_nmb.config(text='文件数：' + str(file_count) + '个')
        megabytes = round(total_size / (1024 ** 2), 2)
        self.label_folder_size.config(text='文件夹大小：' + str(megabytes) + 'M')

    def select_directory(self):
        directory = tk.filedialog.askdirectory()
        self.entry_path.delete(0, tk.END)
        path = self.entry_path.insert(0, directory)
        if path:
            self.folder_info_fram()
            git_f = self.check_is_git_folder(directory)
            if not git_f:
                messagebox.showwarning(title="Error Reminder", message="您选择的目录不是git repo目录！")
                self.entry_path.delete(0, tk.END)
            self.count_files(directory)

    def open_website(self, url):
        open_new_tab(url)

    def on_window_close(self):
        print("Window closed")
        val_list = self.get_all_item_list()
        # if val_list:
        self.save_all_item_to_json(val_list)
        geekerWin.destroy()

    def list_frame(self):
        string_frame = ttk.LabelFrame(self, text="文件夹列表")
        string_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')
        # , selectmode = MULTIPLE
        self.listbox = tk.Listbox(string_frame, width=66, font=('Microsoft YaHei UI', 12))
        self.listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        tree_y_scroll = ttk.Scrollbar(self.listbox, orient='vertical', command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=tree_y_scroll.set)
        tree_y_scroll.place(relx=1, rely=0, relheight=1, anchor='ne')
        # mousewheel scrolling
        self.listbox.bind('<MouseWheel>', lambda event: self.listbox.yview_scroll(-int(event.delta / 60), "units"))

    def folder_info_fram(self):
        self.folder_frame = ttk.LabelFrame(self, text="目录信息")
        self.folder_frame.grid(row=4, column=0, columnspan=2, padx=10, pady=10, ipadx=10, sticky='nsew')

        self.label_file_nmb = ttk.Label(self.folder_frame, text='文件数')
        self.label_file_nmb.config(font=('Microsoft YaHei UI', 10))
        self.label_file_nmb.configure(justify="center", anchor="e")
        self.label_file_nmb.grid(row=0, column=0, padx=15, pady=5, sticky="w")

        self.label_folder_size = ttk.Label(self.folder_frame, text='文件夹大小')
        self.label_folder_size.config(font=('Microsoft YaHei UI', 10))
        self.label_folder_size.configure(justify="center", anchor="e")
        self.label_folder_size.grid(row=0, column=1, padx=15, pady=5, sticky="w")

    def select_path_frame(self):
        mnplt_frame = ttk.LabelFrame(self, text="文件目录")
        mnplt_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, ipadx=10, sticky='nsew')

        # path
        self.entry_path = ttk.Entry(mnplt_frame, justify=tk.LEFT, width=45, font=('Microsoft YaHei UI', 13))
        self.entry_path.insert(0, "浏览并选择目录")
        # self.entry_path.bind("<FocusIn>", lambda e: self.entry_path.delete('0', 'end'))
        self.entry_path.focus_force()
        self.entry_path.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky='ew')

        # select btn
        self.browse_button = tk.Button(mnplt_frame, text="选择目录", command=self.select_directory, bg='grey',
                                       fg='white',
                                       font=('Microsoft YaHei UI', 11, 'normal'))
        self.browse_button.grid(row=0, column=2, padx=10, pady=5, ipadx=10, ipady=0)

        # add path to list
        self.add_button = tk.Button(mnplt_frame, text="添加目录", command=self.add_path, bg='brown', fg='white',
                                    font=('Microsoft YaHei UI', 11, 'bold'))
        self.add_button.grid(row=1, column=0, padx=10, pady=5, ipadx=10, ipady=5)

        # edit path from list
        self.edit_button = tk.Button(mnplt_frame, text="编辑或删除", command=self.edit_item, bg='grey', fg='white',
                                     font=('Microsoft YaHei UI', 11, 'normal'))
        self.edit_button.grid(row=1, column=1, padx=10, pady=5, ipadx=10, ipady=5)

        self.menu_option = tk.StringVar(mnplt_frame)
        self.menu_option.set("保存或读取")
        menu_conf = tk.OptionMenu(mnplt_frame, self.menu_option, "保存列表", "读取列表",
                                  command=self.on_dropdown_menu_click)
        # menu_conf.bind("<Button-1>", self.on_dropdown_menu_click())
        menu_conf.grid(row=1, column=2, padx=10, pady=5, ipadx=10, ipady=5, sticky='ew')

        # start process btn
        self.start_git_pull = tk.Button(mnplt_frame, text="git pull",
                                        command=lambda: self.start_git_these_folders('pull_bt'),
                                        bg='blue',
                                        fg='white',
                                        font=('Microsoft YaHei UI', 11, 'bold'))
        # self.start_git_pull.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.start_git_pull.grid(row=2, column=0, padx=10, pady=5, ipadx=10, ipady=5, sticky='ew')
        self.start_git_push = tk.Button(mnplt_frame, text="git push",
                                        command=lambda: self.start_git_these_folders('push_bt'),
                                        bg='purple',
                                        fg='white',
                                        font=('Microsoft YaHei UI', 11, 'bold'))
        self.start_git_push.grid(row=2, column=1, padx=10, pady=5, ipadx=10, ipady=5, sticky='ew')

        self.read_all_item_to_list_box()

        geekerWin.protocol("WM_DELETE_WINDOW", self.on_window_close)

    def author_frame(self):
        author_frame = ttk.LabelFrame(self, text="关于")
        # author_frame = ttk.Frame(self)
        author_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=10)

        label_link = ttk.Label(author_frame, text='www.ITGeeker.net', font=('Microsoft YaHei UI', 10), cursor="hand2")
        label_link.bind("<Button-1>", lambda e: self.open_website("https://www.itgeeker.net"))
        label_link.grid(row=0, column=0, padx=(10, 0), ipadx=10, ipady=5, sticky="w")

        label_ver = ttk.Label(author_frame, text='开源版本Ver 1.0.0.0', font=('Microsoft YaHei UI', 10), cursor="heart")
        label_ver.config(font=('Microsoft YaHei UI', 10))
        label_ver.bind("<Button-1>",
                       lambda e: self.open_website(
                           "https://www.itgeeker.net/itgeeker-technical-service/itgeeker_batch_git_pull_and_push_tool_with_ui/"))
        label_ver.grid(row=0, column=1, padx=(10, 10), ipadx=10, ipady=5, sticky="e")

    # def menu_frame(self):
    #     menu_frame = ttk.LabelFrame(self, text="菜单")
    #     menu_frame.grid(row=7, column=0, columnspan=3, padx=10, pady=10, ipadx=10)
    #     variable = tk.StringVar(menu_frame)
    #     variable.set("one") # default value
    #     menu_save = tk.OptionMenu(menu_frame, variable, "one", "two", "three")
    #     menu_save.grid(row=0, column=0, padx=10, pady=5, ipadx=10, ipady=5, sticky='ew')


if __name__ == "__main__":
    icon_b64 = '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'
    icondata = base64.b64decode(icon_b64)
    tmp_p = tempfile.gettempdir()
    tempFile = os.path.join(tmp_p, "icon.ico")
    iconfile = open(tempFile, "wb")
    iconfile.write(icondata)
    iconfile.close()

    geekerWin = tk.Tk()
    geekerWin.wm_iconbitmap(tempFile)
    ## Delete the tempfile
    # os.remove(tempFile)

    # geekerWin.geometry("500x580")
    # geekerWin.eval('tk::PlaceWindow . center')
    window_width = 638
    window_height = 610
    display_width = geekerWin.winfo_screenwidth()
    display_height = geekerWin.winfo_screenheight()
    left = int(display_width / 2 - window_width / 2)
    top = int(display_height / 2 - window_height / 2)
    geekerWin.geometry(f'{window_width}x{window_height}+{left}+{top}')

    geekerWin.title("技术奇客小工具-带图形界面的批量Git Pull和Git Push工具")

    list_sheet = GitListFolder(geekerWin)
    list_sheet.pack()
    geekerWin.mainloop()
