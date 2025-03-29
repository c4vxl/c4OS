import webview

webview.create_window("Tour", "http://127.0.0.1:4375", fullscreen=True, on_top=True, focus=True)
webview.start()