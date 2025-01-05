const config = {
    cUrl: 'https://api.countrystatecity.in/v1/countries',
    ckey: 'NHhvOEcyWk50N2Vna3VFTE00bFp3MjFKR0ZEOUhkZlg4RTk1MlJlaA=='
};

const countrySelect = document.querySelector('.country');
const stateSelect = document.querySelector('.state');
const citySelect = document.querySelector('.city');

// अगर countrySelect मौजूद नहीं है, तो कोई कार्रवाई न करें
if (countrySelect && stateSelect && citySelect) {
    const countryData = {};
    const stateData = {};

    // API से डेटा लाने के लिए एक सामान्य फ़ंक्शन
    async function fetchData(url, headers = {}) {
        try {
            const response = await fetch(url, { headers });
            if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
            return await response.json();
        } catch (error) {
            // console.error(`Error fetching data from ${url}:`, error);
            return [];
        }
    }

    // देश लोड करें
    async function loadCountries() {
        const countries = await fetchData(config.cUrl, { "X-CSCAPI-KEY": config.ckey });

        countries.sort((a, b) => a.name.localeCompare(b.name));
        countries.forEach(country => {
            const option = createOption(country.name, country.name);
            countrySelect.appendChild(option);
            countryData[country.name] = country.iso2;
        });

        // प्रारंभिक स्थिति
        disableSelect(stateSelect);
        disableSelect(citySelect);
    }

    // राज्य लोड करें
    async function loadStates() {
        resetSelect(stateSelect);
        resetSelect(citySelect);
        enableSelect(stateSelect);

        const countryCode = countryData[countrySelect.value];
        if (!countryCode) return;

        const states = await fetchData(`${config.cUrl}/${countryCode}/states`, { "X-CSCAPI-KEY": config.ckey });

        states.sort((a, b) => a.name.localeCompare(b.name));
        states.forEach(state => {
            const option = createOption(state.name, state.name);
            stateSelect.appendChild(option);
            stateData[state.name] = state.iso2;
        });
    }

    // शहर लोड करें
    async function loadCities() {
        resetSelect(citySelect);
        enableSelect(citySelect);

        const countryCode = countryData[countrySelect.value];
        const stateCode = stateData[stateSelect.value];
        if (!countryCode || !stateCode) return;

        const cities = await fetchData(`${config.cUrl}/${countryCode}/states/${stateCode}/cities`, { "X-CSCAPI-KEY": config.ckey });

        cities.sort((a, b) => a.name.localeCompare(b.name));
        cities.forEach(city => {
            const option = createOption(city.name, city.name);
            citySelect.appendChild(option);
        });
    }

    // एक ऑप्शन एलिमेंट बनाएँ
    function createOption(value, text) {
        const option = document.createElement('option');
        option.value = value;
        option.textContent = text;
        return option;
    }

    // चयनित सूची को रीसेट करें
    function resetSelect(select) {
        select.innerHTML = '<option value="">Select</option>';
        disableSelect(select);
    }

    // चयनित सूची को सक्रिय करें
    function enableSelect(select) {
        select.disabled = false;
        select.style.pointerEvents = 'auto';
    }

    // चयनित सूची को निष्क्रिय करें
    function disableSelect(select) {
        select.disabled = true;
        select.style.pointerEvents = 'none';
    }

    // इवेंट लिसनर्स जोड़ें
    countrySelect.addEventListener('change', loadStates);
    stateSelect.addEventListener('change', loadCities);

    // पेज लोड होने पर देश लोड करें
    window.onload = loadCountries;
}
