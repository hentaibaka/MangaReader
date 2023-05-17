document.addEventListener('DOMContentLoaded', function() {
    let i = 1;
    const tabsItem = document.querySelectorAll(".tabs_item");
    tabsItem.forEach(function(item) {
        item.id = 'tab_' + i++;
    })

    const tabsBtn = document.querySelectorAll(".tabs_nav_btn");
    i = 1;
    tabsBtn.forEach(function(item) {
        item.dataset.tab = '#tab_' + i++;
    })

    tabsBtn[0].classList.add('active');
    tabsItem[0].classList.add('active');
    tabsBtn.forEach(function(item) {
        let tabId = item.getAttribute("data-tab");
        let currentTab = document.querySelector(tabId);
        item.addEventListener("click", function(){
            
            tabsBtn.forEach(function(item2) {
                item2.classList.remove('active');
            });
            tabsItem.forEach(function(item2) {
                item2.classList.remove('active');
            });

            item.classList.add('active');
            currentTab.classList.add ('active');
        });
    });
});