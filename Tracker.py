import json
import os
import time
import tkinter
from tkinter import *
from tkinter import ttk
monsfile=open(r'mon-data.json',"r+")
mons=json.load(monsfile)
trackertempfile3=r"trackertemp.json"
trackertempfile=open(trackertempfile3,"r+")
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
print(items["004"])
naturesfile=open(r"nature-data.json")
natures=json.load(naturesfile)
pagemon=1
#4 5 6 placement of mons in a battle
#1 2 3 single=1,4, double=1,2,4,5
party=[trackertemp["1"]["mon"],trackertemp["2"]["mon"],trackertemp["3"]["mon"],trackertemp["4"]["mon"],trackertemp["5"]["mon"],trackertemp["6"]["mon"],]
opponent=["-","-","-","-","-"]
ally=["-"]
print(party)
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
typedic={"Normal":0,"Fighting":1,"Flying":2,"Poison":3,"Ground":4,"Rock":5,"Bug":6,"Ghost":7,"Steel":8,"Fire":9,"Water":10,"Grass":11,"Electric":12,"Psychic":13,"Ice":14,"Dragon":15,"Dark":16,"Fairy":17,"Null":18,}
#extracts and calculates relevant type combo for defenders
def coverage(movetype,attacker,defender,attabil,currweat,currterr):
    typemult=1
    weatmult=1
    stabmult=1
    terrmult=1
    for item in range(0,len(mons[defender]["types"])):
        if item!="-":
            typemult=typemult*(typetable[movetype][typedic[mons[defender]["types"][item]]])
    if movetype in mons[attacker]["types"]:
        if attabil=="adaptability":
            stabmult=2
        else:
            stabmult=1.5
    if currterr=="grassy":
        if movetype=="Grass":
            terrmult=1.5
    if currterr=="misty":
        if movetype=="Dragon":
            terrmult=.5
    if currterr=="electric":
        if movetype=="Electric":
            terrmult=1.5
    if currterr=="psychic":
        if movetype=="Psychic":
            terrmult=1.5
    if currweat=="sun":
        if movetype=="Fire":
            weatmult=1.5
        if movetype=="Water":
            weatmult=.5
    if currweat=="rain":
        if movetype=="Fire":
            weatmult=.5
        if movetype=="Water":
            weatmult=1.5
    return typemult*weatmult*stabmult*terrmult
#tracking party from save data
#gui
tracking=Tk()
def NotesClearer():
    clearer=Toplevel()
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
    notesclear=Button(clearer, text = "Clear Notes", command=noteclear)
    notesclear.grid(row=2, column=1)
def Ability_Data(abil):
    abili=Toplevel()
    abili.title("Ability Data")
    abili.geometry("300x50")
    abilitydata=Label(abili,text=abilities[abil]["detail"],wraplength=300)
    abilitydata.pack()
def moveinfo():
    infom=Toplevel()
    infom.title("Ability Data")
    infom.geometry("300x50")
    movedata=Label(infom,text="First two letters are Ph=Physical, Sp=Special, St=Status. Second two are Co.=Contact, NC=Non-Contact.",wraplength=300)
    movedata.pack()
def Mon1_Data(montemp):
    mon1dat=Toplevel()
    mon1dat.title("Mon Data")
    mon1dat.geometry("300x240")
    for abil in mons[montemp]["ability"]:
        abilloc=mons[montemp]["ability"].index(abil)
        abillabel=Button(mon1dat, text=abil,command=lambda abil=abil:Ability_Data(abil))
        #abil=abil stores the value of it when written
        #I thought it normally did that, but apparently otherwise it only calls that after???
        abillabel.grid(row=6+abilloc, column=4)
        abilentry=Label(mon1dat, text="Ability "+str(1+abilloc))
        abilentry.grid(row=6+abilloc,column=3)
    for item in range(0,len(mons[montemp]["moves"])):
        movelabel=Button(mon1dat, text=mons[montemp]["moves"][item])
        movelabel.grid(row=1+item, column=5)
    mon1name=Label(mon1dat,text=montemp)
    mon1name.grid(row=1,column=4)
    mon1type=Label(mon1dat,text="Types")
    mon1type.grid(row=2,column=3)
    mon1type=Label(mon1dat,text=mons[montemp]["types"])
    mon1type.grid(row=2,column=4)
    monbst=Label(mon1dat,text="BST")
    monbst.grid(row=2,column=1)
    mon1bst=Label(mon1dat,text=mons[montemp]["bst"])
    mon1bst.grid(row=2,column=2)
    leave=Button(mon1dat, text="Leave", command=mon1dat.destroy)
    leave.grid(row=1,column=1)
    monevo=Label(mon1dat,text="Evo")
    monevo.grid(row=1,column=2)
    mon1evo=Label(mon1dat,text=mons[montemp]["evo"])
    mon1evo.grid(row=1,column=3)
    itemlabel=Label(mon1dat, text = "Levels")
    itemlabel.grid(row=3, column=3)
    itementry=Label(mon1dat, text=mons[montemp]["lastseenat"])
    itementry.grid(row=3,column=12)
    strinlabel=Label(mon1dat, text = "String")
    strinlabel.grid(row=4, column=3)
    strinentry=Label(mon1dat, text=mons[montemp]["stringnote"], wraplength=100)
    strinentry.grid(row=4,column=4)
    strinlabel=Label(mon1dat, text = "Moveset")
    strinlabel.grid(row=5, column=3)
    mon_moveset=(moveset[str(int(mons[trackertemp["1"]["mon"]]["id"]))])
    strinentry=Label(mon1dat, text=mon_moveset, wraplength=100)
    strinentry.grid(row=5,column=4)
    hplabel=Label(mon1dat, text = "HP")
    hplabel.grid(row=3, column=1)
    hpentry=Label(mon1dat, text=mons[montemp]["notes"][0])
    hpentry.grid(row=3,column=2)
    atklabel=Label(mon1dat, text = "ATK")
    atklabel.grid(row=4, column=1)
    atkentry=Label(mon1dat, text=mons[montemp]["notes"][1])
    atkentry.grid(row=4,column=2)
    deflabel=Label(mon1dat, text = "DEF")
    deflabel.grid(row=5, column=1)
    defentry=Label(mon1dat, text=mons[montemp]["notes"][2])
    defentry.grid(row=5,column=2)
    spalabel=Label(mon1dat, text = "SPA")
    spalabel.grid(row=6, column=1)
    spaentry=Label(mon1dat, text=mons[montemp]["notes"][3])
    spaentry.grid(row=6,column=2)
    spdlabel=Label(mon1dat, text = "SPD")
    spdlabel.grid(row=7, column=1)
    spdentry=Label(mon1dat, text=mons[montemp]["notes"][4])
    spdentry.grid(row=7,column=2)
    spelabel=Label(mon1dat, text = "SPE")
    spelabel.grid(row=8, column=1)
    speentry=Label(mon1dat, text=mons[montemp]["notes"][5])
    speentry.grid(row=8,column=2)
#battleformat list: single, double, triple, SOS(gen 7), horde, multi, party
battleformat="party"
def formatchanger():
    global battleformat
    if battleformat=="party":
        battleformat="single"
    #to be used later then this is properly implemented, not gonna bother with more than singles rn
    elif battleformat=="single":
        battleformat="double"
    elif battleformat=="double":
        battleformat="triple"
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
        if pagemon==1:
            Mon8_Tracker(tracking)
            pagemon=8
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="double":
        if pagemon==1:
            Mon2_Tracker(tracking)
            pagemon=2
        elif pagemon==2:
            Mon8_Tracker(tracking)
            pagemon=8
        elif pagemon==8:
            Mon9_Tracker(tracking)
            pagemon=9
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="multi":
        if pagemon==1:
            Mon7_Tracker(tracking)
            pagemon=7
        elif pagemon==7:
            Mon8_Tracker(tracking)
            pagemon=8
        elif pagemon==8:
            Mon9_Tracker(tracking)
            pagemon=9
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="triple":
        if pagemon==1:
            Mon2_Tracker(tracking)
            pagemon=2
        elif pagemon==2:
            Mon3_Tracker(tracking)
            pagemon=3
        elif pagemon==3:
            Mon8_Tracker(tracking)
            pagemon=8
        elif pagemon==8:
            Mon9_Tracker(tracking)
            pagemon=9
        elif pagemon==9:
            Mon10_Tracker(tracking)
            pagemon=10
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="SOS":
        if pagemon==1:
            Mon8_Tracker(tracking)
            pagemon=8
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="horde":
        if pagemon==1:
            Mon8_Tracker(tracking)
            pagemon=8
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="party":
        if pagemon==1:
            if trackertemp["2"]["mon"]!="-":
                Mon2_Tracker(tracking)
                pagemon=2
            else:
                Mon1_Tracker(tracking)
                pagemon=1
        elif pagemon==2:
            if trackertemp["3"]["mon"]!="-":
                Mon3_Tracker(tracking)
                pagemon=3
            else:
                Mon1_Tracker(tracking)
                pagemon=1
        elif pagemon==3:
            if trackertemp["4"]["mon"]!="-":
                Mon4_Tracker(tracking)
                pagemon=4
            else:
                Mon1_Tracker(tracking)
                pagemon=1
        elif pagemon==4:
            if trackertemp["5"]["mon"]!="-":
                Mon5_Tracker(tracking)
                pagemon=5
            else:
                Mon1_Tracker(tracking)
                pagemon=1
        elif pagemon==5:
            if trackertemp["6"]["mon"]!="-":
                Mon6_Tracker(tracking)
                pagemon=6
            else:
                Mon1_Tracker(tracking)
                pagemon=1
        else:
            Mon1_Tracker(tracking)
            pagemon=1
        print(trackertemp[str(pagemon)]["mon"])
    print(pagemon)
