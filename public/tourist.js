
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
        
        $("#search-results li a").each(function (index) {
            var link = $(this);
            if (index < 26) {
                letter = String.fromCharCode(index + 65);
            } else {
                letter = "";
            }
            var marker = new google.maps.Marker({
                position: new google.maps.LatLng(link.attr("data-lat"), link.attr("data-lon")),
                map: map,
                title: link.text(),
                icon: "http://maps.google.com/mapfiles/marker" + letter + ".png"
            });
            google.maps.event.addListener(marker, 'click', function() {
                document.location = link.attr("href");
            });
        });
        
        $("#map-big").click(function () {
            
            $("#search-results ol, #map-big").hide();
            $("#map").animate({
                width: "100%",
                height: "400px"
            }, "fast", "swing", function () {
                google.maps.event.trigger(map, "resize");
            });
            
        });
        
    }
    
});
