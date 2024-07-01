import tkinter as tk
from tkinter import scrolledtext, filedialog
import subprocess
import threading
import base64
import re
import os

def run_command(pubfileid):
    printlog(f"----------正在下载 {pubfileid}--------\n")
    if 'save_location' not in globals():
        printlog("错误：保存位置未正确设置。\n")
        return
    if not os.path.isdir(save_location):
        printlog("错误：保存位置不存在。\n")
        return
    target_directory = os.path.join(save_location, "projects", "myprojects")
    if not os.path.isdir(target_directory):
        printlog("无效的保存位置：选定目录不包含 \projects\myprojects\n")
        return
    dir_option = f"-dir {save_location}\\projects\\myprojects\\{pubfileid}"  
    command = f"DepotdownloaderMod\\DepotDownloadermod.exe -app 431960 -pubfile {pubfileid} -verify-all -username {username.get()} -password {passwords[username.get()]} {dir_option}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for line in process.stdout:
        printlog(line)
    process.stdout.close()
    process.wait()
    printlog(f"-------------下载完成-----------\n")

def printlog(log):
    console.config(state=tk.NORMAL)
    console.insert(tk.END, log)
    console.yview(tk.END)
    console.config(state=tk.DISABLED)

def run_commands():
    run_button.config(state=tk.DISABLED)
    links = link_text.get("1.0", tk.END).splitlines()
    for link in links:
        if link:
            match = re.search(r'\b\d{8,10}\b', link.strip())
            if match:
                run_command(match.group(0))
            else:
                printlog(f"无效链接：{link}\n") 
    run_button.config(state=tk.NORMAL)

def start_thread():
    threading.Thread(target=run_commands).start()

def on_closing():
    os.system("taskkill /f /im DepotDownloadermod.exe")
    os._exit(0)

def select_save_location():
    selected_directory = filedialog.askdirectory()
    target_directory = os.path.join(selected_directory, "projects", "myprojects")
    if not os.path.isdir(target_directory):
        printlog("无效的保存位置：选定目录不包含 \projects\myprojects\n")
    else:
        printlog(f"路径已设置为 {target_directory}\n")
        global save_location
        save_location = selected_directory
        save_location_label.config(text=f"保存位置：{target_directory}")
        with open('lastsavelocation.cfg', 'w') as file:
            file.write(target_directory)

def load_save_location():
    try:
        with open('lastsavelocation.cfg', 'r') as file:
            target_directory = file.read().strip()
            if os.path.isdir(target_directory):
                global save_location
                save_location = target_directory
            else:
                save_location = "未设置"
    except FileNotFoundError:
        save_location = "未设置"

accounts = {'ruiiixx': 'UzY3R0JUQjgzRDNZ',
    'premexilmenledgconis': 'M3BYYkhaSmxEYg==',
    'vAbuDy': 'Qm9vbHE4dmlw',
    'adgjl1182': 'UUVUVU85OTk5OQ==',
    'gobjj16182': 'enVvYmlhbzgyMjI=',
    '787109690': 'SHVjVXhZTVFpZzE1'
    }
passwords = {account: base64.b64decode(accounts[account]).decode('utf-8') for account in accounts}

load_save_location()

root = tk.Tk()
root.title("Wallpaper Engine 创意工坊下载器")

title_label = tk.Label(root, text="Wallpaper Engine 创意工坊下载器", font=("Arial", 21))
title_label.grid(row=0, column=0)

username_label = tk.Label(root, text="选择账户:")
username_label.grid(row=1, column=0, sticky='w', padx=(130, 0))
username = tk.StringVar(root)
username.set(list(accounts.keys())[0]) 
username_menu = tk.OptionMenu(root, username, *accounts.keys())
username_menu.grid(row=1, column=0)

save_location_button = tk.Button(root, text="选择壁纸引擎路径", command=select_save_location)
save_location_button.grid(row=2, column=0)

save_location_label = tk.Label(root, text=f"壁纸引擎路径：{save_location}")
save_location_label.grid(row=3, column=0)

link_label = tk.Label(root, text="输入创意工坊项目（每行一个，支持链接和文件ID）:")
link_text = scrolledtext.ScrolledText(root, height=10)
link_label.grid(row=4, column=0)
link_text.grid(row=5, column=0)

console_label = tk.Label(root, text="控制台输出：")
console = scrolledtext.ScrolledText(root, height=10)
console_label.grid(row=6, column=0)
console.grid(row=7, column=0)

run_button = tk.Button(root, text="下载", command=start_thread)
run_button.grid(row=8, column=0)

root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()