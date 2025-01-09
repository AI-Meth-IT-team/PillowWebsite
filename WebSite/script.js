function onStart(){
    
    const configFilePath = 'config.json';

    fetch(configFilePath)
        .then(response => {
            if (!response.ok) {
                throw new Error('Nie udało się załadować pliku konfiguracyjnego.');
            }
            return response.json();
        })
        .then(data => {
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
}
function startGame() {
    const scriptPath = '/pełna/ścieżka/do/skryptu.py'; // Podaj właściwą ścieżkę
    const arguments = ['arg1', 'arg2']; // Argumenty do skryptu

    fetch('http://localhost:5000/start-game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            path: scriptPath,
            args: arguments,
        }),
    })
        .then(response => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');
            let output = '';

            // Czytaj strumień danych w czasie rzeczywistym
            function readStream() {
                reader.read().then(({ done, value }) => {
                    if (done) {
                        console.log('Strumień zakończony.');
                        return;
                    }

                    // Dekoduj otrzymane dane
                    output += decoder.decode(value, { stream: true });
                    console.log(output); // Loguj dane na konsolę w czasie rzeczywistym
                    readStream(); // Czytaj dalej
                });
            }

            readStream();
        })
        .catch(error => {
            console.error('Błąd połączenia z serwerem:', error);
        });
}
