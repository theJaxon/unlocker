import plistlib


smbiosdb = plistlib.readPlist('smbiosdb.plist')
# print header
print 'hw.model' + '\t' + 'family' + '\t' + 'board-id' + '\t' + 'serial.type' + '\t' + 'eee.code' + '\t' + \
      'bios.version' + '\t' + 'y1' + '\t' + 'y2' + '\t' + 'y3' + '\t' + 'y4'

for model in smbiosdb.keys():
    data = smbiosdb[model]
    for s in data:
        line = s['SMproductname'] + '\t' + s['SMfamily'] + '\t' + s['SMboardproduct'] + '\t' + str(len(s['SMserial'])) \
               + '\t' + s['Number'] + '\t' + s['SMbiosversion']
        for y in s['Years']:
            line = line + '\t' + y
        print line
