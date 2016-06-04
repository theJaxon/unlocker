import json
import random
import string

# Years and months
#         2010    2011    2012    2013    2014    2015    2016    2017    2018    2019    2020    2021    2022
years = ['C','D','F','G','H','J','K','L','M','N','P','Q','R','T','V','W','X','Y','1','2','3','4','5','6','7','8']

# Week numbers from 1-52
# B is used to shift indexing to 1 and is not used
weeks = ['B','C','D','F','G','H','J','K','L','M','N','P','Q','R','T','V','W','X','Y','1','2','3','4','5','6','7','8',
         'C','D','F','G','H','J','K','L','M','N','P','Q','R','T','V','W','X','Y','1','2','3','4','5','6','7','8']

# Values to generate 3 code production number
production = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
              '0','1','2','3','4','5','6','7','8','9']

# MLB codes
ttt = ['200', '600', '403', '404', '405', '303', '108', '207', '609', '501', '306', '102', '701', '301', '501',
       '101', '300', '130', '100', '270', '310', '902', '104', '401', '902', '500', '700', '802']

cc = ['GU', '4N', 'J9', 'QX', 'OP', 'CD', 'GU']

eeee = ['DYWF', 'F117', 'F502', 'F505', 'F9GY', 'F9H0', 'F9H1', 'F9H2', 'DYWD', 'F504', 'F116', 'F503', 'F2FR',
        'F653', 'F49P', 'F651', 'F49R', 'F652', 'DYW3', 'F64V', 'F0V5', 'F64W', 'FF4G', 'FF4H', 'FF4J', 'FF4K',
        'FF4L', 'FF4M', 'FF4N', 'FF4P', 'DNY3', 'DP00', 'DJWK', 'DM66', 'DNJK', 'DKG1', 'DM65', 'DNJJ', 'DKG2',
        'DM67', 'DNJL', 'DJWM', 'DMT3', 'DMT5', 'DJWN', 'DM69', 'DJWP', 'DM6C']

kk = ['1H', '1M' 'AD' '1F' 'A8' 'UE' 'JA' 'JC' '8C' 'CB' 'FB']

# Loaded JSON model database
smbiosdb = {}

model = None
year = None
week = None
yearweek = None
run = None
mlb = None
rom = None


def loaddb():
    global smbiosdb
    # Load the json database file
    with open('smbiosdb.json') as json_file:
        smbiosdb = json.load(json_file)


def getmlb():
    global mlb

    if model['serial.type'] == 11:
        mlb = yearweek + '0'+ run + id_generator(4)
    elif model['serial.type'] == 12:
        mlb = 'C02{0}{1}{2}{3}{4}{5}'.format(str(year - 2010), str(week).zfill(2),
                    random.choice(ttt), random.choice(cc), random.choice(eeee), random.choice(kk))
    else:
        pass


def getmodel():
    global model
    modeltype = None

    # Build a menu with the types of Mac to select hw.model
    modeltypes = ['iMac', 'Mac mini', 'Mac Pro', 'MacBook', 'MacBook Air', 'MacBook Pro']
    print("[1] iMac\n[2] Mac mini\n[3] Mac Pro\n[4] MacBook\n[5] MacBook Air\n[6] MacBook Pro\n")
    while True:
        try:
            index = int(raw_input('Please enter model family [1-6]: '))
        except:
            print "This is not a number."
        else:
            if (index >= 1) and (index <= 6):
                modeltype = modeltypes[index - 1]
                break
            else:
                print 'Invalid model family selected: ',  index

    # Now build a menu with selected models
    i = 1
    models = []
    for m in smbiosdb:
        if m['family'] == modeltype:
            print '[' + str(i) + '] ' + m['hw.model']
            models.append(m['hw.model'])
            i += 1

    while True:
        try:
            index = int(raw_input('Please enter model [1-{}]: '.format(i - 1)))
        except:
            print "This is not a number."
        else:
            if (index >= 1) and (index <= (i-1)):
                model = models[index - 1]
                break
            else:
                print 'Invalid model selected: ', index

    for m in smbiosdb:
        if m['hw.model'] == model:
            model = m


def getrom():
    global rom

    # Using an Apple Wifi ethernet OUI AC:BC:32
    rom = "acbc32%02x%02x%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
    )


def getrun():
    global run

    # Generate 3 random characters from list
    run = id_generator()


def getweek():
    global year
    global week
    global yearweek

    # Get the serial number type
    serlen = model['serial.type']

    # Save year for MLB processing
    year = model['y1']

    # Get a week number
    while True:
        try:
            week = int(input('Please enter week for year {0} (1 - 53): '.format(year)))
        except:
            print "This is not a week number."
        else:
            if (week >= 1) and (week <= 53):
                break
            else:
                print 'Invalid week: ',  week

    # Format date based on serial number length
    if serlen == 11:
        yearweek = 'CK{0}{1}'.format(str(year)[-1], str(week).zfill(2))
    elif serlen == 12:
        index_year = (year - 2010) * 2

        if week <= 27:
            yearweek = 'C02{0}{1}'.format(years[index_year], weeks[week])
        else:
            yearweek = 'C02{0}{1}'.format(years[index_year + 1], weeks[week])
    else:
        return


def id_generator(size=3, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def main():
    loaddb()
    getmodel()
    getweek()
    getrun()
    getmlb()
    print
    print '# Passthru host definitions - FALSE'
    print 'board-id.reflectHost = "FALSE"'
    print 'hw.model.reflectHost = "FALSE"'
    print 'serialNumber.reflectHost = "FALSE"'
    print 'smbios.reflectHost = "FALSE"'
    print 'efi.nvram.var.ROM.reflectHost = "FALSE"'
    print 'efi.nvram.var.MLB.reflectHost = "FALSE"'
    print 'SMBIOS.use12CharSerialNumber = "TRUE"'
    print 'smc.version = "0"'
    print
    print '# Generated information'
    print 'hw.model = "{0}"'.format(model['hw.model'])
    print 'board-id = "{0}"'.format(model['board-id'])
    print 'serialNumber = "{0}{1}{2}"'.format(yearweek, run, model['eee.code'])
    print 'efi.nvram.var.ROM = "{0}"'.format(rom)
    print 'efi.nvram.var.MLB = "{0}"'.format(mlb)
    print


if __name__ == '__main__':
    main()