def pagechangerleft():
    global pagemon
    if battleformat=="party":
        if pagemon==3:
            if trackertemp["2"]["mon"]!="-":
                Mon2_Tracker(tracking)
                pagemon=2
            else:
                Mon1_Tracker(tracking)
                pagemon=1
        elif pagemon==4:
            if trackertemp["3"]["mon"]!="-":
                Mon3_Tracker(tracking)
                pagemon=3
            else:
                Mon1_Tracker(tracking)
                pagemon=1
        elif pagemon==5:
            if trackertemp["4"]["mon"]!="-":
                Mon4_Tracker(tracking)
                pagemon=4
            else:
                Mon1_Tracker(tracking)
                pagemon=1
        elif pagemon==6:
            if trackertemp["5"]["mon"]!="-":
                Mon5_Tracker(tracking)
                pagemon=5
            else:
                Mon1_Tracker(tracking)
                pagemon=1
        elif pagemon==1:
            if trackertemp["6"]["mon"]!="-":
                Mon6_Tracker(tracking)
                pagemon=6
            elif trackertemp["5"]["mon"]!="-":
                Mon5_Tracker(tracking)
                pagemon=5
            elif trackertemp["4"]["mon"]!="-":
                Mon4_Tracker(tracking)
                pagemon=4
            elif trackertemp["3"]["mon"]!="-":
                Mon3_Tracker(tracking)
                pagemon=3
            elif trackertemp["2"]["mon"]!="-":
                Mon2_Tracker(tracking)
                pagemon=2
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="single":
        if pagemon==1:
            Mon8_Tracker(tracking)
            pagemon=8
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="double":
        if pagemon==8:
            Mon2_Tracker(tracking)
            pagemon=2
        elif pagemon==9:
            Mon8_Tracker(tracking)
            pagemon=8
        elif pagemon==1:
            Mon9_Tracker(tracking)
            pagemon=9
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="multi":
        if pagemon==1:
            Mon7_Tracker(tracking)
            pagemon=7
        elif pagemon==7:
            Mon8_Tracker(tracking)
            pagemon=8
        elif pagemon==8:
            Mon9_Tracker(tracking)
            pagemon=9
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="triple":
        if pagemon==3:
            Mon2_Tracker(tracking)
            pagemon=2
        elif pagemon==8:
            Mon3_Tracker(tracking)
            pagemon=3
        elif pagemon==9:
            Mon8_Tracker(tracking)
            pagemon=8
        elif pagemon==10:
            Mon9_Tracker(tracking)
            pagemon=9
        elif pagemon==1:
            Mon10_Tracker(tracking)
            pagemon=10
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="SOS":
        if pagemon==1:
            Mon8_Tracker(tracking)
            pagemon=8
        else:
            Mon1_Tracker(tracking)
            pagemon=1
    elif battleformat=="horde":
        if pagemon==1:
            Mon8_Tracker(tracking)
            pagemon=8
        else:
            Mon1_Tracker(tracking)
            pagemon=1
def updater():
    if pagemon==2:
        Mon2_Tracker(tracking)
    elif pagemon==3:
        Mon3_Tracker(tracking)
    elif pagemon==4:
        Mon4_Tracker(tracking)
    elif pagemon==5:
        Mon5_Tracker(tracking)
    elif pagemon==6:
        Mon6_Tracker(tracking)
    elif pagemon==7:
        Mon7_Tracker(tracking)
    elif pagemon==8:
        Mon8_Tracker(tracking)
    elif pagemon==9:
        Mon9_Tracker(tracking)
    elif pagemon==10:
        Mon10_Tracker(tracking)
    elif pagemon==11:
        Mon11_Tracker(tracking)
    elif pagemon==12:
        Mon12_Tracker(tracking)
    else:
        Mon1_Tracker(tracking)
    tracking.after(10000,updater)
def gamechanger():
    if trackertemp["game"]=="XY":
        trackertemp["game"]="ORAS"
    elif trackertemp["game"]=="ORAS":
        trackertemp["game"]="SM"
    elif trackertemp["game"]=="SM":
        trackertemp["game"]="USUM"
    elif trackertemp["game"]=="USUM":
        trackertemp["game"]="XY"
    with open(trackertempfile3, "w") as f:
        json.dump(trackertemp,f)
