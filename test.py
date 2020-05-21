import asyncio
import time
import tkinter
from tkinter import ttk


class Window:
    def __init__(self):
        self.__do_while = False
        root = tkinter.Tk()
        root.minsize(200, 200)
        frame = ttk.Frame()
        frame.pack(fill=tkinter.BOTH)
        ttk.Button(frame, text='开始', command=self.start).pack()
        ttk.Button(frame, text='停止', command=self.stop).pack(pady=10)
        root.mainloop()

    def start(self):
        print(time.time())
        self.__do_while = True

        loop = asyncio.get_event_loop()

        async def go():
            # 只print了一次就结束了
            asyncio.create_task(self.exec())

            # 界面卡住了
            # await asyncio.create_task(self.exec())

            # 界面卡住了
            # await self.exec()

        loop.run_until_complete(go())
        print(time.time())

    def stop(self):
        self.__do_while = False

    async def exec(self):
        i = 0
        while self.__do_while:
            print('exec', i)
            i += 1
            await asyncio.sleep(2)


if __name__ == "__main__":
    Window()
