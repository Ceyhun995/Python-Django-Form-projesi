const elements = document.querySelectorAll('form input, textarea, select, input');

elements.forEach(element => {
  element.classList.add('form-control');
});
