import urllib2, json
head = urllib2.urlopen("https://api.github.com/repos/ManiacalLabs/BiblioPixelAnimations/git/refs/head").read()
head_data = json.loads(head)
_ver = "9.9.9b"
if len(head_data) > 0:
    _ver = head_data[0]["object"]["sha"]

print _ver
