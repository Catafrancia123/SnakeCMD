from saveload import detectSave, detectSettings, loadSystemSave, loadSettingsSave
from rich import print as rprint
from clear import clear
from checklevel import calculateBadge
from player import startup
from translations import langset
import sys
import os
import random

# do not touch!
version = "1.0"
compileDate = "26-07-2022"

# find systems and generate list
pathToOses = './oses/'
sys.path.insert(0, pathToOses)
sys.path.insert(0, './lang/')
osesDir = os.listdir(pathToOses)

# sanitize list
osArrayUnsorted = []
for x in osesDir:
    if x == "__pycache__":
        continue
    else:
        x = x.replace('.py', '')
        osArrayUnsorted.append(x)

# import systems
for x in osArrayUnsorted:
    globals()[x] = __import__(x)

# sort array into new array (this is probably inefficient but whatever)
finished = False
arrayCounter = 0
osArray = []
while finished == False:
    arraySelect = random.randrange(0, len(osArrayUnsorted))
    xobj = eval(osArrayUnsorted[arraySelect]).system()
    if xobj.listinbootmenu == arrayCounter:
        osArray.append(osArrayUnsorted[arraySelect])
        osArrayUnsorted.pop(arraySelect)
        arrayCounter +=1
    else:
        continue

    if len(osArrayUnsorted) == 0:
        finished = True

def loadSettings(system):
    xsys = osArray[system]
    xobj = eval(xsys).system()
    x = loadSystemSave(xobj.shortname)
    if x == False:
        print()
    else:
        xlevel = x
        xbadge = calculateBadge(xlevel, xobj.prolevel)

        if hasattr(xobj, "systemunlock"):
            xu = "system" + xobj.systemunlock
            xun = osArray.index(xu)
            xunlo = eval(osArray[xun]).system()
            xunlock = xunlo.unlocklevel
            xsystem = xobj.systemunlock
        else:
            xsystem = False
            xunlock = False

        systemarray = [xobj.shortname, xlevel, xobj.prolevel, xbadge, xobj.startupstring, xsystem, xunlock]

        startup(systemarray)

def boot():

    langobj = loadSettingsSave("lang")
    if langobj == False:
        langobj = langset()
    try:
        globals()[langobj] = __import__(langobj)
    except:
        langobj = "en_US"
        globals()["en_US"] = __import__("en_US")

    detectSettings()
    detectSave()

    global lang
    lang = eval(langobj).language()

    while True:
        clear()
        rprint(lang.sparrow)
        rprint(lang.version.format(version, compileDate))
        rprint(lang.dev)

        bmc = 1 # boot menu counter
        for x in osArray:
            xobj = eval(x).system()
            systemexists = loadSystemSave(xobj.shortname)
            if systemexists == False:
                rprint(lang.notUnlocked.format(bmc, xobj.name, xobj.unlocklevel, xobj.requiredstring))
                bmc += 1
            else:
                systembadge = calculateBadge(systemexists, xobj.prolevel)
                print(str(bmc) + '. ' + xobj.name, systembadge)
                bmc += 1

        choice = input()
        if choice == "":
            print()
        elif choice == "credits":
            clear()
            rprint(lang.credits1)
            print()
            rprint("[#af005f]Catafrancia[/#af005f]") 
            print()
            rprint(lang.credits2)
            rprint("🇺🇸 American English (en_US) - [#af005f]Catafrancia[/#af005f]")
            print()
            input()
        elif choice == "chlang":
            langobj = langset()
            globals()[langobj] = __import__(langobj)
            lang = eval(langobj).language()
        else:
            if not choice.isdigit() or int(choice) > len(osArray):
                clear()
                boot()
            choice = int(choice) - 1
            loadSettings(choice)

boot()
