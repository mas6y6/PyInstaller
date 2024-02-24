import time
import consolemenu
import consolemenu.items as items
import pyinputplus
import tkinter.filedialog as fd
import os
import urllib.request
import subprocess
import progressbar
import requests
import zipfile

settings = {"path":os.getcwd(),"installpip":True,"version":"3.12.2","includepyhelpertools":False}

class bcolors:
    HEADER    = '\033[95m'
    OKBLUE    = '\033[94m'
    OKGREEN   = '\033[92m'
    WARNING   = '\033[93m'
    FAIL      = '\033[91m'
    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC      = '\033[0m'

pbar = None

print(bcolors.OKBLUE+"PyInstaller is made by @mas6y6(on github)"+bcolors.ENDC)
time.sleep(3)

def _show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        widgets = ["Downloading Python: ",progressbar.Bar(),"",progressbar.Percentage()," ",progressbar.ETA()]
        pbar = progressbar.ProgressBar(maxval=total_size,widgets=widgets,line_breaks = False)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

def installpython():
    print(f"Installing python to {settings['path']}...")
    os.chdir(settings['path'])
    print("Checking python version")
    if requests.get(f"https://github.com/mas6y6/pythoninzip/raw/{settings["version"]}/python.zip").status_code == 404:
        print(bcolors.FAIL+"ERROR: Verison of python was not found (REQUESTCODE: 404)"+bcolors.ENDC)
        input("Press \"Enter\" to continue")
    else:
        print(bcolors.OKGREEN+"Python version found downloading"+bcolors.ENDC)
    print("Downloading preinstalled zip file...")
    try:
        urllib.request.urlretrieve(f"https://github.com/mas6y6/pythoninzip/raw/{settings["version"]}/python.zip",f"{settings['path']}\python.zip",_show_progress)
    except Exception as e:
        print(bcolors.FAIL+f"ERROR: Failed to extract python contents {e}"+bcolors.ENDC)
        input("Press \"Enter\" to continue")
    print("Unziping preinstalled zip file...")
    os.chdir(settings['path'])
    with zipfile.ZipFile("python.zip") as zip:
        try:
            zip.extractall()
        except Exception as e:
            print(bcolors.FAIL+f"ERROR: Failed to extract python contents ({e})"+bcolors.ENDC)
            input("Press \"Enter\" to continue")
        else:
            print(bcolors.OKGREEN+"Python successfully extracted"+bcolors.ENDC)
    
     

#pyinputplus.inputYesNo(prompt="",yesVal=True,noVal=False)

def setpath():
    global settingsmenu
    print("The window for the directory selection is open")
    path = fd.askdirectory(title="PyInstaller",mustexist=True)
    settings["path"] = path
    if path == '':
        print(bcolors.FAIL+"ERROR: User canceled \"tkinter.filedialog.askdirectory()\""+bcolors.ENDC)
        input("Press \"Enter\" to continue")
    os.chdir(path)
    print("Reconfiguring menu...")
    settingsmenu.items[0].text = f"Set Install Path {settings['path']}"

def setversion():
    global settingsmenu
    version = input("Python verison: ")
    if version == '' or version == None:
        print(bcolors.FAIL+"ERROR: Invalid version \"input()\""+bcolors.ENDC)
        input("Press \"Enter\" to continue")
    else:
        settings["version"] = version
    print("Reconfiguring menu...")
    settingsmenu.items[1].text = f"Set Install Path {settings['version']}"

settingsmenu = consolemenu.ConsoleMenu(title="Settings",exit_option_text="Back")
setpathitem = items.FunctionItem(text=f"Set Install Path {settings['path']}",function=setpath)
settingsmenu.append_item(setpathitem)
setpathitem = items.FunctionItem(text=f"Python Version {settings['version']}",function=setversion)
settingsmenu.append_item(setpathitem)

cmenu = consolemenu.ConsoleMenu(title="PyInstaller",subtitle=f"This app helps you install python to your USB drive *Not recommended to to install to main drive*",)
installitem = items.FunctionItem(text="Install Now",function=installpython)
cmenu.append_item(installitem)
setting = items.SubmenuItem("Settings",settingsmenu)
cmenu.append_item(setting)
cmenu.show()