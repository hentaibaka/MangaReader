const THEME_COOKIE_MAX_AGE = 7 * 24 * 60 * 60;
const THEME_COOKIE_NAME = 'theme';

const LIGHT_THEME_CLASS = 'light';
const DARK_THEME_CLASS = 'dark';
const CHANGING_THEME_CLASS = 'changing-color';

const DEFAULT_THEME = LIGHT_THEME_CLASS;


function getCookie(name) {
    let matches = document.cookie.match(new RegExp('(?:^|; )' + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + '=([^;]*)'));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

function setCookie(name, value, options = {}) {

    options = {
        ...options
    };
  
    if (options.expires instanceof Date) {
        options.expires = options.expires.toUTCString();
    };
  
    let updatedCookie = encodeURIComponent(name) + '=' + encodeURIComponent(value);
  
    for (let optionKey in options) {
        updatedCookie += '; ' + optionKey;
        let optionValue = options[optionKey];
        if (optionValue !== true) {
            updatedCookie += '=' + optionValue;
        }
    }
    document.cookie = updatedCookie;
}

function deleteCookie(name) {
    setCookie(name, '', {'max-age': -1});
}

function changeThemeCookie(isDark) {
    if (isDark) {
        setCookie(THEME_COOKIE_NAME, DARK_THEME_CLASS, {'max-age': THEME_COOKIE_MAX_AGE, path: '/'});
    } else {
        setCookie(THEME_COOKIE_NAME, LIGHT_THEME_CLASS, {'max-age': THEME_COOKIE_MAX_AGE, path: '/'});
    };
}

function changeTheme(isDark) {
    //получить список всех элементов с классом changing-color
    //удалить у каждого классы dark light
    //добавить класс dark или light

    let elems = document.querySelectorAll('.' + CHANGING_THEME_CLASS);

    elems.forEach((elem) => {
        elem.classList.remove(DARK_THEME_CLASS);
        elem.classList.remove(LIGHT_THEME_CLASS);
    });

    if (isDark) {
        elems.forEach((elem) => {
            elem.classList.add(DARK_THEME_CLASS);
        });
    } else {
        elems.forEach((elem) => {
            elem.classList.add(LIGHT_THEME_CLASS);
        });
    };
}

document.addEventListener('DOMContentLoaded', function() {

    let theme_cookie = getCookie(THEME_COOKIE_NAME);
    
    if (theme_cookie != undefined) {
        changeThemeCookie(theme_cookie == DARK_THEME_CLASS);
        changeTheme(theme_cookie == DARK_THEME_CLASS);
    } else {
        changeThemeCookie(DEFAULT_THEME == DARK_THEME_CLASS);
        changeTheme(DEFAULT_THEME == DARK_THEME_CLASS);
    }

    let light_btn = document.querySelector('#light-theme-btn');
    let dark_btn = document.querySelector('#dark-theme-btn');

    if (light_btn != null) {
        light_btn.addEventListener('click', function() {
            changeThemeCookie(false);
            changeTheme(false);
        });
    };

    if (dark_btn != null) {
        dark_btn.addEventListener('click', function() {
            changeThemeCookie(true);
            changeTheme(true);
        });
    };
});