function getLocation(){
    var latitude, longitude;
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(success, error,{timeout:10000, enableHighAccuracy: true, maximumAge:0});
    }
    function success(position) {
        latitude = position.coords.latitude;
        longitude = position.coords.longitude;

        console.log(latitude + ' ' + longitude);
        loadLocationData();
        const geoApiUrl = `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=pl`;
        console.log(geoApiUrl);

        fetch(geoApiUrl)
        .then(res => res.json())
        .then(data => {
            $("#location").append('Znajdujesz się w ' + data.countryName + ', ' + data.city + ', ' + data.locality);
            $("#mapslink").text('Sprawdź na mapie');
            $("#mapslink").attr("href", `http://maps.google.com/maps?q=${latitude},${longitude}`);
//            $("#id_client").val(2);
        })
    };
    function error(){
        console.log('Unable to retrieve location data');
        $("#location").append('Unable to retrieve location data');
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
//                $(".btn").text(response.seconds)
//                $("#seconds").append('<li>' + response.seconds + '</li>')
            $('#latitude').val(latitude);
            $('#longitude').val(longitude);
            $("#coord").append('Szerokość geograficzna: ' + latitude + '<br>Długość geograficzna: '+ longitude);
        }
    });
   };
};

//$(".btn").click(getLocation());


