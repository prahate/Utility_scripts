import os, sys
from natsort import natsorted
import zipfile

ziplist = []

def unzip_files():
	if ziplist:
		for zfile in ziplist:
			fname, ext = os.path.splitext(zfile)
			try:
				with zipfile.ZipFile(zfile, mode='r') as myzip:
					myzip.extractall(fname)
			except BadZipFile:
				print(f'{zfile} is not valid zip file')
			finally:
				myzip.close()
				print(f'extracted {zfile}')
	else:
		print("No zip files to extract")
			

def create_dirs(dpath):
	if os.path.isdir(dpath):
		try:
			for dirpath, dirnames, filenames in os.walk(dpath):
				for filename in [f for f in filenames if f.endswith(".zip")]:
					full_path = os.path.join(dirpath, filename)
					ziplist.append(full_path)
			
			sortedzip = natsorted(ziplist)
			for i in range(0, len(sortedzip)):
				fname, ext = os.path.splitext(sortedzip[i])
				try:
					os.mkdir(fname)
					print(f"Created direcotry at: {fname}")
				except FileExistsError:
					print(f"Directory '{fname}' already exists")
				except OSError as e:
					print(f"Error creating directory : {e}") 
		except FileNotFoundError:
			print("Folder does not exists, please specify correct folder")
		except Exception as e:
			print(f"An unexpected error occurred: {e}")
	else:
		print("Please provide direcory")
		
if __name__ == "__main__":
	dirname = sys.argv[1]
	create_dirs(dirname)
	unzip_files()

	
