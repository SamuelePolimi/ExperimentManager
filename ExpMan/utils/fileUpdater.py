import csv

def csvToStr(line):
    ret = ""
    for l in line[0:-1]:
        ret += l + ","
    ret+= line[-1] + "\n"
    return ret
    
def update(path, line_number, number_param, param):
    
    fileR_ = open(path,"rb")
    csvFile = csv.reader(fileR_)
    
    line = []
    while True:
        try:
            row = csvFile.next()
        except:
            break
        line.append(row)
    
    fileR_.close()
    
    fileW_ = open(path, "w")
    for i in range(0,len(line)):
        if i == line_number:
            line[i][number_param] = param
        fileW_.write(csvToStr(line[i]))  
    
    fileW_.close()

def updateLine(path, line_number, value):
    
    fileR_ = open(path,"r")
    
    line = fileR_.readlines()
    
    fileR_.close()
    
    fileW_ = open(path, "w")
    for i in range(0,len(line)):
        if i == int(line_number):
            line[i] = value + "\n"
        fileW_.write(line[i])  
    
    fileW_.close()