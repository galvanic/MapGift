$(document).ready(function(){

	var MM_proj = new OpenLayers.Projection('EPSG:4326');
	var OpL_proj = new OpenLayers.Projection('EPSG:900913');

	var places = {}

	$.each( $('form li.where input[type="radio"]'), function(i, radio) {
		var name = this.id;
		var coor = $(this).attr('coor');
		var coor = JSON.parse(coor.replace('(','[').replace(')',']'));
		places[name] = new OpenLayers.LonLat(coor[1], coor[0])
			.transform(MM_proj, OpL_proj);
	});

	var distance = parseInt($('div#map').css('height'))-Object.keys(places).length*23 - 3;
	$('form li.where').css('top', distance + 'px')

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