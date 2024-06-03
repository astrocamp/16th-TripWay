document.addEventListener("DOMContentLoaded", function () {
  const ratingStars = document.querySelectorAll(".rating-star");
  // const isLoggedIn = document.querySelector('input[name="is_logged_in"]').value;

  ratingStars.forEach((star, index) => {
    star.addEventListener("click", function (event) {
      if (isLoggedIn === "False") {
        // 如果用戶未登入
        event.preventDefault(); // 阻止默認行為
        Swal.fire({
          title: "需要登入",
          text: "請先登入以使用評分功能",
          icon: "warning",
          confirmButtonText: "確定",
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = loginUrl; // 重定向到登入頁面
          }
        });
      } else {
        // 檢查是否已經選取了該星星
        if (star.classList.contains("bg-orange-400")) {
          // 如果是，則清除所有星星的選取
          ratingStars.forEach((btn) => btn.classList.remove("bg-orange-400"));
        } else {
          // 如果否，則點亮相應數量的星星
          ratingStars.forEach((btn) => btn.classList.remove("bg-orange-400"));
          for (let i = 0; i <= index; i++) {
            ratingStars[i].classList.add("bg-orange-400");
          }
        }
      }
    });
  });

  // 編輯留言功能
  const editCommentButtons = document.querySelectorAll(".edit-comment-btn");
  editCommentButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const comment = this.closest(".comment");
      const editForm = comment.querySelector(".edit-form");
      const commentContent = comment.querySelector(".comment-content");
      editForm.classList.remove("hidden");
      commentContent.classList.add("hidden");
    });
  });

  // 取消編輯功能
  const cancelEditButtons = document.querySelectorAll(".cancel-edit-btn");
  cancelEditButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const editForm = this.closest(".edit-form");
      const comment = editForm.closest(".comment");
      const commentContent = comment.querySelector(".comment-content");
      editForm.classList.add("hidden");
      commentContent.classList.remove("hidden");
    });
  });

  // 刪除留言功能
  const deleteCommentButtons = document.querySelectorAll(".delete-comment-btn");
  deleteCommentButtons.forEach((button) => {
    button.addEventListener("click", function (event) {
      event.preventDefault();
      confirmDelete(this);
    });
  });
});

function confirmDelete(button) {
  Swal.fire({
    title: "確定刪除此留言嗎?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#d33",
    cancelButtonColor: "#3085d6",
    confirmButtonText: "確認",
    cancelButtonText: "取消",
  }).then((result) => {
    if (result.isConfirmed) {
      // 提交表單進行硬刪除
      button.closest("form").submit();
    }
  });
}
