from TargetSecurityTriggeredException import TargetSecurityTriggeredException
import sys
import pyperclip

from Yad2Page import Yad2Page

if __name__ == "__main__":

    url = sys.argv[1]

    page = Yad2Page(url)
    try:
        post = page.load(False)
    except TargetSecurityTriggeredException:
        post = page.load(True)

    post_str = str(post)
    
    page.close()
    
    pyperclip.copy(post_str)
    print("{title} Copied to clipboard.".format(title=post.title))



