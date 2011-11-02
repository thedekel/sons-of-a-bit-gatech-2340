from django.views.decorators.csrf import csrf_exempt
# Crjeate your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from mordor.models import Party, Character
from mordor.functions import * 
from mordor.coords import *



"""
@author: Alex Williams, Anthony Taormina, Daniel Whatley, Stephen Roca, Yuval Dekel
"""
@csrf_exempt
def start(request):
    return render_to_response("mordor/styletest.html", {})
    
@csrf_exempt
def wag(request):
    play = False
    try:
        request.GET['play']
        play = True
    except:
        pass
    party = Party.objects.get(id=request.GET['p'])
    w=party.wagon_set.all()[0]
    if play:
        takeATurn(party.id)
    qq=0
    try:
        i = Wagon.objects.get(party=Party.objects.get(id=party.id))
        f = Item.objects.get(name="Food")
        qq=Iteminstance.objects.get(inventory=i.inventory,base=f).amount
    except:
        print "No"
        qq=0
    xx,yy = get_player_coords(party.location)
    xtop = (0 if xx<400 else (800 if xx>1200 else xx-400))
    ytop = (0 if yy<300 else (600 if yy>900 else yy-300))
    xx = 400 if 400<xx<1200 else (xx if xx<=400 else xx-800)
    yy = 300 if 300<yy<900 else (yy if yy<=300 else xx-900)

    return render_to_response("mordor/wag.html", {"partyid":request.GET['p'],"dt":party.location*6.25, "fpd":party.rations, "dpd":party.pace*12.5, "fr":qq,"x":xx-24, "y":yy-20, "ytop":-ytop, "xtop":-xtop})

@csrf_exempt
def shop(request):
    party = Party.objects.get(id=request.GET['p'])
    try:
        astore = Store.objects.get(location=party.location)
    except:
        astore = Store.objects.get(location=0)
    items = astore.items.all()
    try:
        w=party.wagon_set.all()[0]
        print "wagon found!", request.POST['item'], request.POST['qty'], astore.price_mult
        buyItem(request.GET['p'],request.POST['item'],int( request.POST['qty']), astore.price_mult)
        print "receiving post for: " + request.POST['qty'], request.POST['item']
    except:
        print "couldn't find wagon or item"
    return render_to_response("mordor/shoptest.html", {'partyid':request.GET['p'],"shopname":astore.name ,"items":items, "party":party, 'weight':w.weight})

@csrf_exempt
def submit(request):
    try:
        if (request.POST['pp']):
            p = Party.objects.get(name=request.POST['pp'])
            p.delete()
    except:
        pass
    
    prof = request.POST['prof']
    mmult = {'r_holder':2,'gardener':1,'tmaker':.5}
    #create a new party
    partyz = Party(name=request.POST["p_name"], money=5000*mmult[prof], pace = float(request.POST['pace']),rations = float(request.POST['ration']))
    partyz.save()
    inv = Store(name="inventory", isVendor=False, price_mult=1)
    inv.save()
    w = Wagon(party=partyz, inventory=inv, weight=0)
    w.save()


    print w
    #create player
    pp = Character(name=request.POST['player'], profession=request.POST['prof'], status = 1, health = 1, isLeader = True, party = partyz)
    pp.save()
    #create members
    for q in ['m1','m2','m3']:
        if request.POST[q]:
            m= Character(name=request.POST[q], profession = "", status = 1, health = 1, isLeader = False, party = partyz)
            m.save()
    return HttpResponse("data received. visit <a href='../config.php?p="+str(partyz.id)+"'>config.php</a> to see your party.")

@csrf_exempt
def config(request):
    p = Party.objects.get(id=request.GET['p'])

    return render_to_response("mordor/conf.html", {'testShop':True,'partyid':request.GET['p'],'part':p, "membs":p.character_set.all()})

