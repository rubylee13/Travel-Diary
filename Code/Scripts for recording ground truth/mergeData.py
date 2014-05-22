import csv

# Procedure that takes as input a string deonting the date, difference between local time zone and UTC time, 
# and the GPS file path name. Output is a list of lists containing GPS data for that day.

def getGPSData(gpsFilePath):

    gpsData = []
    with open(gpsFilePath, 'rb') as csvfile:
        rows = csv.reader(csvfile, delimiter = '\t')
        gpsData = [row for row in rows]
    return gpsData


# Procedure that takes as input strings deonting the tester name, test phone number, date, difference between
# local time zone and UTC time, and the file path name. Output is a list of lists containing ground truth data
# for that tester, phone and day.

def getGroundData(groundFilePath):

    groundData = []
    with open(groundFilePath, 'rU') as csvfile:
        rows = csv.reader(csvfile, dialect=csv.excel_tab, delimiter = ',')
        header = rows.next()
        groundData = [row for row in rows]
    return groundData


# Procedure that takes as input the list of lists containing GPS data and the ground truth, and combines them
# into a single list of lists.

def mergeData(gpsData, groundData):

    i, lastEvent = 0, groundData[-1][5:]
    while groundData:
        while float(gpsData[i][1]) != int(groundData[0][3]):
            for element in groundData[0][5:]:
                gpsData[i].append(element)
            i += 1
        groundData = groundData[1:]
    for element in lastEvent:
        gpsData[i].append(element)
    return gpsData


# Method that combines the GPS data with the ground truth in a tab-delimited text file that can
# subsequently be used to train inference algorithms. The GPS data file must be saved manually
# as a tab-delimited text file on the local hard drive. The ODK file containing ground truth must
# be exported manually as a csv and saved to the local hard drive as well.

def mergeDataFiles(testers, filePath, gpsFilePath, groundFilePath, testerName, date):

    for tester in testers:
        if tester['name'] == testerName:
            fileName = tester['ph'] + '_' + testerName + '_' + date
    
    gpsFile = gpsFilePath + fileName + '.txt'
    groundFile = groundFilePath + fileName + '.csv'
    
    # Directory where the final data file will be saved, no need to change this
    mergedFile = filePath + 'Travel-Diary/Data/Google Play API/' + fileName + '.txt'
    
    gpsData = getGPSData(gpsFile)
    groundData = getGroundData(groundFile)
    data = mergeData(gpsData, groundData)
    
    with open(mergedFile, 'wb') as csvfile:
        fileWriter = csv.writer(csvfile, delimiter = '\t')
        for row in data:
            fileWriter.writerow(row)
 
       
# Entry point to script

if __name__ == "__main__":

    # Personal details, change as appropriate    
    testers = [{'name': 'Andrew', 'ph': '5107259365'}, 
               {'name': 'Caroline', 'ph': '5107250774'},
               {'name': 'Rory', 'ph': '5107250619'},
               {'name': 'Sreeta', 'ph': '5107250786'},
               {'name': 'Vij', 'ph': '5107250740'},
               {'name': 'Ziheng', 'ph': '5107250744'}]
    
    # Base directory where you clone the repository, change as appropriate
    filePath = '/Users/vij/Work/Current Research/'
    
    # Directory where you saved the file with GPS traces, change as appropriate
    gpsFilePath = filePath + 'Travel-Diary/Data/Raw Data/' 
    
    # Directory where you've saved the corrected ground truth, change as appropriate
    groundFilePath = filePath + 'Travel-Diary/Data/Corrected Truth/' 

    # Details of data to be merged    
    testerName = 'Vij'        # Should be the same as that listed in testers
    date = '04302014'         # MMDDYYYY format of day for which you wish to merge data
    
    # Call to merge raw data with ground truth
    mergeDataFiles(testers, filePath, gpsFilePath, groundFilePath, testerName, date)
