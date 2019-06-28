import pyvips
import Image, ImageSequence


def thumbnails(frames, width, height):
    size = width, height

    for frame in frames:
        thumbnail = frame.copy()
        thumbnail.thumbnail(size, Image.ANTIALIAS)
        yield thumbnail

def gif_resize(filename, width, height):
    ok = 0
    name = ""

    for i in filename:
        if ok:
            name = name + i

        if i == '/':  # am aflat numele imaginii in name
            ok = 1

    img = Image.open(filename)

    frames = ImageSequence.Iterator(img)
    frames = thumbnails(frames, width, height)

    path = "output photos/" + name

    out = next(frames)
    out.info = img.info
    out.save(path, save_all=True, append_images=list(frames))




def resize(filename, width, height, format):        #it keeps the scale of the image and resizes it by the smallest paramter you pass it

    ok = 0
    name = ""

    for i in filename:
        if ok:
            name = name + i

        if i == '/':
            ok = 1

    if format == "svg":
        img = pyvips.Image.svgload(filename)
    elif format == "jpg":
        out = pyvips.Image.thumbnail(filename, width, height=height)
        out.write_to_file('output photos/' + name)
        exit(0)
    elif format == "png":
        img = pyvips.Image.pngload(filename)


    resize_index_height = height / img.height
    resize_index_width = width / img.width

    if resize_index_height < resize_index_width:
        img2 = img.resize(resize_index_height)
    else:
        img2 = img.resize(resize_index_width)

    img2.magicksave("output photos/" + name)





width = int(input("Enter the width you want the result image to have: "))
height = int(input("Enter the height you want the result image to have: "))
filepath = input("Enter the path of the image you want to resize: ")

ok = 0
name = ""

for i in filepath:
    if ok:
        name = name + i

    if i == '.':
        ok = 1


if name == "gif":
    gif_resize(filepath, width, height)
elif name == "svg":
    resize(filepath, width, height, "svg")
elif name == "jpg" or name == "jpeg":
    resize(filepath, width, height, "jpg")
elif name == "png":
    resize(filepath, width, height, "png")


