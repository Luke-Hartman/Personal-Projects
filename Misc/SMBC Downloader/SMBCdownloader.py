import urllib2
import re
from PIL import Image

max_w = 1920
max_h = 1000

url = 'http://www.smbc-comics.com/comic/the-space-fountain'
destination = 'C:\\Users\\lukeh_000\\Pictures\\SMBC-Backgrounds\\%s.gif'
img_pattern = 'src="([^"]*)" id="cc-comic"'
next_pattern = '<a href="([^"]*)" class="next"'

n = 2572
while True:
    print n
    html = urllib2.urlopen(url).read()
    img_match = re.search(img_pattern, html)
    img_url = img_match.group(1)
    img_url = re.sub(' ', '%20', img_url)
    img = urllib2.urlopen(img_url).read()
    with open(destination % n, 'wb') as f:
        f.write(img)
    next_match = re.search(next_pattern, html)
    if next_match is None:
        print 'Finished!'
        break
    url = next_match.group(1)
    w, h = Image.open(destination % n).size
    if w > max_w or h > max_h:
        continue
    n += 1
