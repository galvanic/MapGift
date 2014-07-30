/*
MAPSTRACTION   v2.0.18   http://www.mapstraction.com

Copyright (c) 2012 Tom Carden, Steve Coast, Mikel Maron, Andrew Turner, Henri Bergius, Rob Moran, Derek Fowler, Gary Gale
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

 * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
 * Neither the name of the Mapstraction nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/
mxn.register("cloudmade",{Mapstraction:{init:function(a,b){var d=this;var c={key:cloudmade_key};if(typeof cloudmade_styleId!="undefined"){c.styleId=cloudmade_styleId}var e=new CM.Tiles.CloudMade.Web(c);this.maps[b]=new CM.Map(a,e);this.loaded[b]=true;CM.Event.addListener(this.maps[b],"click",function(g,f){if(f&&f.mapstraction_marker){f.mapstraction_marker.click.fire()}else{if(g){d.click.fire({location:new mxn.LatLonPoint(g.lat(),g.lng())})}}if(g){d.clickHandler(g.lat(),g.lng(),g,d)}});CM.Event.addListener(this.maps[b],"dragend",function(){d.endPan.fire()});CM.Event.addListener(this.maps[b],"zoomend",function(){d.changeZoom.fire()})},applyOptions:function(){var a=this.maps[this.api];if(this.options.enableScrollWheelZoom){a.enableScrollWheelZoom()}else{a.disableScrollWheelZoom()}},resizeTo:function(b,a){this.maps[this.api].checkResize()},addControls:function(a){var b=this.maps[this.api];var d=this.addControlsArgs;switch(d.zoom){case"large":this.addLargeControls();break;case"small":this.addSmallControls();break}if(d.map_type){this.addMapTypeControls()}if(d.scale){b.addControl(new CM.ScaleControl());this.addControlsArgs.scale=true}},addSmallControls:function(){var a=this.maps[this.api];a.addControl(new CM.SmallMapControl());this.addControlsArgs.zoom="small"},addLargeControls:function(){var a=this.maps[this.api];a.addControl(new CM.LargeMapControl());this.addControlsArgs.zoom="large"},addMapTypeControls:function(){var a=this.maps[this.api];a.addControl(new CM.TileLayerControl());this.addControlsArgs.map_type=true},dragging:function(a){var b=this.maps[this.api];if(a){b.enableDragging()}else{b.disableDragging()}},setCenterAndZoom:function(a,b){var d=this.maps[this.api];var c=a.toProprietary(this.api);d.setCenter(c,b)},addMarker:function(b,a){var d=this.maps[this.api];var c=b.toProprietary(this.api);d.addOverlay(c);return c},removeMarker:function(a){var b=this.maps[this.api];a.proprietary_marker.closeInfoWindow();b.removeOverlay(a.proprietary_marker)},declutterMarkers:function(a){var b=this.maps[this.api]},addPolyline:function(b,a){var d=this.maps[this.api];var c=b.toProprietary(this.api);d.addOverlay(c);return c},removePolyline:function(a){var b=this.maps[this.api];b.removeOverlay(a.proprietary_polyline)},getCenter:function(){var b=this.maps[this.api];var a=b.getCenter();return new mxn.LatLonPoint(a.lat(),a.lng())},setCenter:function(a,b){var d=this.maps[this.api];var c=a.toProprietary(this.api);if(b!==null&&b.pan){d.panTo(c)}else{d.setCenter(c)}},setZoom:function(a){var b=this.maps[this.api];b.setZoom(a)},getZoom:function(){var a=this.maps[this.api];return a.getZoom()},getZoomLevelForBoundingBox:function(e){var d=this.maps[this.api];var c=e.getNorthEast();var a=e.getSouthWest();var b=d.getBoundsZoomLevel(new CM.LatLngBounds(a.toProprietary(this.api),c.toProprietary(this.api)));return b},setMapType:function(a){var b=this.maps[this.api];switch(a){case mxn.Mapstraction.ROAD:break;case mxn.Mapstraction.SATELLITE:break;case mxn.Mapstraction.HYBRID:break;default:}},getMapType:function(){var a=this.maps[this.api];return mxn.Mapstraction.ROAD},getBounds:function(){var d=this.maps[this.api];var b=d.getBounds();var a=b.getSouthWest();var c=b.getNorthEast();return new mxn.BoundingBox(a.lat(),a.lng(),c.lat(),c.lng())},setBounds:function(b){var d=this.maps[this.api];var a=b.getSouthWest();var c=b.getNorthEast();d.zoomToBounds(new CM.LatLngBounds(a.toProprietary(this.api),c.toProprietary(this.api)))},addImageOverlay:function(c,a,e,i,f,g,d,h){var b=this.maps[this.api]},setImagePosition:function(e,b){var d=this.maps[this.api];var c;var a},addOverlay:function(a,b){var c=this.maps[this.api]},addTileLayer:function(f,a,b,d,e){var c=this.maps[this.api]},toggleTileLayer:function(b){var a=this.maps[this.api]},getPixelRatio:function(){var a=this.maps[this.api]},mousePosition:function(a){var b=this.maps[this.api]}},LatLonPoint:{toProprietary:function(){var a=new CM.LatLng(this.lat,this.lon);return a},fromProprietary:function(a){this.lat=a.lat();this.lon=a.lng()}},Marker:{toProprietary:function(){var d=this.location.toProprietary(this.api);var a={};if(this.iconUrl){var b=new CM.Icon();b.image=this.iconUrl;if(this.iconSize){b.iconSize=new CM.Size(this.iconSize[0],this.iconSize[1]);if(this.iconAnchor){b.iconAnchor=new CM.Point(this.iconAnchor[0],this.iconAnchor[1])}}if(this.iconShadowUrl){b.shadow=this.iconShadowUrl;if(this.iconShadowSize){b.shadowSize=new CM.Size(this.iconShadowSize[0],this.iconShadowSize[1])}}a.icon=b}if(this.labelText){a.title=this.labelText}var c=new CM.Marker(d,a);if(this.infoBubble){c.bindInfoWindow(this.infoBubble)}return c},openBubble:function(){var a=this.proprietary_marker;a.openInfoWindow(this.infoBubble)},hide:function(){var a=this.proprietary_marker;a.hide()},show:function(){var a=this.proprietary_marker;a.show()},update:function(){}},Polyline:{toProprietary:function(){var d=[];var c;for(var a=0,b=this.points.length;a<b;a++){d.push(this.points[a].toProprietary(this.api))}if(this.closed||d[0].equals(d[d.length-1])){c=new CM.Polygon(d,this.color,this.width,this.opacity,this.fillColor||"#5462E3",this.opacity||"0.3")}else{c=new CM.Polyline(d,this.color,this.width,this.opacity)}return c},show:function(){this.proprietary_polyline.show()},hide:function(){this.proprietary_polyline.hide()}}});