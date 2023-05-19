<script lang="ts">
	import { Navbar, NavBrand, DarkMode, Card } from 'flowbite-svelte';
	import { onMount } from 'svelte';
	import { Footer, FooterBrand, FooterCopyright, FooterIcon, FooterLink, FooterLinkGroup } from 'flowbite-svelte';

	// Initialize variables
	var fireIncidents = [];
	var numFireIncidents = 0;
	var totalFireArea = 0;
	var formattedFireArea = 0;
	var fetchDate = '';
	let map;

	onMount(async () => {
		const L = await import('leaflet');

		// API request
		const response = await fetch('https://texas-fire-map-67ugd5bjtq-uc.a.run.app', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' }
		});

		// Large fire data
		const res = await response.json();
		fireIncidents = res['fire_incidents'];
		numFireIncidents = res['num_fire_incidents'];
		totalFireArea = res['total_fire_area'];
		formattedFireArea = res['formatted_fire_area'];
		fetchDate = res['fetch_date'];

		map = L.map('mapid', { attributionControl: false }).setView([31.2813, -98.794], 5);
		L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
			maxZoom: 18,
			id: 'mapbox/streets-v11',
			tileSize: 512,
			zoomOffset: -1,
			accessToken: 'pk.eyJ1Ijoia292ZXJob2x0IiwiYSI6ImNqMWNoemRyNDAwMWUycW1odXJkZndjNGkifQ.tfPnZpI90DtlwLpRck3mpA'
		}).addTo(map);

		var flameIcon = L.icon({
			iconUrl: 'static/flame.png',
			iconSize: [40, 40],
			iconAnchor: [20, 20],
			popupAnchor: [0, -20]
		});

		if (numFireIncidents == 0) {
			// Don't generate map markers if there are no fire incidents
		} else {
			for (var i = 0; i < fireIncidents.length; i++) {
				var marker = L.marker([fireIncidents[i]['latitude'], fireIncidents[i]['longitude']], { icon: flameIcon }).addTo(
					map
				);
				marker.bindTooltip(
					fireIncidents[i]['fire_name'] +
						'<br>' +
						fireIncidents[i]['area'] +
						' acres burned<br>' +
						fireIncidents[i]['report_date']
				);
			}
		}
	});
</script>

<Navbar color="primary" navClass="px-2 sm:px-4 py-4 w-full">
	<NavBrand href="#">
		<span class="self-center whitespace-nowrap pl-4 text-3xl font-semibold lg:pl-0 lg:text-3xl">
			Is Texas On Fire?
		</span>
	</NavBrand>
</Navbar>

<main>
	<div class="p-5">
		{#if numFireIncidents == 0}
			<h5 class="mb-2 text-xl font-bold text-gray-900 dark:text-gray-900">
				No, there are no large wildland fires in Texas as of {fetchDate}
			</h5>
		{:else if numFireIncidents == 1}
			<h5 class="mb-2 text-xl font-bold text-gray-900 dark:text-gray-900">
				Yes, there is {numFireIncidents} large wildland fire in Texas
			</h5>
		{:else}
			<h5 class="mb-2 text-xl font-bold text-gray-900 dark:text-gray-900">
				Yes, there are {numFireIncidents} large wildland fires in Texas
			</h5>
		{/if}
		{#if numFireIncidents > 0}
			<h3 class="mb-2 text-xl text-gray-900 dark:text-gray-900">
				{formattedFireArea} acres are burning as of {fetchDate}
			</h3>
		{/if}
	</div>

	<div id="mapid" />

	<div class="p-5">
		<h5 class="text-base text-gray-900 dark:text-gray-900">
			This app uses the most recent <a href="http://fsapps.nwcg.gov/afm/" class="underline"
				>large fire incident data set</a
			>
			from the USDA Forest Service.<br />
			The USDA large fire incident data set is currently updated every Friday or as fire conditions warrant.
		</h5>
	</div>

	<div class="p-5">
		<h5 class="text-sm text-gray-900 dark:text-gray-900">
			istexasonfire.com is maintained by <a href="https://koverholt.com/" class="underline">Kristopher Overholt</a>
			<br />
			View the <a href="https://github.com/koverholt/texas-fire-map" class="underline">source code on GitHub</a>
		</h5>
	</div>
</main>
