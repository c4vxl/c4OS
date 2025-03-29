import webview
import time
import os
import signal
import flask
import threading

def shutdown():
    time.sleep(1)
    os._exit(0)

def run_flask_server(port=4375):
    app = flask.Flask(__name__)

    @app.route('/')
    def root():
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome</title>

    <style>
body {
    --bg: #e6e0dc;
    --text: #000000;
    --text-accent: #ffffff;
    --primary: rgb(62, 62, 94);
    --accent: #bac3d4;
    --highlight: rgb(218, 207, 183);
}

body {
    width: 100vw;
    height: 100vh;
    overflow-x: hidden;
    background: var(--bg);
    margin: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 5px;
}

* {
    box-sizing: border-box;
    color: var(--text);
    font-family: 'Courier New', Courier, monospace;
    transition: .2s;
    user-select: none;
}

.notification {
    position: fixed;
    width: 100%;
    top: -100%;
    left: 0;
    margin: 0;
    padding: 20px;
    text-align: center;
    background-color: rgb(197, 103, 103);
    color: white;
    animation: notification__animation 5s;
    z-index: 99999;
}
@keyframes notification__animation {
    0% { top: -100%; }
    10% { top: 0px; }
    60% { top: 0px; }
    100% { top: -100%; }
}

.primary, .input, .secondary {
    text-align: center;
    background: var(--primary);
    border: none;
    outline: none;
    padding: 10px 20px;
    cursor: pointer;
    color: white;
    border-radius: 13px;
    border: 2px solid var(--primary);
}
.input:hover { color: var(--text); }
.secondary:not(:hover), .input {
    background: transparent;
    color: var(--text);
}

.input {
    text-align: left;
    padding-left: 0;
    border-left: none;
    border-right: none;
    border-top: none;
    border-radius: 0;
}

.primary:hover, .input:hover, .primary.active { opacity: .86; }


.info {
    width: 20px;
    aspect-ratio: 1 / 1;
    background-color: var(--primary);
    border-radius: 300px;
    position: relative;
    cursor: pointer;
}
.info:not(.no__label)::after {
    content: "i";
    font-size: small;
    position: absolute;
    top: 3px;
    left: 0;
    bottom: 0;
    right: 0;
    margin: auto;
    width: max-content;
    height: max-content;
}
.info:hover .tooltip { opacity: 1; z-index: 999; }
.info .tooltip {
    position: absolute;
    width: max-content;
    background-color: rgb(46, 45, 45);
    padding: 10px 15px;
    border-radius: 30px 0px 30px 30px;
    margin: auto;
    text-align: center;
    right: 110%;
    top: 20px;
    opacity: 0;
    font-size: small;
    color: white;
    max-width: 50ch;
}

.dropdown {
    position: relative;
    width: 40ch;
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 10px 0px;
    overflow: hidden;
}
.dropdown .dropdown__content {
    height: 100%;
    width: 100%;
    overflow: hidden;
    max-height: 90ch;
    overflow-y: scroll;
    gap: 10px;
}
.dropdown:not(.active) .dropdown__content { display: none; }

select:active, select:hover {
    text-align: left;
    color: white;
}

button:disabled {
    cursor: not-allowed;
    opacity: .3;
}

#pages:scope .slide {
    min-width: 100%;
    height: 100%;
}
#pages .slide.active {
    min-width: 100%;
    height: 100%;
}

#themes__slider {
    width: 50vw;
    max-height: 73ch;
    max-width: 90ch;
}
#themes__slider .slide h1 {
    font-size: 140%;
    margin: 0;
    padding: 0;
}
#themes__slider .slide img {
    width: 100%;
    height: 100%;
    object-fit: contain;
}
#themes__slider .slide:not(.active) { opacity: .4; }

highlight {
    background-color: rgb(218, 207, 183);
    border-radius: 3px;
    padding: 5px 10px;
    border-radius: 13px;
    white-space: wrap;
}

.apps__list, .apps__list .apps__item {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
}

.apps__list {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    padding: 20px;
    width: 90%;
    height: 90%;
    max-width: 150ch;
    border: 1px solid var(--primary);
    border-radius: 15px;
    gap: 20px;
}
.apps__list .apps__item {
    text-align: center;
    border-radius: 10px;
    width: 10ch;
    height: 14ch;
    border: 1px solid var(--primary);
    cursor: pointer;
}
.apps__list .apps__item.active, .apps__list .apps__item:hover {
    background: rgb(from var(--primary) r g b / 50%);
    scale: 1.1;
}
.apps__list .apps__item img {
    width: 50%;
    height: auto;
}
.apps__list .apps__item p { margin: 0; height: max-content; color: var(--primary); }

