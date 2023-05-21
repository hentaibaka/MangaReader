document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    listform = document.querySelector('#listform');
    listcancelbtn = document.getElementById("listformcancel");
    
    $("button#listformsubmit").on('click', function(event) {
        event.preventDefault();
        
        $.ajax({
            data: $.param({
                form: Object.fromEntries(new URLSearchParams($(listform).serialize())),
                user: JSON.parse(document.getElementById("username").textContent),
                manga: JSON.parse(document.getElementById("manga_id").textContent)
            }),
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            type: 'POST',
            url: '/ajax/setuserlist/',
            success: function(response) {
                listcancelbtn.hidden = false;
            },
            error: function(response) {
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors);
            }
        });
    });

    $("button#listformcancel").on('click', function(event) {
        event.preventDefault();
        
        $.ajax({
            data: $.param({
                user: JSON.parse(document.getElementById("username").textContent),
                manga: JSON.parse(document.getElementById("manga_id").textContent)
            }),
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            type: 'POST',
            url: '/ajax/deleteuserlist/',
            success: function(response) {
                listcancelbtn.hidden = true;
            },
            error: function(response) {
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors);
            }
        });
    });
});