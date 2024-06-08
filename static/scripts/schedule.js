import Alpine from "alpinejs";
window.Alpine = Alpine;
Alpine.start()

Alpine.data("deleteSchedule", (element) => {
    Swal.fire({
        icon: 'question',
        title: '確定要刪除嗎?',
        text: '若選擇刪除，資料將會消失',
        showCancelButton: true,
        cancelButtonText: '取消',
        confirmButtonText: '刪除',
    }).then((result) => {
        if(result.isConfirmed){
            element.submit()
        }
    })
})