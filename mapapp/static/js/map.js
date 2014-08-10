$(document).ready(function(){

	var MM_proj = new OpenLayers.Projection('EPSG:4326');
	var OpL_proj = new OpenLayers.Projection('EPSG:900913');

	var places = {
		'london':    new OpenLayers.LonLat(-0.12769, 51.50733)
			.transform(MM_proj, OpL_proj),
		'paris':     new OpenLayers.LonLat(2.3508, 48.8567)
			.transform(MM_proj, OpL_proj),
		'stockholm': new OpenLayers.LonLat(18.068611, 59.329444)
			.transform(MM_proj, OpL_proj)
	};

	function updateMeasuredCoordinates() {
		mapcentre = map.getCenter()
			.transform(map.getProjection(), MM_proj);
		mapcentre = mapcentre.lat + ',' + mapcentre.lon;
		mapzoom = map.getZoom().toString();
	}

	var labels = $('form>ul>li>ul label');

	function changeLabelsOpacity(opacity_level) {
		for (var i = labels.length - 1; i >= 0; i--) {
			labels[i].style.opacity = opacity_level;
		};
	}

	// define custom map event listeners
	function mapPanStarts (event) {
		changeLabelsOpacity(0.3);
	}
	function mapPanEnds (event) {
		changeLabelsOpacity(1);
		updateMeasuredCoordinates();
	}
	function mapZoomEnds (event) {
		updateMeasuredCoordinates();
	}

	// initialise map
	var map = new OpenLayers.Map('map', {
		eventListeners: {
			'movestart': mapPanStarts,
			'moveend': mapPanEnds,
			'zoomend': mapZoomEnds,
		},
	});

	var layer = new OpenLayers.Layer.Stamen('toner-background');
	map.addLayer(layer);

	changeCentre('london', 1);


	function changeCentre(area_name, zoom) {
		if(typeof(zoom) === 'undefined') zoom = 11;
		map.setCenter(places[area_name.toLowerCase()], zoom);
	};

	$('form li.where input[type="radio"]').click( function(event) {
		changeCentre(this.id);
	});


	document.getElementById('get_coor').addEventListener('click', function(event) {
		alert(mapcentre);
	});


	function mySubmit() {
		document.getElementById('mapcentreField').value = mapcentre;
		document.getElementById('mapzoomField').value = mapzoom;
		document.getElementById('myForm').submit();
	};

	document.getElementById('generate-map').addEventListener('click', function(event) {
		mySubmit();
	});


});