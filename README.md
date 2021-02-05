# CSE 30332 Final Project

### Contributors

- Ryan DeStefano (rdestefa)
- Conor Holahan &nbsp;(cholahan)

All code was written together in person due to Zoom fatigue, so all commits were made from the same account.

---

### Libraries / Packages and Back End Testing

- Python Libraries Used (&#9733; - Required to run server, &#9734; - Required to test the server):
    - <a href="https://cherrypy.org/" target="_blank"><code>cherrypy</code></a> &#9733;
    - <a href="https://docs.python.org/3/library/sys.html" target="_blank"><code>sys</code></a> &#9733;
    - <a href="https://docs.python.org/3/library/json.html" target="_blank"><code>json</code></a> &#9733;
    - <a href="https://docs.python.org/3/library/unittest.html" target="_blank"><code>unittest</code></a> &#9734;
    - <a href="https://requests.readthedocs.io/en/master/" target="_blank"><code>requests</code></a> &#9734;
- HTML / CSS / JavaScript
    - No libraries or packages need to be installed. Only pure HTML, CSS, and JavaScript were used.
- Makefile / Testing
    - [Installing GNU Make](https://www.gnu.org/software/make/)
    - To run test scripts, ensure the server is running, then run one of these `make` commands from the directory containing `Makefile`:
        - `make` - Runs all test scripts simultaneously
        - `make test` - Runs all test scripts simultaneously
        - `make test-separate` - Runs each test script individually one after another
        - `make test-library` - Runs tests for the OOAPI
        - `make test-tv` - Runs tests for the TV shows controller
        - `make test-users` - Runs both test scripts for the users controller
        - `make test-users-key` - Runs tests for the users controller `KEY` event handlers
        - `make test-users-index` - Runs tests for the users controller `INDEX` event handlers
        - `make test-reset` - Runs tests for the reset controller
        - `make clean` - Empties and removes all `__pycache__` folders from the project

---

### File Tree

<pre>
final_project
\_ jsfrontend
   \_ pages
      \_ new-user.html
      \_ search.html
      \_ show.html
      \_ user.html
   \_ scripts
      \_ main.js
      \_ new-user.js
      \_ search.js
      \_ show.js
      \_ user.js
   \_ css
      \_ main.css
   \_ index.html
\_ ooapi
   \_ test
      \_ test_tv_library.py
   \_ tv_library.py
   \_ tv-shows.json
   \_ user.json
\_ server
   \_ test
      \_ test_reset_endpoint.py
      \_ test_tv_shows.py
      \_ test_users_index.py
      \_ test_users_key.py
   \_ ResetController.py
   \_ TVController.py
   \_ UsersController.py
   \_ server.py
\_ Makefile
\_ index.html
</pre>

---

### Running the Server

- Ensure all packages described above are installed
- Ensure the project has the folder structure described above
- Navigate to the `server` folder
- Execute `python3 server.py` at the command line or run `server.py` from your preferred IDE

---

### OO API Functions

- TV Shows Controller
    - `GET_KEY` - Returns a JSON string of a specific TV show
    - `GET_INDEX` - Returns a JSON string of all TV shows in the database
- Users Controller
    - `GET_KEY` - Returns a JSON string of a specific user
    - `PUT_KEY` - Reads a request body to modify the details of a specific user
    - `DELETE_KEY` - Deletes a specific user from the database
    - `GET_INDEX` - Returns a JSON string of all users in the database
    - `POST_INDEX` - Reads a request body to add a new user to the database
    - `DELETE_INDEX` - Deletes all users from the database
- Reset Controller
    - `PUT_KEY_TV` - Resets a specific TV show in the database
    - `PUT_KEY_USER` - Resets a specific user in the database
    - `PUT_INDEX` - Resets all TV shows and users in the database

---

### JSON Specification

| **Request Type** | **Resource Endpoint**       | **Body**                                                                                                                         | **Expected Response**                                                                                                   | **Inner Working of Handler**                                                                                                   |
|------------------|-----------------------------|----------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------|
| `GET`            | /tv-shows/                  | No body                                                                                                                          | String formatted JSON with all TV shows                                                                                 | `GET_INDEX`<br>Goes through all TV shows and gets all their information to put in a list                                       |
| `GET`            | /tv-shows/south-park        | No body                                                                                                                          | String formatted JSON with just South Park                                                                              | `GET_KEY`<br>Searches for a specific show's data and returns it as a dictionary                                                |
| `GET`            | /users/                     | No body                                                                                                                          | String formatted JSON with all users                                                                                    | `GET_INDEX`<br>Returns a dictionary of all users in the database                                                               |
| `GET`            | /users/ryan-destefano       | No body                                                                                                                          | String formatted JSON with just ryan-destefano                                                                          | `GET_KEY`<br>Searches for a specific user's data and returns it as a dictionary                                                |
| `PUT`            | /users/ryan-destefano       | JSON body with specific attributes to be changed. Example:<br>`{"email": "rdestefa@gmail.com",`<br>`"name": "Ryan F DeStefano"}` | `{"result": "success",`<br>`"attributes": {`<br>`"email": "Changed",`<br>`"name": "Changed"}}`<br>if the request worked | `PUT_KEY`<br>Reads in each attribute, and if it belongs in the list of possible attributes, updates a specific user            |
| `POST`           | /users/                     | JSON body with all new user attributes                                                                                           | `{"result": "success",`<br>`"id": "ryan-destefano"}`<br>if the request worked                                           | `POST_INDEX`<br>Reads in the body of the request, and if it contains all necessary attributes, adds a new user to the database |
| `DELETE`         | /users/                     | Empty JSON body                                                                                                                  | `{"result": "success"}`<br>if the request worked                                                                        | `DELETE_INDEX`<br>Clears entire dictionary of users from the database                                                          |
| `DELETE`         | /users/ryan-destefano       | Empty JSON body                                                                                                                  | `{"result": "success"}`<br>if the request worked                                                                        | `DELETE_KEY`<br>Deletes a specific key-value pair from the users dictionary in the database based on user ID                   |
| `PUT`            | /reset/                     | Empty JSON body                                                                                                                  | `{"result": "success"}`<br>if the request worked                                                                        | `RESET_INDEX`<br>Reloads all TV shows and users from `tv-shows.json` and `users.json`, respectively                            |
| `PUT`            | /reset/tv-shows/south-park  | Empty JSON body                                                                                                                  | `{"result": "success"}`<br>if the request worked                                                                        | `RESET_KEY_TV`<br>Reloads a specific TV show from `tv-shows.json`                                                              |
| `PUT`            | /reset/users/ryan-destefano | Empty JSON body                                                                                                                  | `{"result": "success"}`<br>if the request worked                                                                        | `RESET_KEY_USER`<br>Reloads a specific user from `users.json`                                                                  |

---

### User Interaction

- Home Page
    - Large jumbotron spans the width of the screen at the top of the page
    - All preview images of TV shows in the database are loaded and displayed on a CSS grid
        - Information is loaded through a `GET` request to the `/tv-shows/` endpoint
    - Users can hover over and click on each show to go to a page to learn more about it
- Shows Page
    - More detailed information about a show will be displayed to the user
        - The show is determined by the query string in the URL
        - Information is loaded through a `GET` request to the `/tv-shows/tvid` endpoint
    - A link to the show's official website (if it exists) will be present
    - The user can choose to hide or show a complete list of episodes with descriptions
- Search Page
    - Users can search for specific TV shows based on name, rating, genre, or any combination of the three
        - The user can select which criteria to search for by checking and unchecking each box
    - All matching shows will be displayed below the search bar(s)
        - Information is loaded through a `GET` request to the `/tv-shows/` endpoint
        - The client will then filter the shows based on the search criteria
    - Users can hover over and click on each matching show to go to a page to learn more about it
- Users Page
    - Users can type in their usernames to carry out a number of tasks:
        - Display information specific to the user
        - Update current information with new preferences
        - Delete the user from the database completely
        - Reset the user to their initial preferences
    - These tasks are carried out through a `GET`, `PUT`, or `DELETE` request to either the `/users/uid` or `/reset/users/uid` endpoints
- New User Page
    - Users can enter all necessary information to create an entirely new profile
    - Once the user enters their information, they can register a new account within the database
        - This is accomplished through a `POST` request to the `/users/` endpoint
- Navigation Bar
    - A navigation bar is present at the top of every page with links to the other pages in the client

---

### Front End Testing

- In order to test each aspect of the front end, the following tasks were carried out:
    - Each link was tested to make sure they functioned properly
    - All pages that interact with the server were tested in their entirety
        - All `GET`, `PUT`, `POST`, and `DELETE` requests made by the front end for both TV shows and users were verified to work
    - All buttons and forms were tested and verified to work properly
- Server must be running for any tests to work

---

### Complexity

- Scale
    - Can be used to store as many TV shows / users as one would need (as long as internal storage permits)
    - Could be updated to let users write to the data files that the server draws from in order to add data permanently
    - More functionality could easily be added in the future such as letting users contribute to the TV shows database
    - Could easily be adapted to store objects besides TV shows
- Complexity
    - The project was fairly complex as it has 5 different pages that change based on the show or user
    - Uses the CherryPy Python library for the back end to handle requests made by the JavaScript front end
    - Only pure JavaScript was used in addition to some basic CSS
    - Bootstrap templates were used for each page to make them look more aesthetically pleasing
    - The front end builds each page differently depending on the information it receives and adjusts depending on the requests made

---

### Demonstration

- [Code Walkthrough Video](http://youtube.com/watch?v=3ldkjBpdGzQ)
- [UI Demonstration Video](https://www.youtube.com/watch?v=ues5eVBaFSY&t=3s)
- [Presentation Slides](https://gitlab.com/rdestefa/final_project/-/blob/master/presentation_slides.pdf)