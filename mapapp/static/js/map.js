$(document).ready(function(){


	var MM_proj = new OpenLayers.Projection('EPSG:4326');
	var OpL_proj = new OpenLayers.Projection('EPSG:900913');


	if ("geolocation" in navigator) {
		/* geolocation is available */
		navigator.geolocation.getCurrentPosition( function(position) {
			$('#current-location').click( function(event) {
				var here = new OpenLayers.LonLat(position.coords.longitude, position.coords.latitude)
			.transform(MM_proj, OpL_proj);
				map.setCenter(here, 14);
				// uncheck all the places
				uncheckAllRadios('where');
			});
		});
	} else {
		$('#current-location').hide();
	}

	var places = {}

	$('form li.where input[type=radio]').each( function(i, radio) {
		var name = this.id;
		var data = $(this).data();
		places[name] = new OpenLayers.LonLat(data.lon, data.lat)
			.transform(MM_proj, OpL_proj);
	});

	function uncheckAllRadios(className) {
		$('form li.' + className + ' input[type=radio]').each( function(i, radio) {
			this.checked = false;
		});
	}

	// Place the area list correctly in bottom left corner
	var distance = parseInt($('div#map').css('height'))-(Object.keys(places).length+1)*23 - 3;
	$('form li.where').css('top', distance + 'px')

	function updateMeasuredCoordinates() {
		mapcentre = map.getCenter()
			.transform(map.getProjection(), MM_proj);
		mapcentre = mapcentre.lat + ',' + mapcentre.lon;
		mapzoom = map.getZoom().toString();
	}

	var labels = $('form>ul>li>ul label, form li.where input[type=button]');

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

	changeCentre('london', 3);


	function changeCentre(area_name, zoom) {
		if(typeof(zoom) === 'undefined') zoom = 11;
		map.setCenter(places[area_name.toLowerCase()], zoom);
		console.log(places[area_name.toLowerCase()], zoom);
	};

	$('form li.where input[type=radio]').click( function(event) {
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