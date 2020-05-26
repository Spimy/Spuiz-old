const toggleRead = (notification) => {

    const token = document.getElementsByTagName("input")[0].value;
    notification.classList.toggle("read");

    fetch(`${window.location.href}${notification.getAttribute("href")}/`, {
        method: "PUT",
        headers: {
            "X-CSRFToken": token,
            "X-Requested-With": "XMLHttpRequest"
        }
    });

}