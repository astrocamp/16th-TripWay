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

const copyEditButton = document.querySelector("#copyEditButton")
const copyWatchButton = document.querySelector("#copyWatchButton")

function copyEdit(){
    document.getElementById('copyEditButton').addEventListener('click', function(e) {
        const copyURL = e.target.querySelector("span").textContent;

        // 使用 Clipboard API 來複製
        navigator.clipboard.writeText(copyURL).then(() => {

            var successMessage = document.getElementById('successMessage2');
            successMessage.style.display = 'block';

            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 2000);
        }).catch(err => {
            console.error('複製失敗: ', err);
        })
    })
}
 
function copyWatch(){
    document.getElementById('copyWatchButton').addEventListener('click', function(e) {
        const copyURL = e.target.querySelector("span").textContent;

        navigator.clipboard.writeText(copyURL).then(() => {

            var successMessage = document.getElementById('successMessage');
            successMessage.style.display = 'block';

            setTimeout(() => {
                successMessage.style.display = 'none';
            }, 2000);
        }).catch(err => {
            console.error('複製失敗: ', err);
        });
    });
}

if (copyEditButton){
    copyEdit();
}

if (copyWatchButton){
    copyWatch();
}