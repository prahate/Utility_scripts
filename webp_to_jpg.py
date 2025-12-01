from PIL import Image, UnidentifiedImageError
import os
from natsort import natsorted

# --------------- USER INPUT -------------------- #

folder = r"/home/span-blr-lt167/Documents/"   # Folder containing all the images.
# ------------- ADD ALL THE IMAGES IN A LIST ------------- #

def webp_to_jpg(in_folder):
    imagelist = []
    for dirpath, dirnames, filenames in os.walk(in_folder):
        for filename in [f for f in filenames if f.endswith(".webp")]:
            full_path = os.path.join(dirpath, filename)
            imagelist.append(full_path)
            
    if not imagelist:
        print("No images with webp extension found")
    else:
        imsorted = natsorted(imagelist)            # Sort the images by name.
        for i in range(0, len(imsorted)):
            print(imsorted[i])
    
        for i in range(0, len(imsorted)):
            im = Image.open(imsorted[i]).convert("RGB")
            fname, extension = os.path.splitext(imsorted[i])
            extension = ".jpg"
            im.save(fname + extension, 'JPEG', quality=90)

if __name__ == "__main__":
    webp_to_jpg(folder)