def naturecalcm(numt):
    global Satk,Sdef,Sspa,Sspd,Sspe
    Satk=""
    Sdef=""
    Sspa=""
    Sspd=""
    Sspe=""
    print(natures[trackertemp[numt]["nature"]]["-"])
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
def naturecalcp(numt):
    global Satk,Sdef,Sspa,Sspd,Sspe
    print(natures[trackertemp[numt]["nature"]]["+"])
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
#11 tracking pages for different mons
def Mon1_Tracker(tracking):
    frameclearer()
    trackertempfile=open(r"trackertemp.json","r+")
    trackertemp=json.load(trackertempfile)
    tracking.geometry("360x240")
    tracking.title("Tracker")
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    abillabel=Button(tracking, text = "<-",command=pagechangerleft)
    abillabel.grid(row=1, column=1)
    monlabel=Button(tracking, text=trackertemp["1"]["mon"],command=lambda:Mon1_Data(trackertemp["1"]["mon"]))
    monlabel.grid(row=1, column=3)
    mon_moveset=(moveset[str(int(mons[trackertemp["1"]["mon"]]["id"]))])
    for item in mon_moveset:
        if int(item)>int(trackertemp["1"]["level"]):
            nextmove=item
            break
        nextmove="-"
    changepage=Button(tracking, text="->",command=pagechanger)
    changepage.grid(row=1, column=2)
    changegame=Button(tracking, text=trackertemp["game"],command=gamechanger)
    changegame.grid(row=1, column=4)
    changeform=Button(tracking, text=battleformat,command=formatchanger)
    changeform.grid(row=2, column=4)
    abillabel=Button(tracking, text=trackertemp["1"]["ability"],command=lambda: Ability_Data(trackertemp["1"]["ability"]))
    abillabel.grid(row=4, column=3)
    itemlabel=Label(tracking, text=items[str(trackertemp["1"]["item"]).zfill(3)]["name"])
    itemlabel.grid(row=3, column=3)
    strinlabel=Label(tracking, text=str(trackertemp["1"]["currhp"])+"/"+str(trackertemp["1"]["maxhp"]))
    strinlabel.grid(row=5, column=3)
    for item in range(0,len(mons[trackertemp["1"]["mon"]]["types"])):
        types2=Label(tracking, text =mons[trackertemp["1"]["mon"]]["types"][item])
        types2.grid(row=3+item,column=1)
    hplabel=Label(tracking, text = "HP")
    hplabel.grid(row=1, column=9)
    hpentry=Label(tracking, text=trackertemp["1"]["maxhp"])
    hpentry.grid(row=1,column=10)
    naturecalcm("1")
    naturecalcp("1")
    atklabel=Label(tracking, text = "ATK")
    atklabel.grid(row=2, column=9)
    atkentry=Label(tracking, text=Satk+trackertemp["1"]["atk"])
    atkentry.grid(row=2,column=10)
    deflabel=Label(tracking, text = "DEF")
    deflabel.grid(row=3, column=9)
    defentry=Label(tracking, text=Sdef+trackertemp["1"]["def"])
    defentry.grid(row=3,column=10)
    spalabel=Label(tracking, text = "SPA")
    spalabel.grid(row=4, column=9)
    spaentry=Label(tracking, text=Sspa+trackertemp["1"]["spa"])
    spaentry.grid(row=4,column=10)
    spdlabel=Label(tracking, text = "SPD")
    spdlabel.grid(row=5, column=9)
    spdentry=Label(tracking, text=Sspd+trackertemp["1"]["spd"])
    spdentry.grid(row=5,column=10)
    spelabel=Label(tracking, text = "SPE")
    spelabel.grid(row=6, column=9)
    speentry=Label(tracking, text=Sspe+trackertemp["1"]["spe"])
    speentry.grid(row=6,column=10)
    spelabel=Label(tracking, text = "BST")
    spelabel.grid(row=7, column=9)
    bstlabel=Label(tracking, text=mons[trackertemp["1"]["mon"]]["bst"])
    bstlabel.grid(row=7,column=10)
    #badgelabel=Label(tracking, text = "Badges")
    #badgelabel.grid(row=1, column=11)
    #badge1=Checkbutton(tracking,text="1")
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
    movelabel=Label(tracking, text = "Moves ["+nextmove+"]")
    movelabel.grid(row=6, column=1)
    move1entry=Label(tracking, text=trackertemp["1"]["move1"])
    move1entry.grid(row=7,column=1)
    move2entry=Label(tracking, text=trackertemp["1"]["move2"])
    move2entry.grid(row=8,column=1)
    move3entry=Label(tracking, text=trackertemp["1"]["move3"])
    move3entry.grid(row=9,column=1)
    move4entry=Label(tracking, text=trackertemp["1"]["move4"])
    move4entry.grid(row=10,column=1)
    ppmovelabel=Label(tracking, text = "PP")
    ppmovelabel.grid(row=6, column=2)
    ppmove1entry=Label(tracking, text=moves[trackertemp["1"]["move1"]]["pp"])
    ppmove1entry.grid(row=7,column=2)
    ppmove2entry=Label(tracking, text=moves[trackertemp["1"]["move2"]]["pp"])
    ppmove2entry.grid(row=8,column=2)
    ppmove3entry=Label(tracking, text=moves[trackertemp["1"]["move3"]]["pp"])
    ppmove3entry.grid(row=9,column=2)
    ppmove4entry=Label(tracking, text=moves[trackertemp["1"]["move4"]]["pp"])
    ppmove4entry.grid(row=10,column=2)
    powmovelabel=Label(tracking, text = "Pow")
    powmovelabel.grid(row=6, column=3)
    powmove1entry=Label(tracking, text=moves[trackertemp["1"]["move1"]]["power"])
    powmove1entry.grid(row=7,column=3)
    powmove2entry=Label(tracking, text=moves[trackertemp["1"]["move2"]]["power"])
    powmove2entry.grid(row=8,column=3)
    powmove3entry=Label(tracking, text=moves[trackertemp["1"]["move3"]]["power"])
    powmove3entry.grid(row=9,column=3)
    powmove4entry=Label(tracking, text=moves[trackertemp["1"]["move4"]]["power"])
    powmove4entry.grid(row=10,column=3)
    accmovelabel=Label(tracking, text = "Acc")
    accmovelabel.grid(row=6, column=4)
    accmove1entry=Label(tracking, text=moves[trackertemp["1"]["move1"]]["acc"])
    accmove1entry.grid(row=7,column=4)
    accmove2entry=Label(tracking, text=moves[trackertemp["1"]["move2"]]["acc"])
    accmove2entry.grid(row=8,column=4)
    accmove3entry=Label(tracking, text=moves[trackertemp["1"]["move3"]]["acc"])
    accmove3entry.grid(row=9,column=4)
    accmove4entry=Label(tracking, text=moves[trackertemp["1"]["move4"]]["acc"])
    accmove4entry.grid(row=10,column=4)
    typmovelabel=Label(tracking, text = "Type")
    typmovelabel.grid(row=6, column=5)
    typmove1entry=Label(tracking, text=moves[trackertemp["1"]["move1"]]["type"])
    typmove1entry.grid(row=7,column=5)
    typmove2entry=Label(tracking, text=moves[trackertemp["1"]["move2"]]["type"])
    typmove2entry.grid(row=8,column=5)
    typmove3entry=Label(tracking, text=moves[trackertemp["1"]["move3"]]["type"])
    typmove3entry.grid(row=9,column=5)
    typmove4entry=Label(tracking, text=moves[trackertemp["1"]["move4"]]["type"])
    typmove4entry.grid(row=10,column=5)
    typmovelabel=Button(tracking, text = "Contact", command=moveinfo)
    typmovelabel.grid(row=6, column=6)
    typmove1entry=Label(tracking, text=moves[trackertemp["1"]["move1"]]["detail"][0:2]+", "+moves[trackertemp["1"]["move1"]]["contact"])
    typmove1entry.grid(row=7,column=6)
    typmove2entry=Label(tracking, text=moves[trackertemp["1"]["move2"]]["detail"][0:2]+", "+moves[trackertemp["1"]["move2"]]["contact"])
    typmove2entry.grid(row=8,column=6)
    typmove3entry=Label(tracking, text=moves[trackertemp["1"]["move3"]]["detail"][0:2]+", "+moves[trackertemp["1"]["move3"]]["contact"])
    typmove3entry.grid(row=9,column=6)
    typmove4entry=Label(tracking, text=moves[trackertemp["1"]["move4"]]["detail"][0:2]+", "+moves[trackertemp["1"]["move4"]]["contact"])
    typmove4entry.grid(row=10,column=6)
    #display
    levllabel=Label(tracking, text = "Lv. "+trackertemp["1"]["level"]+" ("+mons[trackertemp["1"]["mon"]]["evo"]+")")
    levllabel.grid(row=2, column=3)
    def jsonsave():
        mon1=trackertemp["1"]["mon"]
        abilcont=trackertemp["1"]["ability"]
        if searchdict(abilities, abilcont)!=None:
            mons[mon1]["ability"].append(abilcont)
        movecont=[move1entry.get(),move2entry.get(),move3entry.get(),move4entry.get(),]
        levlcont=trackertemp["1"]["level"]
        for move in movecont:
            if searchdict(moves, move)!=None:
                mons[mon1]["moves"].append(move+", "+levlcont)
        mons[mon1]["lastseenat"]=levlcont
    #save
    jsonsaver=Button(tracking, text = "S", command=jsonsave)
    jsonsaver.grid(row=2, column=1)
def Mon2_Tracker(tracking):
    frameclearer()
    trackertempfile=open(r"trackertemp.json","r+")
    trackertemp=json.load(trackertempfile)
    tracking.geometry("360x240")
    tracking.title("Tracker")
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    abillabel=Button(tracking, text = "<-",command=pagechangerleft)
    abillabel.grid(row=1, column=1)
    monlabel=Button(tracking, text=trackertemp["2"]["mon"],command=lambda:Mon1_Data(trackertemp["2"]["mon"]))
    monlabel.grid(row=1, column=3)
    mon_moveset=(moveset[str(int(mons[trackertemp["2"]["mon"]]["id"]))])
    for item in mon_moveset:
        if int(item)>int(trackertemp["2"]["level"]):
            nextmove=item
            break
        nextmove="-"
    changepage=Button(tracking, text = "->",command=pagechanger)
    changepage.grid(row=1, column=2)
    abillabel=Button(tracking, text=trackertemp["2"]["ability"],command=lambda: Ability_Data(trackertemp["2"]["ability"]))
    abillabel.grid(row=4, column=3)
    itemlabel=Label(tracking, text=items[str(trackertemp["2"]["item"]).zfill(3)]["name"])
    itemlabel.grid(row=3, column=3)
    strinlabel=Label(tracking, text=str(trackertemp["2"]["currhp"])+"/"+str(trackertemp["2"]["maxhp"]))
    strinlabel.grid(row=5, column=3)
    for item in range(0,len(mons[trackertemp["2"]["mon"]]["types"])):
        types2=Label(tracking, text =mons[trackertemp["2"]["mon"]]["types"][item])
        types2.grid(row=3+item,column=1)
    hplabel=Label(tracking, text = "HP")
    hplabel.grid(row=1, column=9)
    hpentry=Label(tracking, text =trackertemp["2"]["maxhp"])
    hpentry.grid(row=1,column=10)
    naturecalcm("2")
    naturecalcp("2")
    atklabel=Label(tracking, text = "ATK")
    atklabel.grid(row=2, column=9)
    atkentry=Label(tracking, text =Satk+trackertemp["2"]["atk"])
    atkentry.grid(row=2,column=10)
    deflabel=Label(tracking, text = "DEF")
    deflabel.grid(row=3, column=9)
    defentry=Label(tracking, text =Sdef+trackertemp["2"]["def"])
    defentry.grid(row=3,column=10)
    spalabel=Label(tracking, text = "SPA")
    spalabel.grid(row=4, column=9)
    spaentry=Label(tracking, text =Sspa+trackertemp["2"]["spa"])
    spaentry.grid(row=4,column=10)
    spdlabel=Label(tracking, text = "SPD")
    spdlabel.grid(row=5, column=9)
    spdentry=Label(tracking, text =Sspd+trackertemp["2"]["spd"])
    spdentry.grid(row=5,column=10)
    spelabel=Label(tracking, text = "SPE")
    spelabel.grid(row=6, column=9)
    speentry=Label(tracking, text =Sspe+trackertemp["2"]["spe"])
    speentry.grid(row=6,column=10)
    spelabel=Label(tracking, text = "BST")
    spelabel.grid(row=7, column=9)
    bstlabel=Label(tracking, text=mons[trackertemp["2"]["mon"]]["bst"])
    bstlabel.grid(row=7,column=10)
    movelabel=Label(tracking, text = "Moves ["+nextmove+"]")
    movelabel.grid(row=6, column=1)
    move1entry=Label(tracking, text=trackertemp["2"]["move1"])
    move1entry.grid(row=7,column=1)
    move2entry=Label(tracking, text=trackertemp["2"]["move2"])
    move2entry.grid(row=8,column=1)
    move3entry=Label(tracking, text=trackertemp["2"]["move3"])
    move3entry.grid(row=9,column=1)
    move4entry=Label(tracking, text=trackertemp["2"]["move4"])
    move4entry.grid(row=10,column=1)
    ppmovelabel=Label(tracking, text = "PP")
    ppmovelabel.grid(row=6, column=2)
    ppmove1entry=Label(tracking, text=moves[trackertemp["2"]["move1"]]["pp"])
    ppmove1entry.grid(row=7,column=2)
    ppmove2entry=Label(tracking, text=moves[trackertemp["2"]["move2"]]["pp"])
    ppmove2entry.grid(row=8,column=2)
    ppmove3entry=Label(tracking, text=moves[trackertemp["2"]["move3"]]["pp"])
    ppmove3entry.grid(row=9,column=2)
    ppmove4entry=Label(tracking, text=moves[trackertemp["2"]["move4"]]["pp"])
    ppmove4entry.grid(row=10,column=2)
    powmovelabel=Label(tracking, text = "Pow")
    powmovelabel.grid(row=6, column=3)
    powmove1entry=Label(tracking, text=moves[trackertemp["2"]["move1"]]["power"])
    powmove1entry.grid(row=7,column=3)
    powmove2entry=Label(tracking, text=moves[trackertemp["2"]["move2"]]["power"])
    powmove2entry.grid(row=8,column=3)
    powmove3entry=Label(tracking, text=moves[trackertemp["2"]["move3"]]["power"])
    powmove3entry.grid(row=9,column=3)
    powmove4entry=Label(tracking, text=moves[trackertemp["2"]["move4"]]["power"])
    powmove4entry.grid(row=10,column=3)
    accmovelabel=Label(tracking, text = "Acc")
    accmovelabel.grid(row=6, column=4)
    accmove1entry=Label(tracking, text=moves[trackertemp["2"]["move1"]]["acc"])
    accmove1entry.grid(row=7,column=4)
    accmove2entry=Label(tracking, text=moves[trackertemp["2"]["move2"]]["acc"])
    accmove2entry.grid(row=8,column=4)
    accmove3entry=Label(tracking, text=moves[trackertemp["2"]["move3"]]["acc"])
    accmove3entry.grid(row=9,column=4)
    accmove4entry=Label(tracking, text=moves[trackertemp["2"]["move4"]]["acc"])
    accmove4entry.grid(row=10,column=4)
    typmovelabel=Label(tracking, text = "Type")
    typmovelabel.grid(row=6, column=5)
    typmove1entry=Label(tracking, text=moves[trackertemp["2"]["move1"]]["type"])
    typmove1entry.grid(row=7,column=5)
    typmove2entry=Label(tracking, text=moves[trackertemp["2"]["move2"]]["type"])
    typmove2entry.grid(row=8,column=5)
    typmove3entry=Label(tracking, text=moves[trackertemp["2"]["move3"]]["type"])
    typmove3entry.grid(row=9,column=5)
    typmove4entry=Label(tracking, text=moves[trackertemp["2"]["move4"]]["type"])
    typmove4entry.grid(row=10,column=5)
    typmovelabel=Button(tracking, text = "Contact", command=moveinfo)
    typmovelabel.grid(row=6, column=6)
    typmove1entry=Label(tracking, text=moves[trackertemp["2"]["move1"]]["detail"][0:2]+", "+moves[trackertemp["2"]["move1"]]["contact"])
    typmove1entry.grid(row=7,column=6)
    typmove2entry=Label(tracking, text=moves[trackertemp["2"]["move2"]]["detail"][0:2]+", "+moves[trackertemp["2"]["move2"]]["contact"])
    typmove2entry.grid(row=8,column=6)
    typmove3entry=Label(tracking, text=moves[trackertemp["2"]["move3"]]["detail"][0:2]+", "+moves[trackertemp["2"]["move3"]]["contact"])
    typmove3entry.grid(row=9,column=6)
    typmove4entry=Label(tracking, text=moves[trackertemp["2"]["move4"]]["detail"][0:2]+", "+moves[trackertemp["2"]["move4"]]["contact"])
    typmove4entry.grid(row=10,column=6)
    #display
    levllabel=Label(tracking, text = "Lv. "+trackertemp["2"]["level"]+" ("+mons[trackertemp["2"]["mon"]]["evo"]+")")
    levllabel.grid(row=2, column=3)
    def jsonsave():
        mon1=trackertemp["2"]["mon"]
        abilcont=trackertemp["2"]["ability"]
        if searchdict(abilities, abilcont)!=None:
            mons[mon1]["ability"].append(abilcont)
        movecont=[move1entry.get(),move2entry.get(),move3entry.get(),move4entry.get(),]
        levlcont=trackertemp["2"]["level"]
        for move in movecont:
            if searchdict(moves, move)!=None:
                mons[mon1]["moves"].append(move+", "+levlcont)
        mons[mon1]["lastseenat"]=levlcont
    #save
    jsonsaver=Button(tracking, text = "S", command=jsonsave)
    jsonsaver.grid(row=2, column=1)
