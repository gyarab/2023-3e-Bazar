function addRectangle() {
    var rectangle = document.createElement("div");
    rectangle.style.width = "400px";
    rectangle.style.height = "200px";
    rectangle.style.backgroundColor = "black";
    rectangle.style.marginRight = "20px";  
    rectangle.style.marginTop = "20px"; 
    rectangle.style.float = "left";
    
    var textSpan = document.createElement("span");
    textSpan.style.color = "white";
    textSpan.textContent = " Lorem ipsum dolor sit amet consectetur adipisicing elit. ";
    
    rectangle.appendChild(textSpan);
    document.body.appendChild(rectangle);

    rectangle.addEventListener("click", function() {  // Open a new HTML page when the rectangle is clicked
        window.location.href = "#";
    });
}
