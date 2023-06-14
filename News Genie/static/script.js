const b = document.getElementById('box');

function openBox(){
    b.classList.add('rotate-y180')
}

function closeBox(){
    b.classList.remove('rotate-y180')
}

let slideIndex = 1;
showSlides(slideIndex);

function showSlides(n){
    let slides = document.getElementsByClassName('data');
    if(n > slides.length){
        slideIndex = 1
    }
    if(n < 1){
        slideIndex = slides.length
    }
    for(let i = 0; i < slides.length; i++){
        slides[i].style.opacity = '0'
    }
    slides[slideIndex-1].style.opacity = '1'
}

let carousel = document.querySelector('.avatar');
let count = 8;
let selected = 0;

function _Carousel(){
    let angel = selected / count * -360;
    carousel.style.transform = 'rotateY(' + angel + 'deg)'
}

function prev(n){
    showSlides(slideIndex += n);
    selected--;
    _Carousel()
}

function next(n){
    showSlides(slideIndex += n);
    selected++;
    _Carousel()
}