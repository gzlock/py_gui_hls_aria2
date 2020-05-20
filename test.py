import tkinter.ttk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

from core_new import CoreNew


class W:
    def __init__(self):
        self.core: CoreNew = None
        root = tkinter.Tk()

        frame = tkinter.ttk.Frame(root, padding=20)
        frame.pack(fill=tkinter.X)
        self.__dir = tkinter.StringVar()
        input = tkinter.ttk.Entry(frame, textvariable=self.__dir, state='readonly', )
        input.pack(fill=tkinter.X)
        input.bind('<Button-1>', self.select_dir)

        frame = tkinter.ttk.Frame(root, padding=20)
        frame.pack()
        self.start_btn = tkinter.ttk.Button(frame, text='开始', command=self.start)
        self.start_btn.pack()
        self.stop_btn = tkinter.ttk.Button(frame, text='停止', command=self.stop)
        self.stop_btn.pack(pady=20)
        self.__log = ScrolledText(frame)
        self.__log.pack()
        root.mainloop()

    def start(self):
        if len(self.__dir.get()) == 0:
            messagebox.showinfo(message='请选择文件夹')
            return
        self.start_btn.config(state=tkinter.DISABLED)
        self.stop_btn.config(state=tkinter.NORMAL)
        self.core = CoreNew(log=self.log,
                            dir=self.__dir.get(),
                            m3u8_src='https://4gtvfreepc-cds.cdn.hinet.net/live/pool/4gtv-4gtv040/4gtv-live-mid/index.m3u8?token=RIYRIiXssnNymHIExMvJbg&expires=1590010977&token1=GQqukf7YLOoA-SzU9toa8g&expires1=1590010977&_=1589964175187')
        try:
            self.core.load_m3u8()
        except Exception as e:
            messagebox.showerror(title='错误', message=str(e))
            self.stop()
            return
        self.core.start()

    def log(self, msg: str):
        # print('log', msg)
        self.__log.insert(tkinter.END, msg + '\n')
        self.__log.see('end')

    def stop(self):
        if self.core is None:
            return
        self.core.stop()
        self.core = None
        self.start_btn.config(state=tkinter.NORMAL)
        self.stop_btn.config(state=tkinter.DISABLED)

    def select_dir(self, *args):
        value = filedialog.askdirectory(title='选择要存放视频的目录')
        if len(value) > 0:
            self.__dir.set(value)


if __name__ == '__main__':
    W()
