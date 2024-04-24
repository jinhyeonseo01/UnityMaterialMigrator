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

async def ScanData(rootPath):
    guidTable = {}
    allPathData = os.walk(rootPath)

    if allPathData:
        for i in allPathData:
            nowPath = i[0]
            folderNameList = i[1]
            fileNameList = i[2]
            for fileName in fileNameList:
                extensionName = fileName.split('.')[-1]
                if(extensionName == 'meta'):
                    fullPath = f'{nowPath}\\{fileName}'
                    fullPathNonExt = f'{nowPath}\\{extensionName}'

                    with open(f'{nowPath}\\{fileName}', 'r') as file:
                        yamlData = yaml.load(file, Loader=yaml.FullLoader)
                        #파일 추출
                        if yamlData.get('TextureImporter') != None:
                            guidTable[yamlData['guid']] = fullPathNonExt
    if(not guidTable):
        logging.warning('ScanData 잘못된 경로')
    logging.debug(guidTable)




#scanData(r'D:\Files\_Projects\2023_2 Version Stu')

async def main():
    task = ScanData(r'D:\Files\_Projects\2023_2 Version Study\Assets\Models\Avatar_Female_Size01_Aokaku')
    print(f'작업을 기다리는 중')
    data = await task

    #Quit()

    while(not GlobalSetting.windowQuit):
        GlobalSetting.root.update()
        await asyncio.sleep(0.032)
    GlobalSetting.root.quit()




if sys.platform == "win32":
    # Windows에서만 필요한 설정
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

GlobalSetting.root = App()

GlobalSetting.windowQuit = False

GlobalSetting.root.update()

asyncio.run(main())