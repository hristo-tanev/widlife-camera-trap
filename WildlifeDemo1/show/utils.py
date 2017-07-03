import math
from decimal import *
import datetime


def list2String(ilist):
    s = ""
    for i in ilist:
        s += str(i) + ';'

    return s


def string2list(string):
    strings = [x for x in string.split(';')]
    strings.pop()
    ilist = []
    for x in strings:
        x = x.replace('[', '').replace(']', '').split(',')
        ilist.append([float(x[0]), float(x[1])])

    return ilist


def isInto(array, sd, ed):
    for i in array:
        if i.startDate == sd and i.endDate == ed:
            return True

    return False


def format(x):
    if int(x) < 10:
        return '0' + x

    return x


def isLeapYear(year):
    y = int(year)
    if y % 4 == 0 and y % 100 == 0 and y % 400 == 0:
        return True

    return False


def dayOfWeek(day, month, year):
    day = datetime.date(int(year), int(month), int(day))
    return int(day.strftime("%w"))


def getAverageBirds1(array):
    s = 0
    for i in array:
        s += i.birdsDetected

    return Decimal(float(s) / float(len(array)))


def getAverageBirds2(array, days):
    left = -1
    right = -1
    for d in days:
        for i in range(0, len(array)):
            dd = format(array[i].daym) + '.' + \
                format(array[i].month) + '.' + array[i].year
            if dd == d:
                left = i
                break
        if left != -1:
            break

    for d in days:
        for i in range(left, len(array)):
            dd = format(array[i].daym) + '.' + \
                format(array[i].month) + '.' + array[i].year
            if dd == d:
                right = i

    return [left, right]
