# import os
# path="C:\Users\OAO_NY_03-24-2016\Desktop\work\\api\\reports\\"
# print path
# filenames = next(os.walk(path))[2]
import glob
import csv

def networkcode(file):
	return file[50:-11]

files=[]
files=glob.glob("/users/OAO_NY_03-24-2016/Desktop/work/api/reports/*.csv")

for file in files:
	ifile  = open(file, "rb")
	# print networkcode(file)
	reader = csv.reader(ifile)
	ofile  = open('reachreport.csv', "ab")
	writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

	for row in reader:
	    row.append(networkcode(file))
	    writer.writerow(row)	    

	ifile.close()
	ofile.close()