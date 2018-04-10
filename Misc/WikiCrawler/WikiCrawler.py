import urllib2
import re
import time

base = 'https://en.wikipedia.org/wiki/'

def searchWikiHelper(chain, target, depth, maxDepth, found):
    #print chain
    if depth >= maxDepth:
        chain.pop()
        return
    pattern = 'href="/wiki/[^"]*'
    html = urllib2.urlopen(base+chain[-1]).read()
    hits = re.findall(pattern, html)
    for hit in hits:
        name = hit[12:]
        if name in found or '.' in name or ':' in name:
            continue
        chain.append(name)
        if name == target:
            return chain
        found[name]=True
        results = searchWikiHelper(chain, target, depth + 1, maxDepth, found)
        if results is not None:
            return results
    chain.pop()
    return

def searchWiki(start, target):
    for i in range(2, 10):
        print i
        found = dict()
        found[start] = True
        hit = searchWikiHelper([start], target, 1, i, found)
        if hit is not None:
            print i, hit
            return
    print "Failed to find '%s' from '%s'" %  (start, target)

start = 'Puppies'
target = 'Adolf_Hitler'
start_time = time.time()
print("Going from %s to %s" % (start, target))
searchWiki(start, target)
print(time.time() - start_time)
