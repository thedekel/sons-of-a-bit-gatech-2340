# Crjeate your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from mordor.models import Party, Character
from mordor.functions import * 

"""
@author: Alex Williams, Anthony Taormina, Daniel Whatley, Stephen Roca, Yuval Dekel
"""

def start(request):
    return render_to_response("mordor/start.html", {},context_instance=RequestContext(request))
    

def wag(request):
	return render_to_response("mordor/wag.html", {"dt":87, "fpd":5, "dpd":4, "fr":98})#,context_instance=RequestContext(request))
    
def shop(request):
	ss = storeMaker("initial Store", 1000, [])
	items = ss.item_set.all()
	return render_to_response("mordor/shoptest.html", {"shopname":"The first Shop", "items":items})#,context_instance=RequestContext(request))

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
    #create player
    pp = Character(name=request.POST['player'], profession=request.POST['prof'], status = 1, health = 1, isLeader = True, party = partyz)
    pp.save()
    #create members
    for q in ['m1','m2','m3']:
        if request.POST[q]:
            m= Character(name=request.POST[q], profession = "", status = 1, health = 1, isLeader = False, party = partyz)
            m.save()
    return HttpResponse("data received. visit <a href='../config.php'>config.php</a> to see your party.")

def config(request):
    return render_to_response("mordor/config.html", {'parties':Party.objects.all(), "membs":map(lambda a: a.character_set.all()[0].name[0], Party.objects.all())},context_instance=RequestContext(request))

#def store(request):
    #store = Store(store_id=request.POST["id"], name=request.POST["s_name"], )
#    return render_to_response("mordor/store.html", {"Store": })