::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-thumb { background-color: var(--primary); }

#overview {
    display: flex;
    flex-direction: column;
    gap: 20px;
    text-align: left;
    max-width: 90ch;
}

#overview li {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 30px;
    white-space: nowrap;
}

.row { display: flex; align-items: center; gap: 20px; }

.modal, .modal .modal__content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}

.modal {
    position: fixed;
    top: 0;
    width: 100vw;
    height: 100vh;
    background: var(--bg);
    display: none;
}
.modal.active { display: flex; z-index: 999; }

input[type="checkbox"] {
    appearance: none;
    position: relative;
    cursor: pointer;
    width: 20px;
    height: 20px;
    border: 2px solid var(--primary);
    display: inline-block;
    border-radius: 12px;
}
input[type="checkbox"]::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 4px;
    height: 8px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: translate(-50%, -60%) rotate(45deg);
    opacity: 0;
}
input[type="checkbox"]:checked {
    background-color: var(--primary);
}
input[type="checkbox"]:checked::after {
    opacity: 1;
}

.option {
    display: flex;
    align-items: center;
    border: 1px solid var(--primary);
    border-radius: 7px;
    width: 40ch;
    height: 10ch;
    position: relative;
    background: rgb(from var(--primary) r g b / 10%);
}
.option.disabled { background-color: rgb(from var(--primary) r g b / 5%); cursor: unset; border: none; }
.option.active { background: rgb(from var(--highlight) r g b / 50%); border: 1px solid transparent; }
.option input { position: absolute; top: 5px; left: 5px; }
.option p { margin: 0 auto; }
</style>

    <style>


.table {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    gap: 1px;
    border-radius: 15px;
    overflow: hidden;
    position: relative;
    overflow-y: visible;
    max-height: 60ch;
}

.table .row {
    display: flex;
    width: 100%;
    text-align: center;
    align-items: center;
    padding: 10px;
}
.table .row:first-of-type { background: var(--primary); position: sticky; top: 0; z-index: 99; font-weight: 900; }
.table .row:not(:first-of-type) {
    background: rgb(from var(--primary) r g b / 50%);
}
.table .row:not(:first-of-type):hover { opacity: .8; }
.table .row p {
    flex-grow: 1;
    width: 100%;
    text-overflow: ellipsis;
    overflow: hidden;
    margin: 0;
    color: white;
}
</style>

    <style>


.slider {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
}
.slider .slide__container {
    height: 100%;
    display: flex;
    gap: 5px;
    justify-content: left;
    align-items: center;
}

.slider .slide__container .slide {
    text-align: center;
    min-width: 50%;
    height: 50%;
    overflow: hidden;
}

.slider .slide__container .slide.active, .slider .slide__container .slide .slide__content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    min-width: 100%;
    height: max-content;
}
.slider .slide__container .slide .slide__content { flex-grow: 1; min-width: unset; }

.slider .slide__indicator {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
}
.slider .slide__indicator .circle__container .circle {
    width: 20px;
    height: 20px;
    border-radius: 300px;
    display: inline-block;
    border: 1px solid var(--primary);
    position: relative;
}
.slider .slide__indicator .circle__container .circle.active { background: var(--primary); }
.slider .slide__indicator .circle__container .circle:not(:first-of-type) { margin-left: 8px; }
</style>
    <script>
class Slider {
    constructor(element, slides = [], supressNextButtonHandler = false, supressPrevButtonHandler = false) {
        this.slidesContainer = element.querySelector(":scope .slide__container");
        slides.forEach(s => this.slidesContainer.innerHTML += s);
        this.slides = this.slidesContainer.querySelectorAll(".slide");
        this.nextBtn = element.querySelector(":scope > .slide__indicator .next");
        this.prevBtn = element.querySelector(":scope > .slide__indicator .prev");
        this.current = 0;
        this.slides.forEach(s => element.querySelector(":scope > .slide__indicator .circle__container").innerHTML += `<div class="circle"></div>`);
        this.circles = element.querySelectorAll(":scope > .slide__indicator .circle__container .circle");

        if (!supressNextButtonHandler) this.nextBtn?.addEventListener("click", () => this.display(this.current + 1));
        if (!supressPrevButtonHandler) this.prevBtn?.addEventListener("click", () => this.display(this.current - 1));

        this.slides[0]?.classList?.add("active");
        this.offset = (element.offsetWidth / 2) - (this.slides[0].offsetWidth / 2);
        this.display(0);
    };
    display(n) {
        n = n >= 0 ? n : this.slides.length - 1;
        n = n < this.slides.length ? n : 0;
        this.current = n;

        [...this.slides, ...this.circles].forEach(e => e.classList.remove("active"));
        [this.slides[n], this.circles[n]].forEach(e => e.classList.add("active"));
        this.slidesContainer.style.transform = `translateX(${this.offset - (n * (this.slides[n].offsetWidth + 5))}px)`;
    };};</script>
