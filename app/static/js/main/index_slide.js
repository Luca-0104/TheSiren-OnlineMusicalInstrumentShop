// a list of those 5 dots at the bottom of the picture
let dot = document.querySelectorAll(".dot")
// the whole picture list
let picContainer = document.querySelector(".pic-container")
// the text at right side of the slide pic
let slideText = document.getElementById('slide-text')
// initialize the text with the introduction of the first product
slideText.innerHTML = 'This is the introduction of the slide pic1'

/*
    The index of the picture that is being shown in the slide panel.
    Range from 0 to picNum-1
 */
let index = 0

// this is for calculating the time interval
let time

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
    if (index >= dot.length-1) {
        index = 0
    } else {
        index++
    }
}

/**
 * This function is used to refresh the introduction text as the changing
 * of the pictures in the slide window
 */
function refreshIntro(index){
    if (index === 0){
            slideText.innerHTML = 'This is the introduction of the slide pic1'

        }else if (index === 1){
            slideText.innerHTML = 'This is the introduction of the slide pic2'

        }else if (index === 2){
            slideText.innerHTML = 'This is the introduction of the slide pic3'

        }else if (index === 3){
            slideText.innerHTML = 'This is the introduction of the slide pic4'

        }else if (index === 4){
            slideText.innerHTML = 'This is the introduction of the slide pic5'

        }
}

/**
 * This function is used to refresh the link of the button
 * as the changing of the pictures in the left slide window.
 * The link of the button will be dynamically changed into the
 * detail page of the product, which is being shown in the slide window.
 */
function refreshButtonLink(index){

}

/**
 * increase the index by 1 every 5 seconds, which means go into next picture.
 */
function timer(){
    time = setInterval(() => {

        // we will go to the next picture every 5 seconds.
        // goNext() method can check whether should we go back to the first one.
        goNext()
        refreshPosition()

        /*
            When auto changing to the next picture,
            make only the current dot brighter, remove the 'current-dot' class
            from all the other dot elements
         */
        $(dot[index]).addClass('current-dot')
        $(dot[index]).prevAll().removeClass('current-dot')
        $(dot[index]).nextAll().removeClass('current-dot')

        // refresh the introduction text beside the slide window as the changing of slides
        refreshIntro(index);
        // refresh the link of the button
        refreshButtonLink(index);

    }, 5000)
}

/**
 * loop through the dot group, add click listener for
 * each dot to go to the correspond picture
 */
for (let i = 0; i < dot.length; i++) {
    dot[i].addEventListener("click", () => {
        index = i

        /*
            When manually changing to the next picture,
            make only the current dot brighter, remove the 'current-dot' class
            from all the other dot elements
         */
        $(dot[index]).addClass('current-dot')
        $(dot[index]).prevAll().removeClass('current-dot')
        $(dot[index]).nextAll().removeClass('current-dot')

        refreshPosition()

        // refresh the introduction text beside the slide window as the dots being clicked
        refreshIntro(index);
        // refresh the link of the button
        refreshButtonLink(index);

        // we should stop the timer and restart it again,
        // because if not, when we click on a dot button and go to the another picture,
        // the timer has been keeping going, therefore, the time for this new picture can less than the time we have set.
        clearInterval(time)
        timer()
    })
}

// Initially, we set the first dot as the current one.
$(dot[0]).addClass('current-dot')

// start the timer
timer()

