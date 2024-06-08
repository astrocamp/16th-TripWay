document.getElementById('menu-toggle-btn').addEventListener('click', toggleMenu);
function toggleMenu() {
    const menu = document.getElementById('menu-nav');
    if (menu.classList.contains('hidden')) {
        menu.classList.remove('hidden');
    } else {
        menu.classList.add('hidden');
    }
}