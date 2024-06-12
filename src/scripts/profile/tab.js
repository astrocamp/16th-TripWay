document.addEventListener("DOMContentLoaded", () => {
    (function() {
		const labels = document.querySelectorAll("label[data-tab]")
        const contents = document.querySelectorAll(".tab-content")
        const radios = document.querySelectorAll("input[name='my_tabs_1']")

        function showContent(tabId) {
            contents.forEach(content => {
                content.style.display = content.id === tabId ? "block" : "none"
            })
        }

        if (contents) {
            contents.forEach(content => {
                content.style.display = "none"
            })
            showContent("tab-content-1")
        }

        if (labels) {
            labels.forEach(label => {
                label.addEventListener("click", function() {
                    const tabId = this.getAttribute("data-tab")
                    showContent(tabId)
                })
            })
        }

        if (radios) {
            radios.forEach(radio => {
                radio.addEventListener("change", function() {
                    const tabId = this.id === "tab-1" ? "tab-content-1" : "tab-content-2"
                    showContent(tabId)
                })
            })
        }
    })()
})