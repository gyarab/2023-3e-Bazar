function addRectangle() {
    var rectangle = document.createElement("div");
    rectangle.style.width = "400px";
    rectangle.style.height = "200px";
    rectangle.style.backgroundColor = "black";
    rectangle.style.margin = "200px";
    rectangle.style.float = "left";
    var textSpan = document.createElement("span");// Vytvořte text pro span
    textSpan.style.color = "white";// Vytvořte text pro span
    textSpan.textContent = " Lorem ipsum dolor sit amet consectetur adipisicing elit. ";// Vytvořte text pro span
    rectangle.appendChild(textSpan);
    document.body.appendChild(rectangle); //připojení
}
