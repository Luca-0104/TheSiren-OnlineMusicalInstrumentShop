// the 'last' button
let BtnLeft = document.querySelector(".btn-left")
// the 'next' button
let BtnRight = document.querySelector(".btn-right")
// the whole picture list
let picContainer = document.querySelector(".pic-container")
// the number of the pictures of this product. (pictures in the list)
let picNum = document.querySelectorAll(".pic").length;

/*
*   First, we need to change the 'width' of ".pic-container" according to the number of picture.
*   For example, if there are 3 pictures, it should be 300%
*/
//get the width of picture-panel-box
console.log(picNum)
newWidth = (picNum * 100) + "%"
picContainer.style.width = newWidth

/*
    The index of the picture that is being shown in the slide panel.
    Range from 0 to picNum-1
 */
let index = 0

/**
 * This method is used to update the position of the picture list horizontally
 * by changing the attribute 'left' of '.pic-container' class in css file.
 */
function refreshPosition() {
    // drag the picture list to left by 'index' times of the picture width
    // (this is because, in the css file we have defined the width of each picture as 100%)
    picContainer.style.left = (index * -100) + "%"
}

/**
 * This method is used to update the current index
 * to the index of the "NEXT picture".
 * (Notice that we will play the pictures circularly)
 */
function goNext() {
    // if the current index has already reached the last picture, we will set it back to the first picture
    if (index >= picNum - 1) {
        index = 0
    } else {
        index++
    }
}

/**
 * This method is used to update the current index
 * to the index of the "LAST picture".
 * (Notice that we will play the pictures circularly)
 */
function goLast() {
    // if the current index has already reached the first picture, we will set it back to the last (final) one.
    if (index <= 0) {
        index = picNum - 1
    } else {
        index--
    }
}

/**
 * Set a click listener on the left button.
 * Every time clicking on the left button, we will go back to the last picture.
 */
BtnLeft.addEventListener("click", () => {
    // update the index
    goLast()
    // update the position of the picture list according to the new index
    refreshPosition()
});

/**
 * Set a click listener on the right button.
 * Every time clicking on the right button, we will go to the next picture.
 */
BtnRight.addEventListener("click", () => {
    // update the index
    goNext()
    // update the position of the picture list according to the new index
    refreshPosition()
});
