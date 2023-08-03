/*
* equipment.js
*
* These functions are required to change the equipment images, descriptions and tiles when a radio button is clicked
*
* REFERENCES
* https://stackoverflow.com/questions/21432193/how-to-get-the-ids-of-all-elements-of-a-particular-class
* https://stackoverflow.com/questions/15318357/show-hide-image-with-javascript
*/


// shows correct equipment images, descriptions and titles
function showImage(id, classNames) {
    var equipment_id = id.split(" ")[0];
    var classNameList = classNames.split(" ");

    // determine the category of the button which was clicked
    for(var i=0; i < classNameList.length; i++){
        if (classNameList[i] == "fabrication") {
            className = "fabrication";
        } else if (classNameList[i] == "DPT") {
            className = "DPT";
        } else if (classNameList[i] == "assembly") {
            className = "assembly";
        } else if (classNameList[i] == "production") {
            className = "production";
        }
    }

    // get all ids of equipment in selected category
    var equipment_ids = getIds(className);

    // image id: image_id
    // title id: name 0
    // text id: name 1
    // button id: equipment_id = id

    for(var i=0; i < equipment_ids.length; i++){
        // show equipment that was clicked on
        if(equipment_ids[i] === equipment_id) {
            document.getElementById('image_' + equipment_id).style.display = "block";    // change image
            document.getElementById('description_' + equipment_id).style.display = "block";     // change text
            document.getElementById('title_' + equipment_id).style.display = "block";  // change title
        // hide all other equipment in that category
        } else {
            document.getElementById('image_' + equipment_ids[i]).style.display = "none";    // change image
            document.getElementById('description_' + equipment_ids[i]).style.display = "none";     // change text
            document.getElementById('title_' + equipment_ids[i]).style.display = "none";      // change title
        }
    }
}

// get and return all ids of equipment in specified equipment category (ie button set)
 function getIds(className) {
   var elements = document.getElementsByClassName(className);
   var element_ids = [];
   for(var i=0; i<elements.length; i++) {
        element = elements[i].getAttribute("id")
        element_ids.push(element.split(" ")[0]);
   }
   return element_ids;
 }