def Mon3_Tracker(tracking):
    frameclearer()
    trackertempfile=open(r"trackertemp.json","r+")
    trackertemp=json.load(trackertempfile)
    tracking.geometry("360x240")
    tracking.title("Tracker")
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    abillabel=Button(tracking, text = "<-",command=pagechangerleft)
    abillabel.grid(row=1, column=1)
    monlabel=Button(tracking, text=trackertemp["3"]["mon"],command=lambda:Mon1_Data(trackertemp["3"]["mon"]))
    monlabel.grid(row=1, column=3)
    mon_moveset=(moveset[str(int(mons[trackertemp["3"]["mon"]]["id"]))])
    for item in mon_moveset:
        if int(item)>int(trackertemp["3"]["level"]):
            nextmove=item
            break
        nextmove="-"
    changepage=Button(tracking, text = "->",command=pagechanger)
    changepage.grid(row=1, column=2)
    abillabel=Button(tracking, text=trackertemp["3"]["ability"],command=lambda: Ability_Data(trackertemp["3"]["ability"]))
    abillabel.grid(row=4, column=3)
    itemlabel=Label(tracking, text=items[str(trackertemp["3"]["item"]).zfill(3)]["name"])
    itemlabel.grid(row=3, column=3)
    strinlabel=Label(tracking, text=str(trackertemp["3"]["currhp"])+"/"+str(trackertemp["3"]["maxhp"]))
    strinlabel.grid(row=5, column=3)
    for item in range(0,len(mons[trackertemp["3"]["mon"]]["types"])):
        types2=Label(tracking, text =mons[trackertemp["3"]["mon"]]["types"][item])
        types2.grid(row=3+item,column=1)
    hplabel=Label(tracking, text = "HP")
    hplabel.grid(row=1, column=9)
    hpentry=Label(tracking, text =trackertemp["3"]["maxhp"])
    hpentry.grid(row=1,column=10)
    naturecalcm("3")
    naturecalcp("3")
    atklabel=Label(tracking, text = "ATK")
    atklabel.grid(row=2, column=9)
    atkentry=Label(tracking, text =Satk+trackertemp["3"]["atk"])
    atkentry.grid(row=2,column=10)
    deflabel=Label(tracking, text = "DEF")
    deflabel.grid(row=3, column=9)
    defentry=Label(tracking, text =Sdef+trackertemp["3"]["def"])
    defentry.grid(row=3,column=10)
    spalabel=Label(tracking, text = "SPA")
    spalabel.grid(row=4, column=9)
    spaentry=Label(tracking, text =Sspa+trackertemp["3"]["spa"])
    spaentry.grid(row=4,column=10)
    spdlabel=Label(tracking, text = "SPD")
    spdlabel.grid(row=5, column=9)
    spdentry=Label(tracking, text =Sspd+trackertemp["3"]["spd"])
    spdentry.grid(row=5,column=10)
    spelabel=Label(tracking, text = "SPE")
    spelabel.grid(row=6, column=9)
    speentry=Label(tracking, text =Sspe+trackertemp["3"]["spe"])
    speentry.grid(row=6,column=10)
    spelabel=Label(tracking, text = "BST")
    spelabel.grid(row=7, column=9)
    bstlabel=Label(tracking, text=mons[trackertemp["3"]["mon"]]["bst"])
    bstlabel.grid(row=7,column=10)
    movelabel=Label(tracking, text = "Moves ["+nextmove+"]")
    movelabel.grid(row=6, column=1)
    move1entry=Label(tracking, text=trackertemp["3"]["move1"])
    move1entry.grid(row=7,column=1)
    move2entry=Label(tracking, text=trackertemp["3"]["move2"])
    move2entry.grid(row=8,column=1)
    move3entry=Label(tracking, text=trackertemp["3"]["move3"])
    move3entry.grid(row=9,column=1)
    move4entry=Label(tracking, text=trackertemp["3"]["move4"])
    move4entry.grid(row=10,column=1)
    ppmovelabel=Label(tracking, text = "PP")
    ppmovelabel.grid(row=6, column=2)
    ppmove1entry=Label(tracking, text=moves[trackertemp["3"]["move1"]]["pp"])
    ppmove1entry.grid(row=7,column=2)
    ppmove2entry=Label(tracking, text=moves[trackertemp["3"]["move2"]]["pp"])
    ppmove2entry.grid(row=8,column=2)
    ppmove3entry=Label(tracking, text=moves[trackertemp["3"]["move3"]]["pp"])
    ppmove3entry.grid(row=9,column=2)
    ppmove4entry=Label(tracking, text=moves[trackertemp["3"]["move4"]]["pp"])
    ppmove4entry.grid(row=10,column=2)
    powmovelabel=Label(tracking, text = "Pow")
    powmovelabel.grid(row=6, column=3)
    powmove1entry=Label(tracking, text=moves[trackertemp["3"]["move1"]]["power"])
    powmove1entry.grid(row=7,column=3)
    powmove2entry=Label(tracking, text=moves[trackertemp["3"]["move2"]]["power"])
    powmove2entry.grid(row=8,column=3)
    powmove3entry=Label(tracking, text=moves[trackertemp["3"]["move3"]]["power"])
    powmove3entry.grid(row=9,column=3)
    powmove4entry=Label(tracking, text=moves[trackertemp["3"]["move4"]]["power"])
    powmove4entry.grid(row=10,column=3)
    accmovelabel=Label(tracking, text = "Acc")
    accmovelabel.grid(row=6, column=4)
    accmove1entry=Label(tracking, text=moves[trackertemp["3"]["move1"]]["acc"])
    accmove1entry.grid(row=7,column=4)
    accmove2entry=Label(tracking, text=moves[trackertemp["3"]["move2"]]["acc"])
    accmove2entry.grid(row=8,column=4)
    accmove3entry=Label(tracking, text=moves[trackertemp["3"]["move3"]]["acc"])
    accmove3entry.grid(row=9,column=4)
    accmove4entry=Label(tracking, text=moves[trackertemp["3"]["move4"]]["acc"])
    accmove4entry.grid(row=10,column=4)
    typmovelabel=Label(tracking, text = "Type")
    typmovelabel.grid(row=6, column=5)
    typmove1entry=Label(tracking, text=moves[trackertemp["3"]["move1"]]["type"])
    typmove1entry.grid(row=7,column=5)
    typmove2entry=Label(tracking, text=moves[trackertemp["3"]["move2"]]["type"])
    typmove2entry.grid(row=8,column=5)
    typmove3entry=Label(tracking, text=moves[trackertemp["3"]["move3"]]["type"])
    typmove3entry.grid(row=9,column=5)
    typmove4entry=Label(tracking, text=moves[trackertemp["3"]["move4"]]["type"])
    typmove4entry.grid(row=10,column=5)
    typmovelabel=Button(tracking, text = "Contact", command=moveinfo)
    typmovelabel.grid(row=6, column=6)
    typmove1entry=Label(tracking, text=moves[trackertemp["3"]["move1"]]["detail"][0:2]+", "+moves[trackertemp["3"]["move1"]]["contact"])
    typmove1entry.grid(row=7,column=6)
    typmove2entry=Label(tracking, text=moves[trackertemp["3"]["move2"]]["detail"][0:2]+", "+moves[trackertemp["3"]["move2"]]["contact"])
    typmove2entry.grid(row=8,column=6)
    typmove3entry=Label(tracking, text=moves[trackertemp["3"]["move3"]]["detail"][0:2]+", "+moves[trackertemp["3"]["move3"]]["contact"])
    typmove3entry.grid(row=9,column=6)
    typmove4entry=Label(tracking, text=moves[trackertemp["3"]["move4"]]["detail"][0:2]+", "+moves[trackertemp["3"]["move4"]]["contact"])
    typmove4entry.grid(row=10,column=6)
    #display
    levllabel=Label(tracking, text = "Lv. "+trackertemp["3"]["level"]+" ("+mons[trackertemp["3"]["mon"]]["evo"]+")")
    levllabel.grid(row=2, column=3)
    def jsonsave():
        mon1=trackertemp["3"]["mon"]
        abilcont=trackertemp["3"]["ability"]
        if searchdict(abilities, abilcont)!=None:
            mons[mon1]["ability"].append(abilcont)
        movecont=[move1entry.get(),move2entry.get(),move3entry.get(),move4entry.get(),]
        levlcont=trackertemp["3"]["level"]
        for move in movecont:
            if searchdict(moves, move)!=None:
                mons[mon1]["moves"].append(move+", "+levlcont)
        mons[mon1]["lastseenat"]=levlcont
    #save
    jsonsaver=Button(tracking, text = "S", command=jsonsave)
    jsonsaver.grid(row=2, column=1)
