import os
import sys
import django
import math
import webcolors
from show.utils import *
from time import sleep
import datetime
from pyclustering.cluster.xmeans import xmeans
from SimpleCV import VirtualCamera, HaarCascade, DrawingLayer

PATH = os.path.dirname(__file__) + 'show/static/show/images/'
THRESHOLD = 0
numberOfDays = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
pigeon_colors = ['grey', 'gray', 'silver', 'brown', 'ash']

def getBounderies(entries, head, mode):
    days = []
    if mode == 0:
        week = getWeek(entries, head)
        if week[1] != week[3]:
            for i in range(week[0], numberOfDays[week[1]] + 1):
                days.append(format(str(i)) + '.' +
                            format(str(week[1])) + '.' + entries[head].year)
            for i in range(1, week[2] + 1):
                days.append(format(str(i)) + '.' +
                            format(str(week[3])) + '.' + entries[head].year)
        else:
            for i in range(week[0], week[2] + 1):
                days.append(format(str(i)) + '.' +
                            format(str(week[1])) + '.' + entries[head].year)
    else:
        month = numberOfDays[int(entries[head].month)]
        for i in range(1, month + 1):
            days.append(format(str(i)) + '.' +
                        format(entries[head].month) + '.' + entries[head].year)

    return days


def divideIntoMonthSlots(entries):
    head = 0
    index = 1
    while index < len(entries):
        if entries[index].month != entries[head].month:
            sd = "01/" + format(entries[head].month) + "/" + entries[head].year
            ed = str(numberOfDays[int(entries[head].month)]) + "/" + \
                format(entries[head].month) + "/" + entries[head].year
            ads = AdvancedStatsForMonth(
                startDate=sd, endDate=ed, averageNumberOfBirdsForAPeriod=getAverageBirds1(entries[head:index - 1]))
            ads.save()
            head = index
        index += 1
    sd = "01/" + format(entries[head].month) + "/" + entries[head].year
    ed = str(numberOfDays[int(entries[head].month)]) + "/" + \
        format(entries[head].month) + "/" + entries[head].year
    if not isInto(AdvancedStatsForMonth.objects.all(), sd, ed):
        ads = AdvancedStatsForMonth(
            startDate=sd, endDate=ed, averageNumberOfBirdsForAPeriod=getAverageBirds1(entries[head:index]))
        ads.save()
    else:
        ads = AdvancedStatsForMonth.objects.filter(startDate=sd, endDate=ed)
        point = getAverageBirds2(sa, getBounderies(entries, head, 1))
        newval = getAverageBirds1(sa[point[0]:point[1]])
        ads.update(averageNumberOfBirdsForAPeriod=newval)


def getWeek(entries, head):
    bw = int(entries[head].daym) - dayOfWeek(entries[head].daym,
                                             entries[head].month, entries[head].year) + 1
    if bw + 7 > numberOfDays[int(entries[head].month)]:
        ew = 7 - (numberOfDays[int(entries[head].month)] - bw + 1)
        bwm = int(entries[head].month)
        ewm = int(entries[head].month) + 1
    else:
        ew = bw + 6
        bwm = ewm = int(entries[head].month)

    return [bw, bwm, ew, ewm]


def divideIntoWeekSlots(entries):
    head = 0
    index = 1
    while index < len(entries):
        iweek = getWeek(entries, index)
        if iweek[0] != getWeek(entries, head)[0] and iweek[2] != getWeek(entries, head)[2]:
            sd = format(str(getWeek(entries, head)[
                        0])) + '/' + format(entries[head].month) + '/' + entries[head].year
            ed = format(str(getWeek(entries, head)[
                        2])) + '/' + format(entries[head].month) + '/' + entries[head].year
            ads = AdvancedStatsForWeek(
                startDate=sd, endDate=ed, averageNumberOfBirdsForAPeriod=getAverageBirds1(entries[head:index - 1]))
            ads.save()
            head = index
        index += 1
    sd = format(str(getWeek(entries, head)[
                0])) + '/' + format(entries[head].month) + '/' + entries[head].year
    ed = format(str(getWeek(entries, head)[
                2])) + '/' + format(entries[head].month) + '/' + entries[head].year
    if not isInto(AdvancedStatsForWeek.objects.all(), sd, ed):
        ads = AdvancedStatsForWeek(
            startDate=sd, endDate=ed, averageNumberOfBirdsForAPeriod=getAverageBirds1(entries[head:index]))
        ads.save()
    else:
        ads = AdvancedStatsForWeek.objects.filter(startDate=sd, endDate=ed)
        point = getAverageBirds2(sa, getBounderies(entries, head, 0))
        newval = getAverageBirds1(sa[point[0]:point[1]])
        ads.update(averageNumberOfBirdsForAPeriod=newval)


def getNextImageName(dirName):
    name = 0
    files_dir = os.listdir(dirName)
    if len(files_dir) == 0:
        return "1"
    else:
        for file_name in files_dir:
            number = int(file_name.translate(None, ".png"))
            if name < number:
                name = number

    name += 1
    return str(name)


