import Swal from "sweetalert2"

const Toast = Swal.mixin({
  toast: true,
  position: "top",
  showConfirmButton: false,
  timer: 3000,
  didOpen: (toast) => {
    toast.onmouseenter = Swal.stopTimer
    toast.onmouseleave = Swal.resumeTimer
  },
  html: '<button id="close-toast" class="swal2-close w-0 h-0" style="display: block; background-color: transparent; border: none; position: absolute; top: 0; right: 0; font-size: 20px; transform: translate(-50%, -50%);">&#x2715;</button>',
  didRender: (toast) => {
    const closeButton = toast.querySelector("#close-toast")
    closeButton.addEventListener("click", () => {
      Swal.close()
    })
  },
})

export default Toast
