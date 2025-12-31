from fpdf import FPDF
from PIL import Image, UnidentifiedImageError
import os
import argparse
from natsort import natsorted
from resize import resize_image

pdf = FPDF()
# --------------- USER INPUT -------------------- #

folder = r"/home/span-blr-lt167/Documents/"   # Folder containing all the images.
name = "output.pdf"                          # Name of the output PDF file.
resz_ratio= 0.7

# Function to convert webp to jpg
def webp_to_jpg(in_folder):
    imlist = []

    if os.path.isfile(in_folder):
        if in_folder.endswith(".webp"):
            imlist.append(in_folder)
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
    
    imlist.sort()                       # Sort the images by name
    for i in range(0, len(imlist)):
        im = Image.open(imlist[i]).convert("RGB")
        fname, extension = os.path.splitext(imlist[i])
        extension = ".jpg"
        im.save(fname + extension, 'JPEG', quality=60, optimize=True)


def add_images_to_list(in_folder, is_resize):
    imagelist = []  # Contains the list of all images to be converted to PDF.
    
    if os.path.isfile(in_folder):
        if in_folder.endswith(".jpg"):
            imagelist.append(in_folder)
        else:
            print("Please provide valid jpg file")
            return None

    elif os.path.isdir(in_folder):
        # ------------- ADD ALL THE IMAGES IN A LIST ------------- #
        try:
            if is_resize:
                for dirpath, dirnames, filenames in os.walk(in_folder):
                    for filename in [f for f in filenames if f.endswith("_small.jpg") or f.endswith("_small.png")]:
                        full_path = os.path.join(dirpath, filename)
                        imagelist.append(full_path)
            else:
                for dirpath, dirnames, filenames in os.walk(in_folder):
                    for filename in [f for f in filenames if f.endswith(".jpg") or f.endswith(".png")]:
                        full_path = os.path.join(dirpath, filename)
                        imagelist.append(full_path)
        except FileNotFoundError:
            print("Folder does not exists, please specify correct folder")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    imsorted = natsorted(imagelist)     # Sort the images by name.
    #for i in range(0, len(imsorted)):
    #    print(imsorted[i])

    #print("\nFound " + str(len(imsorted)) + " image files. Converting to PDF....\n")
    return imsorted

if __name__ == "__main__":
    # 1. Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Script to convert jpg to pdf.")

    # 3. group arguments
    in_group = parser.add_argument_group("Input group")
    in_group.add_argument("-f", "--file", required=True, help="File/Folder containing jpg files")
    in_group.add_argument("-r", "--resize", action='store_true', required=False, help="Resize the jpg/png images")
    in_group.add_argument("-w", "--webp_to_jpg", action='store_true', required=False, help="Convert webp to jpg")
    
    out_group = parser.add_argument_group("Output group")
    out_group.add_argument("-o", "--output", required=False, help="Output file name")
    out_group.add_argument("-p", "--pdf", action='store_true', required=False, help="Create PDF of image files")
    
    # 3. Parse the arguments
    args = parser.parse_args()
    
    is_file = False
    if not args.file:
        parser.print_help()
        parser.exit(0, message="Please provide input file/folder")
    else:
        if os.path.isfile(args.file):
            is_file = True
        in_file = args.file

       
    converted = []
    resz = False

    if args.webp_to_jpg:
        webp_to_jpg(in_file)

    if args.resize:
        resize_image(in_file, resz_ratio)
        resz = True

    if args.pdf:
        if not args.output and not is_file:
            parser.print_help()
            parser.exit(0, message="Please specify output file name")
        else:
            if not is_file:
                out_pdf = args.output + ".pdf"
        try:
            # -------------- CONVERT TO PDF ------------ #
            for image in add_images_to_list(in_file, resz):
                pdf.add_page()
                pdf.image(image, 0, 0, 210, 297)                 # 210 and 297 are the dimensions of an A4 size sheet.

            if not is_file:
                out_file = os.path.join(in_file, out_pdf)
            elif is_file:
                fname, extension = os.path.splitext(in_file)
                extension = ".pdf"
                out_file = fname + extension
                out_pdf = out_file

            pdf.output(out_file)                                 # Save the PDF.
            converted.append(out_pdf)
        except FileNotFoundError:
            print("FileNotFound:No such file or directory")
        except TypeError:
            print("TypeError:No such file or directory")
        except Exception as e:
            print(f"Exception occured {e}")
        else:
            for i in range(0, len(converted)):
                print(converted[i])
            print("PDF generated successfully!")

