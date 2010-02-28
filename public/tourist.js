$(function () {
    
    /* functions and globals */
    
    var timeout = null,
        loading = loaded = 0,
        map = null,
        markers = {},
        infowindow = new google.maps.InfoWindow();
    
    var mapChanged = function () {
        window.clearTimeout(timeout);
        timeout = window.setTimeout(loadData, 1000);
    }
    
    var loadData = function () {
        
        if (map.getZoom() > 10) {
            
            var bounds = map.getBounds();
            
            var sw = bounds.getSouthWest(),
                ne = bounds.getNorthEast();
            
            var minLat = Math.floor(sw.lat() * 10) / 10,
                maxLat = Math.ceil(ne.lat() * 10) / 10,
                minLon = Math.floor(sw.lng() * 10) / 10,
                maxLon = Math.ceil(ne.lng() * 10) / 10;
            
            for (var lat = minLat; lat <= maxLat; lat = Math.round((lat + 0.1) * 10) / 10) {
                for (var lon = minLon; lon <= maxLon; lon = Math.round((lon + 0.1) * 10) / 10) {
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
                                            //document.location = "/attractions/" + data[index].id + ".html";
                                            var content = '<div id="infowindow">'
                                            if (data[index].thumbnail) {
                                                content += '<img src="' + data[index].thumbnail + '">';
                                            }
                                            content += '<a href="/attractions/' + data[index].id + '.html">' + data[index].title + "</a>";
                                            if (data[index].tags) {
                                                content += '<ul id="tags">';
                                                $.each(data[index].tags, function () {
                                                    content += '<li><a href="/search.html?t=' + this + '">' + this + "</a></li>";
                                                });
                                                content += "</ul>";
                                            }
                                            content += '</div>';
                                            infowindow.setContent(content);
                                            infowindow.open(map, marker);
                                        });
                                        markers[boxId].push(marker);
                                    });
                                }
                            },
                            complete: function () {
                                loaded++;
                                var progress = $("#big-map").width() / loading * loaded;
                                $("#loading").animate({
                                    "border-left": progress + "px solid #f80",
                                    width: ($("#big-map").width() - progress) + "px"
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
        
        bowling: "bowling.png",
        snooker: "billiard.png",
        aquarium: "aquarium.png",
        cinema: "cinema.png",
        theatre: "theater.png",
        casino: "casino.png",
        music: "music-rock.png",
        
        archeological: "museum-archeological.png",
        naval: "museum-naval.png",
        war: "museum-war.png",
        science: "museum-science.png",
        crafts: "museum-crafts.png",
        
        themepark: "themepark.png",
        zoo: "zoo.png",
        art: "publicart.png",
        circus: "circus.png",
        festival: "festival.png",
        waterpark: "waterpark.png",
        ferriswheel: "ferriswheel.png",
        
        playground: "playground.png",
        
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
        stadium: "stadium.png",
        
        sport: "stadium.png",
        nature: "park-urban.png",
        shop: "shoppingmall.png",
        historic: "museum-historical.png",
        museum: "museum-art.png",
        
        dupe: "info.png",
        "delete": "info.png",
        badloc: "info.png",
        todo: "info.png",
        trap: "info.png",
        translated: "info.png"
        
    };
    
    var getMarkerIcon = function (tags) {
        var icon = "info.png";
        $.each(markerIcons, function (item) {
            if ($.inArray(item, tags) > -1) {
                icon = markerIcons[item];
                return false;
            }
        });
        return "http://google-maps-icons.googlecode.com/files/" + icon;
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
        
    case "attraction":
        
        var tags = [];
        $("ul#tags a").each(function () {
            tags.push($(this).text());
        });
        $("h2").css({
            "backgroundImage": "url(" + getMarkerIcon(tags) + ")"
        });
        
        $("p#date").before('<span id="add-comment">Add a comment to this attraction</span>');
        $("#add-comment").click(function () {
            $(this).after('<form id="comment" method="post" action="' + document.location.pathname.replace('.html', '/comment.html') + '"><textarea name="comment"></textarea><input type="submit" value="Add a comment"></form>');
            $(this).slideUp();
            $("#comment").slideDown();
        });
        
        $("#map").click(function () {
            
            $(this).wrap('<div id="map"></div>');
            
            var latLon = $(this).attr("src").match(/([0-9.-]+),([0-9.-]+)/);
            if (latLon[1] && latLon[2]) {
                
                var center = new google.maps.LatLng(parseFloat(latLon[1]), parseFloat(latLon[2]));
                var mapOptions = {
                    center: center,
                    zoom: 11,
                    mapTypeId: google.maps.MapTypeId.ROADMAP,
                    mapTypeControl: false
                };
                var biggerMap = new google.maps.Map(document.getElementById("map"), mapOptions);
                var marker = new google.maps.Marker({
                    position: center,
                    map: biggerMap,
                    icon: "http://www.google.com/intl/en_ALL/mapfiles/marker_orange.png"
                });
                
                $("#map").animate({
                    width: $("#content").width() - 300
                }, function () {
                    google.maps.event.trigger(biggerMap, 'resize');
                });
                
            }
            return false;
            
        }).css("cursor", "pointer").attr("title", "Load an interactive map");
        
        $(".nav .recommend").click(function () {
            var that = $(this);
            $.post(that.attr("href"), null, function () {
                if (that.hasClass("recommended")) {
                    that.text("Recommend this attraction");
                    that.removeClass("recommended");
                } else {
                    that.text("Stop recommending this attraction");
                    that.addClass("recommended");
                }
            });
            return false;
        });
        
        $(".nav .itinerary").click(function () {
            var that = $(this);
            $.post(that.attr("href"), null, function () {
                if (that.hasClass("added")) {
                    that.text("Add to your itinerary");
                    that.removeClass("added");
                } else {
                    that.text("Remove from your itinerary");
                    that.addClass("added");
                }
            });
            return false;
        });
        
        break;
        
    case "map":
        
        if ($("#header:visible").length == 0) {
            $("#big-map").height(
                $(document).height() - 4
            );
        } else {
            $("#big-map").height(
                $(document).height() -
                $("#header").outerHeight() -
                $("#footer").outerHeight() - 
                60
            );
        }
        
        var location = window.location.search.match(/c=([0-9.-]+),([0-9.-]+)/);
        var zoom = 12;
        if (!location) {
            location = [null, 0, 0];
            zoom = 2;
        }
        
        var center = new google.maps.LatLng(parseFloat(location[1]), parseFloat(location[2]));
        var mapOptions = {
            center: center,
            zoom: zoom,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false
        };
        map = new google.maps.Map(document.getElementById("big-map"), mapOptions);
        
        var tags = [];
        $("#tags li").each(function () {
            tags.push($(this).text());
        });
        
        google.maps.event.addListener(map, "dragend", mapChanged);
        google.maps.event.addListener(map, "zoom_changed", mapChanged);
        
        $("#big-map").before('<div id="loading"></div>');
        
        mapChanged();
        
        break;
        
    case "edit":
        
        var center = new google.maps.LatLng(parseFloat($("input[name=lat]").val()), parseFloat($("input[name=lon]").val()));
        var mapOptions = {
            center: center,
            zoom: 14,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
            mapTypeControl: false
        };
        $("input.map").wrap('<div id="map"></div>');
        var map = new google.maps.Map(document.getElementById("map"), mapOptions);
        
        var marker = new google.maps.Marker({
            position: center,
            map: map,
            icon: "http://www.google.com/intl/en_ALL/mapfiles/marker_orange.png"
        });
        
        google.maps.event.addListener(map, "click", function (e) {
            marker.setPosition(e.latLng);
            $("input[name=lat]").val(e.latLng.lat().toFixed(4));
            $("input[name=lon]").val(e.latLng.lng().toFixed(4));
        });
        
        
        $("input[name=tags]")
            .css("display", "none")
            .after('<div><ul id="tags"></ul><input type="text" value=""></div><ul id="predict"></ul>')
            .appendTo("form");
        
        var addTag = function () {
            if ($(".tags input").val() != "") {
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
            .keyup(function (e) {
                if (e.keyCode == '40') { // down
                    if ($("#predict li.active").length) {
                        if ($("#predict li.active").next().length) {
                            $("#predict li.active").removeClass("active").next().addClass("active");
                        }
                    } else {
                        $("#predict li:first").addClass("active");
                    }
                    $(".tags input").val($("#predict li.active").text());
                } else if (e.keyCode == '38') { // up
                    if ($("#predict li.active").prev().length) {
                        $("#predict li.active").removeClass("active").prev().addClass("active");
                    }
                    $(".tags input").val($("#predict li.active").text());
                } else {
                    $("#predict").hide().empty();
                    var val = this.value;
                    if (val) {
                        $.each(markerIcons, function (index) {
                            if (index.substr(0, val.length) == val) {
                                $("#predict").append("<li>" + index + "</li>");
                            }
                        });
                        if ($("#predict li").length) {
                            $("#predict").show();
                        }
                    }
                }
            });
        
        $.each($("input[name=tags]").val().split(" "), function () {
            if (this != "") {
                $("label.tags ul#tags").append("<li>" + this + " <span>x</span></li>");
            }
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
        
        $("label.picture input")
            .css("display", "none")
            .appendTo("#content form");
        $("label.picture").append('<span class="change">Change</span> <span class="paste">Paste in Flickr URL</span>');
        if ($("label.picture img").length == 0) {
            $("label.picture span.change").text("Add");
        }
        var picturePage = 1;
        $("label.picture span.change").click(function () {
            $("label.picture span.change").text("Loading...");
            $.getJSON(
                "http://api.flickr.com/services/rest/?method=flickr.photos.search&format=json&api_key=abfb0fa992b89d701afa5342e183639f&license=4,5,6&per_page=10&page=" + picturePage + "&text=" + encodeURI($("input[name=name]").val()) + "&jsoncallback=?",
                function (data) {
                    if (data.stat == "ok" && data.photos.photo.length > 0) {
                        if ($("label.picture ul").length == 0) {
                            $("label.picture").append("<div><ul></ul></div>");
                        }
                        $.each(data.photos.photo, function () {
                            $("label.picture ul")
                                .append('<li><img src="http://farm' + this.farm + '.static.flickr.com/' + this.server + '/' + this.id + '_' + this.secret + '_s.jpg" alt="" title="' + this.title + '"></li>')
                                .css("width", $("label.picture li").length * 80);
                        });
                        $("label.picture ul img").click(function () {
                            var newUrl = this.src.replace("_s.jpg", "_m.jpg");
                            if ($("label.picture img.picture").length) {
                                $("label.picture img.picture").attr("src", newUrl);
                            } else {
                                $("label.picture").prepend('<img src="' + newUrl + '" class="picture" alt="">');
                            }
                            $("input[name=picture]").val(newUrl);
                            $("label.picture div").remove();
                            $("label.picture span.change").text("Change");
                        });
                        $("label.picture span.change").text("More pictures");
                        picturePage++;
                    } else {
                        $("label.picture span.change").text("No pictures found on Flickr for this attraction");
                    }
                }
            );
        });
        $("label.picture span.paste").click(function () {
            $("label.picture div, label.picture span").remove();
            $("input[name=picture]")
                .appendTo("label.picture")
                .css("display", "block")
                .focus();
        });
        
        break;
        
    }
    
});
