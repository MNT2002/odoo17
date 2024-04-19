// const carouselItemList = document.querySelectorAll('.carousel-item.img-customize');
// console.log(carouselItemList)
// // Kiểm tra xem có ít nhất một phần tử được tìm thấy
// if (carouselItemList.length > 0) {
//     // Thêm lớp 'active' vào phần tử đầu tiên
//     carouselItemList[0].classList.add('active');
// } else {
//     console.error("Không tìm thấy phần tử carousel nào!");
// }


// customize code
let isDown = false;
let startX;
let scrollLeft;
const sliderList = document.querySelectorAll('.MS-content');
sliderList.forEach(slider => {
    slider.addEventListener('mousedown', startDrag);
    slider.addEventListener('touchstart', startDrag);

    function startDrag(e) {
        isDown = true;
        slider.classList.add('active');

        if (e.type === 'mousedown') {
            startX = e.pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        } else if (e.type === 'touchstart') {
            startX = e.touches[0].pageX - slider.offsetLeft;
            scrollLeft = slider.scrollLeft;
        }
    }

    slider.addEventListener('mouseleave', endDrag);
    slider.addEventListener('mouseup', endDrag);
    slider.addEventListener('touchend', endDrag);

    function endDrag(e) {
        isDown = false;
        slider.classList.remove('active');
        // console.log(e.target)
    }

    slider.addEventListener('mousemove', drag);
    slider.addEventListener('touchmove', drag);

    function drag(e) {
        if (!isDown) return;
        e.preventDefault();

        let x;
        if (e.type === 'mousemove') {
            x = e.pageX - slider.offsetLeft;
        } else if (e.type === 'touchmove') {
            x = e.touches[0].pageX - slider.offsetLeft;
        }

        const walk = (x - startX) * 1;
        slider.scrollLeft = scrollLeft - walk;
    }
})

