import { Component } from '@angular/core';
import * as L from 'leaflet';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

  title = "Texas Fire Map";
  fire_incidents:any;
  num_fire_incidents:any;
  total_fire_area:any;
  formatted_fire_area:any;
  fetch_date:any;

  constructor() {

    var xhr = new XMLHttpRequest();
    var self = this;
    xhr.open("GET", "https://us-central1-koverholt-apps-304316.cloudfunctions.net/texas-fire-map");
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send();

    xhr.onload = function () {
      var obj = JSON.parse(this.response);
      self.fire_incidents = JSON.parse(obj["fire_incidents"]);
      self.num_fire_incidents = obj["num_fire_incidents"];
      self.total_fire_area = obj["total_fire_area"];
      self.formatted_fire_area = obj["formatted_fire_area"];
      self.fetch_date = obj["fetch_date"];

      var map = L.map('mapid', {attributionControl: false}).setView([31.2813, -98.7940], 5);
      L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
          maxZoom: 18,
          id: 'mapbox/streets-v11',
          tileSize: 512,
          zoomOffset: -1,
          accessToken: 'pk.eyJ1Ijoia292ZXJob2x0IiwiYSI6ImNqMWNoemRyNDAwMWUycW1odXJkZndjNGkifQ.tfPnZpI90DtlwLpRck3mpA'
      }).addTo(map);

      var flameIcon = L.icon({
          iconUrl: 'assets/flame.png',
          iconSize:     [40, 40],
          iconAnchor:   [20, 20],
          popupAnchor:  [0, -20],
      });

      for (var i=0; i<self.fire_incidents.length; i++) {
        var marker = L.marker([self.fire_incidents[i]["latitude"], self.fire_incidents[i]["longitude"]], {icon: flameIcon}).addTo(map);
        marker.bindTooltip(self.fire_incidents[i]["fire_name"] + "<br>" + self.fire_incidents[i]["area"] + " acres burned<br>" + self.fire_incidents[i]["report_date"])
      }
    }
  }
}
