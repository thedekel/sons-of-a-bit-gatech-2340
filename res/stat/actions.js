ajaxers = []
partyid=null;
page = function(pname){
    for i in ajaxers{
        delete ajaxers.i;
    }
    ajaxers.push(new XMLHttpRequest());
    temp = ajaxers[ajaxers.length-1];
    temp.onreadystatechange = function(){
        if (temp.readystate == 4 && temp.status==200){
            document.getElementById("main").innerHTMl = temp.responseText;
        }
    }
    temp.open("GET", pname, true);
    temp.send()
}
