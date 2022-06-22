const inputs = document.querySelectorAll(".input")

const focando = ({target}) => {
  const span = target.previousElementSibling;
  span.classList.add("span-active");
}

const retirandoFoco = ({target}) => {
  const span = target.previousElementSibling;
  if (target.value === "") {
    span.classList.remove("span-active");
  }
}


inputs.forEach((input) => input.addEventListener("focus", focando));
inputs.forEach((input) => input.addEventListener("focusout", retirandoFoco));