def createDirsForImages():
    now = datetime.datetime.now()
    day = str(now.day)
    month = str(now.month)
    if int(day) < 10:
        day = '0' + day
    if int(month) < 10:
        month = '0' + month
    dayDirectory = day + '.' + month + '.' + str(now.year)
    if not os.path.exists(PATH + dayDirectory + '/'):
        os.makedirs(PATH + dayDirectory + '/')

    return (PATH + dayDirectory + '/')


def isDifferent(center):
    for i in points:
        if (i[0] == center[0] and i[1] == center[1]) or math.hypot(float(center[0] - i[0]), float(center[1] - i[1])) < 40.0:
            return False

    return True


def closest_color(color):
    colors = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        r_d = (r_c - color[0])**2
        g_d = (g_c - color[1])**2
        b_d = (b_c - color[2])**2
        colors[(r_d + g_d + b_d)] = name

    return colors[min(colors.keys())]


def is_in_bird(image, x, y, dx, dy):
    count = 0
    for i in range(0, 8):
        r, g, b = image[x + dx[i], y + dy[i]]
        try:
            color = rgb_to_name((int(r), int(g), int(b)))
        except:
            color = closest_color((int(r), int(g), int(b)))
        for pc in pigeon_colors:
            if pc in color:
                count += 1

    return count == 8


def findBirds(image, dx, dy):
    haarcascade = HaarCascade("pigeon1.0.xml")
    birds = image.findHaarFeatures(haarcascade)
    if birds:
        observations = []
        for bird in birds:
            if is_in_bird(image, bird.x, bird.y, dx, dx):
                observations.append([float(bird.x), float(bird.y)])

        if observations:
            xmeans_instance = xmeans(observations, [[0, 0]], ccore=False)
            xmeans_instance.process()
            centers = xmeans_instance.get_centers()
            for point in centers:
                if isDifferent(point):
                    points.append(point)


def captureAndSave():
    seconds = 0
    points = []
    camera = VirtualCamera("show/pigeons2.mp4", "video")
    while True:
        image = camera.getImage().flipHorizontal().scale(0.5)
        for i in range(1, 10):
            findBirds(image, [0, i, i, i, 0, -i, -i, -i],
                      [i, i, 0, -i, -i, -i, 0, i])

        if seconds == 10:
            layer = DrawingLayer((image.width, image.height))
            for point in points:
                layer.circle((point[0], point[1]), 20, color=(255, 255, 0))

            image.addDrawingLayer(layer)
            image.applyLayers()

            path = createDirsForImages()
            imagen = getNextImageName(path) + '.png'
            now = datetime.datetime.now()

            flew_in = 0
            flew_away = 0

            if len(os.listdir(path)) != 0:
                dbe = Bird.objects.filter(
                    daym=now.day, month=now.month, year=now.year)
                s = 0
                for entry in dbe:
                    s += entry.birdsDetected

                median = s / len(dbe)
                if len(points) != median:
                    new = len(points)
                    last = dbe[len(dbe) - 1]
                    # locs=getBirdLocations(points,string2list(last.birdsPositions))
                    if new > last.birdsDetected:
                        flew_in = new - last.birdsDetected
                    else:
                        flew_away = last.birdsDetected - new

            b = Bird(image_name=imagen, daym=now.day, month=now.month, year=now.year,
                     birdsDetected=new, flew_in=flew_in, flew_away=flew_away)
            b.save()
            image.save(path + imagen)

            seconds = 0
            points = []

        seconds += 1
        sleep(1.0)


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WildlifeDemo1.settings')
    django.setup()
    from show.models import Bird, Size, AdvancedStatsForMonth, AdvancedStatsForWeek

    # for image in os.listdir(PATH+"10.03.2017/"):
    # 	b=Bird(image_name=image, daym="10", month="3", year="2017", birdsDetected=1)
    # 	b.save()
    # Bird.objects.filter(daym="10",month="3",year="2017").delete()
    # AdvancedStatsForMonth.objects.all().delete()
    # AdvancedStatsForWeek.objects.all().delete()
    # Size.objects.all().delete()
    global points
    captureAndSave()
    # global sa
    # sa=sorted(Bird.objects.all(), key=lambda bird: (int(bird.year),int(bird.month),int(bird.daym)))
    # if len(Size.objects.all())==0:
    # 	s=Size(db_size=len(sa))
    # 	s.save()
    #  	divideIntoMonthSlots(sa)
    # 	divideIntoWeekSlots(sa)
    # else:
    # 	size=int(Size.objects.all()[0].db_size)
    # 	if size!=len(sa):
    # 		divideIntoMonthSlots(sa[size+1:])
    # 		divideIntoWeekSlots(sa[size+1:])
    # 		Size.objects.all().delete()
    # 		s=Size(db_size=len(sa))
    # 		s.save()
