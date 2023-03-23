function initMap(latitude, longitude) {
    let id_latitude = latitude;
    let id_longitude = longitude;

    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 15,
        center: { lat: id_latitude, lng:  id_longitude},
    });

    let marker = new google.maps.Marker({
        map,
        draggable: true,
        animation: google.maps.Animation.DROP,
        position: { lat: id_latitude, lng: id_longitude },
    });
    marker.addListener("click");

    google.maps.event.addListener(marker, 'dragend', function (evt) {
        document.getElementById('id_latitude').value = evt.latLng.lat().toFixed(7);
        document.getElementById('id_longitude').value = evt.latLng.lng().toFixed(7);
    });
};

function getLocation(){
    var latitude, longitude;

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error,{timeout:10000, enableHighAccuracy: true, maximumAge:0});
    }

    function success(position) {
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;

        if($('#id_latitude').length > 0 && $('#id_longitude').length > 0){
            $('#id_latitude').val(latitude.toFixed(7));
            $('#id_longitude').val(longitude.toFixed(7));
        };

        loadLocationData();

        if (document.getElementById('map')) {
                initMap(latitude, longitude)
        };

        if (document.getElementById('mapslink')) {
            const geoApiUrl = `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=pl`;

            fetch(geoApiUrl)
            .then(res => res.json())
            .then(data => {
                if($("#mapslink").length >0){
                    $("#mapslink").text('Jesteś w: ' + data.countryName + ', ' + data.city + ', ' + data.locality + ' - zobacz na mapie');
//                    $("#mapslink").attr("href", `https://maps.google.com/maps?q=${latitude},${longitude}`);
                };
            });
        };
    };
    function error(){
        console.log('Unable to retrieve location data');
        $("#mapslink").text('Nie udało się pobrać lokalizacji. Udostępnij swoje położenie, bądź wybierz klienta ręcznie.');
    };

    function setLocation(){
      var nearest_client = $("#id_client").val();
      $.ajax({
        url: '/ajax/client_nearby/',
        data: {
          'latitude': latitude,
          'longitude': longitude

        },
        dataType: 'json',
        success: function (data) {
            $("#id_client").val(data.nearest_client);
        }
      });
    };

    function loadLocationData(){
    $.ajax({
        url: '',
        type: 'post',
        headers: {'X-CSRFToken': csrftoken},
        data: {
            latitude: latitude,
            longitude: longitude
        },
        success: function(){
            setLocation();
        }

    });
   };
};
