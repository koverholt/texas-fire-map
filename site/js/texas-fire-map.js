var xhr = new XMLHttpRequest();
xhr.open("GET", "https://us-central1-koverholt-apps-304316.cloudfunctions.net/texas-fire-map");
xhr.setRequestHeader("Content-Type", "application/json");
xhr.send();

xhr.onload = function () {
  var obj = JSON.parse(this.response);
  var fire_incidents = JSON.parse(obj["fire_incidents"]);
  var num_fire_incidents = obj["num_fire_incidents"];
  var total_fire_area = obj["total_fire_area"];
  var formatted_fire_area = obj["formatted_fire_area"];
  var fetch_date = obj["fetch_date"];

  var map = L.map('mapid', {attributionControl: false}).setView([31.2813, -98.7940], 5);
  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      maxZoom: 18,
      id: 'mapbox/streets-v11',
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'pk.eyJ1Ijoia292ZXJob2x0IiwiYSI6ImNqMWNoemRyNDAwMWUycW1odXJkZndjNGkifQ.tfPnZpI90DtlwLpRck3mpA'
  }).addTo(map);

  var flameIcon = L.icon({
      iconUrl: 'flame.png',
      iconSize:     [40, 40],
      iconAnchor:   [20, 20],
      popupAnchor:  [0, -20],
  });

  for (var i=0; i<fire_incidents.length; i++) {
    var marker = L.marker([fire_incidents[i]["latitude"], fire_incidents[i]["longitude"]], {icon: flameIcon}).addTo(map);
    marker.bindTooltip(fire_incidents[i]["fire_name"] + "<br>" + fire_incidents[i]["area"] + " acres burned<br>" + fire_incidents[i]["report_date"])
  }

  var app = new Vue({
    el: '#app',
    data: {
      num_fire_incidents: num_fire_incidents,
      total_fire_area: total_fire_area,
      formatted_fire_area: formatted_fire_area,
      fetch_date: fetch_date,
    }
  })
};