def Mon4_Tracker(tracking):
    frameclearer()
    trackertempfile=open(r"trackertemp.json","r+")
    trackertemp=json.load(trackertempfile)
    tracking.geometry("360x240")
    tracking.title("Tracker")
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    abillabel=Button(tracking, text = "<-",command=pagechangerleft)
    abillabel.grid(row=1, column=1)
    monlabel=Button(tracking, text=trackertemp["4"]["mon"],command=lambda:Mon1_Data(trackertemp["4"]["mon"]))
    monlabel.grid(row=1, column=3)
    mon_moveset=(moveset[str(int(mons[trackertemp["4"]["mon"]]["id"]))])
    for item in mon_moveset:
        if int(item)>int(trackertemp["4"]["level"]):
            nextmove=item
            break
        nextmove="-"
    changepage=Button(tracking, text = "->",command=pagechanger)
    changepage.grid(row=1, column=2)
    abillabel=Button(tracking, text=trackertemp["4"]["ability"],command=lambda: Ability_Data(trackertemp["4"]["ability"]))
    abillabel.grid(row=4, column=3)
    itemlabel=Label(tracking, text=items[str(trackertemp["4"]["item"]).zfill(3)]["name"])
    itemlabel.grid(row=3, column=3)
    strinlabel=Label(tracking, text=str(trackertemp["4"]["currhp"])+"/"+str(trackertemp["4"]["maxhp"]))
    strinlabel.grid(row=5, column=3)
    for item in range(0,len(mons[trackertemp["4"]["mon"]]["types"])):
        types2=Label(tracking, text =mons[trackertemp["4"]["mon"]]["types"][item])
        types2.grid(row=3+item,column=1)
    hplabel=Label(tracking, text = "HP")
    hplabel.grid(row=1, column=9)
    hpentry=Label(tracking, text =trackertemp["4"]["maxhp"])
    hpentry.grid(row=1,column=10)
    naturecalcm("4")
    naturecalcp("4")
    atklabel=Label(tracking, text = "ATK")
    atklabel.grid(row=2, column=9)
    atkentry=Label(tracking, text =Satk+trackertemp["4"]["atk"])
    atkentry.grid(row=2,column=10)
    deflabel=Label(tracking, text = "DEF")
    deflabel.grid(row=3, column=9)
    defentry=Label(tracking, text =Sdef+trackertemp["4"]["def"])
    defentry.grid(row=3,column=10)
    spalabel=Label(tracking, text = "SPA")
    spalabel.grid(row=4, column=9)
    spaentry=Label(tracking, text =Sspa+trackertemp["4"]["spa"])
    spaentry.grid(row=4,column=10)
    spdlabel=Label(tracking, text = "SPD")
    spdlabel.grid(row=5, column=9)
    spdentry=Label(tracking, text =Sspd+trackertemp["4"]["spd"])
    spdentry.grid(row=5,column=10)
    spelabel=Label(tracking, text = "SPE")
    spelabel.grid(row=6, column=9)
    speentry=Label(tracking, text =Sspe+trackertemp["4"]["spe"])
    speentry.grid(row=6,column=10)
    spelabel=Label(tracking, text = "BST")
    spelabel.grid(row=7, column=9)
    bstlabel=Label(tracking, text=mons[trackertemp["4"]["mon"]]["bst"])
    bstlabel.grid(row=7,column=10)
    movelabel=Label(tracking, text = "Moves ["+nextmove+"]")
    movelabel.grid(row=6, column=1)
    move1entry=Label(tracking, text=trackertemp["4"]["move1"])
    move1entry.grid(row=7,column=1)
    move2entry=Label(tracking, text=trackertemp["4"]["move2"])
    move2entry.grid(row=8,column=1)
    move3entry=Label(tracking, text=trackertemp["4"]["move3"])
    move3entry.grid(row=9,column=1)
    move4entry=Label(tracking, text=trackertemp["4"]["move4"])
    move4entry.grid(row=10,column=1)
    ppmovelabel=Label(tracking, text = "PP")
    ppmovelabel.grid(row=6, column=2)
    ppmove1entry=Label(tracking, text=moves[trackertemp["4"]["move1"]]["pp"])
    ppmove1entry.grid(row=7,column=2)
    ppmove2entry=Label(tracking, text=moves[trackertemp["4"]["move2"]]["pp"])
    ppmove2entry.grid(row=8,column=2)
    ppmove3entry=Label(tracking, text=moves[trackertemp["4"]["move3"]]["pp"])
    ppmove3entry.grid(row=9,column=2)
    ppmove4entry=Label(tracking, text=moves[trackertemp["4"]["move4"]]["pp"])
    ppmove4entry.grid(row=10,column=2)
    powmovelabel=Label(tracking, text = "Pow")
    powmovelabel.grid(row=6, column=3)
    powmove1entry=Label(tracking, text=moves[trackertemp["4"]["move1"]]["power"])
    powmove1entry.grid(row=7,column=3)
    powmove2entry=Label(tracking, text=moves[trackertemp["4"]["move2"]]["power"])
    powmove2entry.grid(row=8,column=3)
    powmove3entry=Label(tracking, text=moves[trackertemp["4"]["move3"]]["power"])
    powmove3entry.grid(row=9,column=3)
    powmove4entry=Label(tracking, text=moves[trackertemp["4"]["move4"]]["power"])
    powmove4entry.grid(row=10,column=3)
    accmovelabel=Label(tracking, text = "Acc")
    accmovelabel.grid(row=6, column=4)
    accmove1entry=Label(tracking, text=moves[trackertemp["4"]["move1"]]["acc"])
    accmove1entry.grid(row=7,column=4)
    accmove2entry=Label(tracking, text=moves[trackertemp["4"]["move2"]]["acc"])
    accmove2entry.grid(row=8,column=4)
    accmove3entry=Label(tracking, text=moves[trackertemp["4"]["move3"]]["acc"])
    accmove3entry.grid(row=9,column=4)
    accmove4entry=Label(tracking, text=moves[trackertemp["4"]["move4"]]["acc"])
    accmove4entry.grid(row=10,column=4)
    typmovelabel=Label(tracking, text = "Type")
    typmovelabel.grid(row=6, column=5)
    typmove1entry=Label(tracking, text=moves[trackertemp["4"]["move1"]]["type"])
    typmove1entry.grid(row=7,column=5)
    typmove2entry=Label(tracking, text=moves[trackertemp["4"]["move2"]]["type"])
    typmove2entry.grid(row=8,column=5)
    typmove3entry=Label(tracking, text=moves[trackertemp["4"]["move3"]]["type"])
    typmove3entry.grid(row=9,column=5)
    typmove4entry=Label(tracking, text=moves[trackertemp["4"]["move4"]]["type"])
    typmove4entry.grid(row=10,column=5)
    typmovelabel=Button(tracking, text = "Contact", command=moveinfo)
    typmovelabel.grid(row=6, column=6)
    typmove1entry=Label(tracking, text=moves[trackertemp["4"]["move1"]]["detail"][0:2]+", "+moves[trackertemp["4"]["move1"]]["contact"])
    typmove1entry.grid(row=7,column=6)
    typmove2entry=Label(tracking, text=moves[trackertemp["4"]["move2"]]["detail"][0:2]+", "+moves[trackertemp["4"]["move2"]]["contact"])
    typmove2entry.grid(row=8,column=6)
    typmove3entry=Label(tracking, text=moves[trackertemp["4"]["move3"]]["detail"][0:2]+", "+moves[trackertemp["4"]["move3"]]["contact"])
    typmove3entry.grid(row=9,column=6)
    typmove4entry=Label(tracking, text=moves[trackertemp["4"]["move4"]]["detail"][0:2]+", "+moves[trackertemp["4"]["move4"]]["contact"])
    typmove4entry.grid(row=10,column=6)
    #display
    levllabel=Label(tracking, text = "Lv. "+trackertemp["4"]["level"]+" ("+mons[trackertemp["4"]["mon"]]["evo"]+")")
    levllabel.grid(row=2, column=3)
    def jsonsave():
        mon1=trackertemp["4"]["mon"]
        abilcont=trackertemp["4"]["ability"]
        if searchdict(abilities, abilcont)!=None:
            mons[mon1]["ability"].append(abilcont)
        movecont=[move1entry.get(),move2entry.get(),move3entry.get(),move4entry.get(),]
        levlcont=trackertemp["4"]["level"]
        for move in movecont:
            if searchdict(moves, move)!=None:
                mons[mon1]["moves"].append(move+", "+levlcont)
        mons[mon1]["lastseenat"]=levlcont
    #save
    jsonsaver=Button(tracking, text = "S", command=jsonsave)
    jsonsaver.grid(row=2, column=1)
