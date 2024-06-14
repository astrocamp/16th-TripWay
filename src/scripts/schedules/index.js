import Alpine from "alpinejs";

// 頁籤顯示與隱藏功能
function showTab(selectedDate, selectedButtonId) {
    const tabContents = document.querySelectorAll(".tab-content");

    //隱藏所有日期頁籤內容
    tabContents.forEach(content => {
      content.style.display = "none";
    });
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
    const btn = document.querySelector(`#${selectedButtonId}`);
    if (btn) {
      btn.classList.add("active-tab");
    }
}

Alpine.data("deleteSchedule", (schedule) => {
  Swal.fire({
    icon: "question",
    title: "確定要刪除嗎?",
    text: "若選擇刪除，資料將會消失",
    showCancelButton: true,
    cancelButtonText: "取消",
    confirmButtonText: "刪除",
  }).then((result) => {
    if(result.isConfirmed){
      schedule.submit()
    }
  })
})

Alpine.data("submitScheduleChange", (start, end, change) => {
  if (start.value <= end.value) {
    change.submit()
  } else {
    alert("離開時間不能早於抵達時間")
  }
})

Alpine.data("deleteMember", (member) => {
  Swal.fire({
    icon: "question",
    title: "確定要刪除成員嗎?",
    showCancelButton: true,
    cancelButtonText: "取消",
    confirmButtonText: "刪除",
  }).then((result) => {
    if(result.isConfirmed){
      member.submit()
    }
  })
})

export default showTab