document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    markform = document.querySelector('#markform');
    markcancelbtn = document.getElementById("markformcancel");

    mark = document.getElementById("mark");
    mark_count = document.getElementById("mark-count");

    $("button#markformsubmit").on('click', function(event) {
        event.preventDefault();
        
        $.ajax({
            data: $.param({
                form: Object.fromEntries(new URLSearchParams($(markform).serialize())),
                user: JSON.parse(document.getElementById("username").textContent),
                manga: JSON.parse(document.getElementById("manga_id").textContent)
            }),
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            },
            type: 'POST',
            url: '/ajax/setusermark/',
            success: function(response) {
                mark_count = response.mark_count;
                if (mark_count > 1000) {
                    mark_count = (mark_count / 1000).toFixed(1);
                    if (mark_count == Math.round(mark_count)) {
                        mark_count = Math.round(mark_count);
                    }
                }

                mark.innerHTML = '⭐' + response.mark;
                mark_count.innerHTML = mark_count + 'К';
                markcancelbtn.hidden = false;
            },
            error: function(response) {
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors);
            }
        });
    });

    $("button#markformcancel").on('click', function(event) {
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
            url: '/ajax/deleteusermark/',
            success: function(response) {
                mark_count = response.mark_count;
                if (mark_count > 1000) {
                    mark_count = (mark_count / 1000).toFixed(1);
                    if (mark_count == Math.round(mark_count)) {
                        mark_count = Math.round(mark_count);
                    }
                }
                mark.innerHTML = '⭐' + response.mark;
                mark_count.innerHTML = mark_count + 'К';
                markcancelbtn.hidden = true;
            },
            error: function(response) {
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors);
            }
        });

    });
});