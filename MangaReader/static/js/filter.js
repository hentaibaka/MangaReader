document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    form = document.querySelector('#filterform');
    
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
                container = document.querySelector('#manga-container');
                container.innerHTML = '';

                response.mangaList.forEach(function (item) {
                    console.log(item);
                    //ну тут типа будет код для создания манги и добавления её в контейнер
                    //сделаю как ты сделаешь шаблон манги на странице каталога
                    //пока смотри в консоли лол
                    //)))0000)00)0000000)00))000000)0)0)00)))00))0
                });
            },
            error: function(response) {
                alert(response.responseJSON.errors);
                console.log(response.responseJSON.errors);
            }
        });
    });
})