</head>
<body>
    <div class="slider" id="pages">
        <div class="slide__container">
            <div class="slide">
                <p style="font-size: 200%; display: flex; align-items: center; gap: 20px;">Welcome, <highlight style="font-size: 60%;">owner</highlight></p>

                <div class="slide__content">
                    <p>This is your new installation of <highlight>c4OS</highlight>.</p>
                    <p>Let's get you familiar with the controls, shall we?</p>
                </div>
            </div>

            <div class="slide">
                <h1>Controls</h1>

                <div class="slide__content">
                    <ul style="display: flex; flex-direction: column; gap: 20px; text-align: left;">
                        <li>Use <highlight>ctr + shift + A</highlight> to launch the runner menu.</li>
                        <li>Use <highlight>ctr + alt + S</highlight> to shutdown your system.</li>
                        <li>Use <highlight>ctr + alt + R</highlight> to reboot your system.</li>
                        <li>Use <highlight>ctr + shift + T</highlight> to open the OS-Theme selector.</li>
                        <li>Use <highlight>super + shift + S</highlight> to make a screenshot.</li>
                        <li>Use <highlight>super + T</highlight> to launch the Terminal.</li>
                        <li>Use <highlight>super + W</highlight> to launch the default Webbrowser.</li>
                        <li>Use <highlight>super + I</highlight> to open the Settings.</li>
                        <li>Use <highlight>super + V</highlight> to see your clipboard history.</li>
                        <li>Use <highlight>super + S</highlight> to open the control panel.</li>
                        <li>Use <highlight>super + A</highlight> to open the Desktop overview.</li>
                        <li>Use <highlight>super + shift + arrow</highlight> to move a window to another Monitor.</li>
                    </ul>

                    <p><i>No worries. You'r gonna figure it out.</i></p>
                </div>
            </div>

            <div class="slide">
                <div class="slide__content">
                    <p>Your system is ready to use. <br> We will install your selected programs in the background.</p>
                </div>
            </div>
        </div>

        <div class="slide__indicator">
            <div class="circle__container"></div>
            <button class="next primary">Next</button>
        </div>
    </div>

    <script>
        let configuration = {};

        /**
         * UI Components
         */
        const openModal = (inner) => document.body.innerHTML += `<div class="modal active" onclick="this.classList.remove('active')"><div class="modal__content">${inner}</div></div>`;
        const createNotification = async (msg) => document.querySelector(".notifications").innerHTML += `<h1 class="notification">${msg}</h1>`;

        /**
         * Page handling
         */
        const pages = new Slider(document.querySelector("#pages"), [], true);
        pages.nextBtn.addEventListener("click", (e) => {
            pages.nextBtn.textContent = pages.current === pages.slides.length - 2 ? "Complete" : "Next";
            
            if (pages.current === pages.slides.length - 1) {
                fetch("/end");
                return;
            };            
            pages.display(pages.current + 1);
        });
    </script>
</body>
</html>"""

    @app.route('/end/')
    def end():
        shutdown()
        return ""

    threading.Thread(target=app.run, kwargs={"host": "127.0.0.1", "port": port, "use_reloader": False}).start()

def start_desktop_app():
    initialized = False
    def close_listener():
        while True:
            time.sleep(1)
            if not webview.windows and initialized:
                os.kill(os.getpid(), signal.SIGINT)
                break
    
    threading.Thread(target=close_listener).start()

    initialized = True
    webview.create_window("Tour", "http://127.0.0.1:4375", fullscreen=True, on_top=True, focus=True)
    webview.start()

threading.Thread(target=run_flask_server).start()
start_desktop_app()