// Message Popup
function messageEvent(element, seconds) {

    const msg = document.getElementById(element);

    msg.className = "show";

    setTimeout(function() {
        msg.className = msg.className.replace("show", "");
    }, seconds*1000);

}