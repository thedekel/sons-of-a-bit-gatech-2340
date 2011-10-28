from django.views.decorators.csrf import csrf_exempt
# Crjeate your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from mordor.models import Party, Character
from mordor.functions import * 

"""
@author: Alex Williams, Anthony Taormina, Daniel Whatley, Stephen Roca, Yuval Dekel
"""
@csrf_exempt
def start(request):
    return render_to_response("mordor/styletest.html", {})
    
@csrf_exempt
def wag(request):
	return render_to_response("mordor/wag.html", {"partyid":request.GET['p'],"dt":87, "fpd":5, "dpd":4, "fr":98})

@csrf_exempt
def shop(request):
	try:
		Party.objects.get(id=request.POST['p']).wagon_set[0].buyItem((requst.POST["item"], request.POST['qty']))
	except:
		pass
	ss = storeMaker("initial Store", 1000, [])
	items = ss.item_set.all()
	print items
	return render_to_response("mordor/shoptest.html", {'partyid':request.GET['p'],"shopname":"The first Shop", "items":items, "party":Party.objects.get(id=request.GET['p'])})

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
    w = Wagon(party=partyz)
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
	return render_to_response("mordor/conf.html", {'partyid':request.GET['p'],'parties':Party.objects.get(id=request.GET['p']), "membs":[Party.objects.get(id=request.GET['p']).character_set.all()]})

