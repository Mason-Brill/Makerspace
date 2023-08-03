/*
* userSpecificElements.js
*
* this function shows the appropriate links/buttons depending on the privilege level of the user
*
* REFERENCES
* https://stackoverflow.com/questions/21432193/how-to-get-the-ids-of-all-elements-of-a-particular-class
* https://stackoverflow.com/questions/15318357/show-hide-image-with-javascript
*/

// shows appropriate links/buttons depending on the privilege level of the user
function showUserSpecificElements() {
    var level = document.cookie.split("=");
    console.log("cookies: ", level);
    // show buttons to send emergency text or submit equipment reservation
    if (level[1] === "student" || level[1] === "worker" || level[1] === "administrator"){
        console.log("user is level")
        document.getElementById("emergency").style.display = "block";
        document.getElementById("reservation").style.display = "block";
    } else {
        console.log("user is level")
        document.getElementById("emergency").style.display = "none";
        document.getElementById("reservation").style.display = "none";
    }

    // show button to start makerspace shift but only on the index page
    if (window.location.pathname === "/" || window.location.pathname === "/login") {
        // show button for workers or administration to log into the makerspace
        if (level[1] === "worker" || level[1] === "administrator") {
            document.getElementById("is-checked-in").style.display = "block";
        } else {
            document.getElementById("is-checked-in").style.display = "none";
        }
    }

    // show button for administrator to edit equipment
    if (level[1] === "administrator") {
        document.getElementById("addEquipment").style.display = "block";
    } else {
        document.getElementById("addEquipment").style.display = "none";
    }

}