console.log("Started show.js for TV database");

window.onload = loadShow;

function loadShow() {
    console.log("Entered loadShow()");
    
    var url  = "http://localhost";
    var port = 51080;
    var key  = location.search.substring(1);
    
    makeTVCall(url, port, key);
    
    console.log("Exited loadShow()");
}

function makeTVCall(url, port, key) {
    console.log("Entered makeTVCall()");
    
    // Set up URL
    var full_url = url + ":" + port + "/tv-shows/" + key;
    
    // Make request
    var xhr = new XMLHttpRequest();
    xhr.open("GET", full_url, true);
    xhr.send(null);
    
    // Handle response
    xhr.onload = function(e) {
        console.log(xhr.responseText);
        addShowToPage(JSON.parse(xhr.responseText));
    }
    
    // Handle errors
    xhr.onerror = function(e) {
        console.error(xhr.statusText);
    }
    
    console.log("Exited makeTVCall()");
}

function addShowToPage(response_json) {
    console.log("Entered addShowToPage()");
    
    var show_box = document.getElementById("show_box");
    var id       = location.search.substring(1);
    var show     = response_json[id];
    
    // Create heading
    var title = document.createElement("h1");
    var text  = document.createTextNode(show["details"]["name"]);
    title.appendChild(text);
    title.setAttribute("style", "text-align:center;");
    show_box.appendChild(title);
    
    // Create image attribute
    var img = document.createElement("img");
    img.setAttribute("class", "center");
    img.setAttribute("src", show["summary"]["images"]["regular"]);
    img.setAttribute("alt", show["details"]["name"]);
    show_box.appendChild(img);
    
    // Add summary
    var line_break = document.createElement("br");
    var summary = document.createElement("p");
    summary.innerHTML = show["summary"]["summary"];
    show_box.appendChild(line_break);
    show_box.appendChild(summary);
    
    // Add genres
    var genres    = document.createElement("h4");
    var bold      = document.createElement("strong");
    var bold_text = document.createTextNode("Genre(s): ");
    bold.appendChild(bold_text);
    genres.appendChild(bold);
    var genres_str = "";
    for (var i = 0; i < show["details"]["genres"].length; i++) {
        if (i == show["details"]["genres"].length - 1) {
            genres_str += show["details"]["genres"][i];
        } else {
            genres_str += show["details"]["genres"][i] + ", ";
        }
    }
    var reg_text = document.createTextNode(genres_str);
    genres.appendChild(reg_text);
    show_box.appendChild(genres);
    
    // Add rating
    if (show["rating"] != null) {
        var rating    = document.createElement("h4");
        var bold      = document.createElement("strong");
        var bold_text = document.createTextNode("Rating: ");
        bold.appendChild(bold_text);
        rating.appendChild(bold);
        var reg_text = document.createTextNode(show["rating"]);
        rating.appendChild(reg_text);
        show_box.appendChild(rating);
    }
    
    // Add network
    var network   = document.createElement("h4");
    var bold      = document.createElement("strong");
    var bold_text = document.createTextNode("Network: ");
    bold.appendChild(bold_text);
    network.appendChild(bold);
    var reg_text = document.createTextNode(show["details"]["network"]);
    network.appendChild(reg_text);
    show_box.appendChild(network);
    
    // Add status
    var status    = document.createElement("h4");
    var bold      = document.createElement("strong");
    var bold_text = document.createTextNode("Status: ");
    bold.appendChild(bold_text);
    status.appendChild(bold);
    if (show["details"]["status"] == "Ended") {
        var status_str = "Ended";
    } else {
        var status_str = "Airing";
    }
    var reg_text = document.createTextNode(status_str);
    status.appendChild(reg_text);
    show_box.appendChild(status);
    
    // Add episode length
    if (show["details"]["episode-length"] != null) {
        var episode_length = document.createElement("h4");
        var bold           = document.createElement("strong");
        var bold_text      = document.createTextNode("Episode Length: ");
        bold.appendChild(bold_text);
        episode_length.appendChild(bold);
        var episode_str = show["details"]["episode-length"] + " minutes (" + show["episodes"].length + " episodes)";
        var reg_text = document.createTextNode(episode_str);
        episode_length.appendChild(reg_text);
        show_box.appendChild(episode_length);
    }
    
    // Create website link
    if (show["summary"]["website"] != null) {
        var website   = document.createElement("h4");
        var bold      = document.createElement("strong");
        var bold_text = document.createTextNode("Website: ");
        bold.appendChild(bold_text);
        website.appendChild(bold);
        var link = document.createElement("a");
        link.setAttribute("href", show["summary"]["website"]);
        var reg_text = document.createTextNode(show["details"]["name"]);
        link.appendChild(reg_text);
        website.appendChild(link);
        show_box.appendChild(website);
    }
    
    // Create episodes button
    var button = document.createElement("button");
    button.setAttribute("type", "button");
    button.setAttribute("id", "episodes_button");
    button.setAttribute("class", "btn btn-primary push-down-2");
    button.innerHTML = "Show Episodes";
    show_box.append(button);
    document.getElementById("episodes_button").onmouseup = toggleEpisodes;
    
    // Create list of episodes
    addEpisodes(show);
     
    console.log("Exited addShowToPage()");
}

function addEpisodes(show) {
    console.log("Entered addEpisodes()");
    
    var episode_box = document.getElementById("episode_box");
    for (var i = 0; i < show["episodes"].length; i++) {
        var episode = document.createElement("div");
        episode.setAttribute("class", "media");
        
        // Add episode image
        if (show["episodes"][i]["image"] != null) {
            var episode_left = document.createElement("div");
            episode_left.setAttribute("class", "media-left");
            var episode_img = document.createElement("img");
            episode_img.setAttribute("class", "media-object");
            episode_img.setAttribute("src", show["episodes"][i]["image"]["medium"]);
            var alt_str = "Season " + show["episodes"][i]["season"] + ", Episode " + show["episodes"][i]["number"];
            episode_img.setAttribute("alt", alt_str);
            episode_img.setAttribute("width", "250");
            episode_img.setAttribute("height", "140");
            episode_left.appendChild(episode_img);
            episode.appendChild(episode_left);
        }
        
        // Add episode heading
        var episode_body = document.createElement("div");
        episode_body.setAttribute("class", "media-body");
        var episode_heading = document.createElement("h4");
        episode_heading.setAttribute("class", "media-heading");
        episode_heading.innerHTML = "<b>(S" + show["episodes"][i]["season"] + " E" + show["episodes"][i]["number"] + ")</b> " + show["episodes"][i]["name"];
        episode_body.appendChild(episode_heading);
        
        // Add episode summary
        var episode_summary = document.createElement("p");
        episode_summary.innerHTML = show["episodes"][i]["summary"];
        episode_body.appendChild(episode_summary);
        episode.appendChild(episode_body);
        
        episode_box.appendChild(episode);
    }
    
    console.log("Exited addEpisodes()");
}

function toggleEpisodes() {
    console.log("Entered toggleEpisodes()");
    
    var episodes = document.getElementById("episode_box");
    var button   = document.getElementById("episodes_button");
    
    if (episodes.style.display == "none") {
        button.innerHTML = "Hide Episodes";
        episodes.style.display = "block";
    } else {
        button.innerHTML = "Show Episodes";
        episodes.style.display = "none";
    }
    
    console.log("Exited toggleEpisodes()");
}