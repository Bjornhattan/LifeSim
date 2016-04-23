# -*- coding: utf-8 -*-
import datetime, random, calendar, time, bisect, collections, json, os, shelve

phoneNoDB = []
startDate = datetime.date(2010, 1, 1)
today = datetime.date(2010, 1, 1)
characters = []
forenames = ["Dave","Liam","Kyle","James","Anthony","Daniel","Dan","Valentino","John","Chris","Chiles","Charlie","Connor","Darren","Matthew","James","Michael","Kevin","Tom","Thomas","Richard","Harry","Edmund","Alexander","Andreas","Andrew","Craig", "Kieren", "Rob", "Jon", "Mark", "Jacob", "Oliver", "William", "Mike", "Zac", "Isaac", "Joseph", "Joe", "Lucas", "Aaron", "Cameron", "Owen", "Seth", "Josh", "Ryan", "Jake", "Edward", "Richard", "George", "Freddie", "Sam", "Samuel", "Callum", "Rhys", "Ollie", "Hugo", "Max", "Oscar", "Aiden", "Theo", "Nathan", "Josh", "Bobby", "Luke", "Logan", "Henry", "Leo", "Riley", "Noah", "Archie", "Kai", "Harvey", "Toby", "Sebastian", "Freddie", "Louis", "Finlay", "Frederick", "Reuben", "Blake", "Theodore", "Felix", "Tristan", "Morgan", "Flynn", "Reggie", "Declan", "Jonathan", "Leighton", "Jason", "Alfred", "Maximilian", "Sean", "Rohan", "Myles", "Christian", "Robin", "Euan", "Francis", "Arlo", "Sidney", "Rahpael", "Eric", "Rufus", "Elias"]
fForenames = ["Laura","Fiona","Mary","Amy","Rachel","Louise","Natalie","Samantha","Tina","Alice","Charity"]
surnames = ["Rainton","Rodriguez","Carver","Curtis","Turnbull","Trumbull","Taylor","Sole","Salisbury","Derbyshire","Hall","Radcliffe","O'Donnell","Whitby","Waites","Wood","Mahon","Rodman","Mellows","Smith","Chapman","McDonald","Molinero","Miller","Morecambe","Shield","York", "Jacobson", "Daniels", "Watts", "Brown", "Johnson", "Lewis", "White", "Gray", "Black", "Green", "Davis", "Hart", "Hill", "Turner", "Jackson", "Scott", "Campbell", "Moore", "Adams", "Stone", "Steel", "Reynolds", "Collins", "Harris", "Clarke", "Edwards", "Lee", "Graham", "Carr", "Gardner", "Wilson", "Lawrence", "Martin", "Ellis", "Brooks", "Marshall", "Baker", "Parker", "Reid", "Atherton", "West", "Carpenter", "Fletcher", "Davison", "Cullen", "Abbott", "Adkins", "Anderson", "Armstrong", "Arher", "Ashby", "Griffin", "Greenwood", "Haley", "Hamilton", "Ashworth", "Atkinson", "Barry", "Bain", "Beck", "Banks", "Austin", "Hayden", "Harper", "Hays", "Henderson", "Baxter", "Boyd", "House", "Hood", "Higgens", "Joyce", "Jamison", "Jordan", "Clayton", "Kirk", "Knight", "Cole", "Daley", "Crouch", "Cox", "MacMillan", "Lowe", "Leslie", "Drake", "Donnelly", "Duncan", "Dunn", "McAllister", "McCoy", "Fischer", "Foster", "Fraser", "Faulkner", "McKay", "Glover", "Gilbert", "Moss", "Wheeler", "Whitaker", "Wright", "Terry", "Sullivan", "Stout", "Stokes", "Sharp", "Reed", "Burns", "Glaude", "Underwood", "Salt", "Tarrant", "Chester", "Hyde", "Sugar", "Park", "Oldman", "Field"]
towns = ["Grimsby", "Scunthorpe", "Hull", "Cleethorpes", "Louth"]
townPops = [50, 15, 10, 5, 5]
daysSinceFish = 65535
totalFish = 0
fbOpponents = ["Barnsley","Bradford","Bristol City","Chesterfield","Colchester","Coventry","Crawley","Crewe","Doncaster","Fleetwood","Gillingham","Leyton Orient","MK Dons","Notts County","Oldham","Peterborough","Port Vale","Preston","Rochdale","Scunthorpe","Sheffield Utd","Swindon","Walsall","Yeovil","Accrington","AFC Wimbledon","Burton","Bury","Cambridge","Carlisle","Cheltenham","Dagenham","Exeter","Hartlepool","Luton","Mansfield","Morecambe","Newport","Northampton","Oxford","Plymouth","Portsmouth","Shrewsbury","Southend","Stevenage","Tranmere","Wycombe","York","AFC Telford","Aldershot","Alfreton","Altrincham","Barnet","Braintree","Bristol Rovers","Chester","Dartford","Dover","Eastleigh","FC Halifax","FGR","Gateshead","Kidderminster","Lincoln","Macclesfield","Nuneaton","Southport","Torquay","Welling","Woking","Wrexham"]
fbFixtures = []
fbHistory = []
fbGoalComments = ["{team} score a marvellous goal!",
                  "It's an excellent goal for {team}",
                  "{team} have scored here at Blundell Park",
                  "An astounding free kick for {team} puts them up a goal",
                  "The {team2} keeper didn't stand a chance against that shot!",
                  "{team} score a critical header in the top corner",
                  "{team} score a well-deserved penalty. {team2} are gutted",
                  "What a goal for {team}! That's really lowered the {team2} morale",
                  "{team}'s striker slots the ball nicely in the bottom corner",
                  ]
                  
