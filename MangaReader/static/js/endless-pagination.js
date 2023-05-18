let counter = 0;

const quantity = 5;

let exists = true;

document.addEventListener('DOMContentLoaded', load);

window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    };
};

function load() {
    const start = counter;
    const end = counter + quantity - 1;
    counter = end + 1;
    if (exists) {
        fetch('/ajax/loadpages?start=' + start + "&end=" + end + "&chapter_id=" + JSON.parse(document.getElementById("chapter_id").textContent))
        .then(response => response.json())
        .then(data => {
            data.pages.forEach(add_page);
            exists = data.exists;
        });
    };
};

function add_page(content) {
    const pagediv = document.createElement('div');
    const img = document.createElement('img');
    img.src = '/media/' + content.photo;
    pagediv.appendChild(img);
    document.querySelector('#container-pages').append(pagediv);
};