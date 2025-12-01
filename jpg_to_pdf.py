from fpdf import FPDF
from PIL import Image, UnidentifiedImageError
import os
from natsort import natsorted

pdf = FPDF()
# --------------- USER INPUT -------------------- #

folder = r"/home/span-blr-lt167/Documents/"   # Folder containing all the images.
name = "output.pdf"                          # Name of the output PDF file.

# Function to convert webp to jpg
def webp_to_jpg(in_folder):
    imlist = []
    for dirpath, dirnames, filenames in os.walk(in_folder):
        for filename in [f for f in filenames if f.endswith(".webp")]:
            full_path = os.path.join(dirpath, filename)
            imlist.append(full_path)

    if not imlist:
        print("No webp images in folder")
        return
    else:
        imlist.sort()                                               # Sort the images by name
    
        for i in range(0, len(imlist)):
            im = Image.open(imlist[i]).convert("RGB")
            fname, extension = os.path.splitext(imlist[i])
            extension = ".jpg"
            im.save(fname + extension, 'JPEG', quality=90)


def add_images_to_list(in_folder):
# ------------- ADD ALL THE IMAGES IN A LIST ------------- #
    imagelist = []  # Contains the list of all images to be converted to PDF.
    for dirpath, dirnames, filenames in os.walk(in_folder):
        for filename in [f for f in filenames if f.endswith(".jpg")]:
            full_path = os.path.join(dirpath, filename)
            imagelist.append(full_path)

    imsorted = natsorted(imagelist)                      # Sort the images by name.
    for i in range(0, len(imsorted)):
        print(imsorted[i])

    print("\nFound " + str(len(imsorted)) + " image files. Converting to PDF....\n")
    return imsorted

if __name__ == "__main__":
    webp_to_jpg(folder)
    # -------------- CONVERT TO PDF ------------ #
    for image in add_images_to_list(folder):
        pdf.add_page()
        pdf.image(image, 0, 0, 210, 297)                 # 210 and 297 are the dimensions of an A4 size sheet.

    out_file = os.path.join(folder, name)
    pdf.output(out_file)                                 # Save the PDF.

    print("PDF generated successfully!")