fbMissComments = ["{team}'s striker hit that too well",
                  "A disappointing strike for {team}",
                  "{team}'s manager isn't happy about that miss",
                  "{team} waste a free kick",
                  "A strong {team} attack comes to nothing",
                  "A shot that poor is never going past the {team2} keeper",
                  "{team2}'s keeper got that too easily. {team} need to do better"
                  ]
              
notifications = []
skills = ["strength",
          "athleticism",
          "intelligence",
          "artistic",
          "computers",
          "musical",
          "charisma",
          "eloquence"]


defaultStats = [[1, 20]] * 8  #The stats types contain lists of the lower and upper bounds for the character's generated stats
PSTeacherType = [[4,17], [8,18], [11,14], [5,14], [5,14], [5,14], [14,20], [11,20]]              
fishermanType = [[11,20], [11,20], [8,20], [1,10], [1,15], [7,15], [12,20], [6,20]]

def ChooseStats():
    while True:
        choice = input("You will now choose a way of distributing your skill points."
                       "\n[1] Choose two skills to focus on"
                       "\n[2] Distribute the points yourself"
                       "\n[3] Distribute the points randomly\n")
        try:
            choice = int(choice) - 1
            if choice > -1 and choice < 3:
                stats = [ChooseStatsTwo, ChooseStatsManual, ChooseStatsRandom][choice]()
                break
        except ValueError:
            pass
    return stats

def ChooseStatsTwo():
    chosenSkills=[]
    while True:
        choice = input("Choose your %s skill to focus on from the list below:\n"%("second" if chosenSkills else "first") +
                       "".join(["[%d] %s\n"%(idx + 1, skills[idx]) for idx in range(8) if idx not in chosenSkills]))
        try:
            choice = int(choice) - 1
            if choice > -1 and choice < 8 and choice not in chosenSkills:
                chosenSkills.append(choice)
        except ValueError:
            pass
        if len(chosenSkills) == 2:
            break 
    return [[13, 20] if idx in chosenSkills else [1, 15] for idx in range(8)]

def ChooseStatsRandom():
    return defaultStats
    
