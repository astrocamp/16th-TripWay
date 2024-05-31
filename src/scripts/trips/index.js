function sortOptionsChange() {
    const sortOptions = document.getElementById('sort-options');
    
    if (sortOptions) {
        sortOptions.addEventListener('change', function() {
            const sortOption = this.value;
            window.location.href = `?sort=${sortOption}`;
        });
    }
}

sortOptionsChange();


function toggleMenuVisibility() {
    const menuToggles = document.querySelectorAll("[id^='menu-']");
    
    if (menuToggles) {
        menuToggles.forEach(function(toggle) {
            toggle.addEventListener("click", function() {
                const tripId = toggle.getAttribute("id").split("-").pop();
                const menuId = "menu-" + tripId;
                const menuElement = document.getElementById(menuId);
                
                if(menuElement) {
                    menuElement.classList.toggle("hidden");
                }
            });
        });
    }
}

document.addEventListener("DOMContentLoaded", toggleMenuVisibility);