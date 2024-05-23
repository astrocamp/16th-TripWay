document.addEventListener("DOMContentLoaded", function() {
    var spinner = document.getElementById("loading-spinner");
    var content = document.getElementById("content");


    setTimeout(function() {
        spinner.style.display = "none";
        content.style.display = "block";
    }, 3500); 
});
