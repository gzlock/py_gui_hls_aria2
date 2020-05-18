from tkinter import Menu as tkMenu
from webbrowser import open


class Menu:
    def __init__(self, root) -> None:
        super().__init__()
        self.menu = menubar = tkMenu(root)
        root.config(menu=menubar)

        helpmenu = tkMenu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=helpmenu)

        helpmenu.add_command(label="本软件开源(Github)", command=lambda: open(
            'https://github.com/gzlock/mrplayer_mainland_live_server'))
