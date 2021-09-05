import os


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
    return allFiles


for file in getListOfFiles('./locale'):
    with open(file, 'r') as f:
        text = f.read()
    text = text.replace('{{', '{')
    text = text.replace('}}', '}')
    text = text.replace('{temp}', '{temperature}')
    text = text.replace('{temp_max}', '{high_temperature}')
    text = text.replace('{temp_min}', '{low_temperature}')
    text = text.replace('{scale}', '{temperature_unit}')
    text = text.replace('{wind}', '{speed}')
    text = text.replace('{wind_max}', '{high_speed}')
    text = text.replace('{wind_min}', '{low_speed}')
    text = text.replace('{wind_unit}', '{speed_unit}')
    with open(file, 'w') as f:
        f.write(text)
