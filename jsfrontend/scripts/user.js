console.log("Started user.js for TV database");

// Set up event handlers for each button
document.getElementById("user_search_button").onmouseup = search;
document.getElementById("user_update_button").onmouseup = update;
document.getElementById("user_reset_button").onmouseup  = reset;
document.getElementById("user_delete_button").onmouseup = deleteUser;

function search() {
    console.log("Entered search()");
    
    var url  = "http://localhost";
    var port = 51080;
    var key  = document.getElementById("user_input").value;
    
    makeUserCall(url, port, key);
    
    console.log("Exited search()");
}

function makeUserCall(url, port, key) {
    console.log("Entered makeUserCall()");
    
    // Set up URL
    var full_url = url + ":" + port + "/users/";
    if (key != null) full_url += key;
    
    // Make GET request
    var xhr = new XMLHttpRequest();
    xhr.open("GET", full_url, true);
    xhr.send(null);
    
    // Handle response
    xhr.onload = function(e) {
        console.log(xhr.responseText);
        displayUserInfo(JSON.parse(xhr.responseText)[key]);
    }
    
    // Handle errors
    xhr.onerror = function(e) {
        console.error(xhr.statusText);
    }
    
    console.log("Exited makeUserCall()");
}

function displayUserInfo(user) {
    console.log("Entered displayUserInfo()");
    
    var user_box = document.getElementById("user_box");
    user_box.innerHTML = "";
    
    // Add user name
    if (user["id"] != null) {
        var id        = document.createElement("h4");
        var bold      = document.createElement("strong");
        var bold_text = document.createTextNode("User ID: ");
        bold.appendChild(bold_text);
        id.appendChild(bold);
        var reg_text = document.createTextNode(user["id"]);
        id.appendChild(reg_text);
        user_box.appendChild(id);
    }
    
    // Add name
    if (user["name"] != null) {
        var name      = document.createElement("h4");
        var bold      = document.createElement("strong");
        var bold_text = document.createTextNode("Name: ");
        bold.appendChild(bold_text);
        name.appendChild(bold);
        var reg_text = document.createTextNode(user["name"]);
        name.appendChild(reg_text);
        
        addForm("name", name);
    }
    
    // Add favorite genres
    var genres    = document.createElement("h4");
    var bold      = document.createElement("strong");
    var bold_text = document.createTextNode("Favorite Genre(s): ");
    bold.appendChild(bold_text);
    genres.appendChild(bold);
    var genres_str = "";
    for (var i = 0; i < user["favorite-genres"].length; i++) {
        if (i == user["favorite-genres"].length - 1) {
            genres_str += user["favorite-genres"][i];
        } else {
            genres_str += user["favorite-genres"][i] + ", ";
        }
    }
    var reg_text = document.createTextNode(genres_str);
    genres.appendChild(reg_text);
    addForm("genres", genres);
    
    // Add preferred episode length
    if (user["preferred-episode-length"] != null) {
        var ep_length = document.createElement("h4");
        var bold      = document.createElement("strong");
        var bold_text = document.createTextNode("Preferred Episode Length: ");
        bold.appendChild(bold_text);
        ep_length.appendChild(bold);
        var reg_text = document.createTextNode(user["preferred-episode-length"]);
        ep_length.appendChild(reg_text);
        
        addForm("ep_length", ep_length);
    }
    
    // Add best day to watch
    if (user["best-day-to-watch"] != null) {
        var best_day  = document.createElement("h4");
        var bold      = document.createElement("strong");
        var bold_text = document.createTextNode("Best Day To Watch: ");
        bold.appendChild(bold_text);
        best_day.appendChild(bold);
        var reg_text = document.createTextNode(user["best-day-to-watch"].charAt(0).toUpperCase() + user["best-day-to-watch"].substring(1));
        best_day.appendChild(reg_text);
        
        addForm("best_day", best_day);
    }
    
    // Add recently watched
    if (user["recently-watched"] != null) {
        var watched   = document.createElement("h4");
        var bold      = document.createElement("strong");
        var bold_text = document.createTextNode("Recently Watched: ");
        bold.appendChild(bold_text);
        watched.appendChild(bold);
        var reg_text = document.createTextNode(user["recently-watched"]);
        watched.appendChild(reg_text);
        
        addForm("watched", watched);
    }
    
    // Add favorite shows
    fav_shows = document.createElement("h4");
    var bold      = document.createElement("strong");
    var bold_text = document.createTextNode("Favorite Show(s): ");
    bold.appendChild(bold_text);
    fav_shows.appendChild(bold);
    for (var i = 0; i < user["favorite-shows"].length; i++) {
        makeTVCall("http://localhost", 51080, user["favorite-shows"][i]);   
    }
    user_box.appendChild(fav_shows);
    
    console.log("Exited displayUserInfo()");
}

function addForm(detail, element) {
    var input = document.createElement("form");
    input.setAttribute("class", "bsr-form ");
    input.setAttribute("action", "");
    var outer_div = document.createElement("div");
    outer_div.setAttribute("class", "form-group");
    var inner_div = document.createElement("div");
    inner_div.setAttribute("class", "input-group");
    var inner_input = document.createElement("input");
    inner_input.setAttribute("type", "text");
    inner_input.setAttribute("class", "form-control");
    inner_input.setAttribute("id", detail + "_input");
    inner_input.setAttribute("placeholder", "Update Info");
    inner_div.appendChild(inner_input);
    outer_div.appendChild(inner_div);
    input.appendChild(outer_div);
    element.appendChild(input);
    
    document.getElementById("user_box").appendChild(element);
}

