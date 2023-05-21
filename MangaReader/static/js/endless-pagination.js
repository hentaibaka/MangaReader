let counter = 0;

const quantity = 5;

let exists = true;
let isLoading = false

//поменять если не подгружает
const offsetParam = 10;

document.addEventListener('DOMContentLoaded', load);

window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - offsetParam && !isLoading) {
        isLoading = true;
        load();
    };
};

function load() {
    const start = counter;
    const end = counter + quantity - 1;

    counter = end + 1;

    if (exists) {
        $.ajax({
            data: $.param({
                start: start,
                end: end,
                chapter_id: JSON.parse(document.getElementById("chapter_id").textContent),
            }),
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            type: 'GET',
            url: '/ajax/loadpages/',
            success: function(response) {
                response.pages.forEach(add_page);
                exists = response.exists;
            },
            error: function(response) {
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors);
            }
        });
    };

    setTimeout(() => {isLoading = false}, 300);
};

function add_page(content) {
    const pagediv = document.createElement('div');
    const img = document.createElement('img');
    img.src = '/media/' + content.photo;

    pagediv.style.display = 'flex';
    pagediv.style.justifyContent = 'center';
    pagediv.style.padding = '0 10px';


    img.style.width = '60%';

    pagediv.appendChild(img);
    document.querySelector('#container-pages').append(pagediv);
};