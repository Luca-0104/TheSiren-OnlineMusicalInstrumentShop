// a list of those 5 dots at the bottom of the picture
let dot = document.querySelectorAll(".dot")
// the whole picture list
let picContainer = document.querySelector(".pic-container")
// the text at right side of the slide pic (product intro)
let slideText = document.getElementById('slide-text')
// the text at right side of the slide pic (product name)
let slideProductName = document.getElementById("slide-product-name")
// the start browsing btn in the slide window
let slideBtn = document.getElementById("slide-start-browsing")

/*
    initialize the first slide (product name + intro + btn)
 */
slideText.innerHTML = 'Solid Korina Body and Long Neck Tenon. Brazilian Rosewood Fingerboard. Hand Lacquered and Aged by the Artisan. Custom Wound “Retrophonic’Humbucker Pickup. Tune-O-Matic Bridge with 1.5" Brass Studs.  50s Wiring with Master Volume and Master Tone. Custom Bumblebee Capacitors. Custom Dogear Pickup Rings.';
slideProductName.innerHTML = "Gibson THE LEO SCALA SUPER '58 FLYING Vs";
slideBtn.href = "/product-details/1";


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
            slideText.innerHTML = 'Solid Korina Body and Long Neck Tenon. Brazilian Rosewood Fingerboard. Hand Lacquered and Aged by the Artisan. Custom Wound “Retrophonic’Humbucker Pickup. Tune-O-Matic Bridge with 1.5" Brass Studs.  50s Wiring with Master Volume and Master Tone. Custom Bumblebee Capacitors. Custom Dogear Pickup Rings.'

        }else if (index === 1){
            slideText.innerHTML = 'Since its release in 1981, the workhorse SD-1 Super Overdrive has been the core gain pedal for generations of players across every musical genre. Based around the revolutionary asymmetrical clipping circuit from the OD-1 Overdrive—one of the three original BOSS compact pedals from 1977—the SD-1 delivers rich, smooth, and highly musical overdrive tones that continue to inspire guitarists everywhere.'

        }else if (index === 2){
            slideText.innerHTML = 'The GL-10 was first introduced back in 2018 and embodies the classic Lowden character, drawing from over 40 years of guitar making heritage to invite the player to explore new tonal possibilities that await.'

        }else if (index === 3){
            slideText.innerHTML = 'The mid-level TD-27KV delivers the immersive sound and response that you only get with V-Drums. At its heart is the powerful new TD-27 sound engine, filled with premium-grade, fully-customizable drum and cymbal sounds. Advanced digital trigger technology detects every playing nuance in ultra-high definition, while large-diameter drum and cymbal pads offer exceptional feel, presented in a spacious acoustic-style layout.'

        }else if (index === 4){
            slideText.innerHTML = 'The latest in our long line of professional MIDI controllers, the Roland A-88MKII is supremely playable, with onboard creative tools for today\'s musicians and producers. Our acclaimed hammer-action keyboard and built-to-last quality combine with modern features like USB-C connectivity, RGB-lit controls, and MIDI 2.0 (coming soon) for the best performance in its class.'

        }
}

/**
 * This function is used to refresh the link of the button
 * as the changing of the pictures in the left slide window.
 * The link of the button will be dynamically changed into the
 * detail page of the product, which is being shown in the slide window.
 */
function refreshButtonLink(index){
        if (index === 0){
            slideBtn.href = "/product-details/1";

        }else if (index === 1){
            slideBtn.href = "/product-details/4";

        }else if (index === 2){
            slideBtn.href = "/product-details/6";

        }else if (index === 3){
            slideBtn.href = "/product-details/9";

        }else if (index === 4){
            slideBtn.href = "/product-details/10";

        }
}

/**
 * THis function refresh the product name on the slide window
 * @param index
 */
function refresh_product_name(index){
        if (index === 0){
            slideProductName.innerHTML = "Gibson THE LEO SCALA SUPER '58 FLYING Vs"

        }else if (index === 1){
            slideProductName.innerHTML = "BOSS’s Legendary Super Overdrive Sound Effectors"

        }else if (index === 2){
            slideProductName.innerHTML = "Lowden GL10 Guitar"

        }else if (index === 3){
            slideProductName.innerHTML = "Roland TD-27KV V-Drums"

        }else if (index === 4){
            slideProductName.innerHTML = "Roland A-88MKII MIDI Keyboard Controller"

        }
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

        // refresh the product name
        refresh_product_name(index)
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

        // refresh the product name
        refresh_product_name(index)
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