def Mon5_Tracker(tracking):
    frameclearer()
    trackertempfile=open(r"trackertemp.json","r+")
    trackertemp=json.load(trackertempfile)
    tracking.geometry("360x240")
    tracking.title("Tracker")
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    abillabel=Button(tracking, text = "<-",command=pagechangerleft)
    abillabel.grid(row=1, column=1)
    monlabel=Button(tracking, text=trackertemp["5"]["mon"],command=lambda:Mon1_Data(trackertemp["5"]["mon"]))
    monlabel.grid(row=1, column=3)
    mon_moveset=(moveset[str(int(mons[trackertemp["5"]["mon"]]["id"]))])
    for item in mon_moveset:
        if int(item)>int(trackertemp["5"]["level"]):
            nextmove=item
            break
        nextmove="-"
    changepage=Button(tracking, text = "->",command=pagechanger)
    changepage.grid(row=1, column=2)
    abillabel=Button(tracking, text=trackertemp["5"]["ability"],command=lambda: Ability_Data(trackertemp["5"]["ability"]))
    abillabel.grid(row=4, column=3)
    itemlabel=Label(tracking, text=items[str(trackertemp["5"]["item"]).zfill(3)]["name"])
    itemlabel.grid(row=3, column=3)
    strinlabel=Label(tracking, text=str(trackertemp["5"]["currhp"])+"/"+str(trackertemp["5"]["maxhp"]))
    strinlabel.grid(row=5, column=3)
    for item in range(0,len(mons[trackertemp["5"]["mon"]]["types"])):
        types2=Label(tracking, text =mons[trackertemp["5"]["mon"]]["types"][item])
        types2.grid(row=3+item,column=1)
    hplabel=Label(tracking, text = "HP")
    hplabel.grid(row=1, column=9)
    hpentry=Label(tracking, text =trackertemp["5"]["maxhp"])
    hpentry.grid(row=1,column=10)
    naturecalcm("5")
    naturecalcp("5")
    atklabel=Label(tracking, text = "ATK")
    atklabel.grid(row=2, column=9)
    atkentry=Label(tracking, text =Satk+trackertemp["5"]["atk"])
    atkentry.grid(row=2,column=10)
    deflabel=Label(tracking, text = "DEF")
    deflabel.grid(row=3, column=9)
    defentry=Label(tracking, text =Sdef+trackertemp["5"]["def"])
    defentry.grid(row=3,column=10)
    spalabel=Label(tracking, text = "SPA")
    spalabel.grid(row=4, column=9)
    spaentry=Label(tracking, text =Sspa+trackertemp["5"]["spa"])
    spaentry.grid(row=4,column=10)
    spdlabel=Label(tracking, text = "SPD")
    spdlabel.grid(row=5, column=9)
    spdentry=Label(tracking, text =Sspd+trackertemp["5"]["spd"])
    spdentry.grid(row=5,column=10)
    spelabel=Label(tracking, text = "SPE")
    spelabel.grid(row=6, column=9)
    speentry=Label(tracking, text =Sspe+trackertemp["5"]["spe"])
    speentry.grid(row=6,column=10)
    spelabel=Label(tracking, text = "BST")
    spelabel.grid(row=7, column=9)
    bstlabel=Label(tracking, text=mons[trackertemp["5"]["mon"]]["bst"])
    bstlabel.grid(row=7,column=10)
    movelabel=Label(tracking, text = "Moves ["+nextmove+"]")
    movelabel.grid(row=6, column=1)
    move1entry=Label(tracking, text=trackertemp["5"]["move1"])
    move1entry.grid(row=7,column=1)
    move2entry=Label(tracking, text=trackertemp["5"]["move2"])
    move2entry.grid(row=8,column=1)
    move3entry=Label(tracking, text=trackertemp["5"]["move3"])
    move3entry.grid(row=9,column=1)
    move4entry=Label(tracking, text=trackertemp["5"]["move4"])
    move4entry.grid(row=10,column=1)
    ppmovelabel=Label(tracking, text = "PP")
    ppmovelabel.grid(row=6, column=2)
    ppmove1entry=Label(tracking, text=moves[trackertemp["5"]["move1"]]["pp"])
    ppmove1entry.grid(row=7,column=2)
    ppmove2entry=Label(tracking, text=moves[trackertemp["5"]["move2"]]["pp"])
    ppmove2entry.grid(row=8,column=2)
    ppmove3entry=Label(tracking, text=moves[trackertemp["5"]["move3"]]["pp"])
    ppmove3entry.grid(row=9,column=2)
    ppmove4entry=Label(tracking, text=moves[trackertemp["5"]["move4"]]["pp"])
    ppmove4entry.grid(row=10,column=2)
    powmovelabel=Label(tracking, text = "Pow")
    powmovelabel.grid(row=6, column=3)
    powmove1entry=Label(tracking, text=moves[trackertemp["5"]["move1"]]["power"])
    powmove1entry.grid(row=7,column=3)
    powmove2entry=Label(tracking, text=moves[trackertemp["5"]["move2"]]["power"])
    powmove2entry.grid(row=8,column=3)
    powmove3entry=Label(tracking, text=moves[trackertemp["5"]["move3"]]["power"])
    powmove3entry.grid(row=9,column=3)
    powmove4entry=Label(tracking, text=moves[trackertemp["5"]["move4"]]["power"])
    powmove4entry.grid(row=10,column=3)
    accmovelabel=Label(tracking, text = "Acc")
    accmovelabel.grid(row=6, column=4)
    accmove1entry=Label(tracking, text=moves[trackertemp["5"]["move1"]]["acc"])
    accmove1entry.grid(row=7,column=4)
    accmove2entry=Label(tracking, text=moves[trackertemp["5"]["move2"]]["acc"])
    accmove2entry.grid(row=8,column=4)
    accmove3entry=Label(tracking, text=moves[trackertemp["5"]["move3"]]["acc"])
    accmove3entry.grid(row=9,column=4)
    accmove4entry=Label(tracking, text=moves[trackertemp["5"]["move4"]]["acc"])
    accmove4entry.grid(row=10,column=4)
    typmovelabel=Label(tracking, text = "Type")
    typmovelabel.grid(row=6, column=5)
    typmove1entry=Label(tracking, text=moves[trackertemp["5"]["move1"]]["type"])
    typmove1entry.grid(row=7,column=5)
    typmove2entry=Label(tracking, text=moves[trackertemp["5"]["move2"]]["type"])
    typmove2entry.grid(row=8,column=5)
    typmove3entry=Label(tracking, text=moves[trackertemp["5"]["move3"]]["type"])
    typmove3entry.grid(row=9,column=5)
    typmove4entry=Label(tracking, text=moves[trackertemp["5"]["move4"]]["type"])
    typmove4entry.grid(row=10,column=5)
    typmovelabel=Button(tracking, text = "Contact", command=moveinfo)
    typmovelabel.grid(row=6, column=6)
    typmove1entry=Label(tracking, text=moves[trackertemp["5"]["move1"]]["detail"][0:2]+", "+moves[trackertemp["5"]["move1"]]["contact"])
    typmove1entry.grid(row=7,column=6)
    typmove2entry=Label(tracking, text=moves[trackertemp["5"]["move2"]]["detail"][0:2]+", "+moves[trackertemp["5"]["move2"]]["contact"])
    typmove2entry.grid(row=8,column=6)
    typmove3entry=Label(tracking, text=moves[trackertemp["5"]["move3"]]["detail"][0:2]+", "+moves[trackertemp["5"]["move3"]]["contact"])
    typmove3entry.grid(row=9,column=6)
    typmove4entry=Label(tracking, text=moves[trackertemp["5"]["move4"]]["detail"][0:2]+", "+moves[trackertemp["5"]["move4"]]["contact"])
    typmove4entry.grid(row=10,column=6)
    #display
    levllabel=Label(tracking, text = "Lv. "+trackertemp["5"]["level"]+" ("+mons[trackertemp["5"]["mon"]]["evo"]+")")
    levllabel.grid(row=2, column=3)
    def jsonsave():
        mon1=trackertemp["5"]["mon"]
        abilcont=trackertemp["5"]["ability"]
        if searchdict(abilities, abilcont)!=None:
            mons[mon1]["ability"].append(abilcont)
        movecont=[move1entry.get(),move2entry.get(),move3entry.get(),move4entry.get(),]
        levlcont=trackertemp["5"]["level"]
        for move in movecont:
            if searchdict(moves, move)!=None:
                mons[mon1]["moves"].append(move+", "+levlcont)
        mons[mon1]["lastseenat"]=levlcont
    #save
    jsonsaver=Button(tracking, text = "S", command=jsonsave)
    jsonsaver.grid(row=2, column=1)
