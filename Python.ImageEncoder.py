# Image encoder
""" Because I can't get my head around jpg compression and it often leads to
them behaving oddly, this program seems better suited to uncompressed images.
Admmittedly this is far less useful in the wild but will still allow me to
practice some steganography. It will be best to use bmp images here"""

# Define application constants
HEADER_SIZE = 1024
FOOTER_SIZE = 1024
MAX_SECRET_LEN = 1024
""" I've done an MD5 hash of "CLEAN" and appended it to the filename to reduce
the chance of overwriting an important file """
CLEAN_IMG_NAME = "CLEANa88a6a0c276fd853999a1faedf19c00e.bmp"


# Read image file in 
def readImg(imageName):
    image = open(imageName, "rb")
    return image

# Write image file out 
def writeImg(imageName):
    image = open(imageName, "wb")
    return image

# Get the size of the image in bytes to prevent overwriting footer
def getSize(imageName):
    import os
    return os.path.getsize(imageName)

# Replace the least significant bit with a 0 
def writeCleanImg(inputImgName, outputImgName):
    # Take the input image and get its size 
    inputImg = readImg(inputImgName)
    inputImgSize = getSize(inputImgName)
    
    # Create/ overwrite the output image 
    outputImg = writeImg(outputImgName)
    
    # Copy the header  
    outputImg.write(inputImg.read(HEADER_SIZE))
    
    # For the bytes not in the Header or Footer 
    for byte in range(inputImgSize - (HEADER_SIZE + FOOTER_SIZE)):
        
        # Set the LSB to 0 and write it to the output image 
        partAsInt = (inputImg.read(1)[0] & 254)
        partAsByte = ((partAsInt).to_bytes(1, byteorder='big'))
        outputImg.write(partAsByte)
        
    # Copy the footer across 
    outputImg.write(inputImg.read(FOOTER_SIZE))
    return 0

# Write a secret message to the image 
def writeEncodedImg(inputImgName, outputImgName, secretMsg):
    # Take the input image and get its size 
    inputImg = readImg(inputImgName)
    inputImgSize = getSize(inputImgName)
    
    # Create/ overwrite the output image 
    outputImg = writeImg(outputImgName)
    
    # Copy the header across 
    outputImg.write(inputImg.read(HEADER_SIZE))
    
    # For the bytes not in the Header or Footer 
    for byte in range(inputImgSize - (HEADER_SIZE + FOOTER_SIZE)):
        
        # Set the LSB to a part of the text and write it to the output image
        partAsInt = (inputImg.read(1)[0] | calculateLSB(byte, secretMsg))
        partAsByte = ((partAsInt).to_bytes(1, byteorder='big'))
        outputImg.write(partAsByte)
        
    # Copy the footer across 
    outputImg.write(inputImg.read(FOOTER_SIZE))
    return 0

def calculateLSB(byte, secretMsg):
    # Get the character to write
    try:
        charToWrite = secretMsg[byte // 8]
    except:
        # No character so nothing to write
        return 0
    # Select the correct bit 
    bit = byte % 8
    # Get the bit to write 
    charBit = (ord(charToWrite) >> bit) & 1
    return charBit

def readEncodedImg(inputImgName):
    # Take the input image and get its size 
    inputImg = readImg(inputImgName)
    inputImgSize = getSize(inputImgName)
    inputImg.read(HEADER_SIZE)
    # For the bytes not in the Header or Footer
    outString = ""
    for byte in range(MAX_SECRET_LEN):
        charInt = 0
        for bit in range(8):
            # Read the LSB
            lsb = inputImg.read(1)[0] & 1
            charInt += lsb << bit
        outString += chr(charInt)
            
    print(outString)
    return 0

def gui():
    print("Clean, Encode, Clean and Encode (.bmp only), Decode or Quit? " +
          "(C, e,a, d, q)" )
    choice = input(">")[0].lower()

    # Quit application 
    if choice == "q":
        return True 

    # All functions require the path to the input image 
    print("Type the name of the input image (include the file extension " +
          "and path if required)""")
    inputImgName = input(">")

    # Some functions require additional parameters 
    if choice != "d":
        print("Type the name of the output image (include the file extension " +
              "and path if required)")
        outputImgName = input(">")
    if choice == "e" or choice == "a":
        print("Type the secret message (max " + str(MAX_SECRET_LEN) +
              " characters)")
        secretMsg = input(">")

    # Run the required function for each choice
    # ENCODE 
    if choice == "e":
        writeEncodedImg(inputImgName, outputImgName, secretMsg)
    # CLEAN AND ENCODE
    elif choice == "a":
        writeCleanImg(inputImgName, CLEAN_IMG_NAME)
        writeEncodedImg(CLEAN_IMG_NAME, outputImgName, secretMsg)
    # DECODE 
    elif choice == "d":
        readEncodedImg(inputImgName)
    # DEFAULT = CLEAN  
    else:
        writeCleanImg(inputImgName, outputImgName)

# Run the GUI while the user has not finished 
finished = False 
while not finished:
    finished = gui()
