document.addEventListener("DOMContentLoaded", function () {
  const ratingStars = document.querySelectorAll(".rating-star");
  const isLoggedIn = document.querySelector('input[name="is_logged_in"]').value;

  ratingStars.forEach((star) => {
    star.addEventListener("click", function (event) {
      if (isLoggedIn === "False") {
        // 如果用戶未登錄
        event.preventDefault(); // 阻止默認行為
        Swal.fire({
          title: "需要登錄",
          text: "請先登錄以使用評分功能",
          icon: "warning",
          confirmButtonText: "確定",
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = loginUrl; // 重定向到登錄頁面
          }
        });
      }
    });
  });

  // 顯示 Sweet Alert 的消息
  // const alertType = document.querySelector('input[name="alert_type"]').value;
  // const alertMessage = document.querySelector('input[name="alert_message"]').value;
  // if (alertType && alertMessage) {
  //   Swal.fire({
  //     text: alertMessage,
  //     icon: alertType,
  //   });
  // }

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
    button.addEventListener("click", function () {
      const commentId = this.getAttribute("data-comment-id");
      Swal.fire({
        title: "確定要刪除嗎？",
        text: "這個操作不能撤銷！",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "刪除",
        cancelButtonText: "取消",
      }).then((result) => {
        if (result.isConfirmed) {
          const form = document.createElement("form");
          form.method = "POST";
          form.action = commentsIndexUrl;
          const csrfInput = document.createElement("input");
          csrfInput.type = "hidden";
          csrfInput.name = "csrfmiddlewaretoken";
          csrfInput.value = csrfToken;
          form.appendChild(csrfInput);
          const deleteInput = document.createElement("input");
          deleteInput.type = "hidden";
          deleteInput.name = "delete_comment_id";
          deleteInput.value = commentId;
          form.appendChild(deleteInput);
          document.body.appendChild(form);
          form.submit();
        }
      });
    });
  });
});
