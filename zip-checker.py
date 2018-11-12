import os
import subprocess as sub
import sys
import time

def user_inputs():
# user input variables
	user_count = input("Please enter the number of zip files to be scanned:  ") 
	infolder = input("Please set the drive path (e.g. M:): " )
	password = input("Please enter the password: ")
	password = f'"{password}"'
	return user_count, infolder, password

choices = user_inputs() # <---- Code starts running here!

# user verifies everything that is written above is correct 
print(f"\n\nNumber of expected files to be scanned: {choices[0]}")
print(f"Drive that is going to be scanned: {choices[1]}")
pass_choice = choices[2]
print(f"Expected password for the files on the drive: {pass_choice[1:-1]}\n")

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
	f.write(f"\nSET countfolder=%CD%\\counts\\")  
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
	f.write(f"\nmd %countfolder%") 
	f.write(f'\nfor /R {choices[1]} %%g in (*.zip) DO %rundir%\\7za.exe l -r -p{choices[2]} "%%~fg" 1> "%countfolder%\\%%~nxg.log.txt" 2>&1')

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

for x in set(err_final): print(f"Error found in: ...{x[-50:]}")

# logic that compares a list of zip files on the drive to zip log files
def comparison_check():
	zip_check = ".zip"
	hd_file_list = []
	for path, subdirs, files in os.walk(choices[1]):
	    for name in files:
	    	if zip_check in name:
	        	hd_file_list.append(os.path.join(name)) 

	text_check = ".txt"
	text_file_list = []
	text_file_list_full = []
	for path, subdirs, files in os.walk(f"{os.getcwd()}\\logs\\"):
	    for name in files:
	    	if text_check in name and "Results.txt" not in name:
	        	text_file_list.append(os.path.join(name[:-8]))
	        	text_file_list_full.append(os.path.join(name,path)) 

	if hd_file_list.sort() == text_file_list.sort():
		comp_bool = True
		return comp_bool
	else:
		comp_bool = False
		return comp_bool

comparison_bool = comparison_check()

# generates list of zipped files on the chosen drive path.  Outputs to "Manifest.txt"
def manifest_gen():
	zip_check = ".zip"
	zip_file_list_path = []
	for path, subdirs, files in os.walk(choices[1]):
	    for name in files:
	    	if zip_check in name:
	        	zip_file_list_path.append(os.path.join(path,name)) 

	return zip_file_list_path
zflp = manifest_gen()

# grabs totals of files contained in a zip file.
counts_list = []
for path, subdirs, files in os.walk(os.getcwd()+"\\counts"):
    for name in files:
        s = os.path.join(path, name)
        counts_list.append(os.path.join(path, name))

print("\ngetting zip totals...")
time.sleep(2.5)
counts_totals = 0
for x in counts_list:
	with open(x, 'r', encoding= "utf-8", errors= "ignore") as searchfile:
		for line in searchfile:
			if '.xml' in line:			
				counts_totals += 1

# creates a  text document with final counts + list of errored zip files
with open("final_counts.txt","a") as g:                                                                      
	g.write(f"\n({choices[0]}) | Expected Number of zips")
	g.write(f"\n({len(hd_file_list)}) | Count of zip files on {choices[1]} and it's subdirectories") # <-- actual file count                                         
	g.write(f"\n({results_count}) | Total Count of Zips that successfully scanned with no password errors")               
	g.write(f"\n({counts_totals}) | XML count from within zips\n")
	g.write(f"\n({len(set(err_final))}) | Number of zips with password errors\n") 
	for x in set(err_final): g.write(f"\nError detected: {x}")
	g.write(f"\n\nAll files successfully copied and scanned = {comparison_bool}")

with open("Manifest.txt","a") as h:
	for x in zflp: h.write(f"\n{x}")    #<-- fix this!	

print("\nA file named 'final_counts.txt' has been added to your current working directory")
print("\nA file named 'Manifest.txt' has added to your current working directory")
print("\nScan complete.")
time.sleep(5)
sys.exit()

# 	#add logic that shows if everything matches or not, and writes it to the text file
