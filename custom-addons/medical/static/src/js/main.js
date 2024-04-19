let moreInforBtn = document.querySelector('.more-infor_btn');
let content = document.querySelector('.content');
if (content) {
    content.style.height = "150px";

    moreInforBtn.addEventListener("click", (event) => {
        if (moreInforBtn.textContent == "Xem thêm") {
            content.style.height = "";
            moreInforBtn.textContent = "Ẩn bớt";
        } else {
            content.style.height = "150px";
            moreInforBtn.textContent = "Xem thêm";
        }
    });
}

