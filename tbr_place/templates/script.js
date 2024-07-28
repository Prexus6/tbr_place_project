const selectBtn = document.querySelector(".QuickPromptSelectBtn");
const items = document.querySelectorAll(".item");
const selectBtnMyBooks = document.querySelector(".list-of-mybooks");
const mybooksList = document.querySelector(".mybooks-dynamic-list");

selectBtn.addEventListener("click", () => {
  selectBtn.classList.toggle("open");
});

items.forEach((item) => {
  item.addEventListener("click", () => {
    item.classList.toggle("checked");

    let checked = document.querySelectorAll(".checked");
    let btnText = document.querySelector(".btn-text");

    if (checked && checked.length > 0) {
      btnText.innerText = `${checked.length} selected`;
    } else {
      btnText.innerText = `Select prompt types:`;
    }
  });
});

selectBtnMyBooks.addEventListener("click", () => {
  selectBtnMyBooks.classList.toggle("open");
  mybooksList.classList.toggle("open");
});
