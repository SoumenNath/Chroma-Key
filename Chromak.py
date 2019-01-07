#Author: Soumen Nath

#import the pygame library
import pygame
#initialize pygame
pygame.init()
print("\n\n\t\t\t----------------------------------------\n\t\t\tWelcome to Soumen's Chroma-Keying System\n\t\t\t----------------------------------------\n\n")
#ask if the user requires instructions
needInstructions = input("Would you like to view the instructions on how to use this program? (yes/no): ")
#if the user answers yes then display the instructions
if needInstructions.lower() == 'yes':
    print("\nThis program can be used to perform a simple chroma-keying (also known as green screening) operation, to merge two images.\nThe first image will be a background image and the second image will be the image of a ghost against a green background.\n\nThe names of the background are as follows: ")
    print("1. abandoned_circus.bmp\n2. abandoned_homestead.bmp\n3. abandoned_plant.bmp\n\nThe names of the ghost images are:\n1. ghost_with_broom.bmp\n2. ghost_with_crutches.bmp\n3. ghost_with_frame.bmp")
    print("\nYou must choose one background image and one ghost image.\nTo indicate your choice, you must enter the name of the image as shown above (note you must include the .bmp), for a total of two inputs.\nAfter the images are chosen, the background image will be displayed in front of you.\nYou should look at the image and enter the x and y co-ordinates at which you the ghost will be centered at.\nNote the dimensions of the image will be given to you and you must enter coordinates that are in the background image.\nTo enter the coordinates, you can either use the keyboard or use the mouse.")
#loop until the user enters a valid background image name
while  True:
    bgImage = input("\nPlease enter the name of the background image: ")
    if bgImage == "abandoned_circus.bmp" or bgImage == "abandoned_homestead.bmp" or bgImage == "abandoned_plant.bmp":
        break
    else:
        print("Error! Please enter the correnct file name.")
#loop until the user enters a validghost image name
while True:
    gImage = input("\nPlease enter the name of the ghost image: ")
    if gImage == "ghost_with_broom.bmp" or gImage == "ghost_with_crutches.bmp" or gImage == "ghost_with_frame.bmp":
        break
    else:
        print("Error! Please enter the correnct file name.")
#load the chosen background and ghost images
loadedBimage = pygame.image.load(bgImage)
loadedGimage = pygame.image.load(gImage)
#get the width and height of the background and ghost images
(width, height) = loadedBimage.get_rect().size
(giWidth, giHeight) = loadedGimage.get_rect().size
#get the coordinates of the center of the ghost image
(cpx, cpy) = loadedGimage.get_rect().center
#create the window surface that will have the dimensions of the background image
window1 = pygame.display.set_mode((width, height))
window1.fill((255, 255, 255))
#copy the backgroun image onto the window surface
window1.blit(loadedBimage, (0, 0))
#update the window surface to display the background image
pygame.display.update()
#Display the dimensions of the background image to the user
print('\nDimensions of the background picture:\nWidth', width, 'Height', height)
#ask the user which method they would like to user to enter the coordinates at which the ghost will be centered at.
while True:
    choice = input("Press 1 to use the terminal to indicate the center coordinates of the ghost image\nOtherwise Press 2 to use the mouse to indicate the center coordinates.\nPlease enter your selection: ")
    if choice != '1' and choice != '2':
        print("Error!")
    else:
        break
#list used to store the coordinates for all the non green pixels in the ghost image
notGreenCor = []
#following for loops are used to traverse through all the pixels in the ghost image
for x in range(giWidth):
    for y in range(giHeight):
        #get the rgb values for the pixel at the current coordinates (x, y)
        (red, green, blue, _) = loadedGimage.get_at((x, y))
        #if the pixel is not green then add the coordinates of the pixel to the list
        if not(red == 0 and green == 255 and  blue == 0):
            notGreenCor.append((x,y))
#function to draw the ghost onto the background image
def drawGhost():
    #traverse through the list with the coordinates of all the non-green pixels
    for coordinate in notGreenCor:
        #get the horizontal and vertical difference between the center coordinate and the non green coordinate
        xdif = cpx - coordinate[0]
        ydif = cpy - coordinate[1]
        #check to seee if the difference results in a value that is still on the screen, so no negative values or values greater than the height or width of the background imgae
        if not(((xCor-xdif) <0) or ((yCor-ydif)<0) or ((xCor-xdif) >= width) or ((yCor-ydif) >= height)):
            #get the rgb values of the coordinates on the ghost image and the corresponding coordinates on the background image, which are based on the cetering coordinates given by the user
            (red1, green1, blue1, _) = loadedGimage.get_at((coordinate[0], coordinate[1]))
            (red2, green2, blue2, _) = loadedBimage.get_at((xCor-xdif, yCor-ydif))
            #average the rgb values of the two coordinates
            avgRed = (red1+red2)/2
            avgGreen = (green1+green2)/2
            avgBlue = (blue1+blue2)/2
            #set the colour of the corresponding coordinates on the background image to the average colour to create the transparency affect.
            loadedBimage.set_at( (xCor-xdif, yCor-ydif), (avgRed, avgGreen, avgBlue) )
    #blit the changed background image onto the window surface
    window1.blit(loadedBimage, (0, 0))
    #update the window surface again
    pygame.display.update()
#if the user user chooses to enter the coordinates using the keyboard
if choice == '1':
    #loop until the user enters a valid x-coordinate
    while True:
        xCor = int(input('\n\nPlease enter the x coordinate at which the ghost will be centered at: '))
        if xCor<0 or xCor>width:
            print('Error!\n'); continue
        else:
            break
    #loop until the user enters a valid y-coordinate
    while True:
        yCor = int(input('\n\nPlease enter the y coordinate at which the ghost will be centered at: '))
        if yCor<0 or yCor>width:
            print('Error!\n'); continue
        else:
            break
    #run the drawGhost function to draw the ghost on the background
    drawGhost()
    #keep displaying the background image containing the ghost until the user chooses to quit
    flag = True
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
    pygame.quit()
    #display this message once the user crosses out the program
    print("\n\nThanks for using this program!")
#if the user user chooses to enter the coordinates using the mouse
else:
    while True:
        #get the x and y coordinates of the mouse
        mx = pygame.mouse.get_pos()[0]
        my = pygame.mouse.get_pos()[1]
        #blit the background image to the window surface and then use a time delay to stop the font object from flickering
        window1.blit(loadedBimage, (0, 0))
        pygame.time.delay(10)
        pygame.display.update()
        #create a sting containing the current x and y coordinates of the mouse
        coor = str(mx)+' ,'+str(my)
        #create a font object
        fo = pygame.font.Font(None, 25)
        #store the string containing the current x and y coordinates in an image
        coorImg = fo.render(coor, True, (255,255,255), (0,0,0))
        #blit this image to the window surace
        window1.blit(coorImg, (mx,my))
        #update the window surface
        pygame.display.update()
        for event in pygame.event.get():
            #end the program if the user chooses to quit
            if event.type == pygame.QUIT:
                print("\n\nThanks for using this program!")
                exit()
            #if the user clicks the mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #reload the original background image and update the window surface
                loadedBimage = pygame.image.load(bgImage)
                pygame.display.update()
                #get the current x and y coordinates
                xCor = mx
                yCor = my
                #run the drawGhost function to draw the ghost on the background
                drawGhost()
#quit the pygame subsystem
pygame.quit()
