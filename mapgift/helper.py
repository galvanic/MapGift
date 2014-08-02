import sys, time


def ask(question, rangeList=["y","yes","oui"], errorText="Enter another value."):
    """
    Asks for and returns user's input. End program with "n".
    question:   string
    rangeList:  list of (acceptable) values
    errorText:  string
    
    Module with function which asks user for something.
    
    If the user input isn't as expected, the function will loop and ask again.
    
    The user gets the option of terminating the program
    or just continuing the program without being asked again:
    The ask function returns without returning the user input, ending the loop.
    
    However, the loop might continue depending on program architecture,
    or there might be a problem since "None" is returned in that case.
    """
    endprog = ["n", "no", "non", "end", "terminate", "finish", "0", "endprog"]
    endloop = ["endloop"]
    if rangeList:
        rangeList = map(str, rangeList)
    while True:
        try:
            user = input(question+" ")
            if user.lower() in endprog:
                sys.exit("End of program.")
            elif user.lower() in endloop:
                return
            # maybe give the option of changing ask when looking at rangeList ?
            # eg. lower() etc ?
            # can't remember what i meant by this ^
            elif not rangeList:
                return user
            elif user.lower() not in rangeList:
                raise ValueError
        except ValueError:
            print(errorText + "\n")
            continue
        break
    return user

def askTimeout(prompt="\nEnter some text:\t", timeout=60):
    '''
    Improvements:
        - add a visual countdown so the user knows how long they have left to answer
    '''
    return

def askF(function):     # doesn't work      # why did I make this ?
    """
    Asks user whether they want to play a function.
    If Yes, plays it and asks again at the end (loops).
    """
    while True:
        ask("Do you want to play the function ?", ["yes", "y"])
        function()
    return


def writeDictToFile(dict, filename, overwrite=False):
    """
    Takes a dictionary and writes it neatly into a file.
    
    Dict key
    --------
    Values
    
    dict:       string -> string or list of values
    filename:   name of an empty file (creates the file if doesn't exist).
    overwrite:  boolean
    """
    # need to make it work if dict values is a list instead of simply a string
    # maybe by checking type ?
    
    # check if file exists
    
    f = open(filename, "w")
    
    for key in dict.keys():
        # write the key as a title
        f.write(str(key) + "\n" + "-"*len(key) + "\n\n")
        # write the value underneath
        f.write(str(dict[key]) + "\n\n\n")
    
    f.close()
    return


def makeSwedishDate(date):
    '''
    Swedes represent their dates as YY/MM/DD, or simply YYMMDD
    Returns time_string
    date:           a time instance
    time_string:    the date instance converted to a string in Swedish format
    '''
    year = time.strftime("%Y", date)[-2:]
    month = time.strftime("%m", date)
    day = time.strftime("%d", date)
    hour = time.strftime("%H", date)
    minutes = time.strftime("%M", date)
    seconds = time.strftime("%S", date)
    time_string = year + month + day + hour + minutes + seconds
    return time_string

def measureProgTime(start_time, trunc=4):
    '''
    Need to write "start_time=time.time()" at the beginning of your program.
    (Kind of) measures program execution time.
    '''
    return str(time.time() - start_time)[:trunc] + " seconds"


# from PIL import Image, ImageFont, ImageDraw

# Make a function that checks whether the parameter passed to it is
# an Image instance or a filepath (presumably to an image, otherwise
# raise error). If it's a filepath, open the Image and return it
# In either case, returns an Image
# Would allow more flexibility for functions operating on Images ? or hassle?

# general merge function to use in window stitching function
def merge(img_list, orientation, distance_btw=0, bg_colour="black"):
    '''
    Merges pictures by appending them together according to chosen orientation.
    img_list:       list of image instances
    orientation:    string,
                        can be "horizontal"/"h"/"hor"/etc or "vertical"/"v"/"vert"/etc)
    distance_btw:   integer or float (float will be converted to an integer),
                        the distance between 2 images,
                        the thickness of the frame surrounding indivdual images
    bg_colour:      any representation of a colour (can be string/tuple/etc as long as Python Image recognizes it as a colour)
                        background colour, the colour of the frame surrounding indivdual images
    
    Improvements:
    - I need a slicker way to manage both orientations
    '''
    d = int(distance_btw)
    
    if orientation.lower() in "horizontal":
        big_side = sum([img.size[0] for img in img_list]) + (len(img_list)+1)*d
        small_side = max([img.size[1] for img in img_list]) + 2*d
        final_size = (big_side, small_side)
    elif orientation.lower() in "vertical":
        big_side = sum([img.size[1] for img in img_list]) + (len(img_list)+1)*d
        small_side = max([img.size[0] for img in img_list]) + 2*d
        final_size = (small_side, big_side)
        
    final_img = Image.new("RGB", final_size, bg_colour)
    x = 0
    for img in img_list:
        w,h = img.size
        if orientation.lower() in "horizontal":
            final_img.paste(img, (x+d,0+d,x+w+d,h+d))
            x += w + d
        elif orientation.lower() in "vertical":
            final_img.paste(img, (0+d,x+d,w+d,x+h+d))
            x += h + d
    return final_img