def Mon6_Tracker(tracking):
    frameclearer()
    trackertempfile=open(r"trackertemp.json","r+")
    trackertemp=json.load(trackertempfile)
    tracking.geometry("360x240")
    tracking.title("Tracker")
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    abillabel=Button(tracking, text = "<-",command=pagechangerleft)
    abillabel.grid(row=1, column=1)
    monlabel=Button(tracking, text=trackertemp["6"]["mon"],command=lambda:Mon1_Data(trackertemp["6"]["mon"]))
    monlabel.grid(row=1, column=3)
    mon_moveset=(moveset[str(int(mons[trackertemp["6"]["mon"]]["id"]))])
    for item in mon_moveset:
        if int(item)>int(trackertemp["6"]["level"]):
            nextmove=item
            break
        nextmove="-"
    changepage=Button(tracking, text = "->",command=pagechanger)
    changepage.grid(row=1, column=2)
    abillabel=Button(tracking, text=trackertemp["6"]["ability"],command=lambda: Ability_Data(trackertemp["6"]["ability"]))
    abillabel.grid(row=4, column=3)
    itemlabel=Label(tracking, text=items[str(trackertemp["6"]["item"]).zfill(3)]["name"])
    itemlabel.grid(row=3, column=3)
    strinlabel=Label(tracking, text=str(trackertemp["6"]["currhp"])+"/"+str(trackertemp["6"]["maxhp"]))
    strinlabel.grid(row=5, column=3)
    for item in range(0,len(mons[trackertemp["6"]["mon"]]["types"])):
        types2=Label(tracking, text =mons[trackertemp["6"]["mon"]]["types"][item])
        types2.grid(row=3+item,column=1)
    hplabel=Label(tracking, text = "HP")
    hplabel.grid(row=1, column=9)
    hpentry=Label(tracking, text =trackertemp["6"]["maxhp"])
    hpentry.grid(row=1,column=10)
    naturecalcm("6")
    naturecalcp("6")
    atklabel=Label(tracking, text = "ATK")
    atklabel.grid(row=2, column=9)
    atkentry=Label(tracking, text =Satk+trackertemp["6"]["atk"])
    atkentry.grid(row=2,column=10)
    deflabel=Label(tracking, text = "DEF")
    deflabel.grid(row=3, column=9)
    defentry=Label(tracking, text =Sdef+trackertemp["6"]["def"])
    defentry.grid(row=3,column=10)
    spalabel=Label(tracking, text = "SPA")
    spalabel.grid(row=4, column=9)
    spaentry=Label(tracking, text =Sspa+trackertemp["6"]["spa"])
    spaentry.grid(row=4,column=10)
    spdlabel=Label(tracking, text = "SPD")
    spdlabel.grid(row=5, column=9)
    spdentry=Label(tracking, text =Sspd+trackertemp["6"]["spd"])
    spdentry.grid(row=5,column=10)
    spelabel=Label(tracking, text = "SPE")
    spelabel.grid(row=6, column=9)
    speentry=Label(tracking, text =Sspe+trackertemp["6"]["spe"])
    speentry.grid(row=6,column=10)
    spelabel=Label(tracking, text = "BST")
    spelabel.grid(row=7, column=9)
    bstlabel=Label(tracking, text=mons[trackertemp["6"]["mon"]]["bst"])
    bstlabel.grid(row=7,column=10)
    movelabel=Label(tracking, text = "Moves ["+nextmove+"]")
    movelabel.grid(row=6, column=1)
    move1entry=Label(tracking, text=trackertemp["6"]["move1"])
    move1entry.grid(row=7,column=1)
    move2entry=Label(tracking, text=trackertemp["6"]["move2"])
    move2entry.grid(row=8,column=1)
    move3entry=Label(tracking, text=trackertemp["6"]["move3"])
    move3entry.grid(row=9,column=1)
    move4entry=Label(tracking, text=trackertemp["6"]["move4"])
    move4entry.grid(row=10,column=1)
    ppmovelabel=Label(tracking, text = "PP")
    ppmovelabel.grid(row=6, column=2)
    ppmove1entry=Label(tracking, text=moves[trackertemp["6"]["move1"]]["pp"])
    ppmove1entry.grid(row=7,column=2)
    ppmove2entry=Label(tracking, text=moves[trackertemp["6"]["move2"]]["pp"])
    ppmove2entry.grid(row=8,column=2)
    ppmove3entry=Label(tracking, text=moves[trackertemp["6"]["move3"]]["pp"])
    ppmove3entry.grid(row=9,column=2)
    ppmove4entry=Label(tracking, text=moves[trackertemp["6"]["move4"]]["pp"])
    ppmove4entry.grid(row=10,column=2)
    powmovelabel=Label(tracking, text = "Pow")
    powmovelabel.grid(row=6, column=3)
    powmove1entry=Label(tracking, text=moves[trackertemp["6"]["move1"]]["power"])
    powmove1entry.grid(row=7,column=3)
    powmove2entry=Label(tracking, text=moves[trackertemp["6"]["move2"]]["power"])
    powmove2entry.grid(row=8,column=3)
    powmove3entry=Label(tracking, text=moves[trackertemp["6"]["move3"]]["power"])
    powmove3entry.grid(row=9,column=3)
    powmove4entry=Label(tracking, text=moves[trackertemp["6"]["move4"]]["power"])
    powmove4entry.grid(row=10,column=3)
    accmovelabel=Label(tracking, text = "Acc")
    accmovelabel.grid(row=6, column=4)
    accmove1entry=Label(tracking, text=moves[trackertemp["6"]["move1"]]["acc"])
    accmove1entry.grid(row=7,column=4)
    accmove2entry=Label(tracking, text=moves[trackertemp["6"]["move2"]]["acc"])
    accmove2entry.grid(row=8,column=4)
    accmove3entry=Label(tracking, text=moves[trackertemp["6"]["move3"]]["acc"])
    accmove3entry.grid(row=9,column=4)
    accmove4entry=Label(tracking, text=moves[trackertemp["6"]["move4"]]["acc"])
    accmove4entry.grid(row=10,column=4)
    typmovelabel=Label(tracking, text = "Type")
    typmovelabel.grid(row=6, column=5)
    typmove1entry=Label(tracking, text=moves[trackertemp["6"]["move1"]]["type"])
    typmove1entry.grid(row=7,column=5)
    typmove2entry=Label(tracking, text=moves[trackertemp["6"]["move2"]]["type"])
    typmove2entry.grid(row=8,column=5)
    typmove3entry=Label(tracking, text=moves[trackertemp["6"]["move3"]]["type"])
    typmove3entry.grid(row=9,column=5)
    typmove4entry=Label(tracking, text=moves[trackertemp["6"]["move4"]]["type"])
    typmove4entry.grid(row=10,column=5)
    typmovelabel=Button(tracking, text = "Contact", command=moveinfo)
    typmovelabel.grid(row=6, column=6)
    typmove1entry=Label(tracking, text=moves[trackertemp["6"]["move1"]]["detail"][0:2]+", "+moves[trackertemp["6"]["move1"]]["contact"])
    typmove1entry.grid(row=7,column=6)
    typmove2entry=Label(tracking, text=moves[trackertemp["6"]["move2"]]["detail"][0:2]+", "+moves[trackertemp["6"]["move2"]]["contact"])
    typmove2entry.grid(row=8,column=6)
    typmove3entry=Label(tracking, text=moves[trackertemp["6"]["move3"]]["detail"][0:2]+", "+moves[trackertemp["6"]["move3"]]["contact"])
    typmove3entry.grid(row=9,column=6)
    typmove4entry=Label(tracking, text=moves[trackertemp["6"]["move4"]]["detail"][0:2]+", "+moves[trackertemp["6"]["move4"]]["contact"])
    typmove4entry.grid(row=10,column=6)
    #display
    levllabel=Label(tracking, text = "Lv. "+trackertemp["6"]["level"]+" ("+mons[trackertemp["6"]["mon"]]["evo"]+")")
    levllabel.grid(row=2, column=3)
    def jsonsave():
        mon1=trackertemp["6"]["mon"]
        abilcont=trackertemp["6"]["ability"]
        if searchdict(abilities, abilcont)!=None:
            mons[mon1]["ability"].append(abilcont)
        movecont=[move1entry.get(),move2entry.get(),move3entry.get(),move4entry.get(),]
        levlcont=trackertemp["6"]["level"]
        for move in movecont:
            if searchdict(moves, move)!=None:
                mons[mon1]["moves"].append(move+", "+levlcont)
        mons[mon1]["lastseenat"]=levlcont
    #save
    jsonsaver=Button(tracking, text = "S", command=jsonsave)
    jsonsaver.grid(row=2, column=1)
