document.addEventListener('DOMContentLoaded', function () {
  const menuToggle = document.getElementById('menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');

  menuToggle.addEventListener('click', function () {
    mobileMenu.classList.toggle('-translate-y-full');
    mobileMenu.classList.toggle('opacity-0');
    mobileMenu.classList.toggle('pointer-events-none');
  });
});