function makeTVCall(url, port, key) {
    console.log("Entered makeTVCall()");
    
    // Set up URL
    var full_url = url + ":" + port + "/tv-shows/";
    if (key != null) full_url += key;
    
    // Make GET request
    var xhr = new XMLHttpRequest();
    xhr.open("GET", full_url, true);
    xhr.send(null);
    
    // Handle response
    xhr.onload = function(e) {
        console.log(xhr.responseText.substring(0, 200));
        addShow(JSON.parse(xhr.responseText)[key]);
    }
    
    // Handle errors
    xhr.onerror = function(e) {
        console.error(xhr.statusText);
    }    
    
    console.log("Exited makeTVCall()");
}

function addShow(tv_show) {
    console.log("Entered addShow()");
    
    // Create media div
    var show = document.createElement("div");
    show.setAttribute("class", "media");

    // Add show image
    if (tv_show["summary"]["images"] != null) {
        // Create link
        var show_link = document.createElement("a");
        show_link.setAttribute("href", "show.html?" + tv_show["details"]["id"]);
        show_link.setAttribute("class", "media-left");

        // Add image
        var show_left = document.createElement("div");
        show_left.setAttribute("class", "media-left");
        var show_img = document.createElement("img");
        show_img.setAttribute("class", "media-object show_list");
        show_img.setAttribute("src", tv_show["summary"]["images"]["medium"]);
        show_img.setAttribute("alt", tv_show["details"]["name"]);
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
    show_heading.innerHTML = tv_show["details"]["name"];
    show_body.appendChild(show_heading);

    // Add show summary
    var show_summary = document.createElement("h5");
    show_summary.innerHTML = tv_show["summary"]["summary"];
    show_body.appendChild(show_summary);
    show.appendChild(show_body);
    fav_shows.appendChild(show);
    
    console.log("Exited addShow()");
}

function update() {
    console.log("Entered update()");
    
    var user = document.getElementById("user_input").value;
    var request_body = {};
    
    var name      = document.getElementById("name_input").value;
    var genres    = document.getElementById("genres_input").value;
    var ep_length = document.getElementById("ep_length_input").value;
    var best_day  = document.getElementById("best_day_input").value;
    var watched   = document.getElementById("watched_input").value;
    
    // Set up request body
    if (name != "" && name != null) {
        request_body["name"] = name;
    }
    if (genres != "" && genres != null) {
        if (genres.includes(", ")) {
            genres_list = genres.split(", ");
            request_body["favorite-genres"] = genres_list;
        } else if (genres.includes(",")) {
            genres_list = genres.split(",");
            request_body["favorite-genres"] = genres_list;
        }
    }
    if (ep_length != "" && ep_length != null) {
        request_body["preferred-episode-length"] = parseInt(ep_length);
    }
    if (best_day != "" && best_day != null) {
        request_body["best-day-to-watch"] = best_day.toLowerCase();
    }
    if (watched != "" && watched != null) {
        request_body["recently-watched"] = watched;
    }
    
    // Set up URL
    var url      = "http://localhost";
    var port     = 51080;
    var full_url = url + ":" + port + "/users/" + user;
    
    // Make PUT request
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", full_url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(request_body));
    
    // Handle response
    xhr.onload = function(e) {
        console.log(xhr.responseText);
        makeUserCall(url, port, user);
    }
    
    // Handle errors
    xhr.onerror = function(e) {
        console.error(xhr.statusText);
    }
    
    console.log("Exited update()");
}

function clearForm() {
    console.log("Entered clearForm()");
    
    document.getElementById("name_input").value = "";
    document.getElementById("genres_input").value = "";
    document.getElementById("ep_length_input").value = "";
    document.getElementById("best_day_input").value = "";
    document.getElementById("watched_input").value = "";
    
    console.log("Exited clearForm()");
}

function reset() {
    console.log("Entered reset()");
    
    var user = document.getElementById("user_input").value;
    var request_body = {};
    
    // Set up URL
    var full_url = "http://localhost:51080/reset/users/" + user;
    
    // Make PUT request
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", full_url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(request_body));
    
    // Handle response
    xhr.onload = function(e) {
        console.log(xhr.responseText);
        document.getElementById("user_box").innerHTML = "<h4 style='text-align:center;'>" + user + " has been reset to its original state.</h4>";
    }
    
    // Handle errors
    xhr.onerror = function(e) {
        console.error(xhr.statusText);
    }
    
    console.log("Exited reset()");
}

function deleteUser() {
    console.log("Entered deleteUser()");
    
    var user = document.getElementById("user_input").value;
    var request_body = {};
    
    // Set up URL
    var full_url = "http://localhost:51080/users/" + user;
    
    // Make PUT request
    var xhr = new XMLHttpRequest();
    xhr.open("DELETE", full_url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(request_body));
    
    // Handle response
    xhr.onload = function(e) {
        console.log(xhr.responseText);
        document.getElementById("user_box").innerHTML = "<h4 style='text-align:center;'>" + user + " has been deleted from the database.</h4>";
    }
    
    // Handle errors
    xhr.onerror = function(e) {
        console.error(xhr.statusText);
    }
    
    console.log("Exited deleteUser()");
}
