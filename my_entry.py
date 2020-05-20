import sys
import tkinter
from tkinter.ttk import Entry


class MyEntry(Entry):
    def __init__(self, master=None, widget=None, **kw):
        super().__init__(master, widget, **kw)
        if sys.platform == 'darwin':
            key = 'Mod1'
        else:
            key = 'Control'
        self.__is_readonly = kw.get('state') == 'readonly'
        # print('entry state', kw.get('state'), self.__is_readonly)
        self.bind('<%s-a>' % key, lambda e: self.after_idle(self.select_all))

    def select_all(self):
        self.select_range(0, 'end')
        # move cursor to the end
        self.icursor('end')

    def config(self, cnf=None, **kw):
        state = kw.get('state')
        if state == tkinter.DISABLED:
            kw['state'] = 'readonly'
        elif state == tkinter.NORMAL and self.__is_readonly:
            kw['state'] = 'readonly'
        return super().configure(cnf, **kw)


if __name__ == '__main__':
    a = dict()
    print(a.get('a'))
if __name__ == '__main__1':
    root = tkinter.Tk()
    v = tkinter.StringVar(value='123')
    entry = MyEntry(root, state='readonly', textvariable=v)
    entry.pack()
    entry.config(state=tkinter.DISABLED)
    entry.mainloop()
