$(function () {
    
    /* functions and globals */
    
    var timeout = null,
        loading = 0,
        map = null,
        markers = {};
    
    var mapChanged = function () {
        if (!loading) {
            window.clearTimeout(timeout);
            timeout = window.setTimeout(loadData, 1000);
        }
    }
    
    var loadData = function () {
        
        if (map.getZoom() > 10) {
            
            $("#loading").show();
            
            $("#instruction").fadeOut();
            
            var bounds = map.getBounds();
            
            var sw = bounds.getSouthWest(),
                ne = bounds.getNorthEast();
                
            var minLat = Math.floor(sw.lat() * 10) / 10,
                maxLat = Math.ceil(ne.lat() * 10) / 10,
                minLon = Math.floor(sw.lng() * 10) / 10,
                maxLon = Math.ceil(ne.lng() * 10) / 10;
            
            for (var lat = minLat; lat < maxLat; lat = lat + 0.1) {
                lat = Math.round(lat * 10) / 10;
                for (var lon = minLon; lon < maxLon; lon = lon + 0.1) {
                    lon = Math.round(lon * 10) / 10;
                    var boxId = lat + "," + lon;
                    if (typeof markers[boxId] == "undefined") {
                        loading++;
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
                                            title: this.title,
                                            icon: getMarkerIcon(data[index].tags)
                                        });
                                        google.maps.event.addListener(marker, 'click', function() {
                                            document.location = "/attractions/" + data[index].id + ".html";
                                        });
                                        markers[boxId].push(marker);
                                    });
                                }
                            },
                            complete: function () {
                                loading--;
                                if (loading == 0) $("#loading").fadeOut();
                            }
                        });
                    }
                }
            }
            
        } else {
            
            $("#instruction").show();
            
            $.each(markers, function () {
                $.each(this, function () {
                    this.setMap(null);
                });
            });
            markers = {};
            
            $("#loading").fadeOut();
            
        }
    };
    
    
    var markerIcons = {
        historic: "http://google-maps-icons.googlecode.com/files/museum-historical.png",
        museum: "http://google-maps-icons.googlecode.com/files/museum-art.png",
        nature: "http://google-maps-icons.googlecode.com/files/park-urban.png",
        shop: "http://google-maps-icons.googlecode.com/files/shoppingmall.png",
        sport: "http://google-maps-icons.googlecode.com/files/stadium.png",
        theatre: "http://google-maps-icons.googlecode.com/files/theater.png",
        themepark: "http://google-maps-icons.googlecode.com/files/themepark.png",
        zoo: "http://google-maps-icons.googlecode.com/files/zoo.png",
        view: "http://google-maps-icons.googlecode.com/files/panoramic180.png"
    };
    
    var getMarkerIcon = function (tags) {
        var icon = "http://google-maps-icons.googlecode.com/files/info.png";
        $.each(tags, function () {
            if (typeof markerIcons[this] == "string") {
                icon = markerIcons[this];
                return false;
            }
        });
        return icon;
    };
    
    
    /* page controller code */
    
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
        map = new google.maps.Map(document.getElementById("map"), mapOptions);
        map.fitBounds(bounds);
        
        $("#search-results li a").each(function (index) {
            var link = $(this);
            if (index < 26) {
                var icon = "http://google-maps-icons.googlecode.com/files/blue" + String.fromCharCode(index + 65) + ".png";
            } else {
                var icon = "/_/marker-blue.png";
            }
            var center = new google.maps.LatLng(link.attr("data-lat"), link.attr("data-lon"));
            var marker = new google.maps.Marker({
                position: center,
                map: map,
                title: link.text(),
                icon: icon
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
        
        $("#map-big").click(function () {
            $("h2").text("Attractions");
            $("#search-results ol, #map-big").hide();
            $("#map").trigger("big")
        });
        
        break;
        
    case "attraction":
        
        var location = $("#map").attr("src").match(/\|([0-9.-]+),([0-9.-]+)/);
        
        $("#map").replaceWith('<div id="map"></div><div id="map-big" title="Bigger map">&laquo;</div>');
        var center = new google.maps.LatLng(parseFloat(location[1]), parseFloat(location[2]));
        var mapOptions = {
            center: center,
            zoom: 14,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false
        };
        map = new google.maps.Map(document.getElementById("map"), mapOptions);
        
        var tags = [];
        $("#tags li").each(function () {
            tags.push($(this).text());
        });
        
        var marker = new google.maps.Marker({
            position: center,
            map: map,
            icon: getMarkerIcon(tags)
        });
        markers["attraction"] = [];
        markers["attraction"].push(marker);
        
        $("#map-big").click(function () {
            $("h2").text("Attractions");
            $("h3, .info, p, img, #tags, a.more, #map-big").hide();
            $("#map").trigger("big")
        });
        
        break;
        
    }
    
    
    /* event handlers */
    
    $("#map").bind("big", function () {
        
        var center = map.getCenter();
        
        $("#map").animate({
            width: "100%",
            height: "400px"
        }, "fast", "swing", function () {
            google.maps.event.trigger(map, "resize");
        });
        
        google.maps.event.addListener(map, "dragend", mapChanged);
        google.maps.event.addListener(map, "zoom_changed", mapChanged);
        
        $("#map").after('<div id="loading">Loading data</div><div id="instruction">Zoom in to see more attractions</div>');
        
        $.each(markers, function () {
            $.each(this, function () {
                this.setMap(null);
            });
        });
        markers = {};
        
        map.setZoom(11);
        
    });
    
});
