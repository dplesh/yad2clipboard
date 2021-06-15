import sys
import pyperclip

from Yad2.Yad2Page import Yad2Page # pylint: disable=import-error
from Yad2.TargetSecurityTriggeredError import TargetSecurityTriggeredError # pylint: disable=import-error

if __name__ == "__main__":

    #url = sys.argv[1]
    url = "https://www.yad2.co.il/s/c/wz8yzpwo" # DEBUG

    page = Yad2Page(url)
    try:
        post = page.load(False)
    except TargetSecurityTriggeredError:
        post = page.load(True)

    template = None
    with open('output_template.txt', 'r', encoding="utf8") as template_file:
            template = template_file.read()
    
    post_str = post.format_post_string(template)
    
    page.close()
    
    pyperclip.copy(post_str)
    print("{title} Copied to clipboard.".format(title=post.title))



