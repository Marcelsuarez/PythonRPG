import json
import math
import random
import time
import pprint
from copy import copy




class Move(object):


    def __init__(self, name, dmg, phys, cost, func, pri, id):
        self.name = name
        self.dmg = dmg
        self.cost = cost
        self.phys = phys
        self.id = id
        self.func = func
        self.pri = pri

    def __str__(self):
        return "***Name: " + self.name + " Dmg: " + str(self.dmg) + " Is phys: " + str(self.phys)

    def __repr__(self):
        return str(self)


movedict = {

    # name, dmg, is phys? , cost, function name, priority level, id
    "Axe Breaker" : Move("Axe Breaker", 1.5, True, 2, "", 0, 0),
    "Battle Roar" : Move("Battle Roar", 0, False, 2, "roar", 0, 1),
    "Slime Rush" : Move("Slime Rush", 1.5, True, 0, "", 0, 2),
    "Attack" : Move("Attack", 1, True, 0, "", 0, 3),
    "Defend" : Move("Defend", 0, False, 0, "defense", 1, 4),
    "Slash" : Move("Slash", 1.5, True, 2, "", 0, 5),
    "Vampiric Strike" : Move("Vampiric Strike", 1.3, True, 3, "", 0, 6),
    "Sanguimancy" : Move("Sanguimancy", 1.2, False, 3, "lifesteal", 0, 7),
    "Crimson Tide" : Move("Crimson Tide", 1.4, False, 2, "", 0, 8),
    "Dragon Breath" : Move("Dragon Breath", 0, False, 4, "firebreath", 0, 9),
    "Meditate" : Move("Meditate", 0, False, 0, "recovermp", 0, 10),
    "Heal" : Move("Heal", 0, False, 3, "heal", 0, 11),
    "Toxic Cloud" : Move("Toxic Cloud", 0, False, 3, "poison", 0, 12),
    "Ancient Flame" : Move("Ancient Flame", 1.1, False, 2, "flame", 0, 13),
    "Summon Dragon" : Move("Summon Dragon", 0, False , 5, "sd", 0,14),
    "Ember" : Move("Ember", 0, False, 0, "firebreath", 0, 15)



}





class Unit(object):




    def __init__(self, hp, mp, df, sdf, atk, spatk, spd, name, moves, type):
        self.hp = hp
        self.mp = mp
        self.df = df
        self.name = name
        self.moves = moves
        self.atk = atk
        self.sdf = sdf
        self.spatk = spatk
        self.spd = spd
        self.type = type
        self.stats = [hp, mp, df, sdf, atk, spatk, spd]
        self.status = None
        self.cmove = None
        self.id = None



    def __str__(self):
        sti = "***" + str(self.type) + " ,Stats: " + str(self.stats) + " ,Name: " + str(self.name) + ", Moves: " + self.getMname() # + " Moves: " + str(self.moves)
        return sti


    def __repr__(self):
        return str(self)


    def printHP(self):
        if self.status != None:
            return self.name + "____ HP: " + str(self.hp) + "/" + str(self.stats[0]) + " Sts: " + self.status.name
        else:
            return self.name + "____ HP: " + str(self.hp) + "/" + str(self.stats[0])


    def AI(self):
        ran = random.randrange(0, len(self.moves))
        return self.moves[ran]

    def getMname(self):
        s = ""
        for move in self.moves:
            s = move.name + "-"
        return s



class Hero(Unit):
    moves = []

    # name, title, hp, mp, df, sdf, atk, spatk, spd, name, moves, type, title, boolean for title
    def __init__(self, title, HP, MP, df, sdf, atk, spatk, spd, moves, type, before):
        super().__init__(HP, MP, df, sdf, atk, spatk, spd, "", moves, type)
        self.title = title
        self.before = before


    def pTitle(self):
        if self.before:
            return self.title + self.name
        else:
            return self.name + self.title

    def printHP(self):
        if self.status != None:
            return self.pTitle() + "____ HP: " + str(self.hp) + "/" + str(self.stats[0]) +  "Sts: " + self.status.name + " MP: " + str(self.mp)
        else:
            return self.pTitle() + "____ HP: " + str(self.hp) + "/" + str(self.stats[0]) + " MP: " + str(self.mp)


#Not sure if I implemented status effects correctly

