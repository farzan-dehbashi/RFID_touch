# python3 file_name.py title
import sys
import dominate
from dominate.tags import *


page_title = sys.argv[1]
doc = dominate.document(title= page_title)

print (doc)


f = open(str(page_title)+".html","a")
f.write(str(doc))
f.close()


