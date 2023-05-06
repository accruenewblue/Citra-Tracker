import json
import os
import time
import tkinter
from tkinter import *
from tkinter import ttk
monsfile=open(r'mon-data.json',"r+")
mons=json.load(monsfile)
trackertempfile=open(r"trackertemp.json","r+")
trackertemp=json.load(trackertempfile)
#trackertemp is brought back to transfer notes from the citra scraper to the tracker gui. 
#temp- will be removed for a more proper system to keep track of type changes later(eg Burn Up)
#monsfilepriv=temp changes not saved on tracker. MAKE SURE TO NOT SAVE THIS.
#also make sure to add a system to track pp usage
movesfile=open(r"move-data.json")
moves=json.load(movesfile)
movesetfile=open(r"movelearn.json")
moveset=json.load(movesetfile)
abilitiesfile=open(r"ability-data.json")
abilities=json.load(abilitiesfile)
itemsfile=open(r"item-data.json")
items=json.load(itemsfile)
naturesfile=open(r"nature-data.json")
natures=json.load(naturesfile)
pagemon="1"
pageflag=FALSE
#4 5 6 placement of mons in a battle
#1 2 3 single=1,4, double=1,2,4,5
#party=[trackertemp["1"]["mon"],trackertemp["2"]["mon"],trackertemp["3"]["mon"],trackertemp["4"]["mon"],trackertemp["5"]["mon"],trackertemp["6"]["mon"],]
#opponent=["-","-","-","-","-"]
#ally=["-"]
#arrays for defining the effectiveness of typed attacks or special moves
typetable={
"Normal":[1,1,1,1,1,.5,1,0,.5,1,1,1,1,1,1,1,1,1,1],
"Fighting":[2,1,.5,.5,1,2,.5,0,2,1,1,1,1,.5,2,1,2,.5,1],
"Flying":[1,2,1,1,1,.5,2,1,.5,1,1,2,.5,1,1,1,1,1,1],
"Poison":[1,1,1,.5,.5,.5,1,.5,0,1,1,2,1,1,1,1,1,2,1],
"Ground":[1,1,0,2,1,2,.5,1,2,2,1,.5,2,1,1,1,1,1,1],
"Rock":[1,.5,2,1,.5,1,2,1,.5,2,1,1,1,1,2,1,1,1,1],
"Bug":[1,.5,.5,.5,1,1,1,.5,.5,.5,1,2,1,2,1,1,2,.5,1],
"Ghost":[0,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,.5,1,1],
"Steel":[1,1,1,1,1,2,1,1,.5,.5,.5,1,.5,1,2,1,1,2,1],
"Fire":[1,1,1,1,1,.5,2,1,2,.5,.5,2,1,1,2,.5,1,1,1],
"Water":[1,1,1,1,2,2,1,1,1,2,.5,.5,1,1,1,.5,1,1,1],
"Grass":[1,1,.5,.5,2,2,.5,1,.5,.5,2,.5,1,1,1,.5,1,1,1],
"Electric":[1,1,2,1,0,1,1,1,1,1,2,.5,.5,1,1,.5,1,1,1],
"Psychic":[1,2,1,2,1,1,1,1,.5,1,1,1,1,.5,1,1,0,1,1],
"Ice":[1,1,2,1,2,1,1,1,.5,.5,.5,2,1,1,.5,2,1,1,1],
"Dragon":[1,1,1,1,1,1,1,1,.5,1,1,1,1,1,1,2,1,0,1],
"Dark":[1,.5,1,1,1,1,1,2,1,1,1,1,1,2,1,1,.5,.5,1],
"Fairy":[1,2,1,.5,1,1,1,1,.5,.5,1,1,1,1,1,2,2,1,1],
"Null":[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
"Freeze-Dry":[1,1,2,1,2,1,1,1,.5,.5,2,2,1,1,.5,2,1,1,1],
"FreezeDryNormalize":[1,1,1,1,1,.5,1,0,.5,1,2,1,1,1,1,1,1,1,1],
"DeltaStreamElectric":[1,1,1,1,0,1,1,1,1,1,2,.5,.5,1,1,.5,1,1,1],
"DeltaStreamIce":[1,1,1,1,2,1,1,1,.5,.5,.5,2,1,1,.5,2,1,1,1],
"DeltaStreamRock":[1,.5,1,1,.5,1,2,1,.5,2,1,1,1,1,2,1,1,1,1],
"FlyingPress":[2,2,.5,.5,1,1,1,0,1,1,1,2,.5,.5,2,1,2,.5,1],
"FlyingPressElectrify":[1,2,2,1,0,.5,2,1,.5,1,2,1,.25,1,1,.5,1,1,1],
"FlyingPressNormalize":[1,2,1,1,1,.25,2,0,.25,1,1,2,.5,1,1,1,1,1,1],
"ThousandArrows":[1,1,1,2,1,2,.5,1,2,2,1,.5,2,1,1,1,1,1,1]}
#defines the columns for the arrays corresponding to the type hit
typedic={"Normal":0,"Fighting":1,"Flying":2,"Poison":3,"Ground":4,"Rock":5,"Bug":6,"Ghost":7,"Steel":8,"Fire":9,"Water":10,"Grass":11,"Electric":12,"Psychic":13,"Ice":14,"Dragon":15,"Dark":16,"Fairy":17,"Null":18}
#extracts and calculates relevant type combo for defenders
def coverage(movetype,defender):
    typemult=1
    for item in range(0,len(mons[defender]["types"])):
        if item!="-":
            typemult=typemult*(typetable[movetype][typedic[mons[defender]["types"][item]]])
    return typemult
def gendefcov(mon):
    moncov=Toplevel()
    global pageflag
    pageflag=TRUE
    cov25=[]
    cov5=[]
    cov1=[]
    cov2=[]
    cov4=[]
    for item in typedic:
        if coverage(item,mon)==0.25:
            cov25.append(item)
        elif coverage(item,mon)==0.5:
            cov5.append(item)
        elif coverage(item,mon)==1:
            cov1.append(item)
        elif coverage(item,mon)==2:
            cov2.append(item)
        elif coverage(item,mon)==4:
            cov4.append(item)
    c25=Label(moncov,text=".25x: "+str(cov25),wraplength=200)
    c25.grid(row=1,column=1)
    c5=Label(moncov,text=".5x: "+str(cov5),wraplength=200)
    c5.grid(row=2,column=1)
    c2=Label(moncov,text="2x: "+str(cov2),wraplength=200)
    c2.grid(row=3,column=1)
    c4=Label(moncov,text="4x: "+str(cov4),wraplength=200)
    c4.grid(row=4,column=1)
def ccomb(movelist,game):
    if game=="XY":
        taglist=["XY"]
    elif game=="ORAS":
        taglist=["XY","ORAS"]
    elif game=="SM":
        taglist=["XY","ORAS","SM"]
    elif game=="USUM":
        taglist=["XY","ORAS","SM","USUM"]
    cov25=[]
    cov5=[]
    cov1=[]
    cov2=[]
    cov4=[]
    temp=[]
    for mon in mons:
        if mons[mon]["tag"] in taglist:
            for item in movelist:
                if coverage(item,mon)==0.25:
                    temp.append(mon)
                    temp.append(coverage(item,mon))
                elif coverage(item,mon)==0.5:
                    temp.append(mon)
                    temp.append(coverage(item,mon))
                elif coverage(item,mon)==1:
                    temp.append(mon)
                    temp.append(coverage(item,mon))
                elif coverage(item,mon)==2:
                    temp.append(mon)
                    temp.append(coverage(item,mon))
                elif coverage(item,mon)==4:
                    temp.append(mon)
                    temp.append(coverage(item,mon))
        if 4 in temp:
            cov4.append(mon)
        elif 2 in temp:
            cov2.append(mon)
        elif 1 in temp:
            cov1.append(mon)
        elif .5 in temp:
            cov5.append(mon)
        elif .25 in temp:
            cov25.append(mon)
        temp=[]
    return cov4,cov2,cov1,cov5,cov25
#tracking party from save data
#gui
tracking=Tk()
#battleformat list: single, double, triple, SOS(gen 7), horde, multi, party
battleformat="party"
def formatchanger():
    global battleformat
    if battleformat=="party":
        battleformat="single"
    #to be used later then this is properly implemented, not gonna bother with more than singles rn
    elif battleformat=="single":
        if trackertemp["2"]["mon"]!="-":
            battleformat="double"
        else:
            battleformat="party"
    elif battleformat=="double":
        if trackertemp["3"]["mon"]!="-":
            battleformat="triple"
        else:
            battleformat="party"
    #elif battleformat=="triple":
        #battleformat="horde"
    else:
        battleformat="party"
def frameclearer():
    for widget in tracking.winfo_children():
        widget.destroy()
def pagechanger():
    global pagemon
    #mon1=party[0]
    #mon2=party[1]
    #mon3=party[2]
    #mon4=party[3]
    #mon5=party[4]
    #mon6=party[5]
    #mon7=ally[0]
    #mon8=opponent[0]
    #mon9=opponent[1]
    #mon10=opponent[2]
    #mon11=opponent[3]
    #mon12=opponent[4]
    if battleformat=="single":
        if pagemon=="1":
            pagemon="8"
        else:
            pagemon="1"
    elif battleformat=="double":
        if pagemon=="1":
            pagemon="2"
        elif pagemon=="2":
            pagemon="8"
        elif pagemon=="8":
            pagemon="9"
        else:
            pagemon="1"
    elif battleformat=="multi":
        if pagemon=="1":
            pagemon="7"
        elif pagemon=="7":
            pagemon="8"
        elif pagemon=="8":
            pagemon="9"
        else:
            pagemon="1"
    elif battleformat=="triple":
        if pagemon=="1":
            pagemon="2"
        elif pagemon=="2":
            pagemon="3"
        elif pagemon=="3":
            pagemon="8"
        elif pagemon=="8":
            pagemon="9"
        elif pagemon=="9":
            pagemon="10"
        else:
            pagemon="1"
    elif battleformat=="SOS":
        if pagemon=="1":
            pagemon="8"
        else:
            pagemon="1"
    elif battleformat=="horde":
        if pagemon=="1":
            pagemon="8"
        else:
            pagemon="1"
    elif battleformat=="party":
        if pagemon=="1":
            if trackertemp["2"]["mon"]!="-":
                pagemon="2"
            else:
                pagemon="1"
        elif pagemon=="2":
            if trackertemp["3"]["mon"]!="-":
                pagemon="3"
            else:
                pagemon="1"
        elif pagemon=="3":
            if trackertemp["4"]["mon"]!="-":
                pagemon="4"
            else:
                pagemon="1"
        elif pagemon=="4":
            if trackertemp["5"]["mon"]!="-":
                pagemon="5"
            else:
                pagemon="1"
        elif pagemon=="5":
            if trackertemp["6"]["mon"]!="-":
                pagemon="6"
            else:
                pagemon="1"
        else:
            pagemon="1"
    updater()
def pagechangerleft():
    global pagemon
    if battleformat=="party":
        if pagemon=="3":
            if trackertemp["2"]["mon"]!="-":
                pagemon="2"
            else:
                pagemon="1"
        elif pagemon=="4":
            if trackertemp["3"]["mon"]!="-":
                pagemon="3"
            else:
                pagemon="1"
        elif pagemon=="5":
            if trackertemp["4"]["mon"]!="-":
                pagemon="4"
            else:
                pagemon="1"
        elif pagemon=="6":
            if trackertemp["5"]["mon"]!="-":
                pagemon="5"
            else:
                pagemon="1"
        elif pagemon=="1":
            if trackertemp["6"]["mon"]!="-":
                pagemon="6"
            elif trackertemp["5"]["mon"]!="-":
                pagemon="5"
            elif trackertemp["4"]["mon"]!="-":
                pagemon="4"
            elif trackertemp["3"]["mon"]!="-":
                pagemon="3"
            elif trackertemp["2"]["mon"]!="-":
                pagemon="2"
        else:
            pagemon="1"
    elif battleformat=="single":
        if pagemon=="1":
            pagemon="8"
        else:
            pagemon="1"
    elif battleformat=="double":
        if pagemon=="8":
            pagemon="2"
        elif pagemon=="9":
            pagemon="8"
        elif pagemon=="1":
            pagemon="9"
        else:
            pagemon="1"
    elif battleformat=="multi":
        if pagemon=="1":
            pagemon="7"
        elif pagemon=="7":
            pagemon="8"
        elif pagemon=="8":
            pagemon="9"
        else:
            pagemon="1"
    elif battleformat=="triple":
        if pagemon=="3":
            pagemon="2"
        elif pagemon=="8":
            pagemon="3"
        elif pagemon=="9":
            pagemon="8"
        elif pagemon=="10":
            pagemon="9"
        elif pagemon=="1":
            pagemon="10"
        else:
            pagemon="1"
    elif battleformat=="SOS":
        if pagemon=="1":
            pagemon="8"
        else:
            pagemon="1"
    elif battleformat=="horde":
        if pagemon=="1":
            pagemon="8"
        else:
            pagemon="1"
    updater()
def updater():
    global pagemon,pageflag
    pagemonenemylist=["7","8","9","10","11","12"]
    pagemonfriendlist=["1","2","3","4","5","6"]
    if pagemon in pagemonfriendlist:
        if trackertemp[pagemon]["mon"]=="-":
            pagemon=str(int(pagemon)+1)
        if pageflag==FALSE:
            PartyMonTracker(tracking,pagemon)
            tracking.after(10000,updater)
    elif pagemon in pagemonenemylist:
        EnemyMonTracker(tracking)
    if pageflag==TRUE:
        pageflag=FALSE
def gamechanger():
    if trackertemp["game"]=="XY":
        trackertemp["game"]="ORAS"
    elif trackertemp["game"]=="ORAS":
        trackertemp["game"]="SM"
    elif trackertemp["game"]=="SM":
        trackertemp["game"]="USUM"
    elif trackertemp["game"]=="USUM":
        trackertemp["game"]="XY"
    with open(r"trackertemp.json", "w") as f:
        json.dump(trackertemp,f)
def naturecalcm(numt):
    global Satk,Sdef,Sspa,Sspd,Sspe
    Satk=""
    Sdef=""
    Sspa=""
    Sspd=""
    Sspe=""
    if natures[trackertemp[numt]["nature"]]["-"]==" Attack":
        Satk="-"
    elif natures[trackertemp[numt]["nature"]]["-"]==" Defense":
        Sdef="-"
    elif natures[trackertemp[numt]["nature"]]["-"]==" Sp. Attack":
        Sspa="-"
    elif natures[trackertemp[numt]["nature"]]["-"]==" Sp. Defense":
        Sspd="-"
    elif natures[trackertemp[numt]["nature"]]["-"]==" Speed":
        Sspe="-"
    else:
        Satk=""
        Sdef=""
        Sspa=""
        Sspd=""
        Sspe=""
def naturecalcp(numt):
    global Satk,Sdef,Sspa,Sspd,Sspe
    if natures[trackertemp[numt]["nature"]]["+"]==" Attack":
        Satk="+"
    elif natures[trackertemp[numt]["nature"]]["+"]==" Defense":
        Sdef="+"
    elif natures[trackertemp[numt]["nature"]]["+"]==" Sp. Attack":
        Sspa="+"
    elif natures[trackertemp[numt]["nature"]]["+"]==" Sp. Defense":
        Sspd="+"
    elif natures[trackertemp[numt]["nature"]]["+"]==" Speed":
        Sspe="+"
    else:
        Satk=""
        Sdef=""
        Sspa=""
        Sspd=""
        Sspe=""
#determine type and power of certain moves
variablemoves=["Low Kick","Grass Knot","Eruption","Water Spout","Natural Gift","Present","Psywave","Heat Crash","Heavy Slam","Magnitude","Wring Out","Crush Grip","Trump Card","Return","Frustration","Reversal","Flail","Fling","Power Trip","Stored Power","Punishment","Electro Ball","Spit Up"]
#hp, friend, userkg are integer values.
#def movepower(move,hp,userkg,oppkg,item,friend,pp):
def movepower(move,hp,friend,pp):
    if moves[move]["power"]=="0":
        if moves[move]["detail"]=="Status":
            return "-"
        elif move=="Eruption" or move=="Water Spout":
            return str(round(150*hp))
        elif move=="Low Kick" or move=="Grass Knot":
            return "WT"
        elif move=="Return":
            return str(round(friend/2.5))
        elif move=="Frustration":
            return str(round((255-friend)/2.5))
        elif move=="Fling":
            return "ITEM"
        elif move=="Crush Grip" or move=="Wring Out":
            return ">HP"
        elif move=="Flail" or move=="Reversal":
            if hp>=.6875:
                return 20
            elif hp>=.3542:
                return 40
            elif hp>=.2083:
                return 80
            elif hp>=.1042:
                return 100
            elif hp>=.417:
                return 150
            elif hp<.417:
                return 200
            else:
                return "ERR"
        elif move=="Trump Card":
            if pp==0:
                return "200"
            elif pp==1:
                return "80"
            elif pp==2:
                return "60"
            elif pp==3:
                return "50"
            else:
                return "40"
        elif move in variablemoves:
            return "VAR"
        else:
            return "0"
    else:
        return moves[move]["power"]
#variabletypes=["Weather Ball","Judgement","Natural Gift","Revelation Dance","Techno Blast","Multi-Attack","Hidden Power"]
def movetype(move,mon,item):
    if move=="Revelation Dance":
        return mons[mon]["types"][0]
    elif move=="Hidden Power":
        return "Null"
    elif move=="Natural Gift":
        return "Normal"
    elif move=="Judgement":
        if item=="298":
            return "Fire"
        elif item=="299":
            return "Water"
        elif item=="300":
            return "Electric"
        elif item=="301":
            return "Grass"
        elif item=="302":
            return "Ice"
        elif item=="303":
            return "Fighting"
        elif item=="304":
            return "Poison"
        elif item=="305":
            return "Ground"
        elif item=="306":
            return "Flying"
        elif item=="307":
            return "Psychic"
        elif item=="308":
            return "Bug"
        elif item=="309":
            return "Rock"
        elif item=="310":
            return "Ghost"
        elif item=="311":
            return "Dragon"
        elif item=="312":
            return "Dark"
        elif item=="313":
            return "Steel"
        elif item=="644":
            return "Fairy"
        else:
            return "Normal"
    elif move=="Techno Blast":
        if item=="116":
            return "Water"
        elif item=="117":
            return "Electric"
        elif item=="118":
            return "Fire"
        elif item=="119":
            return "Ice"
        else:
            return "Normal"
    elif move=="Multi-Attack":
        if item=="912":
            return "Fire"
        elif item=="913":
            return "Water"
        elif item=="915":
            return "Electric"
        elif item=="914":
            return "Grass"
        elif item=="917":
            return "Ice"
        elif item=="904":
            return "Fighting"
        elif item=="906":
            return "Poison"
        elif item=="907":
            return "Ground"
        elif item=="905":
            return "Flying"
        elif item=="916":
            return "Psychic"
        elif item=="909":
            return "Bug"
        elif item=="908":
            return "Rock"
        elif item=="910":
            return "Ghost"
        elif item=="918":
            return "Dragon"
        elif item=="919":
            return "Dark"
        elif item=="911":
            return "Steel"
        elif item=="920":
            return "Fairy"
        else:
            return "Normal"
    else:
        return moves[move]["type"]
#auxiliary page functions
def NotesClearer():
    clearer=Toplevel()
    global pageflag
    pageflag=TRUE
    clearer.title("Are you sure?")
    clearer.geometry("215x85")
    CLEARer=Label(clearer,justify="center",text="Are you sure you would like to do this? This clears all the notes stored so far. Only recommended when a seed dies.",wraplength=220)
    CLEARer.grid(row=1,column=1)
    def noteclear():
        for mon in mons:
            mons[mon]["ability"]=[]
            mons[mon]["notes"]=["","","","","",""]
            mons[mon]["stringnote"]=""
            mons[mon]["lastseenat"]="-"
            mons[mon]["moves"]=[]
        clearer.destroy()
        updater()
    notesclear=Button(clearer, text = "Clear Notes", command=noteclear)
    notesclear.grid(row=2, column=1)
def Ability_Data(abil):
    abili=Toplevel()
    global pageflag
    pageflag=TRUE
    abili.title("Ability Data")
    abili.geometry("300x50")
    abilitydata=Label(abili,text=abilities[abil]["detail"],wraplength=300)
    abilitydata.pack()
def moveinfo():
    infom=Toplevel()
    global pageflag
    pageflag=TRUE
    infom.title("Ability Data")
    infom.geometry("300x50")
    movedata=Label(infom,text="First two letters are Ph=Physical, Sp=Special, St=Status. Second two are Co.=Contact, NC=Non-Contact.",wraplength=300)
    movedata.pack()
def Mon_Data(montemp):
    frameclearer()
    global pageflag
    pageflag=TRUE
    tracking.title("Mon Data")
    for abil in mons[montemp]["ability"]:
        abilloc=mons[montemp]["ability"].index(abil)
        abillabel=Button(tracking, text=abil,command=lambda abil=abil:Ability_Data(abil))
        #abil=abil stores the value of it when written
        #I thought it normally did that, but apparently otherwise it only calls that after???
        abillabel.grid(row=6+abilloc, column=4)
        abilentry=Label(tracking, text="Ability "+str(1+abilloc))
        abilentry.grid(row=6+abilloc,column=3)
    for item in range(0,len(mons[montemp]["moves"])):
        movelabel=Button(tracking, text=mons[montemp]["moves"][item])
        movelabel.grid(row=1+item, column=5)
    mon1name=Label(tracking,text=montemp)
    mon1name.grid(row=1,column=4)
    mon1type=Label(tracking,text="Types")
    mon1type.grid(row=2,column=3)
    mon1type=Label(tracking,text=mons[montemp]["types"])
    mon1type.grid(row=2,column=4)
    monbst=Label(tracking,text="BST")
    monbst.grid(row=2,column=1)
    mon1bst=Label(tracking,text=mons[montemp]["bst"])
    mon1bst.grid(row=2,column=2)
    leave=Button(tracking, text="Leave", command=updater)
    leave.grid(row=1,column=1)
    monevo=Label(tracking,text="Evo")
    monevo.grid(row=1,column=2)
    mon1evo=Label(tracking,text=mons[montemp]["evo"])
    mon1evo.grid(row=1,column=3)
    itemlabel=Label(tracking, text = "Levels")
    itemlabel.grid(row=3, column=3)
    itementry=Label(tracking, text=mons[montemp]["lastseenat"])
    itementry.grid(row=3,column=12)
    strinlabel=Label(tracking, text = "String")
    strinlabel.grid(row=4, column=3)
    strinentry=Label(tracking, text=mons[montemp]["stringnote"], wraplength=100)
    strinentry.grid(row=4,column=4)
    strinlabel=Label(tracking, text = "Moveset")
    strinlabel.grid(row=5, column=3)
    mon_moveset=(moveset[str(int(mons[montemp]["id"]))])
    strinentry=Label(tracking, text=mon_moveset, wraplength=100)
    strinentry.grid(row=5,column=4)
    hplabel=Label(tracking, text = "HP")
    hplabel.grid(row=3, column=1)
    hpentry=Label(tracking, text=mons[montemp]["notes"][0])
    hpentry.grid(row=3,column=2)
    atklabel=Label(tracking, text = "ATK")
    atklabel.grid(row=4, column=1)
    atkentry=Label(tracking, text=mons[montemp]["notes"][1])
    atkentry.grid(row=4,column=2)
    deflabel=Label(tracking, text = "DEF")
    deflabel.grid(row=5, column=1)
    defentry=Label(tracking, text=mons[montemp]["notes"][2])
    defentry.grid(row=5,column=2)
    spalabel=Label(tracking, text = "SPA")
    spalabel.grid(row=6, column=1)
    spaentry=Label(tracking, text=mons[montemp]["notes"][3])
    spaentry.grid(row=6,column=2)
    spdlabel=Label(tracking, text = "SPD")
    spdlabel.grid(row=7, column=1)
    spdentry=Label(tracking, text=mons[montemp]["notes"][4])
    spdentry.grid(row=7,column=2)
    spelabel=Label(tracking, text = "SPE")
    spelabel.grid(row=8, column=1)
    speentry=Label(tracking, text=mons[montemp]["notes"][5])
    speentry.grid(row=8,column=2)
def ccombextra(data):
    extra=Toplevel()
    extra.title("Extra Ccomb Data")
    extradata=Label(extra,text=data,wraplength=1250)
    extradata.pack()
def ccombpage(movetypes,game):
    frameclearer()
    cov4,cov2,cov1,cov5,cov25=ccomb(movetypes,game)
    global pageflag
    pageflag=TRUE
    def extra(de):
        if len(de)<20:
            return str(de)
        else:
            return "HERE"
    header=Label(tracking, text="ACCRUE'S CCOMB CALC")
    header.grid(row=1, column=1,columnspan=2)
    leave=Button(tracking, text="PRESS HERE TO LEAVE", command=updater)
    leave.grid(row=2,column=1,columnspan=2)
    c25l=Label(tracking, text=".25x: "+str(len(cov25)))
    c25l.grid(row=3, column=1)
    c25=Button(tracking,borderwidth=0, text=extra(cov25),wraplength=300,command=lambda:ccombextra(cov25))
    c25.grid(row=3, column=2)
    c5l=Label(tracking, text=".5x: "+str(len(cov5)))
    c5l.grid(row=5, column=1)
    c5=Button(tracking,borderwidth=0,text=extra(cov5),wraplength=300,command=lambda:ccombextra(cov5))
    c5.grid(row=5, column=2)
    c1l=Label(tracking, text="1x: "+str(len(cov1)))
    c1l.grid(row=7, column=1)
    c1=Button(tracking,borderwidth=0,text=extra(cov1),wraplength=300,command=lambda:ccombextra(cov1))
    c1.grid(row=7, column=2)
    c2l=Label(tracking, text="2x: "+str(len(cov2)))
    c2l.grid(row=9, column=1)
    c2=Button(tracking,borderwidth=0,text=extra(cov2),wraplength=300,command=lambda:ccombextra(cov2))
    c2.grid(row=9, column=2)
    c4l=Label(tracking, text="4x: "+str(len(cov4)))
    c4l.grid(row=11, column=1)
    c4=Button(tracking,borderwidth=0,text=extra(cov4),wraplength=300,command=lambda:ccombextra(cov4))
    c4.grid(row=11, column=2)
def PartyMonTracker(tracking,pok):
    frameclearer()
    trackertempfile=open(r"trackertemp.json","r+")
    trackertemp=json.load(trackertempfile)
    tracking.geometry("320x270")
    tracking.title("Tracker")
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    leftbutton=Button(tracking,borderwidth=0,text="<-",command=pagechangerleft)
    leftbutton.place(x=0,y=0)
    changepage=Button(tracking,borderwidth=0,text="->",command=pagechanger)
    changepage.place(x=25,y=0)
    monlabel=Button(tracking,borderwidth=0, text=trackertemp[pok]["mon"],command=lambda:Mon_Data(trackertemp[pok]["mon"]))
    monlabel.place(x=50,y=0)
    mon_moveset=(moveset[str(int(mons[trackertemp[pok]["mon"]]["id"]))])
    for item in mon_moveset:
        if int(item)>int(trackertemp[pok]["level"]):
            nextmove=item
            placemove=str(mon_moveset.index(item))
            break
        nextmove="-"
    changegame=Button(tracking,borderwidth=0, text=trackertemp["game"],command=gamechanger)
    changegame.place(x=5,y=120)
    changeform=Button(tracking,borderwidth=0, text=battleformat,command=formatchanger)
    changeform.place(x=5,y=100)
    hpheals="-"
    statusheals="-"
    ppheals="-"
    abillabel=Button(tracking,borderwidth=0, text="PP: "+ppheals)
    abillabel.place(x=130,y=120)
    abillabel=Button(tracking,borderwidth=0, text="Heals: "+hpheals)
    abillabel.place(x=50,y=100)
    abillabel=Button(tracking,borderwidth=0, text="Status: "+statusheals)
    abillabel.place(x=50,y=120)
    abillabel=Button(tracking,borderwidth=0, text=trackertemp[pok]["ability"],command=lambda: Ability_Data(trackertemp[pok]["ability"]))
    abillabel.place(x=50,y=80)
    itemlabel=Label(tracking, text=items[str(trackertemp[pok]["item"]).zfill(3)]["name"])
    itemlabel.place(x=50,y=60)
    strinlabel=Label(tracking, text=str(trackertemp[pok]["currhp"])+"/"+str(trackertemp[pok]["maxhp"]))
    strinlabel.place(x=50,y=40)
    levllabel=Label(tracking, text = "Lv. "+trackertemp[pok]["level"]+" ("+mons[trackertemp[pok]["mon"]]["evo"]+")")
    levllabel.place(x=50,y=20)
    for item in range(0,len(mons[trackertemp[pok]["mon"]]["types"])):
        types2=Button(tracking,borderwidth=0,text=mons[trackertemp[pok]["mon"]]["types"][item],command=lambda:gendefcov(trackertemp[pok]["mon"]))
        types2.place(x=0,y=20+20*item)
    naturecalcm(pok)
    naturecalcp(pok)
    hplabel=Label(tracking, text = "HP")
    hplabel.place(x=210,y=0)
    hpentry=Label(tracking, text=trackertemp[pok]["maxhp"])
    hpentry.place(x=260,y=0)
    atklabel=Label(tracking, text = "ATK")
    atklabel.place(x=210,y=20)
    atkentry=Label(tracking, text=Satk+trackertemp[pok]["atk"])
    atkentry.place(x=260,y=20)
    deflabel=Label(tracking, text = "DEF")
    deflabel.place(x=210,y=40)
    defentry=Label(tracking, text=Sdef+trackertemp[pok]["def"],)
    defentry.place(x=260,y=40)
    spalabel=Label(tracking, text = "SPA")
    spalabel.place(x=210,y=60)
    spaentry=Label(tracking, text=Sspa+trackertemp[pok]["spa"])
    spaentry.place(x=260,y=60)
    spdlabel=Label(tracking, text = "SPD")
    spdlabel.place(x=210,y=80)
    spdentry=Label(tracking, text=Sspd+trackertemp[pok]["spd"])
    spdentry.place(x=260,y=80)
    spelabel=Label(tracking, text = "SPE")
    spelabel.place(x=210,y=100)
    speentry=Label(tracking, text=Sspe+trackertemp[pok]["spe"])
    speentry.place(x=260,y=100)
    spelabel=Label(tracking, text = "BST")
    spelabel.place(x=210,y=120)
    bstlabel=Label(tracking, text=mons[trackertemp[pok]["mon"]]["bst"])
    bstlabel.place(x=260,y=120)
    #badgelabel=Label(tracking, text = "Badges")
    #badgelabel.grid(row=1, column=11)
    #badge1=Checkbutton(tracking,text=pok)
    #badge1.grid(row=2,column=11)
    #badge2=Checkbutton(tracking,text="2")
    #badge2.grid(row=3,column=11)
    #badge3=Checkbutton(tracking,text="3")
    #badge3.grid(row=4,column=11)
    #badge4=Checkbutton(tracking,text="4")
    #badge4.grid(row=5,column=11)
    #badge5=Checkbutton(tracking,text="5")
    #badge5.grid(row=6,column=11)
    #badge6=Checkbutton(tracking,text="6")
    #badge6.grid(row=7,column=11)
    #badge7=Checkbutton(tracking,text="7")
    #badge7.grid(row=8,column=11)
    #badge8=Checkbutton(tracking,text="8")
    #badge8.grid(row=9,column=11)
    movelabel=Label(tracking, text="--------------------------------------------------------")
    movelabel.place(x=0,y=140)
    movelabel=Label(tracking, text = "Moves: "+placemove+"/"+str(len(mon_moveset))+" ("+nextmove+")")
    movelabel.place(x=0,y=160)
    move1entry=Label(tracking, text=trackertemp[pok]["move1"])
    move1entry.place(x=0,y=180)
    move2entry=Label(tracking, text=trackertemp[pok]["move2"])
    move2entry.place(x=0,y=200)
    move3entry=Label(tracking, text=trackertemp[pok]["move3"])
    move3entry.place(x=0,y=220)
    move4entry=Label(tracking, text=trackertemp[pok]["move4"])
    move4entry.place(x=0,y=240)
    ppmovelabel=Label(tracking, text = "PP")
    ppmovelabel.place(x=110,y=160)
    ppmove1entry=Label(tracking, text=moves[trackertemp[pok]["move1"]]["pp"])
    ppmove1entry.place(x=110,y=180)
    ppmove2entry=Label(tracking, text=moves[trackertemp[pok]["move2"]]["pp"])
    ppmove2entry.place(x=110,y=200)
    ppmove3entry=Label(tracking, text=moves[trackertemp[pok]["move3"]]["pp"])
    ppmove3entry.place(x=110,y=220)
    ppmove4entry=Label(tracking, text=moves[trackertemp[pok]["move4"]]["pp"])
    ppmove4entry.place(x=110,y=240)
    powmovelabel=Label(tracking, text = "Pow")
    powmovelabel.place(x=140,y=160)
    move1pow=movepower(trackertemp[pok]["move1"],(int(trackertemp[pok]["currhp"])/int(trackertemp[pok]["maxhp"])),int(trackertemp[pok]["friendship"]),moves[trackertemp[pok]["move1"]]["pp"])
    powmove1entry=Label(tracking, text=move1pow)
    powmove1entry.place(x=140,y=180)
    move2pow=movepower(trackertemp[pok]["move2"],(int(trackertemp[pok]["currhp"])/int(trackertemp[pok]["maxhp"])),int(trackertemp[pok]["friendship"]),moves[trackertemp[pok]["move2"]]["pp"])
    powmove2entry=Label(tracking, text=move2pow)
    powmove2entry.place(x=140,y=200)
    move3pow=movepower(trackertemp[pok]["move3"],(int(trackertemp[pok]["currhp"])/int(trackertemp[pok]["maxhp"])),int(trackertemp[pok]["friendship"]),moves[trackertemp[pok]["move3"]]["pp"])
    powmove3entry=Label(tracking, text=move3pow)
    powmove3entry.place(x=140,y=220)
    move4pow=movepower(trackertemp[pok]["move4"],(int(trackertemp[pok]["currhp"])/int(trackertemp[pok]["maxhp"])),int(trackertemp[pok]["friendship"]),moves[trackertemp[pok]["move4"]]["pp"])
    powmove4entry=Label(tracking, text=move4pow)
    powmove4entry.place(x=140,y=240)
    accmovelabel=Label(tracking, text = "Acc")
    accmovelabel.place(x=170,y=160)
    accmove1entry=Label(tracking, text=moves[trackertemp[pok]["move1"]]["acc"])
    accmove1entry.place(x=170,y=180)
    accmove2entry=Label(tracking, text=moves[trackertemp[pok]["move2"]]["acc"])
    accmove2entry.place(x=170,y=200)
    accmove3entry=Label(tracking, text=moves[trackertemp[pok]["move3"]]["acc"])
    accmove3entry.place(x=170,y=220)
    accmove4entry=Label(tracking, text=moves[trackertemp[pok]["move4"]]["acc"])
    accmove4entry.place(x=170,y=240)
    move1type=movetype(trackertemp[pok]["move1"],trackertemp[pok]["mon"],trackertemp[pok]["item"])
    typmove1entry=Label(tracking, text=move1type)
    typmove1entry.place(x=210,y=180)
    move2type=movetype(trackertemp[pok]["move2"],trackertemp[pok]["mon"],trackertemp[pok]["item"])
    typmove2entry=Label(tracking, text=move2type)
    typmove2entry.place(x=210,y=200)
    move3type=movetype(trackertemp[pok]["move3"],trackertemp[pok]["mon"],trackertemp[pok]["item"])
    typmove3entry=Label(tracking, text=move3type)
    typmove3entry.place(x=210,y=220)
    move4type=movetype(trackertemp[pok]["move4"],trackertemp[pok]["mon"],trackertemp[pok]["item"])
    typmove4entry=Label(tracking, text=move4type)
    typmove4entry.place(x=210,y=240)
    movepowlist=[move1pow,move2pow,move3pow,move4pow]
    movetypelist=[move1type,move2type,move3type,move4type]
    for item in movepowlist:
        if item=="-" or item=="0":
            movetypelist.remove(movetypelist[movepowlist.index(item)])
            movepowlist.remove(item)
    typmovelabel=Button(tracking,borderwidth=0,text="Type",command=lambda:ccombpage(movetypelist,trackertemp["game"]))
    typmovelabel.place(x=210,y=160)
    typmovelabel=Button(tracking,borderwidth=0, text = "Contact", command=moveinfo)
    typmovelabel.place(x=260,y=160)
    typmove1entry=Label(tracking, text=moves[trackertemp[pok]["move1"]]["detail"][0:2]+", "+moves[trackertemp[pok]["move1"]]["contact"])
    typmove1entry.place(x=260,y=180)
    typmove2entry=Label(tracking, text=moves[trackertemp[pok]["move2"]]["detail"][0:2]+", "+moves[trackertemp[pok]["move2"]]["contact"])
    typmove2entry.place(x=260,y=200)
    typmove3entry=Label(tracking, text=moves[trackertemp[pok]["move3"]]["detail"][0:2]+", "+moves[trackertemp[pok]["move3"]]["contact"])
    typmove3entry.place(x=260,y=220)
    typmove4entry=Label(tracking, text=moves[trackertemp[pok]["move4"]]["detail"][0:2]+", "+moves[trackertemp[pok]["move4"]]["contact"])
    typmove4entry.place(x=260,y=240)
    def jsonsave():
        mon1=trackertemp[pok]["mon"]
        abilcont=trackertemp[pok]["ability"]
        if searchdict(abilities, abilcont)!=None:
            mons[mon1]["ability"].append(abilcont)
        movecont=[trackertemp[pok]["move1"],trackertemp[pok]["move2"],trackertemp[pok]["move3"],trackertemp[pok]["move4"]]
        levlcont=trackertemp[pok]["level"]
        for move in movecont:
            if searchdict(moves, move)!=None:
                mons[mon1]["moves"].append(move+", "+levlcont)
        mons[mon1]["lastseenat"]=levlcont
def EnemyMonTracker(tracking):
    frameclearer()
    page=tkinter.Frame(tracking)
    page.grid()
    tracking.geometry("320x270")
    tracking.title("Tracker")
    #status=["-","Burn","Poison","Sleep","Paralysis","Frozen"]
    #statustext=status[0]
    #def statuschange():
        #statustext=status[status.index(statustext)+1]
    #statusbutton=Button(tracking,text=statustext,command=statuschange)
    #statusbutton.grid(row=8,column=12)
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    opponen=Entry(tracking, width=14)
    opponen.grid(row=7,column=5)
    monentry=Entry(tracking, width=14)
    monentry.grid(row=1,column=5)
    def movedisplay():
        if move1entry.get()!="":
            if opponen.get()!="":
                coverage1=str(coverage(moves[move1entry.get()]["type"],monentry.get(),opponen.get(),abilentry.get(),"null","null"))
            else:
                coverage1=""
            move1label=Label(tracking, text="  "+moves[move1entry.get()]["type"]+", "+moves[move1entry.get()]["pp"]+", "+moves[move1entry.get()]["power"]+", "+moves[move1entry.get()]["acc"]+", "+coverage1)
            move1label.grid(row=3, column=8)
        if move2entry.get()!="":
            if opponen.get()!="":
                coverage2=str(coverage(moves[move2entry.get()]["type"],monentry.get(),opponen.get(),abilentry.get(),"null","null"))
            else:
                coverage2=""
            move2label=Label(tracking, text="  "+moves[move2entry.get()]["type"]+", "+moves[move2entry.get()]["pp"]+", "+moves[move2entry.get()]["power"]+", "+moves[move2entry.get()]["acc"]+", "+coverage2)
            move2label.grid(row=5, column=8)
        if move3entry.get()!="":
            if opponen.get()!="":
                coverage3=str(coverage(moves[move3entry.get()]["type"],monentry.get(),opponen.get(),abilentry.get(),"null","null"))
            else:
                coverage3=""
            move3label=Label(tracking, text="  "+moves[move3entry.get()]["type"]+", "+moves[move3entry.get()]["pp"]+", "+moves[move3entry.get()]["power"]+", "+moves[move3entry.get()]["acc"]+", "+coverage3)
            move3label.grid(row=7, column=8)
        if move4entry.get()!="":
            if opponen.get()!="":
                coverage4=str(coverage(moves[move4entry.get()]["type"],monentry.get(),opponen.get(),abilentry.get(),"null","null"))
            else:
                coverage4=""
            move4label=Label(tracking, text="  "+moves[move4entry.get()]["type"]+", "+moves[move4entry.get()]["pp"]+", "+moves[move4entry.get()]["power"]+", "+moves[move4entry.get()]["acc"]+", "+coverage4)
            move4label.grid(row=9, column=8)
        monbst=Label(tracking, text=(mons[str(monentry.get())]["bst"]+", "+mons[str(monentry.get())]["lastseenat"]))
        monbst.grid(row=2, column=3)
        montype=Label(tracking, text=mons[str(monentry.get())]["types"])
        montype.grid(row=2, column=12)
        if opponen.get()!="":
            oppbst=Label(tracking, text=(mons[str(opponen.get())]["bst"]+", "+mons[str(opponen.get())]["lastseenat"]))
            oppbst.grid(row=6, column=3)
            opptype=Label(tracking, text=mons[str(opponen.get())]["types"])
            opptype.grid(row=6, column=12)
    monsaver=BooleanVar()
    monimage=Checkbutton(tracking,variable=monsaver,onvalue=1,offvalue=0)
    monimage.grid(row=1,column=1)
    abillabel=Button(tracking, text = "<-",command=pagechangerleft)
    abillabel.grid(row=1, column=1)
    def playermondata():
        if monentry.get()!="":
            Mon_Data(monentry.get())
    monlabel=Button(tracking, text="Opponent",command=playermondata)
    monlabel.grid(row=1, column=3)
    changepage=Button(tracking, text = "->",command=pagechanger)
    changepage.grid(row=1, column=2)
    notesclear=Button(tracking, text = "Clear Notes", command=NotesClearer)
    notesclear.grid(row=9, column=5)
    def open_abildata():
        if abilentry.get()!="":
            Ability_Data(abilentry.get())
    abillabel=Button(tracking, text = "Abilities",command=open_abildata)
    abillabel.grid(row=4, column=3)
    abilentry=Entry(tracking, width=14)
    abilentry.grid(row=4,column=5)
    itemlabel=Label(tracking, text = "Held Item")
    itemlabel.grid(row=3, column=3)
    itementry=Entry(tracking, width=14)
    itementry.grid(row=3,column=5)
    strinlabel=Label(tracking, text = "String")
    strinlabel.grid(row=5, column=3)
    strinentry=Entry(tracking, width=14)
    strinentry.grid(row=5,column=5)
    hplabel=Label(tracking, text = "HP")
    hplabel.grid(row=3, column=1)
    hpentry=Entry(tracking, width=4)
    hpentry.grid(row=3,column=2)
    atklabel=Label(tracking, text = "ATK")
    atklabel.grid(row=4, column=1)
    atkentry=Entry(tracking, width=4)
    atkentry.grid(row=4,column=2)
    deflabel=Label(tracking, text = "DEF")
    deflabel.grid(row=5, column=1)
    defentry=Entry(tracking, width=4)
    defentry.grid(row=5,column=2)
    spalabel=Label(tracking, text = "SPA")
    spalabel.grid(row=6, column=1)
    spaentry=Entry(tracking, width=4)
    spaentry.grid(row=6,column=2)
    spdlabel=Label(tracking, text = "SPD")
    spdlabel.grid(row=7, column=1)
    spdentry=Entry(tracking, width=4)
    spdentry.grid(row=7,column=2)
    spelabel=Label(tracking, text = "SPE")
    spelabel.grid(row=8, column=1)
    speentry=Entry(tracking, width=4)
    speentry.grid(row=8,column=2)
    acclabel=Label(tracking, text = "ACC")
    acclabel.grid(row=9, column=1)
    accentry=Entry(tracking, width=4)
    accentry.grid(row=9,column=2)
    movelabel=Label(tracking, text = "Moves")
    movelabel.grid(row=1, column=8)
    move1entry=Entry(tracking, width=14)
    move1entry.grid(row=2,column=8)
    move2entry=Entry(tracking, width=14)
    move2entry.grid(row=4,column=8)
    move3entry=Entry(tracking, width=14)
    move3entry.grid(row=6,column=8)
    move4entry=Entry(tracking, width=14)
    move4entry.grid(row=8,column=8)
    movesaver=Button(tracking, text = "Display", command=movedisplay)
    movesaver.grid(row=8, column=3)
    levllabel=Label(tracking, text = "Level")
    levllabel.grid(row=2, column=1)
    levlentry=Entry(tracking, width=4)
    levlentry.grid(row=2,column=2)
    def jsonsave():
        if monsaver.get()==1:
            mon1=opponen.get()
        else:
            mon1=monentry.get()
        abilcont=abilentry.get()
        if searchdict(abilities, abilcont)!=None:
            mons[mon1]["ability"].append(abilcont)
        movecont=[move1entry.get(),move2entry.get(),move3entry.get(),move4entry.get(),]
        levlcont=levlentry.get()
        for move in movecont:
            if searchdict(moves, move)!=None:
                mons[mon1]["moves"].append(move+", "+levlcont)
        mons[mon1]["lastseenat"]=levlcont
        if strinentry.get()!="":
            mons[mon1]["stringnote"]=strinentry.get()
        if hpentry.get()!="":
            mons[mon1]["notes"][0]=hpentry.get()
        if atkentry.get()!="":
            mons[mon1]["notes"][1]=atkentry.get()
        if defentry.get()!="":
            mons[mon1]["notes"][2]=defentry.get()
        if spaentry.get()!="":
            mons[mon1]["notes"][3]=spaentry.get()
        if spdentry.get()!="":
            mons[mon1]["notes"][4]=spdentry.get()
        if speentry.get()!="":
            mons[mon1]["notes"][5]=speentry.get()
    jsonsaver=Button(tracking, text = "Save", command=jsonsave)
    jsonsaver.grid(row=9, column=3)
updater()
tracking.mainloop()
monsfile2=r"mon-data.json"
with open(monsfile2, "w") as f:
    json.dump(mons, f)