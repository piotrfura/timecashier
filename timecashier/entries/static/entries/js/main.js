$(document).ready(function(){
    $(".btn").click(function(){
        var latitude, longitude;
        if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error,{timeout:10000});
        }
        function success(position) {
//            console.log(position)
            latitude = position.coords.latitude;
            longitude = position.coords.longitude;

            console.log(latitude + ' ' + longitude);
            loadLocationData();
//            const geoApiUrl = `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=pl`;
//            console.log(geoApiUrl);
        };
        function error(){
            status.textContent = 'Unable to retrieve your location';
        };
        function loadLocationData(){
        $.ajax({
            url: '',
            type: 'get',
            data: {
//                button_text: $(this).text()
                latitude: latitude,
                longitude: longitude
            },
            success: function(response){
//                $(".btn").text(response.seconds)
//                $("#seconds").append('<li>' + response.seconds + '</li>')
                $("#seconds").append('<li>Szerokość geograficzna: ' + latitude + ', Długość geograficzna: '+ longitude + '</li>')
            }
        });
       };
    });
//    $("#seconds").on('click', 'li', function(){
////    kliknięcia itemów na liscie notimplemented
//    })
});