def addText(text, image, text_location, text_colour, text_size, font="/Library/Fonts/Georgia.ttf"):
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font, text_size)
    draw.text(text_location, text, fill=text_colour, font=font)
    return image

def addTitle(image, text,
            loc="top", text_colour="white",
            text_size=36, distance_from_sides=8):
    d = distance_from_sides
    w, h = image.size
    if loc == "top":
        text_location = (0+d, 0+d)
    elif loc == "bottom":
        text_location = (0+d, h-text_size-d)
    return addText(text, image, text_location, text_colour, text_size)

def fancyTitle(text, img):
    '''
    Modified version of script I found online when googling "add text to image PIL"
    Quite a nice way to put a title on an image.
    text:   string of text to add (will be converted to string anyway)
    img:    Image instance to which to add a title to
    
    Improvements:
    - possibility to tweak more parameters when calling the function
      eg.   title at bottom/top
            size of text
            size of band
            colour of band
            colour of text
            font of text
    '''
    font_size = 20
    line_width = 22
    font = ImageFont.truetype("/Library/Fonts/Georgia.ttf", font_size)
    distance_from_top = img.size[1] - line_width - 10
    imgbg = Image.new('RGBA', img.size, "black")  # make an entirely black image
    mask = Image.new('L',img.size,"black")        # make a mask that masks out all
    draw = ImageDraw.Draw(img)                      # setup to draw on the main image
    drawmask = ImageDraw.Draw(mask)                 # setup to draw on the mask
    y = distance_from_top + line_width/2
    drawmask.line((0, y, img.size[0], y),
                fill="#999999", width=line_width)   # draw a line on the mask to allow some bg through
    img.paste(imgbg, mask=mask)                     # put the (somewhat) transparent bg on the main
    line_top = distance_from_top
    draw.text((10,line_top), str(text), font=font, fill="white")
    del draw
    del drawmask
    return img

def makeSmaller(image, proportion=0.6):
    w,h = image.size
    width = int(proportion*w)
    height = int(proportion*h)
    return image.resize((width,height), Image.ANTIALIAS)

def resizeToSmallest(img_list, side_to_equalise):
    '''
    What if the ratio isn't similar ? => choose which side you want to equalise
    '''
    if side_to_equalise in "width":
        side = 0
    elif side_to_equalise in "height":
        side = 1
    smallest_size = min([img.size[side] for img in img_list])
    
    for index in range(len(img_list)):
        img = img_list[index]
        if img.size[side] == smallest_size:
            continue #to next image
        old_width, old_height = img.size
        if side_to_equalise in "width":
            new_width = smallest_size # width is equalised
            new_height = int(old_height * new_width / old_width)
        elif side_to_equalise in "height":
            new_height = smallest_size # height is equalised
            new_width = int(old_width * new_height / old_height)
        new_size = (new_width, new_height)
        img_list[index] = img.resize(new_size, Image.ANTIALIAS)
    return img_list

def imageOnDemand(imgFunc, save_folder="/Users/jc5809/Desktop/", format="PNG", timeout=6):
    # make saving folder if it doesn't already exist
    while True:
        print("\n\n\nGenerating image...\n")
        start_time = time.time()
        image = imgFunc()
        print("It took", measureProgTime(start_time), "to generate your image.")
        image.show()
        user = raw_input("\nDo you want to save this image ?\t")
        #user = askTimeout("\nDo you want to save this image ?\t", timeout)
        if user.lower() in ["y","yes","o","oui","save"]:
            image.save(str(save_folder)+"im"+str(makeSwedishDate(time.localtime()))+"."+str(format.lower()), format.upper())
        del image
        ask("\nDo you want to make a new image ?")
    return


# import Carbon.Snd
# def beep():
#     Carbon.Snd.SysBeep(1)

"""
make scripts to extract stuff from webpages
eg. from facebook pages
    eg. from the music pages to download the music
        from the underground pages to evaluate events possible
        from the feminist page to then search whether something i want to post has already been posted
"""

