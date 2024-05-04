var moreInforBtn = document.querySelector('.more-infor_btn');
var content = document.querySelector('.content');
if (content) {
    moreInforBtn.addEventListener("click", (event) => {
      if (content.classList.contains("non_click")) {
        content.classList.remove("non_click");
        moreInforBtn.textContent = "Ẩn bớt";
        } else {
          content.classList.add("non_click");
          moreInforBtn.textContent = "Xem thêm";
        }
    });
}
// auto slide
if (document.querySelector('.slideshow-wrapper')) {
  autoSlideInterval = setInterval(function(){
    plusSlides(1)
}, 6000);
}
var slideIndex = 1;
showSlides(slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
}

function currentSlide(n) {
  showSlides(slideIndex = n);
}


function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
  }
  if (slides.length > 0) {
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
  }
}