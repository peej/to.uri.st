
$(function () {
    
    switch ($("body").attr("id")) {
    
    case "home":
        
        $("#lookat label input").focus();
        $("#lookat a").click(function () {
            $("#lookat label input").val($(this).text());
            return false;
        }).dblclick(function () {
            $(this).click();
            $("#lookat").submit();
        });
        
        break;
        
    case "search":
        
        var bounds = new google.maps.LatLngBounds();
        $("#search-results li a").each(function () {
            bounds.extend(
                new google.maps.LatLng($(this).attr("data-lat"), $(this).attr("data-lon"))
            );
        });
        
        $("#search-results img").replaceWith('<div id="map"></div><div id="map-big" title="Bigger map">&laquo;</div>');
        var mapOptions = {
          center: bounds.getCenter(),
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          mapTypeControl: false
        };
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);
        map.fitBounds(bounds);
        
        var markers = {};
        
        $("#search-results li a").each(function (index) {
            var link = $(this);
            if (index < 26) {
                letter = String.fromCharCode(index + 65);
            } else {
                letter = "";
            }
            var center = new google.maps.LatLng(link.attr("data-lat"), link.attr("data-lon"));
            var marker = new google.maps.Marker({
                position: center,
                map: map,
                title: link.text(),
                icon: "http://maps.google.com/mapfiles/marker" + letter + ".png"
            });
            google.maps.event.addListener(marker, 'click', function() {
                document.location = link.attr("href");
            });
            var boxId = (Math.round(center.lat() * 10) / 10) + "," + (Math.round(center.lng() * 10) / 10);
            if (typeof markers[boxId] == "undefined") {
                markers[boxId] = [];
            }
            markers[boxId].push(marker);
        });
        
        console.log(markers);
        
        $("#map-big").click(function () {
            
            $("#search-results ol, #map-big").hide();
            $("#map").animate({
                width: "100%",
                height: "400px"
            }, "fast", "swing", function () {
                google.maps.event.trigger(map, "resize");
            });
            
            var loadData = function () {
                
                if (map.getZoom() > 10) {
                    
                    var bounds = map.getBounds();
                    
                    var sw = bounds.getSouthWest(),
                        ne = bounds.getNorthEast();
                        
                    var minLat = Math.floor(sw.lat() * 3) / 3,
                        maxLat = Math.ceil(ne.lat() * 3) / 3,
                        minLon = Math.floor(sw.lng() * 3) / 3,
                        maxLon = Math.ceil(ne.lng() * 3) / 3;
                    
                    for (var lat = minLat; lat < maxLat; lat = lat + 0.3) {
                        lat = Math.round(lat * 10) / 10;
                        for (var lon = minLon; lon < maxLon; lon = lon + 0.3) {
                            lon = Math.round(lon * 10) / 10;
                            var boxId = lat + "," + lon;
                            if (typeof markers[boxId] == "undefined") {
                                markers[boxId] = [];
                                $.ajax({
                                    url: "/search.js?c=" + lat + "," + lon,
                                    dataType: "json",
                                    success: function (data) {
                                        if (typeof data == "object") {
                                            $.each(data, function (index) {
                                                var center = new google.maps.LatLng(this.location.lat, this.location.lon);
                                                var marker = new google.maps.Marker({
                                                    position: center,
                                                    map: map,
                                                    title: this.title
                                                });
                                                google.maps.event.addListener(marker, 'click', function() {
                                                    document.location = "/attractions/" + data[index].id + ".html";
                                                });
                                                markers[boxId].push(marker);
                                            });
                                        }
                                    }
                                });
                            }
                        }
                    }
                    
                } else {
                    
                    console.log("remove", markers);
                    $.each(markers, function () {
                        $.each(this, function () {
                            console.log("remove it");
                            this.setMap(null);
                        });
                    });
                    markers = {};
                    
                }
            };
            
            google.maps.event.addListener(map, "dragend", loadData);
            google.maps.event.addListener(map, "zoom_changed", loadData);
            
        });
        
    }
    
});