def ChooseStatsManual():
    print("You have 75 points to distribute between the 8 skills. You can put a maximum of 20 points into a skill.")
    finalSkills = [[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
    pointsLeft = 120
    while pointsLeft != 0:
        for idx in range(8):
            while pointsLeft != 0:
                print("Points remaining: %d"%pointsLeft)
                points = input("%s (%d): "%(skills[idx], finalSkills[idx][0]))
                try:
                    points = int(points)
                    if points <= pointsLeft and points >= 0 and finalSkills[idx][0] + points <= 20:
                        pointsLeft -= points
                        finalSkills[idx][0] += points
                        finalSkills[idx][1] += points
                        break
                except ValueError:
                    pass
        if pointsLeft > 0:
            print("You still have %d points left. You will now assign the remaining points."%pointsLeft)
    finalSkills += [[0,0]] * (8 - len(finalSkills))
    return finalSkills

def Indef(name):  #Returns 'a'/'an' plus name
    return "%s %s"%("an" if list(name)[0] in "aeiou" else "a", name)
    
def RandomDate(start, end): #Returns a random datetime.date object between start and end dates
    return start + datetime.timedelta(days = random.randrange((end - start).days))

def Ord(n): #Returns the ordinal version of n
    return str(n)+("th" if 4 <= n%100 <= 20 else {1:"st", 2:"nd", 3:"rd"}.get(n%10, "th"))

def DisplayDate(date): #Returns a human-readable date
    return "%s %s %s"%(calendar.day_name[date.weekday()], Ord(date.day), date.strftime("%B %Y"))

def WeightedChoice(weights): #Returns a weighted choice from a {choice: weight} dictionary
    totals = []
    runningTotal = 0
    for w in weights:
        runningTotal += w
        totals.append(runningTotal)
    rnd = random.random() * runningTotal
    return bisect.bisect(totals, rnd)

class Item():
    def __init__(self, *args, **kwargs):
        self.itemTypes = args[0]
        self.name = args[1]
        self.rating = 0
        for name, value in kwargs.items():
            setattr(self, name, value)
    def __repr__(self):
        return self.name
    
class Character():
    def __init__(self, statsType):
        self.achievements = []
        self.cash = 0
        self.GenPhoneNo()
        self.inv = []
        self.attributes = {}
        for idx in range(8): #Sets the character's stats according to the lower and upper bounds of the statsType list
            if type(statsType[idx]) == list:
                self.attributes[skills[idx]] = random.randint(statsType[idx][0], statsType[idx][1])
            else:
                self.attributes[skills[idx]] = statsType[idx]
    def AddCash(self, cash):
        self.cash += cash
    def AddItem(self, item, quantity=1):
        self.inv.extend([item]*quantity)
    def DisplayInv(self, selling=False, itemTypes=[]):
        items = collections.OrderedDict({})
        self.inv.sort(key = lambda item: item.name)
        for item in self.inv:
            if set(itemTypes) <= set(item.itemTypes):
                if item not in items:
                    items[item] = 1
                else:
                    items[item] += 1
        print("\n%sName                              Quantity   Type             Value(£)"%("#   " if selling else "") +
              "\n%s¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"%("¯¯¯¯" if selling else ""))
        if len(items) > 0:
            for idx, item in enumerate(items):
                print("%s%s%s%d%s%s%s%s"%(str(idx + 1) + " " * (4 - len(str(idx))) if selling else "",
                                          item.name, " " * (34 - len(item.name)),
                                          items[item], " " * (11 - len(str(items[item]))),
                                          item.itemTypes[0].title(), " " * (17 - len(item.itemTypes[0])),
                                          str(item.price) if hasattr(item, "price") else "N/A") + "\n")
            return dict([(idx, [item, items[item]]) for idx, item in enumerate(items)])
        else:
            print("\n" + " " * 33 + "Empty\n\n")
                                    
    def RemoveItem(self, item, quantity=1):
        for i in range(quantity):
            if self.HasItem(item):
                self.inv.remove(item)
    def HasItem(self, item):
        return item in self.inv
    def HasItemOfType(self, itemTypes):
        for item in self.inv:
            if set(itemTypes) <= set(item.itemTypes):
                return True
    def GetItemsOfType(self, itemTypes):
        return [item for item in self.inv if set(itemTypes) <= set(item.itemTypes)]
    def GetBestItemOfType(self, itemTypes):
        items = self.GetItemsOfType(itemTypes)
        items.sort(key = lambda item: item.rating)
        return items[-1]
    def PrintInfo(self):
        print ("\n{0}"
                "\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"
                "\nPlace of birth: {1}"
                "\nDate of birth: {2}"
                "\nAge: {3}"
                "\nHeight: {4}cm"
                "\nStrength: {5}"
                "\nAthleticism: {6}"
                "\nIntelligence: {7}"
                "\nArtistic ability: {8}"
                "\nComputing: {9}"
                "\nMusical ability: {10}"
                "\nCharisma: {11}"
                "\nEloquence: {12}"
                "\n{13}".format(self.FullName(),
                                self.placeOfBirth,
                                self.DOBString(),
                                self.CalcAge(),
                                round(self.CalcHeight(), 1),
                                self.strength,
                                self.athleticism,
                                self.intelligence,
                                self.artistic,
                                self.computers,
                                self.musical,
                                self.charisma,
                                self.eloquence,
                                "Player relationship: %d"%self.CalcPlayerRelation() if self.charType != "player" else ""))
    def __getattr__(self, name):
        if name in self.__getattribute__("attributes"):
            return self.attributes[name]
        else:
            raise AttributeError
    def EditStat(self, stat, val):
        maxLevel = min(5*self.CalcAge(), 90)
        finalStat = self.attributes[stat] + val
        if finalStat >= 1 and finalStat <= 20:
            self.attributes[stat] = finalStat
    def IsPlayer(self):
        if self.charType == "player":
            return True
    def CalcOverall(self):
        overall = 0
        for attr in self.attributes:
            overall += attributes[attr]
        return int(round(overall/8))
    def GenPhoneNo(self):
        while True:
            phoneNo = "087%d"%random.randint(10000000,99999999)
            if phoneNo not in phoneNoDB:
                self.phoneNo = phoneNo
                phoneNoDB.append(phoneNo)
                break
    def DOBString(self):
        return DisplayDate(self.dateOfBirth)
    def FullName(self):
        return "%s %s"%(self.forename, self.surname)
    def CalcPlayerRelation(self, minrel=0, maxrel=180):
        gap = 0
        playerIndex = GetPlayerIndex()
        for attr in self.attributes:
            gap += abs(getattr(self, attr) - getattr(GetPlayer(), attr))
        self.playerRelation = max(maxrel-gap,minrel)
        return self.playerRelation
    def CalcAge(self, days=False):
        dob = self.dateOfBirth
        if not days:
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        else:
            return (today - dob).days
    def CalcHeight(self):
        if self.CalcAge() >= 18:
            self.height = self.potHeight
            return self.height
        else:
            if random.randint(0,7) == 7:
                self.height += 4.4/52.2
            return self.height
    def AddAchievement(self, achievement):
        if achievement not in self.achievements:
            self.achievements.append(achievement)
            notifications.append("New achievement: " + achievement.name)
            if len(achievement.rewards) != 0:
                notifications.append("Reward added!")
            achievement.Reward(self)
    def DisplayAchievements(self):
        print("\n                             Achievements"
              "\n¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"
              "\n")
        if len(self.achievements) == 0:
            print("                       You have achieved nothing\n")
        for achievement in self.achievements:
            print("%s-%s-\n%s%s\n"%(" " * round((68 - len(achievement.name))/2), achievement.name,
                                  " " * round((70 - len(achievement.desc))/2), achievement.desc))

class Achievement():
    def __init__(self, name, desc, rewards=[]):
        self.name = name
        self.desc = desc
        self.rewards = rewards
    def Reward(self, char):
        for reward in self.rewards:
            if type(reward).__name__ == "int":
                char.AddCash(reward)
            elif type(reward).__name__ == "Character":
                char.AddItem(reward)

                
AchFishing1 = Achievement("Gone Fishing", "Go fishing in the Humber")
AchFishing2 = Achievement("We Only Sing When We're Fishing", "Catch 25 fish")
AchFishing3 = Achievement("Nanofishing", "Buy the Grimsby Institue Nano Tube Rod")
AchCollecting1 = Achievement("Grimsby Kit","Own the whole Grimsby Town kit") # This is a new achievement!

CodFish = Item(["food", "fish"], "Cod", price = 5)
CarpFish = Item(["food", "fish"], "Carp", price = 12)
CobblerFish = Item(["food", "fish"], "River Cobbler", price = 16)
TroutFish = Item(["food", "fish"], "Trout", price = 24)
ForkbeardFish = Item(["food", "fish"], "Greater Forkbeard", price = 56)
Vendace = Item(["food", "fish"], "Vendace", price = 230)

fish = [CodFish, CarpFish, CobblerFish, TroutFish, ForkbeardFish, Vendace]

AmateurRod = Item(["rod"], "Amateur Rod", price=10, rating=4, fishChances=[25, 7, 3, 1, 0, 0])
TrainingRod = Item(["rod"], "Fisherman's Training Rod", price=50, rating=5, fishChances=[20, 10, 5, 2, 1, 0])
RealRod = Item(["rod"], "Fisherman's Real Rod", price=250, rating=6, fishChances=[7, 7, 5, 2, 1, 0])
OfficialRod = Item(["rod"], "GTFC Official Rod", price=500, rating=7, fishChances=[10, 10, 10, 7, 4, 1])
NanotubeRod = Item(["rod"], "Grimsby Institute NanoTube Rod", price=5000, rating=8, fishChances=[4, 4, 4, 4, 3, 2])
MonacoRod = Item(["rod"], "Monaco Rod", price=10000, rating=10, fishChances=[1, 1, 1, 1, 2, 2])

rods = [AmateurRod, TrainingRod, RealRod, OfficialRod, NanotubeRod, MonacoRod]

OldShoe = Item(["waste"], "Old Shoe")
PlasticBag = Item(["waste"], "Plastic Bag")
RustyBar = Item(["waste"], "Rusty Bar")

fishingWaste = [OldShoe, PlasticBag, RustyBar]

GrimsbyShirt = Item(["clothing","shirt","footballshirt","grimsbymerch"],"Grimsby Shirt",price=40)
GrimsbyScarf = Item(["clothing","scarf","footballscarf","grimsbymerch"],"Grimsby Scarf",price=10)
GrimsbyShorts = Item(["clothing","trousers","footballshorts","grimsbymerch"],"Grimsby Shorts",price=10)
GrimsbySocks = Item(["clothing","socks","footballsocks","grimsbymerch"],"Grimsby Socks",price=10)

grimsbyKit = [GrimsbyShirt,GrimsbyScarf,GrimsbyShorts,GrimsbySocks] # Sold at Shop 3

BookFC001 = Item(["book","fictionbook","childrensbook"],"The Happy Dragon",price=7)
BookFC002 = Item(["book","fictionbook","childrensbook"],"Paul the Platypus",price=7)
BookNC001 = Item(["book","nonfictionbook","childrensbook"],"MDE Guide to Addition",price=10) # Should increase Intelligence somehow?
BookNC002 = Item(["book","nonfictionbook","childrensbook"],"School Yard Politics",price=10) # Should increase Charisma somehow?
BookFY001 = Item(["book","fictionbook","youngbook"],"King of the Torus",price=15)
BookFY002 = Item(["book","fictionbook","youngbook"],"Of Rats and Rascals",price=15)
BookNY001 = Item(["book","nonfictionbook","youngbook"],"Linguistics: Broken Down",price=20) # Should increase Eloquence somehow?
BookNY002 = Item(["book","nonfictionbook","youngbook"],"ProgrammingIsFun",price=20) # Should increase Computing somehow?
BookNY003 = Item(["book","nonfictionbook","youngbook", "fishing"], "Fishing for Fun", price=15)
BookFA001 = Item(["book","fictionbook","adultbook"],"The Goddess of Burton Manor",price=30)
BookFA002 = Item(["book","fictionbook","adultbook"],"Sport of Chairs",price=30)
BookNA001 = Item(["book","nonfictionbook","adultbook"],"If Escher Did It, You Can",price=40) # Should increase Artistic somehow? 
BookNA002 = Item(["book","nonfictionbook","adultbook"],"Mozart Reconsidered",price=40) # Should increase Musical somehow?
BookNA003 = Item(["book", "nonfictionbook", "adultbook", "fishing"], "Fish of the Humber", price=30)

Books = [BookFC001,BookFC002,BookNC001,BookNC002,BookFY001,BookFY002,BookNY001,BookNA002,BookFA001,BookFA002,BookNA001,BookNA002] # Sold at Shop 5

def GetPlayer():  #getIdx=True will return the player's index in the characters list
    for char in characters:
        if char.IsPlayer():
            return char

def GetPlayerIndex():
    for i, char in enumerate(characters):
        if char.IsPlayer():
            return i

def GetType(typeFilter, getIdx = False, chars = characters):
    if getIdx:
        return [chars.index(char) for char in chars if char.charType == typeFilter]
    else:
        return [char for char in chars if char.charType == typeFilter]
    
def GetAttr(attr, value = None, getIdx = False, chars = characters):
    matches = []
    for idx, char in enumerate(chars):
        if hasattr(char, attr):
            matches.append(idx if getIdx else char)
            if value is not None and getattr(char, attr) != value:
                del(matches[-1])
    return matches
    
def Chargen(charType, **kwargs):
    if charType == "player":
        forename = input ("What is your forename? ").title()
        surname = input ("What is your surname? ").title()
        placeob = input ("Where were you born? ").title()
        dob = datetime.date(2000, 1, 1)
        stage = ""
        statsType = ChooseStats()
    else:
        forename = random.choice(forenames)
        surname = random.choice(surnames)
        if charType == "shopowner":
            stage = "work"
        elif charType=="psteacher":
            lowerDate = datetime.date(1950, 1, 1)
            upperDate = datetime.date(1990, 12, 31)
            stage = "work"
            statsType = PSTeacherType
        elif charType=="classmate":
            lowerDate = datetime.date(1999, 9, 1)
            upperDate = datetime.date(2000, 8, 31)
            stage = "primary"
            statsType = defaultStats
        elif charType=="customclassmate":
            lowerDate = datetime.date(1999, 9, 1)
            upperDate = datetime.date(2000, 8, 31)
            stage = "primary"
            statsType = kwargs["stats"]
        elif charType=="friend":
            if GetPlayer().stage=="primary":
                lowerDate = datetime.date(1997, 1, 1)
                upperDate = datetime.date(2002, 12, 31)
                stage = "work"
                statsType = defaultStats
            elif GetPlayer().stage=="":
                lowerDate = datetime.date(1996, 1, 1)
                upperDate = datetime.date(2000, 12, 31)
                stage = "work"
                statsType = defaultStats
        elif charType=="fisherman":
            lowerDate = datetime.date(today.year - 70, 1, 1)
            upperDate = datetime.date(today.year - 30, 12, 31)
            stage = "work"
            statsType = fishermanType
            
        if "dob" in kwargs:
            dob = kwargs["dob"]
        else:
            dob = RandomDate(lowerDate, upperDate)
        if "pob" in kwargs:
            placeob = kwargs["pob"]
        else:
            placeob = towns[WeightedChoice(townPops)]
        if "stats" in kwargs:
            statsType = kwargs["stats"]

    char = Character(statsType)
    char.charType = charType
    char.forename = forename
    char.surname = surname
    char.placeOfBirth = placeob.title()
    char.dateOfBirth = dob
    char.height = random.normalvariate(4.4*char.CalcAge(True)/365 + 95, 7.5)
    char.potHeight = char.height + 4.4 * (18 - char.CalcAge(True)/365)
    char.stage = stage
    for name, value in kwargs.items():
        setattr(char, name, value)
    characters.append(char)
  
def PrimarySchool():
    print("Today is your first day at a new Primary School in " + GetPlayer().placeOfBirth)
    characters[GetPlayerIndex()].__setattr__("stage", "primary")
    startingIdx = len(characters)
    classMatesIndices = list(range(startingIdx, startingIdx + 30))
    randomClassMates = input("Would you like random classmates? [y/n]").lower() # Saying Yes doesn't seem to work perfectly. Also, part of me wants the ability to have some random classmates and some chosen, but this is very hard to do...
    if randomClassMates == "y":
        for n in range(30):
            Chargen("classmate")
    else:
      for n in range(30):
        print("%s Classmate:\n"%Ord(n+1))
        forename = input("Forename: ")
        surname = input("Surname: ")
        placeOfBirth = input("Place of birth: ")
        stats = ChooseStats()
        Chargen("customclassmate", forename=forename, surname=surname, placeOfBirth=placeOfBirth, stats=stats)
    for n in range(3):
        Chargen("psteacher")
    classMatesIndices.sort(key = lambda idx: characters[idx].CalcPlayerRelation())
    print("Your top three friends are:\n%s\n%s\n%s"%(characters[classMatesIndices[-1]].FullName(),
                                                     characters[classMatesIndices[-2]].FullName(),
                                                     characters[classMatesIndices[-3]].FullName()))
    
def PSEvent(charIndex):
    char = characters[charIndex]
    fullName = char.FullName()
    eventNo = random.randint(1,400)
    if eventNo == 1 or (eventNo == 3 and char.intelligence > 10):
        print(fullName + " hands in an excellent project.")
        characters[charIndex].EditStat("intelligence", 1)
    if eventNo == 2 or (eventNo == 3 and char.intelligence < 11):
        print(fullName + " rushes a homework.")
        characters[charIndex].EditStat("intelligence", -1)
    if eventNo == 4:
        print(fullName + " does well in the ICT suite.")
        characters[charIndex].EditStat("computers", 1)

def GiveHomework():
    homeworkTypes = [("Maths Homework", "maths"), ("Science Homework", "science"), ("English Homework", "english"), ("Generic Homework", "generic")]
    if today.weekday() == 4:
        dateDue = today + datetime.timedelta(days=3)
        homeworkType = random.choice(homeworkTypes)
        Homework = Item([homeworkType[1], "homework"], homeworkType[0], due=dateDue)
        characters[GetPlayerIndex()].AddItem(Homework)
        print("You have been given %s to complete by %s"%(homeworkType[0], DisplayDate(dateDue)))

def CheckHomework():
    if today.weekday() == 0:
        homeworks = GetAttr("due", today, False, GetPlayer().GetItemsOfType(["homework"]))
        if homeworks:
            homework = homeworks[0]
            print("You hand in your %s"%homework.name)
            characters[GetPlayerIndex()].RemoveItem(homework)

def DoHomeWork():
    homeworks = GetAttr("due", None, False, GetPlayer().GetItemsOfType("homework"))
    if homeworks:
        homeworks.sort(key = lambda item: item.due)
        homework = homeworks[-1]
        
    
def Help(topic):
    if topic == "locations":
        print("community - the community centre."
              "\nfish - go fishing!"
              "\nshops - the shopping precinct.")
    elif topic == "commands":
        print("ach - display your achievements in game"
              "cash - display your $$$"
              "\nhelp - show help"
              "\ninv - display your inventory"
              "\nJump - travel forwards in time"
              "\nlist - list the people you know"
              "\nsave - save the game"
              "\nvisit - visit a location")
    elif topic == "":
        while True:
            topic = input("Topics:"
                          "\n\n[1] Commands"
                          "\n[2] Locations"
                          "\nWhich topic would you like help on? ")
            try:
                topic = int(topic) - 1
                if topic <= 2 and topic >= 0:
                    break
            except ValueError:
                pass
        Help(["commands", "locations"][topic])
    else:
        print("Unkown help topic")
        
def Visit(place):
    global daysSinceFish
    if place == "community":
        Chargen("friend")
        print("You have met " + characters[-1].FullName())
    elif place == "fish":
        if daysSinceFish>2:
            characters[GetPlayerIndex()].AddAchievement(AchFishing1)
            Fish()
            daysSinceFish = 0
        else:
            print("The fishermen tell you that you should wait before fishing again.")
    elif place == "shops":
        Shopping()
    elif place == "stadium":
        FbStadium()
    else:
        print("Invalid location. Type 'help locations' for a list of locations.")

def Fish():
    global totalFish
    totalFishBefore = totalFish
    fishermenIdx = GetAttr("rota", today.weekday(), True, GetType("fisherman"))
    if len(fishermenIdx) == 0:
        Chargen("fisherman", rota=today.weekday(), inv=rods*10, cash=500)
        wardenIdx = len(characters)-1
    else:
        wardenIdx = fishermenIdx[0]
    warden = characters[wardenIdx]
    wardenName = warden.FullName()
    print("The fishermen invite you to go fishing."
          "\nThe day's warden, %s, welcomes you onto the boat."%wardenName)
    if not GetPlayer().HasItemOfType("rod"):
        print(wardenName + " sees that you don't have a rod."
              "\nHe goes over to his collection and pulls out an amateur rod and gives it to you.")
        characters[GetPlayerIndex()].AddItem(AmateurRod)
    print("He offers you the chance to buy a rod.")
    buyRod  = input("Would you like to buy a new rod? [y/n]").lower()
    if buyRod == "y":
        Trade(wardenIdx, ["rod"])
    rod = GetPlayer().GetBestItemOfType(["rod"])
    if rod == NanotubeRod:
        characters[GetPlayerIndex()].AddAchievement(AchFishing3)
    print("You take out your %s..."%rod.name)
    for attempt in range(rod.rating):
        time.sleep(1)
        if random.randint(1, 25) < rod.rating*1.5 + round(GetPlayer().strength/5):
            print(random.choice(["You caught a fish!", "That one met its end!", "You got one!", "Nice catch!", "Pro catch!", "You caught one!"]))
            characters[GetPlayerIndex()].AddItem(fish[WeightedChoice(rod.fishChances)])
            totalFish += 1
        else:
            if random.randint(1,3) == 3:
                waste = random.choice(fishingWaste)
                characters[GetPlayerIndex()].AddItem(waste)
                print("You caught %s"%Indef(waste.name))
            else:
                print(random.choice(["Nice miss", "You didn't get that one.", "That one got away!", "That fish didn't bite.", "You missed!", "You missed that one."]))
        time.sleep(1)
    if totalFish > 24:
        characters[GetPlayerIndex()].AddAchievement(AchFishing2)
    if totalFishBefore == totalFish:
        print("You caught nothing! You may wish to buy a better rod.")
    if GetPlayer().HasItemOfType(["fish"]) and input("%s offers to buy some fish from you."
                                                    "\nWould you like to sell fish to %s? [y/n]"%(wardenName, wardenName)).lower() == "y":
        Trade(wardenIdx, ["fish"], False)

class Shop:
    def __init__(self, ownerIndex, name="", desc="", itemTypes=[], buy=False, sell=True):
        self.name = name
        self.desc = desc
        self.ownerIndex = ownerIndex
        self.itemTypes = itemTypes
        self.buy = buy
        self.sell = sell

shops = []
        
#Make your shops here
Chargen("shopowner", stats=[14,17,7,12,11,5,14,3],
        forename="Alex", surname="Rodman",
        dob=datetime.date(1987, 2, 15), pob="Sutton Coldfield",
        height = 188, potheight = 188,
        inv = rods*15 + [BookNA003, BookNY003]*5,
        cash = 5000)
Rodmans = Shop(len(characters) -1, "Rodman's Fishing Equipment", ["rod", "fishing"], buy=True)
shops.append(Rodmans)
#Grimsby Town Tickets" # Works well
#Grimsby Town Merchandise" # Added items
#Bailey & Severn Travel" # Requires custom menu
#History Bookstore" # Added items
#Athletix Sportswear") # Not done yet

def Shopping():
    print("Welcome to the shopping precinct")
    for i, shop in enumerate(shops):
        print("[%d]"%(i+1), shop.name)
    while True:
        shopNo = input("Which number shop would you like to visit? (0 to exit) ")
        try:
            shopNo = int(shopNo) 
            if shopNo > 0 and shopNo <= len(shops):
                shopNo -= 1
                break
            elif shopNo == 0:
                return
        except:
            pass
    shop = shops[shopNo]
    print("Welcome to", shop.name)
    while True:
        if shop.buy:
            if shop.sell:
                while True:
                    bs = input("Are you buying(1) or selling(2)? ")
                    if bs in ["1", "2"]:
                        break
                if bs == "1":
                    buy = True
                else:
                    buy = False
            else:
                buy = False
        elif shop.sell:
            buy = True
        if buy:
            Trade(shop.ownerIndex, shop.itemTypes)
        else:
            Trade(shop.ownerIndex, shop.itemTypes, False)
        while True:
            stay = input("Stay in " + shop.name + "? [y/n]").lower()
            if stay in ["y", "n"]:
                break
        if stay == "n":
            break


def Trade(vendorIdx, itemTypes=[], buy=True):
    vendor = characters[vendorIdx]
    if buy:
        sellerIdx = vendorIdx
        buyerIdx = GetPlayerIndex()
    else:
        sellerIdx = GetPlayerIndex()
        buyerIdx = vendorIdx
    seller = characters[sellerIdx]
    buyer = characters[buyerIdx]
    while True:
        items = seller.DisplayInv(True, itemTypes)
        print("%s's cash: £%d"%(vendor.forename, vendor.cash))
        print("Your cash: £%d"%GetPlayer().cash)
        if items == None:
            print("%s no items to sell!"%("You have" if not buy else seller.forename + " has"))
            break
        if buyer.cash == 0:
            print("%s ran out of cash!"%("You" if buy else buyer.forename))
            break
        itemNo = input("Number of item to %s (0 to exit): "%("sell" if not buy else "buy"))
        try:
            itemNo = int(itemNo) - 1
            if itemNo >= 0 and itemNo < len(items):
                item = items[itemNo][0]
                print(item.name)
                itemCount = items[itemNo][1]
                if itemCount > 1:
                    while True:
                        itemQuantity = input("How many would you like to %s? (0 for none)"%("sell" if not buy else "buy"))
                        try:
                            itemQuantity = int(itemQuantity)
                            if itemQuantity >= 0 and itemQuantity <= itemCount:
                                break
                        except ValueError:
                            pass
                else:
                    itemQuantity = 1
                
                totalPrice = item.price * itemQuantity    
                if itemQuantity > 0 and itemQuantity <= itemCount and buyer.cash >= totalPrice:
                    characters[sellerIdx].RemoveItem(item, itemQuantity)
                    items[itemNo][1] -= 1
                    characters[sellerIdx].AddCash(totalPrice)
                    characters[buyerIdx].AddCash(-totalPrice)
                    characters[buyerIdx].AddItem(item, itemQuantity)
                elif itemQuantity == 0:
                    break
                else:
                    print("%s not have enough cash!"%("You do" if buy else buyer.forename + " does"))
                    
            elif itemNo == -1:
                break
        except ValueError:
            pass
    
def FixtureGen(): #Returns the name of the opposing team in the upcoming football game and the date of the game as datetime.date object
    if (today - startDate).days % 14 + 7 - startDate.weekday() in range(5, 12):
        daysUntilMatch = 6 - (today.weekday() + 1) % 7
    else:
        daysUntilMatch =  13 - (today.weekday() + 1) % 7
    nextMatchDate = today + datetime.timedelta(days=daysUntilMatch)
    opponent = random.choice(fbOpponents)
    return [opponent, nextMatchDate]
    
def FbTicket():
    fixture = fbFixtures[-1]
    if today > fixture[1]:
        fixture = FixtureGen()
        fbFixtures.append(fixture)
    elif today == fixture[1] and fixture in fbHistory:
        fixture = FixtureGen()
        fixture[1] += datetime.timedelta(days=14)
        fbFixtures.append(fixture)
    print("Next Match: GTFC vs. " + fixture[0] +
          "\nDate: " + DisplayDate(fixture[1]) +
          "\nPrice: £15")
    ticketShop = input ("Would you like to buy tickets? [y/n]").lower()
    if ticketShop == "y":
        if GetPlayer().cash >= 15:
            ticket = Item("ticket", "GTFC vs. %s Tickets"%fixture[0], price=15, fixture=fixture)
            characters[GetPlayerIndex()].AddCash(-15)
            characters[GetPlayerIndex()].AddItem(ticket)
        else:
            print("You don't have enough cash.")

def FbStadium():
    fixture = fbFixtures[-1]
    if fixture[1] == today and fixture not in fbHistory:
        if GetPlayer().HasItemOfType("ticket"):
            playerTickets = GetPlayer().GetItemsOfType("ticket")
            for ticket in playerTickets:
                if ticket.fixture == fixture:
                    characters[GetPlayerIndex()].RemoveItem(ticket)
                    FbGame()
        else:
            print("You do not have a ticket for today's game.") # Buy on the gate for £17 perhaps? Simulates reality where buy on the day tickets cost more...
    else:
        print("There is no game on today. The next one is on " + DisplayDate(fixture[1]))

def FbGame():
    fbHistory.append(fbFixtures[-1])
    opponent = fbFixtures[-1][0]
    homeScore = 0
    awayScore = 0
    print("Grimsby Town face off against %s here at Blundell Park"%opponent)
    time.sleep(2)
    print("And it's off!")
    for i in range(8):
        time.sleep(3)
        teams = [opponent, "Grimsby Town"]
        team = teams.pop(random.randint(0,1))
        team2 = teams[0]
        if random.randint(1,5) > 3:
            if team == opponent:
                awayScore += 1
            else:
                homeScore += 1
            print(random.choice(fbGoalComments).format(team=team, team2=team2))
        else:
            print(random.choice(fbMissComments).format(team=team, team2=team2))
    time.sleep(3)
    if homeScore > awayScore:
        print("Grimsby Town win %d-%d! What a game!"%(homeScore, awayScore))
    elif awayScore > homeScore:
        print("%s have won today's game %d-%d"%(opponent, awayScore, homeScore))
    else:
        print("It's a %d-%d draw for Grimsby Town and %s"%(homeScore, awayScore, opponent))

def ShowAchievements(*args):
    GetPlayer().DisplayAchievements()
    
def Cash(*args):
    print("£%d"%GetPlayer().cash)
    
def List(*args):
    for char in characters:
        char.PrintInfo()
        
def SaveGame(*args):
    d = shelve.open("save")
    d['chars'] = characters
    d.close()
    d = shelve.open("save")
    print(d['chars'][0].FullName())
    
def Inv(*args):
    GetPlayer().DisplayInv()
    
commands = {"inv": Inv,
            "list": List,
            "help": Help,
            "visit": Visit,
            "cash": Cash,
            "ach": ShowAchievements,
            "save": SaveGame}
            
print("\n                      |    |  |¯¯  |¯¯"
      "\n                      |    |  |--  |--"
      "\n                      |__  |  |    |__\n"
      "\n                      |¯¯¯   |  |\\  /|"
      "\n                      |___   |  | \\/ |"
      "\n                          |  |  |    |"
      "\n                       ___|  |  |    |\n\n"
      "\n                          _"
      "\n                         |o|"
      "\n                     __  |o|    ___"
      "\n                    |]]| |o|_  / _ \  _"
      "\n              ______|()|_| []|_|/_\|_|o|______"
      "\n\n\nWelcome to LifeSim v6!"
      "\nTo progress the day, strike 'Enter'."
      "\nEnter commands to do things, type 'help commands' for a list."
      "\nFor help on a certain topic, type 'help <topic>'."
      "\nEnjoy!\n")

Chargen("player")
GetPlayer().PrintInfo()
while input("Do you wish to keep this character? [y/n]").lower() != "y":
    del(characters[-1])
    Chargen("player")
    GetPlayer().PrintInfo()
characters[GetPlayerIndex()].AddCash(10000)
fbFixtures.append(FixtureGen())

while True: #Main game loop
    daysPast = 0
    while daysPast < 45000:
        for i in range(len(notifications)):
            print(notifications.pop(0))
        today = datetime.date(2010, 1, 1) + datetime.timedelta(days=daysPast)
        if GetPlayer().stage != "primary" and today.weekday() == 0:
            PrimarySchool()
        cmd = input(DisplayDate(today) + " ").lower().split()
        if len(cmd) != 0:
            if cmd[0] == "jump" and len(cmd) > 1:
                    try:
                        days = int(cmd[1])
                        if days < 0:
                            print("You cannot travel back in time")
                        else:
                            daysPast += days
                    except ValueError:
                        print("Invalid number of days")
            if cmd[0] in commands:
                commands[cmd[0]]("".join(cmd[1:]))
            elif cmd[0] != "jump":
                print("Unknown command")
        else:
            if GetPlayer().stage == "primary" and today.weekday() < 5:
                CheckHomework()
                GiveHomework() # We should probably embeliish homework somewhat...
                for charIndex in range(len(characters)):
                    if characters[charIndex].stage == "primary":
                        PSEvent(charIndex)
            if today.weekday() == 6:
                print("You have been given £5.")
                characters[GetPlayerIndex()].cash += 5
                if today.year == 2014 and today.month == 7 and today.day == 14:
                    print("Happy July 14th 2014, everyone!") # Had to be done!
            currentHeight = GetPlayer().height
            newHeight = GetPlayer().CalcHeight()
            heightDif = (newHeight - currentHeight) * 10
            if heightDif > 0:
                notifications.append("You've grown by %dmm!"%round(heightDif))
            daysPast += 1
            daysSinceFish += 1
    restart = input("You are dead. Do you wish to run the simulation again? [y/n]").lower()
    if restart.lower() == "n":
        break
