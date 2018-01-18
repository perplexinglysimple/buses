import json
import re
import fileinput
from os import listdir, isfile, join

onlyfiles = [f for f in listdir(mypath + "\\data\\") if isfile(join(mypath + "\\data\\", f))]

split_on = ']}]'
error_message1 = '{"error":true,"message":"Empty response from service.","data":"{\\"Main\\":\\"[]\\"}"}'
error_message2 = '[]'

for file in onlyfiles:
#cleaning the data of errors
#error -> {"error":true,"message":"Empty response from service.","data":"{\"Main\":\"[]\"}"}
#also garbage [][] gets placed
data = ''
with open(file, 'r') as original:
	data = original.read()
with open(file, 'w') as modified:
	#dta_split = data.split(split_on)
	#errors_removed = []
	#for number in range(len(data_split)):
	#	data_split[number]
		
	clean_data = data.replace(error_message1, '').replace(error_message2, '')
	#for item in errors_removed:
	#	clean_data = clean_data + item
	#begin of file add [ and end of file ]
	modified = modified.write('[' + clean_data + ']')

#"}][{" -> "}],[{"
with fileinput.FileInput(file, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace("}][{", "}],[{"), end='')

a = open("text_bus.txt")
print(json.load(a))