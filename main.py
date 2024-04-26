import os
import logging
import asyncio
import yaml
import sys
import json
import PIL
import tkinter
import customtkinter

from globalSetting import *
import customtkinter as ctk

#yaml(PyYaml) 외부 패키지
#PIL(pillow) 외부 패키지
#customtkinter 외부 패키지

logging.basicConfig(
    level=logging.DEBUG
)


GlobalSetting.root = App()

GlobalSetting.windowQuit = False

GlobalSetting.root.update()
GlobalSetting.root.mainloop()

