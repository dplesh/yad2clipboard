import sys
import pyperclip

from Yad2.Yad2Page import Yad2Page # pylint: disable=import-error
from Yad2.Yad2EstatePost import Yad2EstatePost
from Yad2.Yad2VehiclePost import Yad2VehiclePost
from Yad2.TargetSecurityTriggeredError import TargetSecurityTriggeredError # pylint: disable=import-error

if __name__ == "__main__":


    #url = sys.argv[1]
    #url = "https://www.yad2.co.il/s/c/wz8yzpwo" # DEBUG Estate
    url = "https://www.yad2.co.il/s/c/o39pta6o" # DEBUG Vehicle

    page = Yad2Page(url)
    try:
        post = page.load(False)
    except TargetSecurityTriggeredError:
        post = page.load(True)

    template_path = ""

    if type(post) is Yad2VehiclePost:
        template_path = "vehicle_output_template.txt"
    elif type(post) is Yad2EstatePost:
        template_path = "estate_output_template.txt"
    
    template = ""
    with open(template_path,'r',encoding="utf8") as f:
        template = f.read()
    
    post_str = post.format_post_string(template)
    
    page.close()
    
    pyperclip.copy(post_str)
    print("{title} Copied to clipboard.".format(title=post.title))



