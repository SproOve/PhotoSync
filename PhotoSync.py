import os, json, shutil, time

json_path = os.path.join(os.getcwd()
, 'config.json')

with open(json_path, 'r') as f:
    config_dict = json.load(f)

#path
mobileCamPath = config_dict.__getitem__('mobilecamPath')
messengerPath = config_dict.__getitem__('messengerPath')
cam1Path = config_dict.__getitem__('cam1Path')
cam2Path = config_dict.__getitem__('cam2Path')
destPath = config_dict.__getitem__('destPath')

if os.path.exists(destPath) == False:
    os.mkdir(destPath)


#Standard Texts
txtRemoved = " wurde gelöscht"
txtUntagged = " wurde ungetagged"
txtSkipUndone = " wird übersprungen - Es sind noch nicht gelöschte Archive vorhanden"

def getQuartal(month):
    month = int(month)
    if  0 < month <= 3:
        quartal = 'Q1'
    elif 3 < month <= 6:
        quartal = 'Q2'
    elif 6 < month <= 9:
        quartal = 'Q3'
    elif 9 < month <= 12:
        quartal = 'Q4'
    return quartal


def workFolder(path, operation, messenger):
    for folders, subfolders, filenames in os.walk(path):
        for file in filenames:
            filepath = folders + '\\' + file
            changetime = time.gmtime(os.path.getctime(filepath))
            doSomething = checkFileFormat(filepath)
            if doSomething == True:
                if messenger == True:
                    destinationPath = destPath + '\\' + str(changetime.tm_year) + '-messenger'
                    # print(filepath, destinationPath)
                else:
                    quartal = getQuartal(changetime.tm_mon)
                    destinationPath = destPath + '\\' + str(changetime.tm_year) + '-' + quartal
                    # print(filepath, quartal, destinationPath)
                if os.path.exists(destinationPath) == False:
                    os.mkdir(destinationPath)
                if operation == 'copy':
                    print(filepath + ' wird kopiert')
                    shutil.copy2(filepath, destinationPath)
                elif operation == 'move':
                    print(filepath + ' wird verschoben')
                    shutil.move(filepath, destinationPath)
            else:
                print(filepath + ' ist keine Mediendatei')

def checkFileFormat(file):
    validFileFormats = config_dict.__getitem__('validFileFormats')
    returnVal = False
    for fileFormat in validFileFormats:
        if file.lower().endswith(fileFormat):
            returnVal = True
    return returnVal

def mobileCamRun():
    
    mode =  config_dict.__getitem__('mobilecamOp')
    messenger = False
    if os.path.exists(mobileCamPath) == True:
        workFolder(mobileCamPath, mode, messenger)
    else:
        print('Pfad ' + mobileCamPath + ' nicht vorhanden') 
    
def messengerRun():
    mode = config_dict.__getitem__('messengerOp')
    messenger = True
    if os.path.exists(messengerPath) == True:
        workFolder(messengerPath, mode, messenger)
    else:
        print('Pfad ' + messengerPath + ' nicht vorhanden')

def cam1Run():
    mode = config_dict.__getitem__('cam1Op')
    messenger = False
    if os.path.exists(cam1Path) == True:
        workFolder(cam1Path, mode, messenger)
    else:
        print('Pfad ' + cam1Path + ' nicht vorhanden')

def cam2Run():
    mode = config_dict.__getitem__('cam2Op')
    messenger = False
    if os.path.exists(cam2Path) == True:
        workFolder(cam2Path, mode, messenger)
    else:
        print('Pfad ' + cam2Path + ' nicht vorhanden')        

if cam1Path == cam2Path:
    cam1Run()
else:
    cam1Run()
    cam2Run()
mobileCamRun()
messengerRun()
print('\n Fertig! \n')
enterPrompt = input("Zum Beenden Enter-Taste drücken...")


