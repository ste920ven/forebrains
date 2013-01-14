var lat,lng;
var watcher;
var map,marker;
var markers={};


function getLocation(f)
  {
  if (navigator.geolocation)
    {
var opts= {'enableHighAccuracy':true,
'timeout':10000,
'maximumAge':0};
    navigator.geolocation.getCurrentPosition(f,function(){},opts);
  }
      else{field.innerHTML="doesn't work on this browser";}
}


function makeMap(position)
  {
   lat = position.coords.latitude;
   lng = position.coords.longitude;
   $.getJSON("/update",{name:name,x:lat,y:lng},function(){});


   var mapOptions = {
       center: new google.maps.LatLng(lat,lng),
       zoom: 14,
       mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("field"), mapOptions);
    watcher = navigator.geolocation.watchPosition(updateMarker,
updateMarker,
{'enableHighAccuracy':true,
'timeout':10000,
'maximumAge':0});
  }



function makeMarker(m) {
 
   var myLatlng = new google.maps.LatLng(m[1],m[2]);
    opts={position:myLatlng,title:m[0]}
    
    console.log(m[0]);
    console.log(name);

    if (m[0]!=name) {
opts['icon']={'url':'/static/green_MarkerA.png'};
    }
    var marker = new google.maps.Marker(opts);
    marker.setMap(map);
    return marker;
}

function updateMarker(position) {

    getLocation(function(p) {
lat = p.coords.latitude;
lng = p.coords.longitude;
$.getJSON("/update",{name:name,x:lat,y:lng},function(){});
    });

    $.getJSON("/getMarkers",function(d){
// see what markers to create
for (var i in d) {
console.log(d[i]);
console.log(markers[d[i][0]]);
if ( d[i][1]!=-1 && markers[d[i][0]] == undefined) {
var m =makeMarker(d[i]);
markers[d[i][0]]=m;
}
}

// now update the positions
for (var i in d) {
if (d[i][1]==-1 && d[i][2]==-1)
continue;
try {
markers[d[i][0]].setPosition(new google.maps.LatLng(d[i][1],d[i][2]));
}
catch (err) {}
}

});

}


function initializeMap() {
    getLocation(makeMap);
}