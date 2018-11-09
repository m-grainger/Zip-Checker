import os
import subprocess as sub
import sys
import time

def user_inputs():
# user input variables
	user_count = input("Please enter the number of files that you are expecting to be scanned: ") 
	infolder = input("Please set the drive path (e.g. M:): " )
	password = input("Please enter the password: ")
	password = f'"{password}"'
	return user_count, infolder, password

choices = user_inputs() # <---- Code starts running here!


# user verifies everything that is written above is correct 
print(f"\n\nNumber of expected files to be scanned: {choices[0]}")
print(f"Drive that is going to be scanned: {choices[1]}")
print(f"Expected password for the files on the drive: {choices[2][1:-1]}\n")

# making sure that the above information is correct
g2g = input("Does this look correct?  [Y / N]: \n")
if g2g == "Y" or g2g =="y":
	pass
else:
	print("\nPlease restart the application\n")
	print("Closing...")
	time.sleep(2.5)
	sys.exit()

# making sure that we only count files that end in ".zip" on the HDD
zip_check = ".zip"
hd_file_list = []
for path, subdirs, files in os.walk(choices[1]):
    for name in files:
    	if zip_check in name:
        	hd_file_list.append(os.path.join(path, name)) # only inserts into list if ".zip" is in the file name

     
# creates a text file that replicates ZipTest.bat 
with open("ZipTest.txt", "a") as f:
	f.write(f"SET logfolder=%CD%\\logs\\") 
	f.write(f"\nSET taillines=5")
	f.write(f"\n") # just adding a blank line here
	f.write(f"\nSET rundir=%CD%")
	f.write(f"\nmd %logfolder%")
	f.write(f'\nfor /R {choices[1]} %%g in (*.zip) DO %rundir%\\7za.exe t -r -p{choices[2]} "%%~fg" 1> "%logfolder%\\%%~nxg.log.txt" 2>&1')
	f.write(f'\nfor /R %logfolder% %%g in (*.log.txt) DO (')
	f.write(f'\n{"    "}echo -- Start %%~ng -- >> %logfolder%\\Results.txt')
	f.write(f'\n{"    "}%rundir%\\tail.exe -n %taillines% "%%~fg" 1>> %logfolder%\\Results.txt 2>&1')
	f.write(f'\n{"    "}echo -- End %%~ng -- >> %logfolder%\\Results.txt')
	f.write(f'\n{"    "}echo. >> %logfolder%\\Results.txt')
	f.write(f'\n{"    "})')

os.rename(f"{os.getcwd()}\\ZipTest.txt","ZipTest.bat") # renames the ZipTest.txt file to ZipTest.bat

print(f"Opening and running ZipTest.bat...\n")
time.sleep(2.5)

# subprocess function call to wait for ziptest.bat to finish
bat_path = f"{os.getcwd()}\\ZipTest.bat"
p = sub.Popen(bat_path, stdout=sub.PIPE, shell=True)
(output, err) = p.communicate()
p_status = p.wait()

print("File scan has completed!\n")
print("Scanning results.txt...\n")                                                                                                             

# creates a list of text files generated from ZipTest.bat
text_list = []
for path, subdirs, files in os.walk(os.getcwd()+"\\logs"):
    for name in files:
        s = os.path.join(path, name)
        text_list.append(os.path.join(path, name)) 

# counts the number of times that "Everything is Ok" is printed in "Results.txt"
results_count = open(f"{os.getcwd()}\\logs\\results.txt", 'r').read().count("Everything is Ok")            

# reads ALL text files (except for "Results.txt") to scan for password errors                       																						 
print("Scanning for text files that contain an error...\n")
time.sleep(2.5)
error_list = []
for x in text_list:
	with open(x, 'r', encoding= "utf-8", errors= "ignore") as searchfile:
		for line in searchfile:
			if 'Wrong password?' in line:				
				error_list.append(x)

# removes "Results.txt" from the error list
check = f"{os.getcwd()}\\logs\\Results.txt"
err_final = [x for x in error_list if check not in x]

for x in set(err_final): print(f"Error found in: ...{x[-30:]}")

# creates a  text document with final counts + list of errored zip files
with open("final_counts.txt","a") as g:                                                                      
	g.write(f"Total number of files that you entered: {choices[0]}")                                         
	g.write(f"\nTotal Count of files that successfully scanned with no errors: {results_count}")               
	g.write("\n")
	g.write(f"Total Count of zip files located in the drive {choices[1]} and it's subdirectories: {len(hd_file_list)}\n\n") # <-- actual file count 
	for x in set(err_final): g.write(f"Error detected: {x}\n")


print("\n\nScanning and Logging Complete.\nA file named 'final_counts.txt' has been added to your current working directory")
time.sleep(5)
sys.exit()
