document.addEventListener('DOMContentLoaded', function() {
    const btn = document.querySelector('.js-scroll')
    
    btn.addEventListener("click", () => window.scrollTo({top: 0, behavior: 'smooth'}))
    
    window.addEventListener("scroll", () => {
        if (window.scrollY > 100) {
            btn.classList.remove("d-none")
        } else {
            btn.classList.add("d-none")
        }
    })
});