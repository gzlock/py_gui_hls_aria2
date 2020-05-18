from tkinter import Menu as tkMenu, messagebox
from webbrowser import open


class Menu:
    def __init__(self, root) -> None:
        super().__init__()
        self.menu = menubar = tkMenu(root)
        root.config(menu=menubar)

        helpmenu = tkMenu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=helpmenu)

        helpmenu.add_command(label="关于本软件", command=self.show_about)
        helpmenu.add_command(label="本软件开源项目主页(Github)", command=lambda: open(
            'https://github.com/gzlock/py_gui_hls_aria2'))

    def show_about(self):
        messagebox.showinfo(title='关于本软件', message='开发者：gzlock88@gmail.com\n集成以下开源软件：\nAria2\nFFmpeg')
