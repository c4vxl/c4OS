import argparse
import webview
import time
import os
import signal
import customtkinter as ctk
import subprocess
import flask
import threading
import requests

def shutdown():
    time.sleep(1)
    os._exit(0)

def ask_for_permission(theme, window_width = 500, window_height = 300) -> bool:
    result = None
    def yes():
        nonlocal result
        result = True
        root.destroy()
    def no():
        nonlocal result
        result = False
        root.destroy()
    
    root = ctk.CTk()
    root.title(f"Install {theme}")
    root.geometry(f"{window_width}x{window_height}+{(root.winfo_screenwidth() // 2) - (window_width // 2)}+{(root.winfo_screenheight() // 2) - (window_height // 2)}")
    root.overrideredirect(True)

    label = ctk.CTkLabel(root, text=f"Do you want to install the '{theme}'-Theme", wraplength=250, font=("'Courier New', Courier, monospace", 16))
    label.place(relx=0.5, rely=0.3, anchor="center")

    btn_frame = ctk.CTkFrame(root)
    btn_frame.place(relx=0.5, rely=0.7, anchor="center")

    yes_btn = ctk.CTkButton(btn_frame, text="Yes", command=yes)
    yes_btn.pack(pady=3)
    no_btn = ctk.CTkButton(btn_frame, text="No", command=no)
    no_btn.pack()

    root.mainloop()

    return result

def install_theme_github(github_usr, repo, ask_for_perms = True):
    cmd = f"bash <(curl -s https://raw.githubusercontent.com/{github_usr}/{repo}/refs/heads/main/installer.sh)"
    if ask_for_perms:
        cmd = f"pkexec $({cmd})"
    print(cmd)
    subprocess.run(cmd, shell=True, check=True)

