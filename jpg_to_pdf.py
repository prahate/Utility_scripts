from fpdf import FPDF
from PIL import Image, UnidentifiedImageError
import os
import argparse
from natsort import natsorted

pdf = FPDF()
# --------------- USER INPUT -------------------- #

folder = r"/home/span-blr-lt167/Documents/"   # Folder containing all the images.
name = "output.pdf"                          # Name of the output PDF file.

# Function to convert webp to jpg
def webp_to_jpg(in_folder):
    imlist = []

    if os.path.isfile(in_folder):
        if in_folder.endswith(".webp"):
            imlist.append(in_folder)
            return
        else:
            print("Not a webp file")
            return

    elif os.path.isdir(in_folder):
        try:
            for dirpath, dirnames, filenames in os.walk(in_folder):
                for filename in [f for f in filenames if f.endswith(".webp")]:
                    full_path = os.path.join(dirpath, filename)
                    imlist.append(full_path)
        except FileNotFoundError:
            print("Folder does not exists, please specify correct folder")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        if not imlist:
            print("No webp images in folder")
            return
        else:
            imlist.sort()                                               # Sort the images by name
    
            for i in range(0, len(imlist)):
                im = Image.open(imlist[i]).convert("RGB")
                fname, extension = os.path.splitext(imlist[i])
                extension = ".jpg"
                im.save(fname + extension, 'JPEG', quality=60, optimize=True)


def add_images_to_list(in_folder):
    imagelist = []  # Contains the list of all images to be converted to PDF.
    
    if os.path.isfile(in_folder):
        if in_folder.endswith(".jpg"):
            imagelist.append(in_folder)
            return
        else:
            print("Please provide valid jpg file")
            return None

    elif os.path.isdir(in_folder):
        # ------------- ADD ALL THE IMAGES IN A LIST ------------- #
        try:
            for dirpath, dirnames, filenames in os.walk(in_folder):
                for filename in [f for f in filenames if f.endswith(".jpg")]:
                    full_path = os.path.join(dirpath, filename)
                    imagelist.append(full_path)
        except FileNotFoundError:
            print("Folder does not exists, please specify correct folder")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        imsorted = natsorted(imagelist)                      # Sort the images by name.
        for i in range(0, len(imsorted)):
            print(imsorted[i])

        print("\nFound " + str(len(imsorted)) + " image files. Converting to PDF....\n")
        return imsorted

if __name__ == "__main__":
    # 1. Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Script to convert jpg to pdf.")
    
    # 2. Add arguments
    parser.add_argument("-f", "--file", required=True, help="File/Folder containing jpg files")
    parser.add_argument("-o", "--output", required=True, help="Output pdf file name")
    
    # 3. Parse the arguments
    args = parser.parse_args()
       
    if args.file:
        in_file = args.file
    else:
        in_file = None

    if args.output:
        out_pdf = args.output + ".pdf"
    else:
        out_pdf = "output.pdf"
            
    if in_file:
        try:
            webp_to_jpg(in_file)
            # -------------- CONVERT TO PDF ------------ #
            for image in add_images_to_list(in_file):
                pdf.add_page()
                pdf.image(image, 0, 0, 210, 297)                 # 210 and 297 are the dimensions of an A4 size sheet.

            out_file = os.path.join(in_file, out_pdf)
            pdf.output(out_file)                                 # Save the PDF.
        except FileNotFoundError:
            print("No such file or directory")
        except TypeError:
            print("No such file or directory")
        except Exception as e:
            print(f"Exception occured {e}")
        else:
            print("PDF generated successfully!")
    
