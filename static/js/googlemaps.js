var lat,lng;
var watcher;
var map, player, yourMarker, pursuer, target, pursuerMarker, targetMarker, game, targetLat, targetLng, pursuerLat, pursuerLng, gamestarted, allMarkers, alive,notTarget,notPurse;
var startRefresh = 1;
$(document).ready(function(){
    initializeMap();
    $.ajaxSetup({
	async: false
    });
    $.getJSON("/started",function(data){
	gamestarted = data;
    });  
    $.getJSON("/getCurrentUser", function (data) {
	player = data;
    });
    $.getJSON("/getCurrentGame", function (data) {
	game = data;
    });
    $.getJSON("/alive", function (data) {
	alive = data;
    });
    if(alive) {
	$.getJSON("/getTarget", function (data) {
	    target = data;
	});
	$.getJSON("/getPursuer", function (data) {
	    pursuer = data;
	});
    }
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
	navigator.geolocation.getCurrentPosition(e,function(){},opts);
    }
    else{field.innerHTML="Geolocation is not supported by this browser.";}
}
 var gamestarted = false;
function makeMap(position)
{
    if (alive) {
	$.getJSON("/alive", function (data) {
	    alive = data;
	    console.log(alive);
	}); 
    }
    lat = position.coords.latitude;
    lng = position.coords.longitude;
    console.log(lat);
    console.log(lng);
    $.getJSON("/updatelocation",{xcor:lat,ycor:lng},function(){});
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
    setInterval(updateYourMarker,500);
    if (gamestarted) {
    $.getJSON("/getTargetLocation", function (data) {
	targetLat = data[0];
	targetLng = data[1];
	var targetLatlng = new google.maps.LatLng(targetLat,targetLng);
	var targetMarker = new google.maps.Marker({
	    position: targetLatlng,
	    map: map,
	    icon: {"url": "/static/Tlingit-dagger-1-icon.png"},
	    title: "TARGET"
	});
    });
    };
    if (gamestarted){
    $.getJSON("/getPursuerLocation", function (data) {
	pursuerLat = data[0];
	pursuerLng = data[1];
	var pursuerLatlng = new google.maps.LatLng(pursuerLat,pursuerLng);
	var pursuerMarker = new google.maps.Marker({
	    position: pursuerLatlng,
	    map: map,
	    icon: {"url": "/static/Spy.png"},
	    title: "PURSUER",
	});
    });};
    
}


function updateYourMarker(e){
    $.getJSON("/started",function (data) {
	if (data == true && startRefresh == 1)
	startRefresh = 2;
    });
    if (alive) {
	$.getJSON("/pcheckin",function(data) {
	    if (data) {
		notPursuer = true;
		updateMarkers(68);
	    }
	}
	$.getJSON("/alive", function (data) {
	    alive = data;
	});
    }
    if (startRefresh == 2) {
	gamestarted = true;
	updateMarkers(68);
	startRefresh = 0;
    }
    if (alive) {
    getLocation(function(p) {
	lat = p.coords.latitude;
	lng = p.coords.longitude;
	try {
	    yourMarker.setPosition(new google.maps.LatLng(lat, lng));
	}
	catch (err) {}
  });
    $("checkin").click(updateMarkers);
    }
    else {
	if (gamestarted) {
	    $.getJSON("/dead",function(){});
	}
    }
}
function updateMarkers(e){
  if (gamestarted) {
      if (!notTarget) {
      $.getJSON("/getTargetLocation", function (data) {
	  targetLat = data[0];
	  targetLng = data[1];
	  targetLatlng = new google.maps.LatLng(targetLat,targetLng);
	  try {
	      targetMarker.setPosition(targetLatlng);
	  }
	  catch (err) {}
	  notTarget = false;
      });}
      if (!notPurse) {
      $.getJSON("/getPursuerLocation", function (data) {
	  pursuerLat = data[0];
	  pursuerLng = data[1];
	  pursuerLatlng = new google.maps.LatLng(pursuerLat,pursuerLng);
	  try {
	      pursuerMarker.setPosition(pursuerLatlng);
	  }
	  catch (err) {}
	  notPurse = false;
      });}
  };
}