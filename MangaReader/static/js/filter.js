document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    form = document.querySelector('#filterform');

    container = document.querySelector("#manga-container")
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        $.ajax({
            data: $(this).serialize(),
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            type: 'POST',
            url: '/ajax/filter/',
            success: function(response) {
                container.innerHTML = '';

                response.mangaList.forEach(function (item) {
                    console.log(item);
                    const a = document.createElement("a");

                    a.href = '/manga/' + item.slug;
                    a.classList.add("block_manga");

                    const div = document.createElement("div");
                    
                    div.style = "background-image: url(/media/" + item.photo + ");";
                    div.classList.add("image")

                    const h4 = document.createElement("h4");

                    h4.innerHTML = item.title;
                    h4.classList.add("manga_title");

                    div.appendChild(h4);
                    a.appendChild(div);

                    container.appendChild(a);
                });
            },
            error: function(response) {
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors);
            }
        });
    });
})