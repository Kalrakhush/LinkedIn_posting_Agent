// Custom JavaScript for any interactive behavior or animations
document.addEventListener("DOMContentLoaded", function () {
    // Example: Animate form fields on focus
    const inputs = document.querySelectorAll("input, textarea");
    inputs.forEach((input) => {
      input.addEventListener("focus", function () {
        this.classList.add("animate__animated", "animate__pulse");
      });
      input.addEventListener("blur", function () {
        this.classList.remove("animate__animated", "animate__pulse");
      });
    });
  });
  