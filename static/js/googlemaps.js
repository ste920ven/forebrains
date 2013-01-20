var lat,lng;
var watcher;
var map,yourMarker, pursuerMarker, targetMarker;

$(document).ready(function(){
    initializeMap();
});

function initializeMap() {
    getLocation(makeMap);  
}

function getLocation(e)
{
    if (navigator.geolocation)
    {
	var opts= {'enableHighAccuracy':true,
		   'timeout':10000,
		   'maximumAge':0};
	navigator.geolocation.getCurrentPosition(f,function(){},opts);
    }
    else{field.innerHTML="Geolocation is not supported by this browser.";}
}


function makeMap(position)
{
    lat = position.coords.latitude;
    lng = position.coords.longitude;
    console.log(lat);
    console.log(lng);
    //$.getJSON("/updatelocation",{player:player, name:name,xcor:lat,ycor:lng},function(){});
    var mapOptions = {
	center: new google.maps.LatLng(lat,lng),
	zoom: 14,
	mapTypeId: google.maps.MapTypeId.ROADMAP
	};
    map = new google.maps.Map(document.getElementById("field"), mapOptions);
    watcher = navigator.geolocation.watchPosition(updateYourMarker,
						  updateYourMarker,
						  {'enableHighAccuracy':true,
						   'timeout':10000,
						   'maximumAge':0});
    var myLatlng = new google.maps.LatLng(lat,lng);
    console.log(myLatlng);
    var yourMarker = new google.maps.Marker({
	position: myLatlng,
	map: map,
	title:"YOU"
    });
}

function updateYourMarker(e){
    getLocation(function(p) {
	lat = p.coords.latitude;
	lng = p.coords.longitude;
	var yourMarker;
	yourMarker.setPosition(new google.maps.LatLng(lat, lng));
    });
}
