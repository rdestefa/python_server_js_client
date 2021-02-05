console.log("Started new-user.js for TV database");

// Set up event handlers for each button
document.getElementById("submit-button").onmouseup = createUser;
document.getElementById("clear-button").onmouseup = clearForm;

function createUser() {
    console.log("Entered createUser()");
    document.getElementById("message_box").innerHTML = "";
    
    // Set up URL
    var url      = "http://localhost";
    var port     = 51080;
    var full_url = url + ":" + port + "/users/";
    
    // Get values from form
    var username   = document.getElementById("user_name").value;
    var name       = document.getElementById("name").value;
    var dob        = document.getElementById("date_of_birth").value;
    var email      = document.getElementById("email").value;
    var fav_shows  = document.getElementById("favorite_shows").value;
    var fav_genres = document.getElementById("favorite_genres").value;
    var watched    = document.getElementById("recently_watched").value;
    var best_day   = document.getElementById("best_day_to_watch").value;
    var ep_length  = document.getElementById("preferred_episode_length").value;
    
    // Set up request body
    var request_body = {};
    var forms_filled = true;
    
    if (username != "" && username != null) {
        request_body["id"] = username;
    } else {
        forms_filled = false;
    }
    if (name != "" && name != null) {
        request_body["name"] = name;
    } else {
        forms_filled = false;
    }
    if (dob != "" && dob != null) {
        request_body["dob"] = dob;
    } else {
        forms_filled = false;
    }
    if (email != "" && email != null) {
        request_body["email"] = email;
    } else {
        forms_filled = false;
    }
    if (fav_shows != "" && fav_shows != null) {
        if (fav_shows.includes(", ")) {
            shows_list = fav_shows.split(", ");
            request_body["favorite-shows"] = shows_list;
        } else if (fav_shows.includes(",")) {
            shows_list = fav_shows.split(",");
            request_body["favorite-shows"] = shows_list;
        } else {
            forms_filled = false;
        }
    } else {
        forms_filled = false;
    }
    if (fav_genres != "" && fav_genres != null) {
        if (fav_genres.includes(", ")) {
            genres_list = fav_genres.split(", ");
            request_body["favorite-genres"] = genres_list;
        } else if (fav_genres.includes(",")) {
            genres_list = fav_genres.split(",");
            request_body["favorite-genres"] = genres_list;
        } else {
            forms_filled = false;
        }
    } else {
        forms_filled = false;
    }
    if (watched != "" && watched != null) {
        request_body["recently-watched"] = watched;
    } else {
        forms_filled = false;
    }
    if (best_day != "" && best_day != null) {
        request_body["best-day-to-watch"] = best_day;
    } else {
        forms_filled = false;
    }
    if (ep_length != "" && ep_length != null) {
        request_body["preferred-episode-length"] = parseInt(ep_length);
    } else {
        forms_filled = false;
    }
    
    // Make POST request
    if (forms_filled == true) {
        var xhr = new XMLHttpRequest();
        xhr.open("POST", full_url, true);
        xhr.setRequestHeader("Content-Type", "application/json");
        xhr.send(JSON.stringify(request_body));
        
        // Handle response
        xhr.onload = function(e) {
            console.log(xhr.responseText);
            if (JSON.parse(xhr.responseText)["result"] == "success") {
                document.getElementById("message_box").innerHTML = "<h4 style='text-align:center;'>Welcome, " + username + "!</h4>";
                clearForm();   
            }
        }
        
        // Handle errors
        xhr.onerror = function(e) {
            console.error(xhr.statusText);
        }
    } else {
        document.getElementById("message_box").innerHTML = "<h4 style='text-align:center;'>Error creating new user. Ensure that all areas of the form are filled in and all lists are separated by commas.</h4>";
    }
    
    console.log("Exited createUser()");
}

function clearForm() {
    console.log("Entered clearForm()");
    
    document.getElementById("user_name").value = "";
    document.getElementById("name").value = "";
    document.getElementById("date_of_birth").value = "";
    document.getElementById("email").value = "";
    document.getElementById("favorite_shows").value = "";
    document.getElementById("favorite_genres").value = "";
    document.getElementById("recently_watched").value = "";
    document.getElementById("best_day_to_watch").value = "";
    document.getElementById("preferred_episode_length").value = "";
    
    console.log("Exited clearForm()");
}