class Status(object):

    def __init__(self, name, dur, turn):
        self.name = name
        self.dur = dur
        self.end = turn + dur


    def kill(self):
        del self

    def update(self):
        self.dur = self.dur + 1

    def __str__(self):
        return "Name:" + self.name + ", Turns left: " + str(self.end - self.dur)

    def __repr__(self):
        return str(self)


    @classmethod
    def statCheck(cls, status, unit, turn):
        if status.name == "Defense" and status.dur < status.end:
            unit.df = unit.df + 2
        elif status.name == "Defense" and status.dur >= status.end:
            unit.df = unit.df - 2
            print("Defense has worn off!")
            unit.status = None

        if status.name == "Poison" and status.dur < status.end:
            print(unit.name + " is afflicted by poison and has lost 2 HP!")
            unit.hp = unit.hp - 2
        elif status.name == "Poison" and status.dur >= status.end:
            print(unit.name + " has been cured of poison")
            unit.status = None




#Mfunc class serves as a wrapper to store move functions, working as a move dictionary.


class Mfunc(object):


    #(self, atker, atk, dmg, df, enem):
    #Each function requires the hero, the move the hero is suing, the damage of the move, the target, and the list of enemies
    @classmethod
    def heal(self, atker, atk, dmg, df, enem, turn):
        atker.hp =+ 5
        print(atker.name + " has healed 5 HP!")
        if atker.hp > atker.stats[0]:
            atker.hp = atker.stats[0]

    @classmethod
    def lifesteal(self, atker, atk, dmg, df, enem, turn):
        atker.hp = atker.hp + (dmg / 2)
        print(atk.name + " has restored " + str(dmg / 2) + " points of HP!")
        if atker.hp > atker.stats[0]:
            atker.hp = atker.stats[0]


    @classmethod
    def firebreath(self, atker, atk, dmg, df, enem, turn):
        if atk.name == "Dragon Breath":
            print(atker.name + " lets out a breath of fire!")
            time.sleep(1)
            for unit in enem:
                time.sleep(0.5)
                unit.hp = unit.hp - 5
                print(unit.name + " was hit for 5 dmg!")
                time.sleep(1)
        else:
            print(atker.name + " lets out an ember!")
            time.sleep(1)
            for unit in enem:
                time.sleep(0.5)
                unit.hp = unit.hp - 2
                print(unit.name + " was hit for 2 dmg!")



    @classmethod
    def recovermp(self, atker, atk, dmg, df, enem, turn):
        atker.mp = atker.mp + 5
        if atker.mp > atker.stats[1]:
            atker.mp = atker.stats[1]
        print(atker.name + " has restored 5 MP!")

    # (self, atker, atk, dmg, df, enem):
    @classmethod
    def defense(self, atker, atk, dmg, df, enem, turn):
        atker.status = Status("Defense", 0, turn)
        print(atker.name + " has raised his shield!!")

    @classmethod
    def poison(self, atker, atk, dmg, df, enem, turn):
        df.status = Status("Poison", 3, turn)
        print( df.name + " has been poisoned!")

    @classmethod
    def flame(self, atker, atk, dmg, df, enem, turn):
        flametest = random.randrange(0, 4)
        if flametest <= 2:
            atker.spatk = atker.spatk + 1
            print(atker.name + "'s special attack has increased by 1!")


    @classmethod
    def roar(self, atker, atk, dmg, df, enem, turn):
        df.df = df.df - 1
        print(df.name + "'s defense has lowered by 1 point!")

    # hp, mp, df, sdf, atk, spatk, spd, name, moves, type
    @classmethod
    def sd(self, atker, atk, dmg, df, enem, turn):
        print(atker.name + " has summoned a dragon companion!")
        dragpet = Unit(10, 10, 9, 9, 7, 7, 8, "Whelp", [movedict["Ember"], movedict["Slash"]], "Dragon")
        heroes.append(dragpet)

#Hero dictionary, where all the playable classes are stored


herodict = {
    # name, title, hp, mp, df, sdf, atk, spatk, spd, name, moves, type, boolean for title
    "Warrior":
        Hero(" the Warrior", 30.0, 10, 11, 11, 14, 2, 10, [movedict["Axe Breaker"], movedict["Battle Roar"] ] , "Warrior", False),
    "Vampire":
        Hero("Vampire Lord ", 20.0, 20, 10, 10, 7, 14, 15, [movedict["Sanguimancy"], movedict["Crimson Tide"], movedict["Heal"]], "Vampire", True),
    "Dragon":
        Hero("Dragon Caller ", 25.0, 25, 10, 9, 9, 15, 13, [movedict["Ancient Flame"], movedict["Dragon Breath"], movedict["Summon Dragon"]], "Dragon", True)






}

#Monster dictionary, where all the monsters are stored

