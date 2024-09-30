from PIL import Image
import fitz


## Python Version: Python 3.11.3 ##

########  Main Method : Start ##########

def crop_image(path, pageno, left_crop_word, right_crop_word):
    """
    Input-
    Passed Arguments are-
    1. path of the pdf, 
    2. page number of the pdf where the image to be extracted,
    3. the word for which top left pixel will be calculated,
    4. the word for which right bottom pixel will be calculated.

    Output-
    1.the page in image form, from which the required image to be cropped.
    2. The x-pixel and y-pixel values for the top-left side word.
    3. The x-pixel and y-pixel values for the right-bottom side word. 

    """
    with fitz.open(path) as doc:
        page=doc.load_page(pageno)
        pix=page.get_pixmap()
        image=Image.frombytes("RGB",[pix.width, pix.height], pix.samples)
        lx0, ly0 ,lx1, ly1=0,0,0,0
        rx0, ry0 ,rx1, ry1=0,0,0,0
        for word in page.get_text_words():
            word_text=word[4]
            if word_text==left_crop_word:
                lx0, ly0 ,lx1, ly1=word[:4]
            if word_text==right_crop_word:
                rx0, ry0 ,rx1, ry1=word[:4]
    return image, lx0, ly0, rx1, ry1

########  Main Method : End ##########