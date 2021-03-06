import tkinter
from tkinter import ttk

frameList = [tkinter.Frame, tkinter.LabelFrame, ttk.Frame, ttk.LabelFrame, tkinter.Toplevel]


class Frame:
    LABEL_WIDTH = 10
    LABEL_PADDING = 4
    layout: tkinter.Widget
    without_disable: list = []

    def __init__(self):
        self.__is_disable = False

    def disable(self, disabled: bool = True):
        if self.__is_disable == disabled:
            return
        self.__is_disable = disabled
        state = tkinter.NORMAL
        if disabled:
            state = tkinter.DISABLED
        Frame.disable_child(self.layout, state=state, without=self.without_disable)

    @staticmethod
    def disable_child(frame: tkinter.Widget, state, without: list):
        for child in frame.winfo_children():
            if type(child) in frameList:
                Frame.disable_child(child, state, without=without)
            elif child not in without:
                child.config(state=state)
