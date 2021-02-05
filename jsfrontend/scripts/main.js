console.log("Started main.js for TV database");

window.onload = loadImages;
    
function loadImages() {
    console.log("Entered loadImages()");
    
    var url  = "http://localhost";
    var port = 51080;
    
    makeTVCall(url, port, null);
    
    console.log("Exited loadImages()");
}

function makeTVCall(url, port, key) {
    console.log("Entered makeTVCall()");
    
    // Set up URL
    var full_url = url + ":" + port + "/tv-shows/";
    if (key != null) full_url += key;
    
    // Make request
    var xhr = new XMLHttpRequest();
    xhr.open("GET", full_url, true);
    xhr.send(null);
    
    // Handle response
    xhr.onload = function(e) {
        console.log(xhr.responseText.substring(0, 200));
        addImagesToPage(JSON.parse(xhr.responseText));
    }

    // Handle errors
    xhr.onerror = function(e) {
        console.error(xhr.statusText);
    }
    
    console.log("Exited makeTVCall()");
}

function addImagesToPage(response_json) {
    console.log("Entered addImagesToPage()");
    
    var shows_grid = document.getElementById("shows_list");
    for (var i = 0; i < response_json["tv-shows"].length; i++) {
        var img_url = response_json["tv-shows"][i]["summary"]["images"]["medium"];
        var title   = response_json["tv-shows"][i]["details"]["name"];
        var id      = response_json["tv-shows"][i]["details"]["id"];
        
        // Create link attribute
        var link = document.createElement("a");
        link.setAttribute("href", "pages/show.html?" + id);
        
        // Create image attribute
        var img = document.createElement("img");
        img.setAttribute("class", "nav_item");
        img.setAttribute("src", img_url);
        img.setAttribute("alt", title);
        
        link.appendChild(img);
        shows_grid.appendChild(link);
    }
    
    console.log("Exited addImagesToPage()");
}