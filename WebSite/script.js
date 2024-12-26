function onStart(){
    //ładowanie z pliku wartości brightnes
    var slider = document.getElementsByClassName('brightnesSlider')[0];
    if (slider) {
        slider.value = 66; // tu bedzie sie bralo z pliku wartosci i dawalo tu
    }



// a niżej bedzie pobieranie wartosci z pliku tak na pozniej cn czyli bedzie jakos tak zapisywany

// config.json
//{
//    "brightness": 66
//}

    /*
    const configFilePath = 'config.json';

    // Pobieranie wartości jasności z pliku JSON
    fetch(configFilePath)
        .then(response => {
            if (!response.ok) {
                throw new Error('Nie udało się załadować pliku konfiguracyjnego.');
            }
            return response.json();
        })
        .then(data => {
            // Sprawdzenie, czy w pliku JSON znajduje się wartość jasności
            if (data && typeof data.brightness !== 'undefined') {
                const slider = document.getElementsByClassName('brightnesSlider')[0];
                if (slider) {
                    slider.value = data.brightness;
                    console.log(`Ustawiono jasność na ${data.brightness}`);
                } else {
                    console.error('Nie znaleziono elementu suwaka.');
                }
            } else {
                console.error('Plik JSON nie zawiera wartości brightness.');
            }
        })
        .catch(error => {
            console.error('Błąd podczas ładowania pliku konfiguracyjnego:', error);
        });

    */
}
function startGame(){
    
}
