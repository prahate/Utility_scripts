# Source - https://stackoverflow.com/a
# Posted by Andrei M., modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-25, License - CC BY-SA 4.0

from PIL import Image
import os

imagelist=[]

path = r"/home/span-blr-lt167/Documents/"
resize_ratio = 0.7  # where 0.5 is half size, 2 is double size

def resize_image(in_path, resz_ratio):
    if os.path.isfile(in_path):
        if in_path.endswith(".jpg") or in_path.endswith(".png"):
            imagelist.append(in_path)
        else:
            print("Not a jpg/png file")
            return
    elif os.path.isdir(in_path):
        for dirpath, dirnames, filenames in os.walk(in_path):
            for filename in [f for f in filenames if f.endswith(".jpg") or f.endswith(".png")]:
                full_path = os.path.join(dirpath, filename)
                imagelist.append(full_path)
    
    imagelist.sort() 
            
    for i in range(0, len(imagelist)):
        image = Image.open(imagelist[i])
        fname, extension = os.path.splitext(imagelist[i])

        new_image_height = int(image.size[0] / (1/resz_ratio))
        new_image_length = int(image.size[1] / (1/resz_ratio))

        image = image.resize((new_image_height, new_image_length), Image.LANCZOS)
        if resize_ratio > 1:
            image.save(fname + "_large" + extension, 'JPEG', quality=90)
        else:
            image.save(fname + "_small" + extension, 'JPEG', quality=90)

if __name__ == "__main__":
    resize_image(path, resize_ratio)

