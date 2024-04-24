import logging
import os
import sys
import tkinter
import yaml
import re

import command

import customtkinter as ct
from tkinter import filedialog
from PIL import Image

class GlobalSetting:
    root = None
    windowQuit = False
    quitEventList = []

class App(ct.CTk):
    color_NormalEnable = "gray90"
    color_NormalDisable = "gray30"
    color_Complate = "chartreuse2"
    color_YetComplate = "goldenrod1"
    color_NotComplate = "firebrick1"

    def valid_projectPath_var(self, var, index, mode):
        if(not self.valid_projectPath.get()):
            if (self.enable_goto_step1.get()):
                self.enable_goto_step1.set(False)
        else:
            self.scanData = self.ScanData(self.projectPath)
            print(self.scanData)

        self.button_step1_projectPath_pathText.configure(
            text_color=self.color_Complate if self.valid_projectPath.get() else self.color_NotComplate)
        self.button_step1_materialAdd_button.configure(
            text_color=self.color_Complate if self.valid_projectPath.get() else self.color_NotComplate)
        self.button_step1_materialAdd_button.configure(
            state=ct.NORMAL if self.valid_projectPath.get() else ct.DISABLED)
        pass

    def valid_material_table_id(self, var, index, mode):
        if(self.select_MaterialGroupIndex.get() != -1):
            self.enable_goto_step1.set(True)
            # ['ct']['parent']

            # self.shaderGUIDToMaterialTable[]['data']
        pass

    def valid_Step0(self, var, index, mode):

        pass
    def valid_Step1(self, var, index, mode):
        self.button_step1_next_button.configure(
            text_color=self.color_Complate if self.enable_goto_step1.get() else self.color_NotComplate)
        self.button_step1_next_button.configure(
            state=ct.NORMAL if self.enable_goto_step1.get() else ct.DISABLED)

        nowIndex = 0
        nextIndex = nowIndex + 1
        self.topbar_buttons[nowIndex].configure(
            text_color=self.color_Complate if self.enable_goto_step1.get() else self.color_YetComplate)

        if not self.enable_goto_step1.get():
            for i in range(len(self.topbar_buttons))[nextIndex:]:
                self.topbar_buttons[i].configure(ct.DISABLED)
            self.topbar_buttons[nextIndex].configure(state=ct.DISABLED)
        else:
            self.topbar_buttons[nextIndex].configure(text_color=self.color_YetComplate)
            self.topbar_buttons[nextIndex].configure(state = ct.NORMAL)
        pass


    def valid_Step2(self, var, index, mode):
        print(self.step1_next_step2_button)
        self.step1_next_step2_button.configure(
            text_color=self.color_Complate if self.enable_goto_step2.get() else self.color_NotComplate)
        self.step1_next_step2_button.configure(
            state=ct.NORMAL if self.enable_goto_step2.get() else ct.DISABLED)

        nowIndex = 1
        nextIndex = nowIndex + 1

        if not self.enable_goto_step2.get():
            for i in range(len(self.topbar_buttons))[nextIndex:]:
                self.topbar_buttons[i].configure(ct.DISABLED)
            self.topbar_buttons[nextIndex].configure(state=ct.DISABLED)
            self.topbar_buttons[nowIndex].configure(state=ct.NORMAL, text_color=self.color_YetComplate)
        else:
            if(self.enable_goto_step1.get()):
                self.topbar_buttons[nextIndex].configure(text_color=self.color_YetComplate)
                self.topbar_buttons[nextIndex].configure(state = ct.NORMAL)

                self.topbar_buttons[nowIndex].configure(state=ct.NORMAL, text_color=self.color_Complate)

    def valid_Step3(self, var, index, mode):

        nowIndex = 2
        nextIndex = nowIndex + 1

        if not self.enable_goto_step3.get():
            for i in range(len(self.topbar_buttons))[nextIndex:]:
                self.topbar_buttons[i].configure(ct.DISABLED)
            self.topbar_buttons[nextIndex].configure(state=ct.DISABLED)
            self.topbar_buttons[nowIndex].configure(state=ct.NORMAL, text_color=self.color_YetComplate)
        else:
            if (self.enable_goto_step2.get()):
                self.topbar_buttons[nextIndex].configure(text_color=self.color_YetComplate)
                self.topbar_buttons[nextIndex].configure(state=ct.NORMAL)

                self.topbar_buttons[nowIndex].configure(state=ct.NORMAL, text_color=self.color_Complate)


    def __init__(self):
        super().__init__()

        self.image_none = ct.CTkImage(Image.open('./images/image_icon_light.png'), size=(30, 30))

        self.projectPath = 'C:\\'
        self.valid_projectPath = ct.BooleanVar(value=False)
        self.valid_projectPath.trace_add('write', self.valid_projectPath_var)

        self.shaderGUIDToMaterialTable = { }
        self.scanData = { }

        self.select_MaterialGroupIndex = tkinter.IntVar(value=-1)
        self.select_MaterialGroupIndex.trace_add('write', self.valid_material_table_id)

        self.enable_goto_step0 = ct.BooleanVar(value=False)
        self.enable_goto_step1 = ct.BooleanVar(value=False)
        self.enable_goto_step2 = ct.BooleanVar(value=False)
        self.enable_goto_step3 = ct.BooleanVar(value=False)

        self.enable_goto_step0.trace_add('write', self.valid_Step0)
        self.enable_goto_step1.trace_add('write', self.valid_Step1)
        self.enable_goto_step2.trace_add('write', self.valid_Step2)
        self.enable_goto_step3.trace_add('write', self.valid_Step3)

        self.protocol("WM_DELETE_WINDOW", onClose)
        self.bind('<Escape>', lambda e: onClose())
        self.title("Unity Material Migrator")
        self.defualtSize = (1300, 800)
        self.geometry(f"{self.defualtSize[0]}x{self.defualtSize[1]}+{int(self.winfo_screenwidth()/2 - self.defualtSize[0]/2)}+{int(self.winfo_screenheight()/2-self.defualtSize[1]/2)}(pixel)")
        #self.winfo_screenwidth()/2 - self.defualtSize[0]/2}x{self.winfo_screenheight()/2-self.defualtSize[1]/2

        ct.set_appearance_mode('dark')

        self.grid_columnconfigure((0), weight=0)
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)


        self.sidebar_frame = ct.CTkFrame(self, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=10, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(1, weight=1)

        self.sidebar_Label = ct.CTkLabel(self.sidebar_frame, text="Material\nMigrator", width=260, height=150, font=ct.CTkFont(size=34, weight="bold"))
        self.sidebar_Label.grid(row=0,column=0,padx=(5,5),pady=(5,5), sticky="ew")

        self.sidebar_CommandScroll = ct.CTkScrollableFrame(master=self.sidebar_frame,label_text="Command Records",
                              label_font=ct.CTkFont(size=20, weight="bold"))
        self.sidebar_CommandScroll.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.sidebar_CommandList = []
        self.sidebar_CommandLabel = []

        self.sidebar_Rollback_Button = ct.CTkButton(master=self.sidebar_frame, text="Rollback", height=65, font=ct.CTkFont(size=24),
                                 command=lambda: self.LastUnDoCommand())
        self.sidebar_Rollback_Button.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="sew")

        self.topbar_frame = ct.CTkFrame(self, height=50, corner_radius=0)
        self.topbar_frame.grid(row=0, column=1, columnspan = 10, sticky="nsew")
        self.topbar_frame.grid_rowconfigure(4, weight=1)

        self.topbar_buttons = []
        for i in range(4):
            nowButton = ct.CTkButton(self.topbar_frame, corner_radius=0, height=40, border_spacing=10,
                                                    text="Home",
                                                    font = ct.CTkFont(size=14), #, weight="bold"
                                                    fg_color="transparent", text_color=("gray10", "gray90"),
                                                    hover_color=("gray70", "gray30"),
                                                    text_color_disabled=["gray10", App.color_NotComplate],
                                                    anchor="w") #image=self.home_image,
            nowButton.grid(row=0, column=i, sticky="ew")
            nowButton.configure(state=ct.DISABLED)
            self.topbar_buttons.append(nowButton)

        self.topbar_buttons[0].configure(state=ct.NORMAL, text="Material Load")
        self.topbar_buttons[1].configure(text="Property Modity")
        self.topbar_buttons[2].configure(text="Converting")
        self.topbar_buttons[3].configure(text="Complate")

        self.topbar_buttons[0].configure(command = lambda: self.GotoStep(0))
        self.topbar_buttons[1].configure(command = lambda: self.GotoStep(1))
        self.topbar_buttons[2].configure(command = lambda: self.GotoStep(2))


        self.step_root_frame = []
        for i in range(4):
            self.step_root_frame.append(ct.CTkFrame(self, corner_radius=0, fg_color="transparent"))
            self.step_root_frame[i].grid_rowconfigure((0), weight=1)
            self.step_root_frame[i].grid_columnconfigure((0), weight=1)

            #self.main_frame.grid_rowconfigure(4, weight=1)
        #self.step_root_frame[0].grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))

        self.InitStep0(self.step_root_frame[0])
        self.InitStep1(self.step_root_frame[1])
        self.InitStep2(self.step_root_frame[2])
        self.InitStep3(self.step_root_frame[3])

        self.GotoStep(0)


    def InitStep0(self, root_frame):

        root_frame.grid_rowconfigure((0, 1, 2), weight=1)
        root_frame.grid_columnconfigure((0), weight=1)

        self.button_step1_projectPath_frame = ct.CTkFrame(root_frame, corner_radius=0, fg_color="transparent")
        self.button_step1_projectPath_frame.grid(row=0, column=0,  padx=(0, 0), pady=(0, 0),sticky="nsew")
        self.button_step1_projectPath_button = ct.CTkButton(self.button_step1_projectPath_frame, corner_radius=10, height=60, width=300,  #border_spacing=10,
                                                            text="Project Path",
                                                            font=ct.CTkFont(size=24),  # , weight="bold"
                                                            #text_color=("gray10", "gray90"),
                                                            #hover_color=("gray70", "gray30"),
                                                            text_color_disabled = ("gray10", App.color_NormalDisable),
                                                            #compound="top",
                                                            anchor = "center",
                                                            command=self.GetProjectPath)  # image=self.home_image,
        self.button_step1_projectPath_button.pack(side=ct.TOP)

        self.button_step1_projectPath_pathText = ct.CTkLabel(self.button_step1_projectPath_frame, text=self.projectPath)
        self.button_step1_projectPath_pathText.pack(side=ct.TOP)

        #nowButton.grid(row=0, column=0)

        self.button_step1_materialAdd = ct.CTkFrame(root_frame, corner_radius=0, fg_color="transparent")
        self.button_step1_materialAdd.grid(row=1, column=0, padx=(0, 0), pady=(0, 0), sticky="nsew")
        self.button_step1_materialAdd_button = ct.CTkButton(self.button_step1_materialAdd, corner_radius=10, height=60, width=300,  # border_spacing=10,
                                                            text="Material Append",
                                                            font=ct.CTkFont(size=24),  # , weight="bold"
                                                            # text_color=("gray10", "gray90"),
                                                            # hover_color=("gray70", "gray30"),
                                                            text_color_disabled=("gray10", App.color_NormalDisable),
                                                            # compound="top",
                                                            anchor="center",
                                                            command=self.GetMaterials)  # image=self.home_image,
        #nowButton.grid(row=1, column=0)
        self.button_step1_materialAdd_button.pack(side=ct.TOP)


        self.scrollable_shader = ct.CTkScrollableFrame(root_frame, height=400, orientation="horizontal") # horizontal
        self.scrollable_shader.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")  # ew
        self.scrollable_shader.grid_rowconfigure(0, weight=0)
        self.scrollable_shader.grid_rowconfigure(1, weight=1)
        self.scrollable_shader_list = []

        self.button_step1_next_button = ct.CTkButton(root_frame, corner_radius=10, height=60,
                                                     width=20,  # border_spacing=10,
                                                     text="Next",
                                                     font=ct.CTkFont(size=24),  # , weight="bold"
                                                     # text_color=("gray10", "gray90"),
                                                     # hover_color=("gray70", "gray30"),
                                                     text_color_disabled=("gray10", App.color_NormalDisable),
                                                     # compound="top",
                                                     anchor="center",
                                                     command=lambda: self.GotoStep(1))  # image=self.home_image,
        self.button_step1_next_button.grid(row=3, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.select_MaterialGroupIndex.set(-1)
        self.valid_projectPath.set(False)
        self.enable_goto_step1.set(False)

    def InitStep1(self, root_frame):
        self.step1_prevMaterialIndex = -1
        self.step1_changePropertyName_Table = {}

        self.step1_property_frame = ct.CTkScrollableFrame(root_frame, label_text="Material Propertys", label_font=ct.CTkFont(size=20, weight="bold"))
        self.step1_property_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.step1_property_frame.grid_columnconfigure(0, weight=1)
        self.step1_property_element_list = []

        self.step1_next_step2_button = ct.CTkButton(root_frame, corner_radius=10, height=60,
                                                    width=20,  # border_spacing=10,
                                                    text="Next",
                                                    font=ct.CTkFont(size=24),  # , weight="bold"
                                                    # text_color=("gray10", "gray90"),
                                                    # hover_color=("gray70", "gray30"),
                                                    text_color_disabled=("gray10", App.color_NormalDisable),
                                                    # compound="top",
                                                    anchor="center",
                                                    command=lambda: self.GotoStep(2))  # image=self.home_image,
        self.step1_next_step2_button.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="ew")

        self.enable_goto_step2.set(True)
        pass

    def InitStep2(self, root_frame):
        root_frame.grid_columnconfigure((0, 1),weight=1)
        root_frame.grid_rowconfigure((0), weight=1)

        self.step2_MaterialNameList = []
        self.step2_MaterialEnableList = []

        self.step2_Scroll_Material = ct.CTkScrollableFrame(root_frame,
                                                           label_text="Convert Material Select",
                                                           label_font=ct.CTkFont(size=24))
        self.step2_Scroll_Material.grid(row=0, column=0, padx=(5, 5), pady=(5, 5), sticky="nsew")  # ew
        self.step2_Scroll_Material.grid_columnconfigure(0, weight=1)
        self.step2_Scroll_Material.grid_rowconfigure(0, weight=1)

        self.step2_rightOption_Frame = ct.CTkFrame(master=root_frame, fg_color="transparent")
        self.step2_rightOption_Frame.grid(row=0,column=1, sticky="nsew")
        self.step2_rightOption_Frame.grid_columnconfigure((0), weight=1)
        self.step2_rightOption_Frame.grid_rowconfigure((0), weight=1)

        self.step2_CommandCreateSwitch_Var = ct.BooleanVar(value=True)
        self.step2_CommandCreateSwitch = ct.CTkSwitch(master=self.step2_rightOption_Frame, text="Create Commend", font=ct.CTkFont(size=18), variable=self.step2_CommandCreateSwitch_Var)
        self.step2_CommandCreateSwitch.grid(row=0,column=0,padx=(10,10),pady=(10, 10), sticky="w")#, sticky="nsew"

        self.step2_NextStep3_Button = ct.CTkButton(master=self.step2_rightOption_Frame, height=100, font=ct.CTkFont(size=28), text='Next', command=lambda :self.GotoStep(3))
        self.step2_NextStep3_Button.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="sew")


    def InitStep3(self, root_frame):
        root_frame.grid_rowconfigure(0, weight=1)
        root_frame.grid_columnconfigure(0, weight=1)
        endButton = ct.CTkButton(master=root_frame, text="Convert",width=350,height= 120, font=ct.CTkFont(size=48), command=lambda : self.ConvertComplate())
        endButton.grid(row=0,column=0)

    def SetStep0Data(self):
        pass
    def SetStep1Data(self):
        self.enable_goto_step2.set(True)

        if(self.select_MaterialGroupIndex.get() != self.step1_prevMaterialIndex):
            self.step1_changePropertyName_Table = {}
        self.step1_prevMaterialIndex = self.select_MaterialGroupIndex.get()
        self.step1_changePropertyName_Table = {}
        dataList = None
        dataTable = {}
        for i, v in self.shaderGUIDToMaterialTable.items():
            if (v['index'] == self.select_MaterialGroupIndex.get()):
                dataList = v['data']
                break

        propertyTypes = ['m_TexEnvs', 'm_Ints', 'm_Floats', 'm_Colors']

        if(dataList != None):
            for data in dataList:
                #dataTable['']
                propertys = data['Material']['m_SavedProperties']

                for propertyType in propertyTypes:
                    textureList = propertys[propertyType]
                    dataTable.setdefault(propertyType, {})
                    for propertyTexture in textureList:
                        for key, value in propertyTexture.items():
                            dataTable[propertyType].setdefault(key, [])
                            dataTable[propertyType][key].append(value)

            self.select_property_dataTable = dataTable
            self.select_property_dataList = dataList

        for i in self.step1_property_element_list:
            self.remove_tk(i)
        self.step1_property_element_list.clear()


        for nowType in propertyTypes:

            for key, value in self.select_property_dataTable[nowType].items():
                propertyFrame = ct.CTkFrame(self.step1_property_frame, corner_radius=0, fg_color="transparent")
                propertyFrame.grid(row=len(self.step1_property_element_list), column=0, padx=(10, 10), pady=(3, 3), sticky="nsew")
                propertyFrame.grid_columnconfigure(5, weight=1)

                propertyLabel = ct.CTkLabel(master=propertyFrame,text=key,width=300, font=ct.CTkFont(size=15, weight="bold"), anchor='w')
                propertyLabel.grid(row=0, column=0, padx=(10, 0), sticky="nsw")

                propertyTypeContext = ct.CTkLabel(master=propertyFrame, text="Type : ", width=30,
                                           font=ct.CTkFont(size=14), anchor='e')
                propertyTypeContext.grid(row=0, column=1, padx=(10, 0), sticky="nsw")

                propertyType = ct.CTkLabel(master=propertyFrame, text=nowType, width=70,
                                            font=ct.CTkFont(size=14), anchor='w')
                propertyType.grid(row=0, column=2, padx=(0, 0), sticky="nsw")

                propertyValueContext = ct.CTkLabel(master=propertyFrame, text="Value : ", width=30,
                                           font=ct.CTkFont(size=14), anchor='e')
                propertyValueContext.grid(row=0, column=3, padx=(10, 0), sticky="nsw")

                if(nowType == "m_TexEnvs"):
                    guid = None
                    for nowValue in value:
                        guid = nowValue['m_Texture'].get('guid')
                        if(guid != None): break
                    path = ""
                    if(guid != None):
                        path = self.scanData.get(guid)
                        pass
                    image = None
                    if(path != "" and path !=None):
                        splitPath = path.split('/')
                        path = '/'.join(splitPath[0:-1])
                        splitFileName = splitPath[-1].split('.')
                        fileName = '.'.join(splitFileName[0:-1])
                        image = ct.CTkImage(Image.open(os.path.join(path, fileName)), size=(40, 40))
                    else:
                        image = self.image_none
                    propertyValue = ct.CTkLabel(master=propertyFrame, text="", width=50, anchor='w', image=image, compound="left")
                elif nowType == 'm_Colors':
                    propertyValue = ct.CTkLabel(master=propertyFrame, text=f'r:{round(value[0]['r'],3)} g:{round(value[0]['g'],2)} b:{round(value[0]['b'],3)}, a:{round(value[0]['a'],3)}', width=50, anchor='w')
                else:
                    propertyValue = ct.CTkLabel(master=propertyFrame, text=value[0], width=50, anchor='w')
                propertyValue.grid(row=0, column=4, padx=(0, 0), sticky="nsw")

                self.step1_changePropertyName_Table.setdefault(key, ct.StringVar(value=key))
                entry = ct.CTkEntry(propertyFrame, placeholder_text="PropertyID",textvariable=self.step1_changePropertyName_Table[key])
                entry.grid(row=0, column=5, padx=(20, 10), pady=(3, 3), sticky="nsew")


                self.step1_property_element_list.append(propertyFrame)

    def SetStep2Data(self):
        for i in self.step2_MaterialNameList:
            self.remove_tk(i)

        self.step2_MaterialNameList.clear()
        self.step2_MaterialEnableList.clear()

        dataList = None
        for i, v in self.shaderGUIDToMaterialTable.items():
            if (v['index'] == self.select_MaterialGroupIndex.get()):
                dataList = v['data']
                break
        if(dataList == None):
            return


        for index, data in enumerate(dataList):
            boolData = ct.BooleanVar(value=True)

            label = ct.CTkSwitch(self.step2_Scroll_Material, text=data['Material']['m_Name'], variable=boolData)
            label.grid(row=index, column=0, padx=(5, 5), pady=(5, 5))

            self.step2_MaterialEnableList.append(boolData)
            self.step2_MaterialNameList.append(label)

        self.enable_goto_step3.set(value=True)

    def SetStep3Data(self):
        self.topbar_buttons[3].configure(state=ct.NORMAL, text_color=self.color_Complate)
        pass

    def ConvertComplate(self):

        try:
            dataList = None
            pathList = None
            for i, v in self.shaderGUIDToMaterialTable.items():
                if (v['index'] == self.select_MaterialGroupIndex.get()):
                    dataList = v['data'].copy()
                    pathList = v['path'].copy()
                    break
            if (dataList == None):
                return
            pattern = re.compile(r"^\s*- (.+):$")

            pathList2 = []
            dataList2 = []
            for index, path in enumerate(pathList):
                if (self.step2_MaterialEnableList[index].get()):
                    newLineDatas = []

                    with open(path,'r') as file:
                        lineDatas = file.readlines()
                        for line in lineDatas:
                            matchData = pattern.match(line)
                            if(matchData):
                                data = matchData.groups()[0].strip()
                                if (data in self.step1_changePropertyName_Table.keys()):
                                    line = line.replace(data, self.step1_changePropertyName_Table[data].get())
                            newLineDatas.append(line)
                    newData = ''.join(newLineDatas)
                    pathList2.append(path)
                    dataList2.append(newData)


                    shaderGUID = None
                    index2 = -1
                    oldData = None

                    for k,v in self.shaderGUIDToMaterialTable.items():
                        if(path in v['path']):
                            shaderGUID = k
                            index2 = v['path'].index(path)
                            oldData = v['data'][index2]

                    if(shaderGUID != None and index2 != -1 and oldData != None):
                        childLabels = self.shaderGUIDToMaterialTable[shaderGUID]['ct']['childs']

                        self.shaderGUIDToMaterialTable[shaderGUID]['data'].remove(oldData)
                        self.shaderGUIDToMaterialTable[shaderGUID]['path'].remove(path)

                        self.remove_tk(childLabels[index2])
                        self.shaderGUIDToMaterialTable[shaderGUID]['ct']['childs'].remove(childLabels[index2])

            command = Command_MaterialConvert(pathList2, dataList2)
            command.Do()
            self.AppendCommend(command)
        finally:
            pass


        self.enable_goto_step0.set(value=True)
        self.enable_goto_step1.set(value=False)
        self.enable_goto_step2.set(value=False)
        self.enable_goto_step3.set(value=False)

        for i in self.topbar_buttons[1:]:
            i.configure(state=ct.DISABLED)

        self.GotoStep(0)
        pass

    def GetProjectPath(self):
        prevPath = self.projectPath
        self.projectPath = filedialog.askdirectory(title='프로젝트 경로 세팅', initialdir=self.projectPath)

        valid = False
        if('Assets' in self.projectPath.split('/')):
            valid = True
            self.projectPath = '/'.join(self.projectPath.split('/')[0:self.projectPath.split('/').index('Assets')+1])

        elif self.projectPath != '':
            folders = os.listdir(self.projectPath)
            if ('Assets' in folders):
                valid = True
                self.projectPath = self.projectPath + '/Assets'
        else:
            self.projectPath = prevPath
            valid = False
        self.button_step1_projectPath_pathText.configure(text=self.projectPath)
        self.valid_projectPath.set(valid)

    def GetMaterials(self):
        fileNames = filedialog.askopenfilenames(title='Material Append', filetypes=(('Material (.mat)', "*.mat"),))
        for fileName in fileNames:
            if(fileName != None):
                with open(fileName, 'r') as file:
                    datas = file.readlines()
                    filterData = []
                    for data in datas:
                        if(not('---' in data) and not('%YAML' in data) and not('%TAG' in data)):
                            filterData.append(data)
                    text = '\n'.join(filterData)
                    yamlData = yaml.load(text, Loader=yaml.Loader)
                    propertyData = yamlData['Material']['m_SavedProperties']

                    #print(yamlData['Material']['m_SavedProperties']['m_TexEnvs'])  #

                    shaderGUID = yamlData['Material']['m_Shader']['guid']

                    if(self.shaderGUIDToMaterialTable.get(shaderGUID) == None):
                        index = len(self.scrollable_shader_list)
                        self.shaderGUIDToMaterialTable[shaderGUID] = {'ct':{'parent':None,'childs':[]}, 'data':[],'path':[], 'guid':shaderGUID, 'index':index}
                        radio_button_2 = ct.CTkRadioButton(master=self.scrollable_shader,
                                                           text="Select",
                                                           variable=self.select_MaterialGroupIndex,
                                                           value=index
                                                           )
                        radio_button_2.grid(row=0, column=index, pady=(5, 5), padx=(5, 5), sticky="ew")

                        scrollable_material = ct.CTkScrollableFrame(self.scrollable_shader,
                                                                 label_text=shaderGUID)
                        scrollable_material.grid(row=1, column=index, padx=(5, 5), pady=(5, 5), sticky="ns")  # ew
                        scrollable_material.grid_columnconfigure(0, weight=1)

                        self.scrollable_shader_list.append(scrollable_material)
                        self.shaderGUIDToMaterialTable[shaderGUID]['ct']['parent'] = scrollable_material
                    nowName = yamlData['Material']['m_Name']
                    materialFind = False
                    for i in self.shaderGUIDToMaterialTable[shaderGUID]['data']:
                        if i['Material']['m_Name'] == nowName:
                            materialFind = True
                            break
                    if(not materialFind):
                        label = ct.CTkLabel(self.shaderGUIDToMaterialTable[shaderGUID]['ct']['parent'], text=yamlData['Material']['m_Name'])
                        label.grid(row=len(self.shaderGUIDToMaterialTable[shaderGUID]['ct']['childs']),column=0,padx=(5,5), pady=(5,5))
                        self.shaderGUIDToMaterialTable[shaderGUID]['ct']['childs'].append(label)
                        self.shaderGUIDToMaterialTable[shaderGUID]['data'].append(yamlData)
                        self.shaderGUIDToMaterialTable[shaderGUID]['path'].append(fileName)

    def GotoStep(self, index):
        for i in range(len(self.step_root_frame)):
            if i == index:
                self.step_root_frame[i].grid(row=1, column=1, sticky="nsew", padx=(10, 10), pady=(10, 10))
                if (i == 0):
                    self.SetStep0Data()
                if (i == 1):
                    self.SetStep1Data()
                if (i == 2):
                    self.SetStep2Data()
                if (i == 3):
                    self.SetStep3Data()
            else:
                self.step_root_frame[i].grid_forget()
            self.topbar_buttons[i].configure(fg_color=("gray75", "gray25") if i == index else "transparent")
        pass

    def ScanData(self, rootPath):
        guidTable = {}
        allPathData = os.walk(rootPath)

        if allPathData:
            for i in allPathData:
                nowPath = i[0]
                folderNameList = i[1]
                fileNameList = i[2]
                for fileName in fileNameList:
                    extensionName = fileName.split('.')[-1]
                    if (extensionName == 'meta'):
                        fullPath = f'{nowPath}/{fileName}'
                        fullPathNonExt = f'{nowPath}/{extensionName}'

                        with open(f'{nowPath}/{fileName}', 'r') as file:
                            yamlData = yaml.load(file, Loader=yaml.FullLoader)
                            # 파일 추출
                            if yamlData.get('TextureImporter') != None:
                                guidTable[yamlData['guid']] = fullPath
        if (not guidTable):
            logging.warning('ScanData 잘못된 경로')
        logging.debug(guidTable)

        return guidTable

    def AppendCommend(self, command):
        commandLabel = ct.CTkLabel(master=self.sidebar_CommandScroll, text=command.name, width=70,
                                            font=ct.CTkFont(size=14), anchor='center')
        commandLabel.grid(row=len(self.sidebar_CommandLabel), column=0, padx=(5, 5), pady=(2, 2), sticky="ew")
        self.sidebar_CommandLabel.append(commandLabel)
        self.sidebar_CommandList.append(command)

    def LastUnDoCommand(self):
        if len(self.sidebar_CommandList) > 0:
            self.sidebar_CommandList[-1].UnDo()
            self.remove_tk(self.sidebar_CommandLabel[-1])
            self.sidebar_CommandLabel.remove(self.sidebar_CommandLabel[-1])
            self.sidebar_CommandList.remove(self.sidebar_CommandList[-1])

    def Quit(self):
            Quit()

    def open_input_dialog_event(self):
        dialog = ct.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        ct.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ct.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")

    def remove_tk(self, widget : ct.CTkLabel):

        for child in widget.winfo_children():
            self.remove_tk(child)

        widget.grid_forget()
        widget.pack_forget()
        widget.place_forget()
        widget.destroy()

        # 하위 객체들 제거

def QuitEventExecute():
    for event in GlobalSetting.quitEventList:
        event()

def onClose():
    logging.debug("OnClose 호출")
    QuitEventExecute()
    GlobalSetting.windowQuit = True
    GlobalSetting.root.quit()
    sys.exit()

def Quit():
    logging.debug("Quit 호출")
    onClose()


class Command_MaterialConvert(command.CommandBox):
    def __init__(self, paths, afterDatas):
        self.name = 'MaterialConvert'
        self.prevDatas = []
        self.afterDatas = afterDatas
        self.paths = paths
        self.error = True

    def Do(self):
        for index, path in enumerate(self.paths):
            if os.path.exists(path):
                with open(path, 'r') as fileData:
                    self.prevDatas.append("".join(fileData.readlines()))
                with open(path, 'w') as fileData:
                    fileData.write(self.afterDatas[index])
            else:
                self.error = False
        pass
    def UnDo(self):
        for index, path in enumerate(self.paths):
            if self.prevDatas != [] and os.path.exists(path):
                with open(path, 'w') as fileData:
                    fileData.write(self.prevDatas[index])
            else:
                self.error = False
        pass