#hp, mp, df, sdf, atk, spatk, spd, name, moves, type
mdict = {
    #Slimes
    0 :  {
        0 : Unit(10.0, 0, 7, 7, 12, 3, 11, "Quicksilver Slime", [movedict["Attack"], movedict["Slime Rush"]], "Slime"),
        1 : Unit(14.0, 0, 9, 7, 8, 3, 8, "Metal Slime", [movedict["Attack"], movedict["Slime Rush"]], "Slime")
    },
    #Zombies
    1 :  {
        0 : Unit(15.0, 12, 6, 6, 12, 3, 11, "Zombie", [movedict["Attack"], movedict["Vampiric Strike"]], "Zombie")
    }


}

#if there is a custom.json present, then this function will parse all the correct info and add it into the dictionary
#before the battle begins
def json_appendor(d, mdict):
    j = 0
    i = str(j)
    for key in d["Monsters"]:
        name1 = d["Monsters"][i]["Name"]
        type1 = d["Monsters"][i]["Type"]
        hp1 = float(d["Monsters"][i]["HP"])
        mp1 = int(d["Monsters"][i]["MP"])
        atk1 = int(d["Monsters"][i]["Atk"])
        spatk1 = int(d["Monsters"][i]["Spatk"])
        df1 = int(d["Monsters"][i]["Def"])
        sdf1 = int(d["Monsters"][i]["Sdef"])
        spd1 = int(d["Monsters"][i]["Spd"])
        mv1 = d["Monsters"][i]["Moves"]
        moves1 = []
        kn = 0
        for item in mv1:
            moves1.append(movedict[mv1[kn]])
            kn += 1
        nmons = Unit(hp1, mp1, df1, sdf1, atk1, spatk1, spd1, name1, moves1, type1)
        print(nmons.name + " has been added!")
        numb = len(mdict)
        mdict[numb] = { j : nmons}
        i = +1

#I've been tinkering a lot with the battle formule, right now it's just a simple linear equation I came up
#It's been working good so far but this is prone to heavy changes in the future later on
def dmgFormula(atk, base, df):
    rand = float(random.randrange(8, 13) / 10)
    if base == 0:
        return 0
    #dmg = round(((((atk * base) / 2) + 1) - (df / 2) * rand), 2)
    dmg = round(((((atk * base)  - df) / 2) + 2)/ rand, 2)

    return dmg



def dmgCalc(attacker, attack, defensor):
    if attack.phys:
        atk = attacker.atk
        base = attack.dmg
        df = defensor.df
    else:
        atk = attacker.spatk
        base = attack.dmg
        df = defensor.sdf

    dmg = dmgFormula(atk, base, df)
    if dmg < 1 and dmg != 0:
        dmg = 1

    return dmg



def randEncounter(max): #function that handles random enemy encounters
    list = []
    if max == 0:
        max = random.randrange(1,3)#max 2 monsters goes from 1 to 2
    for i in range(0, max):
        rand = random.randrange(0, (len(mdict)))
        rand2 = random.randrange(0, (len(mdict[rand])))
        monster = copy(mdict[rand][rand2])
        list.append(monster)
    return list


def deathCheck(unit):
        if unit.name == name and unit.hp <= 0:
            print("You lost!")
            exit()
        if unit.hp <= 0:
            time.sleep(1)
            print(unit.name + " has been slain!")
            if unit in enem:
                enem.remove(unit)
            else:
                heroes.remove(unit)
        if len(enem) == 0:
            print("You win!")
            exit()

def randTarget(targets):
    rtarget = random.randrange(0, len(targets))
    return targets[rtarget]


#actual code

try:    #check for custom json to load
    with open('custom.json') as fp:
        custom = json.load(fp)
        print("Json parsed!")
        json_appendor(custom, mdict)

except FileNotFoundError:
    print('Json not found')


classcheck = True
name = input("Enter your name: ")

while(classcheck):      #cant leave loop until valid class is selected
    print('Current classes:')
    classcheck = False
    for value in herodict:
        print(value)
    clas = input("Select your class: ")

    try:
        heroes = [herodict[clas]]

    except KeyError:
        print("Please enter a valid class")
        time.sleep(1)
        classcheck = True


hero = heroes[0]

hero.name = name


turn = 1

enem = randEncounter(0)

battle = heroes + enem

enc = "You have encountered: "

for i in enem:
    enc = enc + i.name + ", "



print("Battle Start!")
print("")
print("")
time.sleep(1)
print(enc)
time.sleep(1)
print("")
print("")


