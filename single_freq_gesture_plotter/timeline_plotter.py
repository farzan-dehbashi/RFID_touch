import argparse
import dominate
from dominate.tags import *

parser = argparse.ArgumentParser(description= 'This code reads from a reading directory (in) and plots each of gestures included in that directory in an html file. The style of this plot is a timeline for each tag which is hardcoded in the program.')
parser.add_argument('-i', '--frequency', type= float, metavar='', required= False, help='sets frequency of the reader')
parser.add_argument('-m', '--printmean', action= 'store_true',required=False, help='prints mean dataframe') #for no argument use store_true
args = parser.parse_args()

in_dir = 'input'
out_dir = 'out'

doc = dominate.document(title='Dominate your HTML')

with doc.head:
    link(rel='stylesheet', href='style.css')
    script(type='text/javascript', src='script.js')

with doc:
    with div(id='header').add(ol()):
        for i in ['home', 'about', 'contact']:
            li(a(i.title(), href='/%s.html' % i))

    with div():
        attr(cls='body')
        p('Lorem ipsum..')

print(doc)




