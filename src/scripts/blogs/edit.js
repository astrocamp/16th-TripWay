import Alpine from "alpinejs";
import Swal from "sweetalert2";

Alpine.data("deleteBlog", (blog) => {
  Swal.fire({
    icon: "question",
    title: "確定要刪除嗎?",
    text: "若選擇刪除，資料將會消失",
    showCancelButton: true,
    cancelButtonText: "取消",
    confirmButtonText: "刪除",
  }).then((result) => {
    if(result.isConfirmed){
      blog.submit()
    }
  })
})