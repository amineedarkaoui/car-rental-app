document.addEventListener("DOMContentLoaded", function () {
    let navbar = document.querySelector('.navbar');
    let links = document.querySelectorAll('header .header-container nav ul li a');
    let logo = document.querySelector('.header-container div:first-child a.logo');

    window.addEventListener('scroll', function () {
      if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
        links.forEach(function(link) {
          link.classList.add('scrolled-link');
        });
        if (logo) {
          logo.classList.add('scrolled-logo');
        }
      } else {
        navbar.classList.remove('scrolled');
        links.forEach(function(link) {
          link.classList.remove('scrolled-link');
        });
        if (logo) {
          logo.classList.remove('scrolled-logo');
        }
      }
    });
  });
  
// --------------------- cars animation ----------


function isElementInViewport(el) {
  let rect = el.getBoundingClientRect();
  return (
      rect.top >= -100 &&
      rect.left >= -100 &&
      rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
      rect.right <= (window.innerWidth || document.documentElement.clientWidth)
  );
}

function handleScroll() {
  let carDivs = document.querySelectorAll('.car');

  carDivs.forEach(function (div) {
      if (isElementInViewport(div, 100)) {
          div.classList.add('visible');
      } else if(!div.classList.contains('skip')){
          div.classList.remove('visible');
      }
  });
}



window.addEventListener('scroll', handleScroll);

handleScroll();