def run_flask_server(port=4375):
    app = flask.Flask(__name__)

    @app.route('/')
    def root():
        return """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Themes</title><style> body.light { --bg: #e6e0dc; --text: #000000; --text-accent: #ffffff; --primary: rgb(62, 62, 94); } body.dark { --bg: #1f1f20; --text: #ffffff; --text-accent: #000000; --primary: rgb(62, 62, 94); } body, html, .primary, .themes section, .themes, .title__bar { background: var(--bg); display: flex; flex-direction: column; align-items: center; justify-content: center; } body { width: 100vw; height: 100vh; margin: 0; padding: 0; } .themes { flex-direction: row; flex-wrap: wrap; gap: 15px; height: 100vh; overflow-y: scroll; padding: 15px 0px; } * { color: var(--text); transition: .2s; box-sizing: border-box; font-family: 'Courier New', Courier, monospace; } .br { border-radius: 13px; overflow: hidden; } .full-width { width: 100%; } .primary, .secondary { text-align: center; background: var(--primary); border: none; outline: none; padding: 10px 20px; cursor: pointer; } .primary:hover, .secondary:hover { opacity: .86; } .secondary { background: transparent; border: 2px solid var(--primary); } .themes section { border: 1px solid var(--text); border-radius: 13px; height: 60ch; width: 95vw; max-width: 50ch; justify-content: space-between; overflow: hidden; padding: 10px; } .themes section img { width: 100%; border-radius: 13px; } .hr { width: 75%; height: 1px; background-color: var(--text); } ::-webkit-scrollbar { width: 3px; } ::-webkit-scrollbar-thumb { background-color: var(--primary); } .title__bar { gap: 40px; max-height: 16ch; position: relative; width: 100%; } .title__bar .svg { position: absolute; top: 0; bottom: 0; margin: auto; right: 15px; width: 3ch; height: 3ch; cursor: pointer; } .title__bar .svg svg { width: 100%; height: auto; } .modal { position: fixed; top: 0; width: 100vw; height: 100vh; background: var(--bg); display: flex; flex-direction: column; align-items: center; justify-content: center; z-index: 999; } .modal input { width: 90vw; max-width: 100ch; } .modal:not(.active) { display: none; } </style></head><body class="light"><div class="title__bar"><h1>Select a Theme</h1><div id="switch__darkmode__icon__dark" onclick="setDarkMode(true)" class="svg"><svg width="60" height="61" viewBox="0 0 60 61" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M31.6114 59.9514C29.9231 59.9507 28.2375 59.8131 26.5714 59.54C18.422 58.2027 11.1365 53.6855 6.31515 46.9806C1.49378 40.2756 -0.469278 31.9312 0.857136 23.78C1.59937 19.1396 3.38822 14.7291 6.08811 10.8827C8.788 7.03637 12.3281 3.85508 16.44 1.58C17.1337 1.19238 17.9242 1.01217 18.7174 1.0608C19.5106 1.10942 20.2731 1.38483 20.9143 1.85429C21.5697 2.30271 22.0806 2.93194 22.385 3.66542C22.6893 4.3989 22.7739 5.20502 22.6286 5.98571L20.4 5.81429L22.5086 6.19143C21.3189 12.5017 22.4306 19.0293 25.6419 24.5901C28.8532 30.1509 33.9513 34.3764 40.0114 36.5C44.6783 38.1196 49.699 38.4338 54.5314 37.4086C55.2961 37.2585 56.0874 37.325 56.8163 37.6006C57.5452 37.8762 58.1826 38.3499 58.6567 38.9683C59.1307 39.5868 59.4226 40.3254 59.4995 41.1008C59.5763 41.8762 59.4349 42.6577 59.0914 43.3571C56.4474 48.356 52.4932 52.5413 47.6523 55.4645C42.8114 58.3878 37.2664 59.9388 31.6114 59.9514ZM18.2914 5.45429C15.0125 7.3135 12.1615 9.84196 9.92392 12.8753C7.68629 15.9086 6.11209 19.3789 5.30364 23.0606C4.4952 26.7422 4.47062 30.5528 5.2315 34.2445C5.99238 37.9363 7.52169 41.4266 9.71999 44.4886C12.3696 48.1923 15.9178 51.1611 20.0309 53.1158C24.1439 55.0705 28.6866 55.9467 33.2316 55.6621C37.7766 55.3775 42.1745 53.9415 46.0116 51.489C49.8487 49.0365 52.9988 45.6482 55.1657 41.6429C49.6517 42.7513 43.9421 42.3726 38.6228 40.5457C31.6042 38.0848 25.697 33.1949 21.9684 26.7595C18.2398 20.324 16.9356 12.7673 18.2914 5.45429Z" fill="black"/></svg></div><div id="switch__darkmode__icon__light" onclick="setDarkMode(false)" class="svg"><svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg"><g clip-path="url(#clip0_19001_8)"><mask id="mask0_19001_8" style="mask-type:luminance" maskUnits="userSpaceOnUse" x="0" y="0" width="60" height="60"><path d="M0 0H60V60H0V0Z" fill="white"/></mask><g mask="url(#mask0_19001_8)"><path d="M30 0C30.663 0 31.2989 0.263392 31.7678 0.732233C32.2366 1.20107 32.5 1.83696 32.5 2.5V12.5C32.5 13.163 32.2366 13.7989 31.7678 14.2678C31.2989 14.7366 30.663 15 30 15C29.337 15 28.7011 14.7366 28.2322 14.2678C27.7634 13.7989 27.5 13.163 27.5 12.5V2.5C27.5 1.83696 27.7634 1.20107 28.2322 0.732233C28.7011 0.263392 29.337 0 30 0ZM12.3225 8.7875C11.851 8.33211 11.2195 8.08012 10.564 8.08581C9.90851 8.09151 9.28147 8.35443 8.81795 8.81795C8.35443 9.28147 8.09151 9.90851 8.08581 10.564C8.08012 11.2195 8.33211 11.851 8.7875 12.3225L15.8575 19.3925C16.329 19.8479 16.9605 20.0999 17.616 20.0942C18.2715 20.0885 18.8985 19.8256 19.362 19.362C19.8256 18.8985 20.0885 18.2715 20.0942 17.616C20.0999 16.9605 19.8479 16.329 19.3925 15.8575L12.3225 8.7875ZM2.5 27.5C1.83696 27.5 1.20107 27.7634 0.732233 28.2322C0.263392 28.7011 0 29.337 0 30C0 30.663 0.263392 31.2989 0.732233 31.7678C1.20107 32.2366 1.83696 32.5 2.5 32.5H12.5C13.163 32.5 13.7989 32.2366 14.2678 31.7678C14.7366 31.2989 15 30.663 15 30C15 29.337 14.7366 28.7011 14.2678 28.2322C13.7989 27.7634 13.163 27.5 12.5 27.5H2.5ZM45 30C45 29.337 45.2634 28.7011 45.7322 28.2322C46.2011 27.7634 46.837 27.5 47.5 27.5H57.5C58.163 27.5 58.7989 27.7634 59.2678 28.2322C59.7366 28.7011 60 29.337 60 30C60 30.663 59.7366 31.2989 59.2678 31.7678C58.7989 32.2366 58.163 32.5 57.5 32.5H47.5C46.837 32.5 46.2011 32.2366 45.7322 31.7678C45.2634 31.2989 45 30.663 45 30ZM44.1425 40.6075C43.671 40.1521 43.0395 39.9001 42.384 39.9058C41.7285 39.9115 41.1015 40.1744 40.638 40.638C40.1744 41.1015 39.9115 41.7285 39.9058 42.384C39.9001 43.0395 40.1521 43.671 40.6075 44.1425L47.6775 51.2125C47.9081 51.4513 48.184 51.6417 48.489 51.7728C48.794 51.9038 49.1221 51.9727 49.454 51.9756C49.7859 51.9785 50.1151 51.9153 50.4224 51.7896C50.7296 51.6639 51.0088 51.4782 51.2435 51.2435C51.4782 51.0088 51.6639 50.7296 51.7896 50.4224C51.9153 50.1151 51.9785 49.7859 51.9756 49.454C51.9727 49.1221 51.9038 48.794 51.7728 48.489C51.6417 48.184 51.4513 47.9081 51.2125 47.6775L44.1425 40.6075ZM19.3925 44.1425C19.6313 43.9119 19.8217 43.636 19.9528 43.331C20.0838 43.026 20.1527 42.698 20.1556 42.366C20.1585 42.0341 20.0953 41.7049 19.9696 41.3976C19.8439 41.0904 19.6582 40.8112 19.4235 40.5765C19.1888 40.3418 18.9096 40.1561 18.6024 40.0304C18.2951 39.9047 17.9659 39.8415 17.634 39.8444C17.302 39.8473 16.974 39.9162 16.669 40.0472C16.364 40.1783 16.0881 40.3687 15.8575 40.6075L8.7875 47.675C8.54872 47.9056 8.35827 48.1815 8.22725 48.4865C8.09622 48.7915 8.02726 49.1196 8.02437 49.4515C8.02149 49.7834 8.08474 50.1126 8.21045 50.4199C8.33615 50.7271 8.52178 51.0063 8.75651 51.241C8.99124 51.4757 9.27037 51.6613 9.57762 51.7871C9.88486 51.9128 10.2141 51.976 10.546 51.9731C10.878 51.9702 11.206 51.9013 11.511 51.7703C11.816 51.6392 12.0919 51.4488 12.3225 51.21L19.3925 44.1425ZM51.2125 12.3225C51.6679 11.851 51.9199 11.2195 51.9142 10.564C51.9085 9.90851 51.6456 9.28147 51.182 8.81795C50.7185 8.35443 50.0915 8.09151 49.436 8.08581C48.7805 8.08012 48.149 8.33211 47.6775 8.7875L40.6075 15.8575C40.3687 16.0881 40.1783 16.364 40.0472 16.669C39.9162 16.974 39.8473 17.302 39.8444 17.634C39.8415 17.9659 39.9047 18.2951 40.0304 18.6024C40.1561 18.9096 40.3418 19.1888 40.5765 19.4235C40.8112 19.6582 41.0904 19.8439 41.3976 19.9696C41.7049 20.0953 42.0341 20.1585 42.366 20.1556C42.698 20.1527 43.026 20.0838 43.331 19.9528C43.636 19.8217 43.9119 19.6313 44.1425 19.3925L51.2125 12.3225ZM32.5 47.5C32.5 46.837 32.2366 46.2011 31.7678 45.7322C31.2989 45.2634 30.663 45 30 45C29.337 45 28.7011 45.2634 28.2322 45.7322C27.7634 46.2011 27.5 46.837 27.5 47.5V57.5C27.5 58.163 27.7634 58.7989 28.2322 59.2678C28.7011 59.7366 29.337 60 30 60C30.663 60 31.2989 59.7366 31.7678 59.2678C32.2366 58.7989 32.5 58.163 32.5 57.5V47.5ZM30 17.5C26.6848 17.5 23.5054 18.817 21.1612 21.1612C18.817 23.5054 17.5 26.6848 17.5 30C17.5 33.3152 18.817 36.4946 21.1612 38.8388C23.5054 41.183 26.6848 42.5 30 42.5C33.3152 42.5 36.4946 41.183 38.8388 38.8388C41.183 36.4946 42.5 33.3152 42.5 30C42.5 26.6848 41.183 23.5054 38.8388 21.1612C36.4946 18.817 33.3152 17.5 30 17.5Z" fill="white"/></g></g><defs><clipPath id="clip0_19001_8"><rect width="60" height="60" fill="white"/></clipPath></defs></svg></div></div><div class="modal" id="source__modal" onclick="this.classList.toggle('active')"><p>Source:</p><input type="text" class="primary br" onfocus="this.select()" onclick="this.parentNode.classList.toggle('active')"></div><div class="hr"></div><input type="text" class="secondary br" placeholder="Search" style="width: 90vw; max-width: 50ch; margin: 10px 0px;" autofocus id="search__bar"><div class="themes"><!--JS will put themes in--></div><script> const setDarkMode = (isDark) => { let dark_btn = document.querySelector("#switch__darkmode__icon__dark"); let light_btn = document.querySelector("#switch__darkmode__icon__light"); if (isDark) { document.body.classList.remove("light"); document.body.classList.add("dark"); dark_btn.style.display = 'none'; light_btn.style.display = 'unset'; } else { document.body.classList.remove("dark"); document.body.classList.add("light"); light_btn.style.display = 'none'; dark_btn.style.display = 'unset'; }; }; let isDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches; setDarkMode(isDarkMode); const org = "c4dots"; const addTheme = (repo) => { document.querySelector(".themes").innerHTML += ` <section><img src="https://raw.githubusercontent.com/${repo}/refs/heads/main/prev/a.png" alt="" onerror='this.style.display = "none"'><h1>${repo.split("/")[1]}</h1><div class="full-width" style="padding: 10px; display: flex; flex-direction: column; gap: 2px;"><button class="secondary full-width" onclick="document.querySelector('#source__modal input').value = 'https://github.com/${repo}'; document.querySelector('#source__modal').classList.add('active');">View source</button><button class="primary full-width" style="color: var(--text-accent);" onclick="installTheme('${repo}')">Load</button></div></section> `; }; const loadRepos = async () => { let response = await fetch(`https://api.github.com/users/${org}/repos`); response = await response.json(); return response.map(x => `${org}/${x.name}`); }; const installTheme = (theme) => { let parts = theme.split("/"); fetch(`/install/?usr=${parts[0]}&repo=${parts[1]}`) }; const init = async () => { let repos = await loadRepos(); console.log("Repos found:"); console.log(repos); repos.forEach(element => { addTheme(element); }); document.querySelector("#search__bar").addEventListener("input", (e) => { document.querySelector(".themes").innerHTML = ""; repos.filter(r => r.split("/")[1].includes(e.target.value)).forEach(r => addTheme(r)); }); }; init(); </script></body></html>"""
    
    @app.route("/install/")
    def install_theme():
        usr, repo = flask.request.args.get("usr"), flask.request.args.get("repo")

        if ask_for_permission(repo):
            install_theme_github(usr, repo)
            shutdown()
        return ""

    threading.Thread(target=app.run, kwargs={"host": "127.0.0.1", "port": port, "use_reloader": False}).start()

