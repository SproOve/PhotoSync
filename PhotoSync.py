import os, shutil, send2trash, re, datetime, time

from dotenv import load_dotenv

# Create .env file path.
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# Load file from the path.
load_dotenv(dotenv_path)

#path
mobileCamPath = os.getenv('MOBILECAMPATH')
messengerPath = os.getenv('MESSENGERPATH')
cam1Path = os.getenv('CAM1PATH')
cam2Path = os.getenv('CAM2PATH')
destPath = os.getenv('DESTPATH')

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
    validFileFormats = ['jpg', 'jpeg', 'mov', 'mp4', 'png']
    returnVal = False
    for fileFormat in validFileFormats:
        if file.lower().endswith(fileFormat):
            returnVal = True
    return returnVal

def mobileCamRun():
    mode =  os.getenv('MOBILECAMOP')
    messenger = False
    if os.path.exists(mobileCamPath) == True:
        workFolder(mobileCamPath, mode, messenger)
    else:
        print('Pfad ' + mobileCamPath + ' nicht vorhanden') 
    
def messengerRun():
    mode = os.getenv('MESSENGEROP')
    messenger = True
    if os.path.exists(messengerPath) == True:
        workFolder(messengerPath, mode, messenger)
    else:
        print('Pfad ' + messengerPath + ' nicht vorhanden')

def cam1Run():
    mode = os.getenv('CAM1PATH')
    messenger = False
    if os.path.exists(cam1Path) == True:
        workFolder(cam1Path, mode, messenger)
    else:
        print('Pfad ' + cam1Path + ' nicht vorhanden')

def cam2Run():
    mode = os.getenv('CAM2PATH')
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


