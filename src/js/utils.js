import languages_states_choices from '../../app/clsite/choices/countries+states'

export function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


export function getAllCountries() {
    return languages_states_choices.map(el => el.name)
}

export function getStatesByCountry(country) {
    const choice = languages_states_choices.find(el => {
        return el.name === country
    })
    return choice ? choice.states : []
}