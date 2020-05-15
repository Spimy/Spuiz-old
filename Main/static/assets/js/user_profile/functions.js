const loadCSS = (filename) => {

    const file = document.createElement("link");
    file.setAttribute("rel", "stylesheet");
    file.setAttribute("type", "text/css");
    file.setAttribute("href", filename);

    document.head.append(file);

}