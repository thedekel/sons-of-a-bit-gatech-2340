from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from mordor.models import *
from mordor.functions import * 
from mordor.coords import *



"""
@author: Alex Williams, Anthony Taormina, Daniel Whatley, Stephen Roca, Yuval Dekel
"""
def checkmsg(ret, pid):
    print "gov"
    aparty = Party.objects.get(id=pid)
    if aparty.stopmsg!="":
        print "NOOOOOO"
        return [True, render_to_response("v/msg.html", {'msg':aparty.stopmsg, 'ret':ret, 'pid':pid})]
    print "no"
    return [False, 1]
    
@csrf_exempt
def main(request):
    return render_to_response("v/main.html")

@csrf_exempt
def start(request):
    return render_to_response("v/start.html") 

@csrf_exempt
def newparty(request):
    return render_to_response("v/newparty.html") 

def status(request):
    aparty = Party.objects.get(id=request.GET['p'])
    pace = aparty.pace
    a=checkmsg("status",aparty.id)
    if a[0]:
        aparty.stopmsg=""
        aparty.save()
        return a[1]
    rations = aparty.rations
    wag = Wagon.objects.get(party = aparty)
    inv = Inventory.objects.get(wagon = wag)
    fr = inv.foodCount()
    dd = aparty.location*6.25
    mons = aparty.money

    xx, yy = get_player_coords(aparty.location)
    xtop = (0 if xx<380 else (760 if xx>1220 else xx-380))
    ytop = (0 if yy<300 else (600 if yy>900 else yy-300))
    xx = 380 if 380<xx<1220 else (xx if xx<=380 else xx-760)
    yy = 300 if 300<yy<900 else (yy if yy<=300 else xx-900)


    return render_to_response("v/status.html", {'food_rem':fr, 'dist':dd, 'money':mons, 'pacer':pace*12.5, 'pace':pace, 'rations':rations, 'partyid':aparty.id, 'xtop':-xtop, 'ytop':-ytop, 'x':xx, 'y':yy, 'shoptest':(1 if searchStore(aparty.id) else 0) })

def visitstore(request):
    aparty = Party.objects.get(id=request.GET['p'])
    wag = Wagon.objects.get(party=aparty)
    astore = Store.objects.get(location = aparty.location)
    pid = aparty.id
    itemsset = astore.items.all()
    mult = astore.price_mult
    mon = aparty.money
    wt = wag.weight
    return render_to_response("v/store.html", {"money":mon, "weight":wt, "itemset":itemsset, "mult":mult, "partyid":pid, 'sname':astore.name }) 

def inventoryscr(request):
    aparty = Party.objects.get(id=request.GET['p'])
    wag = Wagon.objects.get(party = aparty)
    inv = Inventory.objects.get(wagon=wag)
    return render_to_response("v/inventory.html", {"money":aparty.money, "weight":wag.weight, "itemset":inv.iteminstance_set.all()})
    

def pur(request):
    pid = request.GET['p']
    iname=request.GET['iname']
    num=int(request.GET['val'])
    mult = float(request.GET['mult'])
    buyItem(pid, iname, num, mult)
    return HttpResponse("")


@csrf_exempt
def advanceTurn(request):
    pid = request.GET['p']
    takeATurn(pid)
    return HttpResponse("")


@csrf_exempt
def changerats(request):
    pid = request.GET['p']
    newp = request.GET['newp']
    newr = request.GET['newr']
    aparty = Party.objects.get(id=pid)
    aparty.pace = newp
    aparty.rations = newr
    aparty.save()
    return HttpResponse("")

@csrf_exempt
def makeParty(request):
    prof = request.GET['prof']
    mon = {u'r_holder':10000, u'gardener':5000,u'tmaker':2500}.get(prof, 5000)
    aparty = Party(name=request.GET['pname'],money=mon,pace=request.GET['pace'],rations=request.GET['rations'],location=0)
    aparty.save()
    for i in range(1,4):
        m = Character(name = request.GET['m%i'%i], party=aparty)
        m.save()
    cha = Character(name = request.GET['playername'], profession = prof, isLeader=True, party=aparty) 
    cha.save()
    wag = Wagon(party = aparty)
    wag.save()
    inv = Inventory(wagon = wag)
    inv.save()
    aparty.stopmsg = 'Party successfully created!'
    aparty.save()
    return HttpResponse(unicode(aparty.id))
