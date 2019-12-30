import subprocess
import requests
from zipfile import ZipFile
from io import BytesIO
import os
import sys

DriverPath = sys.argv[1]

def extract_file(zf, info, extract_dir):
    zf.extract(info.filename, path=extract_dir)
    #out_path = os.path.join(extract_dir, info.filename)
    out_path = zf.extract(info.filename, path=extract_dir)
    perm = info.external_attr >> 16
    os.chmod(out_path, perm)


arr = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"]
proc = subprocess.Popen(arr, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
o, e = proc.communicate()
s = o.decode('ascii')
v = s.split(" ")[2]
r = (".").join(v.split(".")[:3])

req = requests.get(
    'https://chromedriver.storage.googleapis.com/LATEST_RELEASE_%s' % r)
d = req.text
c = requests.get('https://chromedriver.storage.googleapis.com/%s/chromedriver_mac64.zip' % d, allow_redirects=True, stream=True
                 )

with ZipFile(BytesIO(c.content)) as zf:
    for info in zf.infolist():
        extract_file(zf, info, DriverPath)
        
print("Latest Chrome Driver installed")