def Mon7_Tracker(tracking):
    frameclearer()
    page=tkinter.Frame(tracking)
    page.grid()
    tracking.geometry("360x240")
    tracking.title("Tracker")
    status=["-","Burn","Poison","Sleep","Paralysis","Frozen"]
    statustext=status[0]
    def statuschange():
        statustext=status[status.index(statustext)+1]
    statusbutton=Button(tracking,text=statustext,command=statuschange)
    statusbutton.grid(row=8,column=12)
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    opponen=Entry(tracking, width=14)
    opponen.grid(row=7,column=12)
    monentry=Entry(tracking, width=14)
    monentry.grid(row=1,column=12)
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
            Mon1_Data(monentry.get())
    monlabel=Button(tracking, text="Opponent",command=playermondata)
    monlabel.grid(row=1, column=3)
    changepage=Button(tracking, text = "->",command=pagechanger)
    changepage.grid(row=1, column=2)
    def open_abildata():
        if abilentry.get()!="":
            Ability_Data(abilentry.get())
    abillabel=Button(tracking, text = "Abilities",command=open_abildata)
    abillabel.grid(row=4, column=3)
    abilentry=Entry(tracking, width=14)
    abilentry.grid(row=4,column=12)
    itemlabel=Label(tracking, text = "Held Item")
    itemlabel.grid(row=3, column=3)
    itementry=Entry(tracking, width=14)
    itementry.grid(row=3,column=12)
    strinlabel=Label(tracking, text = "String")
    strinlabel.grid(row=5, column=3)
    strinentry=Entry(tracking, width=14)
    strinentry.grid(row=5,column=12)
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
    move1entry=Entry(tracking, width=18)
    move1entry.grid(row=2,column=8)
    move2entry=Entry(tracking, width=18)
    move2entry.grid(row=4,column=8)
    move3entry=Entry(tracking, width=18)
    move3entry.grid(row=6,column=8)
    move4entry=Entry(tracking, width=18)
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
def Mon8_Tracker(tracking):
    frameclearer()
    page=tkinter.Frame(tracking)
    page.grid()
    tracking.geometry("360x240")
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
            Mon1_Data(monentry.get())
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
    move1entry=Entry(tracking, width=18)
    move1entry.grid(row=2,column=8)
    move2entry=Entry(tracking, width=18)
    move2entry.grid(row=4,column=8)
    move3entry=Entry(tracking, width=18)
    move3entry.grid(row=6,column=8)
    move4entry=Entry(tracking, width=18)
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
def Mon9_Tracker(tracking):
    frameclearer()
    page=tkinter.Frame(tracking)
    page.grid()
    tracking.geometry("360x240")
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
            Mon1_Data(monentry.get())
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
    move1entry=Entry(tracking, width=18)
    move1entry.grid(row=2,column=8)
    move2entry=Entry(tracking, width=18)
    move2entry.grid(row=4,column=8)
    move3entry=Entry(tracking, width=18)
    move3entry.grid(row=6,column=8)
    move4entry=Entry(tracking, width=18)
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
def Mon10_Tracker(tracking):
    frameclearer()
    page=tkinter.Frame(tracking)
    page.grid()
    tracking.geometry("360x240")
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
            Mon1_Data(monentry.get())
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
    move1entry=Entry(tracking, width=18)
    move1entry.grid(row=2,column=8)
    move2entry=Entry(tracking, width=18)
    move2entry.grid(row=4,column=8)
    move3entry=Entry(tracking, width=18)
    move3entry.grid(row=6,column=8)
    move4entry=Entry(tracking, width=18)
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
def Mon11_Tracker(tracking):
    frameclearer()
    page=tkinter.Frame(tracking)
    page.grid()
    tracking.geometry("360x240")
    tracking.title("Tracker")
    status=["-","Burn","Poison","Sleep","Paralysis","Frozen"]
    statustext=status[0]
    def statuschange():
        statustext=status[status.index(statustext)+1]
    statusbutton=Button(tracking,text=statustext,command=statuschange)
    statusbutton.grid(row=8,column=12)
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    opponen=Entry(tracking, width=14)
    opponen.grid(row=7,column=12)
    monentry=Entry(tracking, width=14)
    monentry.grid(row=1,column=12)
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
            Mon1_Data(monentry.get())
    monlabel=Button(tracking, text="Opponent",command=playermondata)
    monlabel.grid(row=1, column=3)
    changepage=Button(tracking, text = "->",command=pagechanger)
    changepage.grid(row=1, column=2)
    def open_abildata():
        if abilentry.get()!="":
            Ability_Data(abilentry.get())
    abillabel=Button(tracking, text = "Abilities",command=open_abildata)
    abillabel.grid(row=4, column=3)
    abilentry=Entry(tracking, width=14)
    abilentry.grid(row=4,column=12)
    itemlabel=Label(tracking, text = "Held Item")
    itemlabel.grid(row=3, column=3)
    itementry=Entry(tracking, width=14)
    itementry.grid(row=3,column=12)
    strinlabel=Label(tracking, text = "String")
    strinlabel.grid(row=5, column=3)
    strinentry=Entry(tracking, width=14)
    strinentry.grid(row=5,column=12)
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
    move1entry=Entry(tracking, width=18)
    move1entry.grid(row=2,column=8)
    move2entry=Entry(tracking, width=18)
    move2entry.grid(row=4,column=8)
    move3entry=Entry(tracking, width=18)
    move3entry.grid(row=6,column=8)
    move4entry=Entry(tracking, width=18)
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
def Mon12_Tracker(tracking):
    frameclearer()
    page=tkinter.Frame(tracking)
    page.grid()
    tracking.geometry("360x240")
    tracking.title("Tracker")
    status=["-","Burn","Poison","Sleep","Paralysis","Frozen"]
    statustext=status[0]
    def statuschange():
        statustext=status[status.index(statustext)+1]
    statusbutton=Button(tracking,text=statustext,command=statuschange)
    statusbutton.grid(row=8,column=12)
    def searchdict(dict, text):
        for item in dict:
            if item==text:
                return item
    opponen=Entry(tracking, width=14)
    opponen.grid(row=7,column=12)
    monentry=Entry(tracking, width=14)
    monentry.grid(row=1,column=12)
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
            Mon1_Data(monentry.get())
    monlabel=Button(tracking, text="Opponent",command=playermondata)
    monlabel.grid(row=1, column=3)
    changepage=Button(tracking, text = "->",command=pagechanger)
    changepage.grid(row=1, column=2)
    def open_abildata():
        if abilentry.get()!="":
            Ability_Data(abilentry.get())
    abillabel=Button(tracking, text = "Abilities",command=open_abildata)
    abillabel.grid(row=4, column=3)
    abilentry=Entry(tracking, width=14)
    abilentry.grid(row=4,column=12)
    itemlabel=Label(tracking, text = "Held Item")
    itemlabel.grid(row=3, column=3)
    itementry=Entry(tracking, width=14)
    itementry.grid(row=3,column=12)
    strinlabel=Label(tracking, text = "String")
    strinlabel.grid(row=5, column=3)
    strinentry=Entry(tracking, width=14)
    strinentry.grid(row=5,column=12)
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
    move1entry=Entry(tracking, width=18)
    move1entry.grid(row=2,column=8)
    move2entry=Entry(tracking, width=18)
    move2entry.grid(row=4,column=8)
    move3entry=Entry(tracking, width=18)
    move3entry.grid(row=6,column=8)
    move4entry=Entry(tracking, width=18)
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