def start_desktop_app():
    initialized = False
    def close_listener():
        while True:
            time.sleep(1)
            if not webview.windows and initialized:
                shutdown()
                break
    
    threading.Thread(target=close_listener).start()

    initialized = True
    webview.create_window("Themes", "http://127.0.0.1:4375", width=1200, height=700)
    webview.start()


parser = argparse.ArgumentParser(description="Allows you to load a theme.")

parser.add_argument("--github-user", "-gu", type=str, help="Set the github user/organization to get the themes from.")
parser.add_argument("--list", "-l", action="store_true", help="Lists every possible theme.")
parser.add_argument("--install", "-i", type=str, help="Install a theme.")

args = parser.parse_args()

def default(x, y):
    return x if x is not None else y

usr = default(args.github_user, "c4dots")

def get_themes():
    return [ f"{usr}/{x['name']}" for x in requests.get(f"https://api.github.com/users/{usr}/repos").json() ]

if args.list:
    for theme in get_themes():
        print(f"https://github.com/{theme}")
elif args.install:
    if args.install.__contains__("/"):
        install_theme_github(args.install.split("/")[0], args.install.split("/")[1], False)
    else:
        install_theme_github(usr, args.install, False)
else:
    threading.Thread(target=run_flask_server).start()
    start_desktop_app()