console.log("Started search.js for TV database");

// Add event listener for clear button
document.getElementById("clear-button").onmouseup = clearForm;

var name_check   = document.getElementById("name_check");
var genre_check  = document.getElementById("genre_check");
var rating_check = document.getElementById("rating_check");

// Add event listeners for all checkboxes
name_check.addEventListener("change", function() {toggleSearch("name");});
genre_check.addEventListener("change", function() {toggleSearch("genre");});
rating_check.addEventListener("change", function() {toggleSearch("rating");});

if (location.search.substring(1) == "name") {
    name_check.checked = true;
    toggleSearch("name");
} else if (location.search.substring(1) == "genre") {
    genre_check.checked = true;
    toggleSearch("genre");
} else if (location.search.substring(1) == "rating") {
    rating_check.checked = true;
    toggleSearch("rating");
} else if (location.search.substring(1) == "multiple") {
    ["name", "genre", "rating"].forEach(function(element, index, array) {
        document.getElementById(element + "_check").checked = true;
        toggleSearch(element);
    })
}

function toggleSearch(criteria) {
    console.log("Entered toggleSearch()");
    
    var search_div = document.getElementById(criteria + "_search");
    var check_box = document.getElementById(criteria + "_check");
        
    if (check_box.checked == true) {
        // Make label
        var search_lab = document.createElement("label");
        search_lab.setAttribute("for", "exampleInputAmount");
        search_lab.innerHTML = criteria.charAt(0).toUpperCase() + criteria.substring(1);
        search_div.appendChild(search_lab);

        // Make inner div
        var bar_div = document.createElement("div");
        bar_div.setAttribute("class", "input-group");

        // Make input bar
        var search_bar = document.createElement("input");
        search_bar.setAttribute("type", "text");
        search_bar.setAttribute("class", "form-control");
        search_bar.setAttribute("id", criteria + "_search_bar");
        bar_div.appendChild(search_bar);

        // Make right icon
        var icon_div = document.createElement("div");
        icon_div.setAttribute("class", "input-group-addon");
        var icon = document.createElement("button");
        icon.setAttribute("type", "button");
        icon.setAttribute("class", "btn btn-xs btn-primary");
        icon.setAttribute("id", criteria + "_search_button");
        icon.innerHTML = "Search";
        icon.onmouseup = search;
        icon_div.appendChild(icon);
        bar_div.appendChild(icon_div);
        search_div.appendChild(bar_div);
    } else {
        search_div.innerHTML = "";
    }
        
    console.log("Exited toggleSearch()");
}

function search() {
    console.log("Entered search()");
    
    var url  = "http://localhost";
    var port = 51080;
    
    makeTVCall(url, port, null);
    
    console.log("Exited search()");
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
        checkTVShows(JSON.parse(xhr.responseText)["tv-shows"]);
    }

    // Handle errors
    xhr.onerror = function(e) {
        console.error(xhr.statusText);
    }
    
    console.log("Exited makeTVCall()");
}

function checkTVShows(shows) {
    var show_box = document.getElementById("show_box");
    show_box.innerHTML = "";
    
    if (shows == null) {
        
    } else {
        // Search for matching items
        for (var i = 0; i < shows.length; i++) {
            var good = true;
            
            // Check if name matches
            if (name_check.checked == true) {
                var name_search = document.getElementById("name_search_bar").value.toLowerCase();
                
                if (!shows[i]["details"]["name"].toLowerCase().includes(name_search)) {
                    good = false;
                }
            }
            
            // Check if genre matches
            if (genre_check.checked == true) {
                var genre_search = document.getElementById("genre_search_bar").value.toLowerCase();
                var genre_ok = false;
                
                for (var j = 0; j < shows[i]["details"]["genres"].length; j++) {
                    if (shows[i]["details"]["genres"][j].toLowerCase().includes(genre_search)) {
                        genre_ok = true;
                    }
                }
                
                if (genre_ok == false) {
                    good = false;
                }
            }
            
            // Check if rating matches
            if (rating_check.checked == true) {
                var rating_search = parseFloat(document.getElementById("rating_search_bar").value);
                
                if (rating_search > shows[i]["rating"]) {
                    good = false;
                }
            }
            
            // If criteria are met, add the show to the list
            if (good == true) {
                // Create media div
                var show = document.createElement("div");
                show.setAttribute("class", "media");
                
                // Add show image
                if (shows[i]["summary"]["images"] != null) {
                    // Create link
                    var show_link = document.createElement("a");
                    show_link.setAttribute("href", "show.html?" + shows[i]["details"]["id"]);
                    show_link.setAttribute("class", "media-left");
                
                    // Add image
                    var show_left = document.createElement("div");
                    show_left.setAttribute("class", "media-left");
                    var show_img = document.createElement("img");
                    show_img.setAttribute("class", "media-object show_list");
                    show_img.setAttribute("src", shows[i]["summary"]["images"]["medium"]);
                    show_img.setAttribute("alt", shows[i]["details"]["name"]);
                    show_img.setAttribute("width", "160");
                    show_img.setAttribute("height", "225");
                    show_left.appendChild(show_img);
                    show_link.appendChild(show_left);
                    show.appendChild(show_link);
                }
                
                // Add show heading
                var show_body = document.createElement("div");
                show_body.setAttribute("class", "media-body");
                var show_heading = document.createElement("h4");
                show_heading.setAttribute("class", "media-heading");
                show_heading.innerHTML = shows[i]["details"]["name"];
                show_body.appendChild(show_heading);
                
                // Add show summary
                var show_summary = document.createElement("p");
                show_summary.innerHTML = shows[i]["summary"]["summary"];
                show_body.appendChild(show_summary);
                show.appendChild(show_body);
                show_box.appendChild(show);
            }
        }
    }
}

function clearForm() {
    if (name_check.checked) {
        document.getElementById("name_search_bar").value = "";
    }
    if (genre_check.checked) {
        document.getElementById("genre_search_bar").value = "";
    }
    if (rating_check.checked) {
        document.getElementById("rating_search_bar").value = "";
    }
}