while(True):

    battle = heroes + enem

    print("Turn:", turn)

    for unit in battle:
        if unit.status != None:
            unit.status.update()
            print(unit.status)


    battle.sort(key=lambda x: x.spd, reverse = True)
    #fastest at the top of the list, so fastest is index 0
    #enem = []
    #for i in range(0, len(battle)):
        #if battle[i].name != name:
            #enem.append(battle[i])


    for unit in battle:
        unit.hp = round(unit.hp, 2)



        print(unit.printHP())
        print("--------------")

    l1 = True

    while(l1):
        tcheck = False
        print("1. Attack")
        print("2. Defend")
        print("3. Abilities")
        print("4. Inspect")

        k = input()
        j = int(k)

        if j == 1:
            val = movedict["Attack"]
            l1 = False
            tcheck = True
        if j == 2:
            val = movedict["Defend"]
            l1 = False
        if j == 3:
            print("")
            print("Special Abilities: ")
            for i in range(0, len(hero.moves)):
                print ( str(1+i) + ". " + hero.moves[i].name + " MP Cost: " + str(hero.moves[i].cost))

            print( str(len(hero.moves) + 1) + ". Back"  )

            k = input()
            j = int(k)
            if j <= len(hero.moves) and j > 0:
                val = hero.moves[j-1]
                if val.cost > hero.mp:
                    tcheck = False
                    print("Not enough MP to cast current spell, select another")
                else:
                    tcheck = True
                    k = 0
            elif j == len(hero.moves) + 1:
                tcheck = False
                k = 0

        if j == 4:
            if len(enem) == 1:
                print("-----------------------")
                print(enem[0])
                print("-----------------------")
            else:
                for unit in enem:
                    print("-----------------------")
                    print(unit)
                    print("-----------------------")


        if len(enem) > 2 and tcheck:
            print("Select your Target")
            print("---------")
            for i in range(0, len(enem)):
                print(str(i + 1) + ". " + enem[i].printHP())
            print(    str(len(enem))  + ". Back")
            k = input()
            j = int(k)
            if j <= len(enem) and j > 0:
                target = enem[j - 1]
                l1 = False
            elif j == len(enem) + 1:
                tcheck = False
                pass
        elif tcheck:
            for unit in battle:
                if unit.name != name and unit in enem:
                    l1 = False
                    target = unit

    #check for priority and re-sort list accordingly
    #set current move values and add them to unit
    pcheck = False
    for unit in battle:
        if unit.name == name:
            unit.cmove = val
        else:
            ran = unit.AI()
            unit.cmove = ran
        if unit.cmove.pri > 0:
            pcheck = True

    if pcheck:
        battle.sort(key = lambda x: x.cmove.pri, reverse = True)




    #print(target)
    # actual battle process for loop, it iterates according to the amound of units that are in battle
    print("-----------\n------------")
    for unit in battle:
        if unit in heroes:
            if unit.name == name:
                deathCheck(unit)
                print(unit.name + " uses " + val.name + " on " + target.name + "!")
                time.sleep(2)
                dmg1 = round(dmgCalc(hero, val, target), 2)
                if val.dmg != 0:
                    print("It dealt " + str(dmg1) + " to " + target.name + "!")
                    target.hp = target.hp - dmg1
                    time.sleep(1)
                if val.func != "":
                    getattr(Mfunc, val.func)(hero, val, dmg1, target, enem, turn)
                if unit.status != None:
                    Status.statCheck(unit.status, unit, turn)
                    time.sleep(1)
                unit.mp = unit.mp - val.cost
            else:
                deathCheck(unit)
                ran = unit.cmove
                target1 = randTarget(enem)
                print(unit.name + " uses " + ran.name + " on " + target1.name + "!")
                time.sleep(2)
                dmg2 = round(dmgCalc(unit, ran, target1), 2)
                if ran.dmg != 0:
                    print("It dealt " + str(dmg2) + " to " + target1.name + "!")
                    target1.hp = target1.hp - dmg2
                    time.sleep(1)
                if ran.func != "":
                    getattr(Mfunc, ran.func)(unit, ran, dmg2, target1, enem, turn)
                if unit.status != None:
                    Status.statCheck(unit.status, unit, turn)
                    time.sleep(1)
                unit.mp = unit.mp - ran.cost

        elif unit in enem:
            deathCheck(unit)
            ran = unit.cmove
            target2 = randTarget(heroes)
            print(unit.name + " uses " + ran.name + " on " + target2.name + "!")
            time.sleep(2)
            dmg2 = round(dmgCalc(unit, ran, target2), 2)
            if ran.dmg != 0:
                print("It dealt " + str(dmg2) + " to " + target2.name + "!")
                target2.hp = target2.hp - dmg2
                time.sleep(1)
            if ran.func != "":
                getattr(Mfunc, ran.func)(unit, ran, dmg2, target2, heroes, turn)
            if unit.status != None:
                Status.statCheck(unit.status, unit, turn)
                time.sleep(1)
            unit.mp = unit.mp - ran.cost




    for unit in battle:
        deathCheck(unit)



    turn+=1


    print("-----------\n------------")
























