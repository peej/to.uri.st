$(function () {
    
    /* functions and globals */
    
    var timeout = null,
        loading = loaded = 0,
        map = null,
        markers = {};
    
    var mapChanged = function () {
        window.clearTimeout(timeout);
        timeout = window.setTimeout(loadData, 1000);
    }
    
    var loadData = function () {
        
        if (map.getZoom() > 10) {
            
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
                                loaded++;
                                var progress = $("#map").width() / loading * loaded;
                                $("#loading").animate({
                                    "border-left": progress + "px solid #f80",
                                    width: ($("#map").width() - progress) + "px"
                                }, "slow");
                                if (loading == loaded) {
                                    loading = loaded = 0;
                                }
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
            
            $("#loading").width(0);
            
        }
    };
    
    
    var markerIcons = {
        nature: "park-urban.png",
        wildlife: "animals.png",
        beach: "beach.png",
        lake: "lake.png",
        wetland: "wetland.png",
        forest: "forest.png",
        waterfall: "waterfall.png",
        castle: "castle.png",
        palace: "palace.png",
        citywalls: "gateswalls.png",
        tower: "tower.png",
        ruins: "ruins.png",
        church: "church.png",
        farm: "farm.png",
        windmill: "windmill.png",
        vineyard: "wineyard.png",
        watermill: "watermill.png",
        garden: "garden.png",
        bridge: "bridge.png",
        fountain: "fountain.png",
        monument: "monument.png",
        worldheritagesite: "worldheritagesite.png",
        statue: "statue.png",
        park: "park-urban.png",
        picnic: "picnic.png",
        view: "panoramic180.png",
        cave: "cave.png",
        
        bookshop: "bookstore.png",
        giftshop: "gifts.png",
        artgallery: "artgallery.png",
        market: "market.png",
        bar: "bar.png",
        cafe: "coffee.png",
        icecream: "icecream.png",
        shop: "shoppingmall.png",
        
        bowling: "bowling.png",
        snooker: "billiard.png",
        aquarium: "aquarium.png",
        cinema: "cinema.png",
        theatre: "theater.png",
        casino: "casino.png",
        music: "music-rock.png",
        
        historic: "museum-historical.png",
        archeological: "museum-archeological.png",
        naval: "museum-naval.png",
        war: "museum-war.png",
        science: "museum-science.png",
        crafts: "museum-crafts.png",
        museum: "museum-art.png",
        
        themepark: "themepark.png",
        zoo: "zoo.png",
        art: "publicart.png",
        circus: "circus.png",
        festival: "festival.png",
        waterpark: "waterpark.png",
        ferriswheel: "ferriswheel.png",
        
        playground: "playground.png",
        
        stadium: "stadium.png",
        americanfootball: "usfootball.png",
        baseball: "baseball.png",
        basketball: "basketball.png",
        cricket: "cricket.png",
        football: "soccer.png",
        golf: "golf.png",
        rugby: "rugby.png",
        tennis: "tennis.png",
        cycling: "cyclingsport.png",
        racetrack: "racing.png",
        archery: "archery.png",
        climbing: "climbing.png",
        fishing: "fishing.png",
        hiking: "hiking.png",
        horse: "horseriding.png",
        skateboarding: "skateboarding.png",
        pool: "pool.png",
        kayaking: "kayak.png",
        boating: "sailboat-sport.png",
        surfing: "surfing.png",
        swimming: "swim-outdoor.png",
        waterskiing: "waterskiing.png",
        windsurfing: "windsurfing.png",
        icehockey: "icehockey.png",
        iceskating: "iceskating.png",
        snowboarding: "snowboarding.png",
        skiing: "skiing.png",
        sport: "stadium.png"
        
    };
    
    var getMarkerIcon = function (tags) {
        var icon = "info.png";
        $.each(tags, function () {
            if (typeof markerIcons[this] == "string") {
                icon = "http://google-maps-icons.googlecode.com/files/" + markerIcons[this];
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
        
    case "edit":
        
        $("input[name=tags]")
            //.css("display", "none")
            .after('<div><ul id="tags"></ul><input type="text" value=""></div><ul id="predict"></ul>')
            .parent().addClass("tags").end()
            .appendTo("form");
        
        var addTag = function () {
            if ($(".tags input").val()) {
                $("input[name=tags]").val($("input[name=tags]").val() + " " + $(".tags input").val());
                $("label.tags ul#tags").append("<li>" + $(".tags input").val() + " <span>x</span></li>");
                $(".tags input").val("");
            }
        }
        
        $(".tags input")
            .focusin(function () {
                $(".tags div").addClass("active");
            })
            .focusout(function (e) {
                $(".tags div").removeClass("active");
            })
            .keypress(function (e) {
                if (e.which == '13' || e.which == '32') {
                    addTag();
                    e.preventDefault();
                }
            })
            .keyup(function () {
                $("#predict").hide().empty();
                var val = this.value;
                if (val) {
                    $.each(markerIcons, function (index) {
                        if (index.substr(0, val.length) == val) {
                            $("#predict").append("<li>" + index + "</li>");
                        }
                    });
                    $("#predict").show();
                }
            });
        
        $.each($("input[name=tags]").val().split(" "), function () {
            $("label.tags ul#tags").append("<li>" + this + " <span>x</span></li>");
        });
        
        $("ul#tags li span").live("click", function () {
            $(this).parent().remove();
            var newtags = "";
            $("ul#tags li").each(function () {
                newtags += $(this).text().substr(0, $(this).text().length - 1);
            });
            $("input[name=tags]").val($.trim(newtags));
        });
        
        $("ul#predict li").live("click", function () {
            $(".tags input").val($(this).text());
            $("#predict").hide().empty();
            addTag();
        });
        
        break;
        
    }
    
    
    /* event handlers */
    
    var newWidth = $("#content").width() - 2;
    
    $("#map").bind("big", function () {
        
        var center = map.getCenter();
        
        $("#map").css({
            width: newWidth,
            height: "400px"
        });
        google.maps.event.trigger(map, "resize");
        
        google.maps.event.addListener(map, "dragend", mapChanged);
        google.maps.event.addListener(map, "zoom_changed", mapChanged);
        
        $("#map").before('<div id="loading"></div>').after('<div id="instruction">Zoom in to see more attractions</div>');
        
        $.each(markers, function () {
            $.each(this, function () {
                this.setMap(null);
            });
        });
        markers = {};
        
        map.setZoom(11);
        
    });
    
});
