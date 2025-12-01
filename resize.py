# Source - https://stackoverflow.com/a
# Posted by Andrei M., modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-25, License - CC BY-SA 4.0

from PIL import Image
import os

imagelist=[]

path = r"/home/span-62/Documents/Claim/"
resize_ratio = 1.2  # where 0.5 is half size, 2 is double size

def resize_aspect_fit():
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in [f for f in filenames if f.endswith(".jpg")]:
            full_path = os.path.join(dirpath, filename)
            imagelist.append(full_path)
    
    imagelist.sort() 
            
    for i in range(0, len(imagelist)):
        image = Image.open(imagelist[i])
        fname, extension = os.path.splitext(imagelist[i])

        new_image_height = int(image.size[0] / (1/resize_ratio))
        new_image_length = int(image.size[1] / (1/resize_ratio))

        image = image.resize((new_image_height, new_image_length), Image.LANCZOS)
        if resize_ratio > 1:
            image.save(fname + "_large" + extension, 'JPEG', quality=90)
        else:
            image.save(fname + "_small" + extension, 'JPEG', quality=90)

if __name__ == "__main__":
    resize_aspect_fit()

