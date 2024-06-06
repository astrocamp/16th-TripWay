function toggleMenu() {
    const menuToggleBtn = document.getElementById('menu-toggle-btn');
    const menuNav = document.getElementById('menu-nav');

    if (menuToggleBtn && menuNav) {
        menuToggleBtn.addEventListener('click', () => {
            menuNav.classList.toggle('hidden');
        });
    } else {
        console.error('Menu toggle button or navigation menu not found.');
    }
}
export default toggleMenu