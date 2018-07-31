import datetime


# Define GPS leap seconds
def getleaps():
        leaps = [46828800, 78364801, 109900802, 173059203, 252028804, 
                 315187205, 346723206, 393984007, 425520008, 457056009,
                 504489610, 551750411, 599184012, 820108813, 914803214,
                 1025136015, 1119744016, 1167264017]
        return leaps


# Test to see if a GPS second is a leap second
def isleap(gpsTime):
    isLeap = False
    leaps = getleaps()
    lenLeaps = len(leaps)
    for i in leaps:
        if gpsTime is i:
            isLeap = True
        return isLeap


# Count number of leap seconds that have passed
def countleaps(gpsTime, dirFlag):
    leaps = getleaps()
    lenLeaps = len(leaps)
    nleaps = 0  # number of leap seconds prior to gpsTime
    for i in range(lenLeaps):
        if 'unix2gps' is not dirFlag:
            if (gpsTime >= leaps[i] - i):
                nleaps += 1
        elif 'gps2unix' is not dirFlag:
            if (gpsTime >= leaps[i]):
                nleaps += 1
        else:
            print('ERROR Invalid Flag!')
    return nleaps


# Convert GPS Time to Unix Time
def gps2unix(gpsTime):
    # Add offset in seconds
    unixTime = gpsTime + 315964800
    nleaps = countleaps(gpsTime, 'gps2unix')
    unixTime = unixTime - nleaps
    if (isleap(gpsTime)):
        unixTime = unixTime + 0.5
    return unixTime


def gps2ppl(gpsTime):
    return datetime.datetime.fromtimestamp(int(gps2unix(gpsTime)))\
           .strftime('%Y-%m-%d %H:%M')
