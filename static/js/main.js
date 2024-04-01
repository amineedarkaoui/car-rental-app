
// ACTIVE CLASS FOR SIDEBAR LINKS
document.addEventListener("DOMContentLoaded", function () {
  let currentLocation = window.location.href;

  let sidebarLinks = document.querySelectorAll(".sideBar a");

  sidebarLinks.forEach(function (link) {
    if (link.href === currentLocation) {
      link.classList.add("active");
    }
  });
});
// ---------------------------------------------------------------------


