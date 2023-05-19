const THEME_COOKIE_MAX_AGE = 7 * 24 * 60 * 60;


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
        setCookie('theme', 'dark', {'max-age': THEME_COOKIE_MAX_AGE});
    } else {
        setCookie('theme', 'light', {'max-age': THEME_COOKIE_MAX_AGE});
    };
}

function changeTheme(isDark) {
    //получить список всех элементов с классом changing-color
    //удалить у каждого классы dark light
    //добавить класс dark или light

    let elems = document.querySelectorAll('.changing-color');

    elems.forEach((elem) => {
        elem.classList.remove('dark');
        elem.classList.remove('light');
    });

    if (isDark) {
        elems.forEach((elem) => {
            elem.classList.add('dark');
        });
    } else {
        elems.forEach((elem) => {
            elem.classList.add('light');
        });
    };
}

document.addEventListener('DOMContentLoaded', function() {

    let theme_cookie = getCookie('theme');
    
    if (theme_cookie != undefined) {
        changeThemeCookie(theme_cookie == 'dark');
        changeTheme(theme_cookie == 'dark');
    } else {
        changeThemeCookie(false);
        changeTheme(false);
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