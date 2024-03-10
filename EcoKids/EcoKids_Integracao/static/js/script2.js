function menuShow() {
    let menuMobile = document.querySelector('.mobile-menu');
    if (menuMobile.classList.contains('open')) {
        menuMobile.classList.remove('open');
        document.querySelector('.icon').src = "img/menu_white_36dp.svg";
    } else {
        menuMobile.classList.add('open');
        document.querySelector('.icon').src = "img/close_white_36dp.svg";
    }
}

function toggleTheme() {
    var body = document.body;
    body.classList.toggle("dark-theme");
}

var themeToggle = document.getElementById("theme-toggle");
themeToggle.addEventListener("click", toggleTheme);