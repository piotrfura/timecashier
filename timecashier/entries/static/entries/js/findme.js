const findMyLocation = () => {
    const status = document.querySelector('.status');
    var mapslink = document.querySelector('.mapslink');


    const success = (position) => {
        console.log(position)
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        console.log(latitude + ' ' + longitude);
        const geoApiUrl = `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${latitude}&longitude=${longitude}&localityLanguage=pl`;
        console.log(geoApiUrl);

        fetch(geoApiUrl)
        .then(res => res.json())
        .then(data => {
            status.textContent = 'Znajdujesz się w ' + data.countryName + ', ' + data.city + ', ' + data.locality;
            mapslink.textContent = 'Sprawdź na mapie';
            mapslink.href = `http://maps.google.com/maps?q=${latitude},${longitude}`;
        })

    }

    const error = () => {
        status.textContent = 'Unable to retrieve your location';

    }

    navigator.geolocation.getCurrentPosition(success, error);

}

document.querySelector('.find-location').addEventListener('click', findMyLocation);