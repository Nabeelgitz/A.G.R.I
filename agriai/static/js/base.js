// =========================
// NAVBAR SHADOW ON SCROLL
// =========================

const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {

    if(window.scrollY > 40) {

        navbar.style.background = 'rgba(27, 67, 50, 0.45)';
        navbar.style.boxShadow = '0 10px 30px rgba(0,0,0,0.35)';

    }
    else {

        navbar.style.background = 'rgba(255,255,255,0.10)';
        navbar.style.boxShadow = '0 8px 32px rgba(0,0,0,0.25)';

    }

});


// =========================
// BUTTON HOVER GLOW
// =========================

const buttons = document.querySelectorAll('.nav-btn');

buttons.forEach(button => {

    button.addEventListener('mouseenter', () => {

        button.style.transform = 'translateY(-4px) scale(1.02)';

    });


    button.addEventListener('mouseleave', () => {

        button.style.transform = 'translateY(0px) scale(1)';

    });

});