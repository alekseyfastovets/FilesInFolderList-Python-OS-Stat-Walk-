#__________________________________________________________________
#функция обработки метаданных файла (зависимости math, time, os)

import props
import os
import math
import time

def metaData(path:str) -> dict:
    meta = os.stat(path)
    fSize = meta.st_size # size of file, in bytes
    mTime = time.localtime(meta.st_mtime) # time of most recent content modification
    aTime = time.localtime(meta.st_atime) # time of most recent access
    cTime = time.localtime(meta.st_ctime) # time of most recent metadata change
    
    def convert_size(size_bytes):
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])
    
    def convert_time(timeObj):
        mTimeStr = ''
        for i in range(0,6):
            if len(str(mTime[i])) == 1 and i != 3:
                mTimeStr =mTimeStr + '0'+str(mTime[i])
            else:
                mTimeStr =mTimeStr + str(mTime[i])
            if i <= 1:
                mTimeStr =mTimeStr + '.'
            elif i == 2:
                mTimeStr =mTimeStr + ' '
            elif i > 2 and i <= 4:
                mTimeStr =mTimeStr + ':'
            else:
                pass
        return mTimeStr
    
    return {'accessTime' : convert_time(aTime),
            'modificationTime' : convert_time(mTime),
            'changeTime' : convert_time(cTime),
            'fileSize' : convert_size(fSize)}
        
    
    
#Конец фукнкции обработки метаданных
#__________________________________________________________________



#__________________________________________________________________
#функция обработки файлов в папке (зависимости os)

def filesArray(path:str, splitSteps = 3) -> list:
    filesData = [] # Массив который наполняется обработанными данными
    files = os.walk(path)
    
    for folder in files:
        if folder[2] != []:
            for file in folder[2]:
                data = [] # Массив который наполняется обработанными данными
                countType = 0
                typesInFile = []
                for types in props.props.get('reportTypes'):
                    if types in str(file).lower():
                        countType += 1
                        typesInFile.append(types)
                    else:
                        pass
                data.append('-'+str(countType)+'-')
                filePath = str(folder[0]).replace(path,'').replace('\\','|')
                if len(filePath) != 0:
                    data.append(filePath) # Добавляем полный путь к файлу
                else:
                    data.append('-')
                    
                splittedFilePath = str(filePath).split('|')
                
                i = 1
                while True:
                    
                    if len(splittedFilePath) >= (i+1):
                        data.append(splittedFilePath[i])
                    else:
                        data.append('-')
                    i += 1
                    if (i+1) > (splitSteps+1):
                        break
                
                data.append(file) #добавляем название файла
                fullFilePath = str(folder[0])+'\\'+str(file) # Полный путь к файлу. Использум для функции metaData
                meta = metaData(fullFilePath)
                data.append(meta.get('modificationTime'))
                
                if len(typesInFile) == 0:
                    data.append('не удалось определить тип')
                    filesData.append(data)
                else:
                    for elem in typesInFile:
                        pre_data = data[:]
                        if elem == 'тз начало':
                            pre_data.append('остатки')
                            filesData.append(pre_data)
                        else:
                            pre_data.append(elem)
                            filesData.append(pre_data)
                    
                    
                    
                    
                        
    
    print('Это массив Локальных данных в функции:_________________________')
    for i in filesData:
        print(i)
    print('КОНЕЦ_________________________________________')
    return filesData
                                


#Конец фукнкции обработки файлов в папке
#__________________________________________________________________



if __name__ == '__main__':
    path = r'TEST.xlsx'
    data = metaData(path)
    print(data)
    
    pathData = r'testData'
    filesData = filesArray(pathData,3)
    
    for i in filesData:
        print(i)
    






    
    


        
    
        
    

    
