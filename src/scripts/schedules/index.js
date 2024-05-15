// 頁籤顯示與隱藏
function openTab(tabName, btnId) {
    let i, tabContent;
    tabContent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabContent.length; i++) {
      tabContent[i].style.display = "none";
    }
    // document.getElementById("schedule" + tabName).style.display = "block";
     // 顯示日期欄位
    const scheduleTab = document.getElementById("schedule" + tabName);
    if (scheduleTab) {
        scheduleTab.style.display = "block";
    } else {
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