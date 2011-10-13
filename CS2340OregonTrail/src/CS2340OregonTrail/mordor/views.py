# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from mordor.models import Party, Character

def start(request):
    """
    This function opens up the "create a new party page"
    """
    return render_to_response("mordor/styletest.html", {},context_instance=RequestContext(request))
    

def submit(request):
    """
    Handler function for receiving sumbission from the new party screen. 
    """
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
    """
    This function will create a page that displays the currently available parties and their stats.
    """
    return render_to_response("mordor/config.html", {'parties':Party.objects.all(), "membs":map(lambda a: a.character_set.all()[0].name[0], Party.objects.all())},context_instance=RequestContext(request))