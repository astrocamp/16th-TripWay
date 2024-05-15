// 頁籤顯示與隱藏功能
function openTab(tabName, btnId) {
    let i, tabContent;
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
      tabContent[i].style.display = "none";
    }
    // 顯示該日期頁籤的景點
    const scheduleTab = document.getElementById("schedule" + tabName);
    if (scheduleTab) {
        scheduleTab.style.display = "block";
    }

    // 移除所有頁籤的顏色
    const buttons = document.querySelectorAll('.tab');
    buttons.forEach(button => {
      button.classList.remove('active-tab');
    });
    
    // 添加被選中頁籤的顏色
    const btn = document.querySelector('#' + btnId);
    btn.classList.add("active-tab");
  }


export default openTab