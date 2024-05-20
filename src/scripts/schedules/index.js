// 頁籤顯示與隱藏功能
function showTab(selectedDate, selectedButtonId) {
    const tabContents = document.querySelectorAll(".tab-content");

    //隱藏所有日期頁籤內容
    for (let i = 0; i < tabContents.length; i++) {
      tabContents[i].style.display = "none";
    }
    // 顯示該日期頁籤的景點
    const dateTabContent = document.querySelector("#schedule" + selectedDate);
    if (dateTabContent) {
      dateTabContent.style.display = "block";
    }
    // 移除所有頁籤的顏色
    const buttons = document.querySelectorAll(".tab");
    buttons.forEach(button => {
      button.classList.remove("active-tab");
    });
    
    // 添加被選中頁籤的顏色
    const btn = document.querySelector("#" + selectedButtonId);
    btn.classList.add("active-tab");
  }

export default showTab