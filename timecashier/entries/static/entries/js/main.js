function getLocation(){
    var latitude, longitude;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success, error,{timeout:10000, enableHighAccuracy: true, maximumAge:0});
    }
    function success(position) {
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;

//        console.log(latitude + ' ' + longitude);
        loadLocationData();
        const geoApiUrl = `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=pl`;
//        console.log(geoApiUrl);

        fetch(geoApiUrl)
        .then(res => res.json())
        .then(data => {
            if($("#mapslink").length >0){
                $("#mapslink").text('Znajdujesz się w ' + data.countryName + ', ' + data.city + ', ' + data.locality + ' (' + latitude + ', '+ longitude + ') - klinij, aby sprawdzić w Mapach Google');
                $("#mapslink").attr("href", `https://maps.google.com/maps?q=${latitude},${longitude}`);
            };
            if($('#id_latitude').length > 0 && $('#id_longitude').length > 0){
                console.log($('#id_latitude').val() == '');
                if($('#id_latitude').val() == ''){
                    $('#id_latitude').val(latitude.toFixed(7));
                    $('#id_longitude').val(longitude.toFixed(7));
                };
            };

        });

    };
    function error(){
        console.log('Unable to retrieve location data');
        $("#mapslink").text('Nie udało się pobrać lokalizacji. Udostępnij swoje położenie, bądź wybierz klienta ręcznie.');
    };

    function setLocation(){
//    $("#id_start_date").change(function () {
      var nearest_client = $("#id_client").val();
//        var latitude = $("#latitude").val();
//        var longitude = $("#longitude").val();
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
//            $('#id_latitude').val(latitude);
//            $('#id_longitude').val(longitude);
            setLocation();
        }

    });
   };
};

