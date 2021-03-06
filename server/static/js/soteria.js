/*
Author: Daniel Leef
Last Modified: May 31, 2020
*/

/*
deleteRow : deletes whichever row selected by the user 
            using a global current_row variable as the index
*/
function deleteRow() {
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    var table = document.getElementById("schedule-table");
    let name = this.name;
    let row = parseInt(name.substring(3));
    table.deleteRow(row);
    del_rows.splice(row-1, 1);

    updateIDs(row);
    updateRowDelIndexes(row);
    current_row -= 1;

}


/*
updateIDs : updates element IDs whenever a row gets deleted 
*/
function updateIDs(row) {

    for (var i = row+1; i < sched_id; i++) {

        let from = document.getElementById("from"+i);
        let to = document.getElementById("to"+i);
        let priority = document.getElementById("priority"+i);
        if (from != null) {
            from.id = 'from'+(i-1);
            to.id = 'to'+(i-1);
            priority.id = 'priority'+(i-1);

        }

    }

}

/*
updateRowDelIndexes : updates del_rows indices for ease of deletion in the future 
                      and removes autocomplete listeners + rows
*/
function updateRowDelIndexes(row) {
    for (var i = row; i < del_rows.length; i++) {
        del_rows[i].name = "row" + (i);
    }
    places[row] = null;
    auto_listeners.splice(row-1, 1);
    auto_rows.splice(row-1, 1);
    // removeAutoRow(row-1);
}

function compare(a, b) {
    if (a[0] === b[0]) {
        return 0;
    }
    else {
        return (a[0] < b[0]) ? -1 : 1;
    }
}

/*
checkTimesValidity : ensure no times are empty or overlap in the Scheduler
*/
function checkTimesValidity() {
    var times = [];
    var from_t;
    var to_t;
    for (var i = 0; i < current_row; i++) {
        var to = "to";
        var from = "from";

        if (i != 0) {
            // update ids
            to += i;
            from += i;
            from_t = document.getElementById(from);
            to_t = document.getElementById(to);
            if (from_t.value == "" || to_t.value == "") {
             alert("ERROR: PLEASE ENTER VALID TIMES BEFORE ADDING MORE ROWS");
             return false;
            }
            times.push([from_t.value, to_t.value])
        }
        else {
            // take as is
            from_t = document.getElementById(from);
            to_t = document.getElementById(to);
            if (from_t.value == "" || to_t.value == "") {
             alert("ERROR: PLEASE ENTER VALID TIMES BEFORE ADDING MORE ROWS");
             return false;
            }
            times.push([from_t.value, to_t.value])
        }
    }
    times.sort(compare);
    if (times.length > 1) {

      for (var j = 1; j < times.length; j++) {

        if (times[j][0] <= times[j-1][1] && times[j][0] >= times[j-1][0]) {
          alert("ENTRIES OVERLAP: PLEASE MAKE SURE NONE OF YOUR ACTIVITIES OVERLAP IN TIME")
          return false;
        }

        }

    }

    return true;

}

/*
deleteRow : ensures all entries are filled in
*/
function checkEntriesValidity() {
    var entry;
    for (var i = 0; i < sched_id; i++) {
        var entry = "SCHEDULE_INPUT";

        if (i != 0) {
            // update ids
            entry += i;
            entry_t = document.getElementById(entry);
            if (entry_t !== null) {

              if (entry_t.value == "") {
             alert("ERROR: PLEASE ENTER VALID PLACES BEFORE ADDING MORE ROWS");
             return false;
            }
            }
        }
        else {
            // take as is
            entry_t = document.getElementById(entry);
            if (entry_t.value == "") {
             alert("ERROR: PLEASE ENTER VALID TIMES BEFORE ADDING MORE ROWS");
             return false;
            }

        }
    }
    return true;
}

/*
deleteRow : ensures all priorities are filled in
*/
function checkPriorities() {

    var entry;
    for (var i = 0; i < sched_id; i++) {
        var entry = "priority";

        if (i != 0) {
            // update ids
            entry += i;
            entry_t = document.getElementById(entry);
            if (entry_t !== null) {

                if (entry_t.value == "") {
                alert("ERROR: PLEASE ENTER VALID PRIORITIES BEFORE ADDING MORE ROWS");
                return false;
            }

            }
        }
        else {
            // take as is
            entry_t = document.getElementById(entry);
            if (entry_t.value == "") {
                alert("ERROR: PLEASE ENTER VALID PRIORITIES BEFORE ADDING MORE ROWS");
                return false;
            }

        }

    }

    return true;

}

/*
insertRow : inserts a new row at the bottom of the schedule table,
            delete function is passed in which is assigned to each row
*/
function insertRow(delete_function) {
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    var table = document.getElementById("schedule-table");
    let valid_times = checkTimesValidity();
    if (valid_times) {
    let valid_entries = checkEntriesValidity();
        if (valid_entries) {
            let valid_priorities = checkPriorities();
            if (valid_priorities) {

            var row = table.insertRow(-1)
            var cell = row.insertCell(0);
            var priorities = document.createElement("select");
            priorities.id = "priority" + current_row;
            priorities.class = "priority";
            for (var i = 1; i <= 5; i++) {
            var opt = document.createElement("option");
            var t = document.createTextNode(i.toString());
            opt.appendChild(t);
            priorities.appendChild(opt);
            }
            cell.appendChild(priorities);

            var cell2 = row.insertCell(1);
            var t1 = document.createElement("input");
            t1.id = "SCHEDULE_INPUT" + sched_id;
            t1.type = "text";
            cell2.appendChild(t1);
            addAutoRow();

            var cell3 = row.insertCell(2);
            var from = document.createElement("label");
            from.htmlFor = "from" + current_row;
            from.innerHTML = "From: ";
            cell3.appendChild(from);

            var cell4 = row.insertCell(3);
            var appt_from = document.createElement("input");
            appt_from.id = "from" + current_row;
            appt_from.type = "time";
            appt_from.min = "09:00";
            appt_from.max = "18:00";
            cell4.appendChild(appt_from);

            var cell5 = row.insertCell(4);
            var to = document.createElement("label");
            to.htmlFor = "to" + current_row;
            to.innerHTML = "To: ";
            cell5.appendChild(to);

            var cell6 = row.insertCell(5);
            var appt_to = document.createElement("input");
            appt_to.id = "to" + current_row;
            appt_to.type = "time";
            appt_to.min = "09:00";
            appt_to.max = "18:00";
            cell6.appendChild(appt_to);

            var cell7 = row.insertCell(6);
            var del = document.createElement("input");
            del.type = "button";
            del.id = "delete";
            del.name = "row" + current_row;
            del.value = "Delete this row";
            del.onclick = delete_function;
            cell7.appendChild(del);
            del_rows.push(del);

            current_row += 1;
            sched_id += 1;



            }

        }

    }
}

/*
displayMode : changes the main display
*/
function displayMode(evt, mode) {
    var i, tabcontent, tablinks;
    document.getElementById("OUTPUT").innerHTML = "";
    this.output_displayed = false;
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(mode).style.display = "block";
    evt.currentTarget.className += " active";

}
/*
Legacy Code

function removeAutoRow(del_row) {
    jQuery(document).ready(function ($) {
        $(function() {
            google.maps.event.removeListener(auto_listeners[del_row]);
            google.maps.event.clearInstanceListeners(auto_rows[del_row]);
            places[del_row] = null;

            auto_listeners.splice(del_row, 1);
            auto_rows.splice(del_row, 1);
        })
    })
}
*/

/*
addAutoRow : adds a row to the Scheduler that includes autocomplete functionality
*/
function addAutoRow() {
    jQuery(document).ready(function ($) {
        $(function() {
            var new_sched_input = $("#SCHEDULE_INPUT" + sched_id)[0];
            auto_rows[current_row-1] = new google.maps.places.Autocomplete(new_sched_input);
            auto_rows[current_row-1].setFields(['place_id', 'geometry', 'name', 'formatted_address', 'type']);
            auto_listeners[current_row-1] = auto_rows[current_row-1].addListener('place_changed', function() {
            var place = this.getPlace();
            if (!place.geometry) {
                window.alert("No details available for input: '" + place.name + "'");
                return;
            }
            var address = '';
            if (place.address_components) {
                address = [
                    (place.address_components[0] && place.address_components[0].short_name || ''),
                    (place.address_components[1] && place.address_components[1].short_name || ''),
                    (place.address_components[2] && place.address_components[2].short_name || '')
                ].join(' ');
            }
            places[sched_id] = place;

            });
        })
    })

 }

/*
initialize: initializes autocompletion in the Best Time and Best Places modes
*/
function initialize() {
    jQuery(document).ready(function ($) {
    $(function() {

        // auto_bst listener
        auto_bst.addListener('place_changed', function() {
        var place = this.getPlace();
        if (!place.geometry) {
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }
        var address = '';
        if (place.address_components) {
            address = [
                (place.address_components[0] && place.address_components[0].short_name || ''),
                (place.address_components[1] && place.address_components[1].short_name || ''),
                (place.address_components[2] && place.address_components[2].short_name || '')
            ].join(' ');
            }
        bst_place = place;
        });


        // auto_schedule listener
        auto_schedule.addListener('place_changed', function() {
        var place = this.getPlace();
        if (!place.geometry) {
            window.alert("No details available for input: '" + place.name + "'");
            return;
        }
        var address = '';
        if (place.address_components) {
            address = [
                (place.address_components[0] && place.address_components[0].short_name || ''),
                (place.address_components[1] && place.address_components[1].short_name || ''),
                (place.address_components[2] && place.address_components[2].short_name || '')
            ].join(' ');
        }
        // add the element to auto_row dictionary
        places[0] = place;

        });
    })
    })
}


/*
loading : displays a loading sign when waiting for output
*/
function loading() {
    loopItem += 1;
    if (loopItem == 3) {
        loopItem = 0;
    }
    var container = document.createElement("span");
    var text = document.createTextNode("Loading" + dots[loopItem]);
    container.appendChild(text);
    container.style.color = "blue";
    var title = document.createElement("HEADER");
    var y = document.createElement("H2");
    y.appendChild(container);
    title.appendChild(y);
    document.getElementById("OUTPUT").innerHTML = "";
    document.getElementById("OUTPUT").appendChild(title);
    // document.getElementById("OUTPUT").innerHTML = "<span style='color: blue; font-weight: bolder;'>Loading" + dots[loopItem] + "</span>";

}


/*
submitBST : this function packages the inputted place ID and sends to the Best Time logic module.
            The data returned from the logic module is then displayed to the user.
*/
function submitBST(){
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    let entry = auto_bst.getPlace();
    var valid = true;
    if (document.getElementById("BST_INPUT").value == "" || entry == undefined) {
        // alert("ERROR: PLEASE ENTER A VALID PLACE BEFORE SUBMITTING")
        valid = false;
      }
    loadingInterval = setInterval(loading, 250);
    this.output_displayed = true;
    window.scrollBy(0, 200);

    if (valid) {
    let payload = {
        placeId: entry.place_id,
        location: entry.geometry.location,
        type: entry.types
    }
    document.getElementById("sched_button").disabled = true;
    document.getElementById("bft_button").disabled = true;
    $.ajax({
        url: "/times/bestTime",
        type: "POST",
        data: JSON.stringify(payload),
        contentType: "application/json",
        success: function(data) {
            clearInterval(loadingInterval);
            displayOutputBST(data, entry.name);
        },
        statusCode: {
                    500: function() {
                    document.getElementById("sched_button").disabled = false;
                    document.getElementById("bft_button").disabled = false;
                    clearInterval(loadingInterval);
                    displayFailureMessage()

                    }

                }
    })
    }
    else {

        clearInterval(loadingInterval);
        displayFailureMessage();
    }
}

/*
submitBFT : this function calls the Google Maps API to retrieve the top ten results relevant
            to the user's input. The place IDs of each result is then packaged and sent to the
            Best Places Logic Module.
*/
function submitBFT(){
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    var valid = true;
   //  var entry = auto_bft.getPLace()
    var entry = document.getElementById("BFT_INPUT");
    if (entry.value == "") {
      alert("ERROR: PLEASE ENTER A TYPE BEFORE SUBMITTING")
      valid = false;
    }
        if (valid) {
        loadingInterval = setInterval(loading, 250);
        this.output_displayed = true;
        window.scrollBy(0, 200);

        var names = [];
        var addresses = [];
        var types = {};
        const proxyurl = "https://cors-anywhere.herokuapp.com/";
        const url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=" + entry.value + "&key=AIzaSyAZFKIOvAOaqbLQ6FlrrxCMPBofdoNYTUs"; // site that doesn’t send Access-Control-*
        fetch(proxyurl + url) // https://cors-anywhere.herokuapp.com/https://example.com
        .then(response => response.json())
        .then(contents => {
            if (contents.status == "OK") {
            let results = contents.results;
            var placeIds = [];
            for (var i = 0; i < 10; i++) {
                let cur = results[i];
                placeIds.push(cur.place_id);
                types[cur.place_id] = cur.types;
                names.push(cur.name);
                addresses.push(cur.formatted_address);
            }
            let payload = {
            placeId : placeIds,
            type : types
            }   
                document.getElementById("defaultOpen").disabled = true;
                document.getElementById("sched_button").disabled = true;
                $.ajax({
                url: "/times/bestPlace",
                type: "POST",
                data: JSON.stringify(payload),
                contentType: "application/json",
                success: function(data) {
                    clearInterval(loadingInterval);
                    displayOutputBFT(data, names, placeIds, addresses);
                },
                statusCode: {
                    500: function() {
                    document.getElementById("defaultOpen").disabled = false;
                    document.getElementById("sched_button").disabled = false;
                    clearInterval(loadingInterval);
                    displayFailureMessage()

                    }

                }
            });
            
            }
            else {
                clearInterval(loadingInterval);
                displayFailureMessage();
            }
            })
        .catch(() => {clearInterval(loadingInterval); displayFailureMessage();});

        }


}

/*
displayFailureMessage : displays an error message for when user inputs invalid places
*/
function displayFailureMessage() {
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    var output = document.getElementById("OUTPUT");
    var title = document.createElement("HEADER");
    title.setAttribute("id", "output_header"); 
    var y = document.createElement("H2");
    var t = document.createTextNode("Unfortunately, we couldn't find popular times data for the specified input(s)");
    y.appendChild(t);
    title.appendChild(y);
    output.appendChild(title);
    this.output_displayed = true;
}

/*
displayFailureMessageSchedule2 : displays an error message for the scheduler when the user inputs an invalid place
*/
function displayFailureMessageSchedule2() {
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    var output = document.getElementById("OUTPUT");
    var title = document.createElement("HEADER");
    title.setAttribute("id", "output_header"); 
    var y = document.createElement("H2");
    var t = document.createTextNode("One or more of your inputs is invalid");
    y.appendChild(t);
    title.appendChild(y);
    output.appendChild(title);
    this.output_displayed = true;
}

/*
displayFailureMessageSchedule1 : displays an error message for when the user enters an invalid time range in the scheduler
*/
function displayFailureMessageSchedule1() {
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    var output = document.getElementById("OUTPUT");
    var title = document.createElement("HEADER");
    title.setAttribute("id", "output_header"); 
    var y = document.createElement("H2");
    var t = document.createTextNode("Unfortunately, we couldn't find popular times data for the specified input(s). Please ensure all time frames are valid (>= 1 min durations).");
    y.appendChild(t);
    title.appendChild(y);
    output.appendChild(title);
    this.output_displayed = true;
}


function validTimeDifference(index) {
    var to = "to";
    var from = "from";
    if (index != 0) {
        to += index;
        from += index;
    }
    let from_t = document.getElementById(from);
    let to_t = document.getElementById(to);

    if (from_t.value == "" || to_t.value == "") {
        alert("ERROR: PLEASE ENTER VALID TIMES BEFORE SUBMITTING");
        return false;
    }

    return true;
}

function validPriority(index) {
    var priority = "priority";
    if (index != 0) {
        priority += index;
    }
    var element = document.getElementById(priority);
    if (element.value == "") {
        alert("ERROR: PLEASE ENTER VALID PRIORITIES BEFORE ADDING MORE ROWS");  
        return false;
    }
    return true;
}

function getTimeDifference(index) {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();

    today = mm + '/' + dd + '/' + yyyy; 
    var to = "to";
    var from = "from";
    if (index != 0) {
        to += index;
        from += index;
    }
    let from_t = document.getElementById(from);
    let to_t = document.getElementById(to);

    var timeStart = new Date(today + " " + from_t.value);
    var timeEnd = new Date(today + " " + to_t.value);
    if (to_t.value < from_t.value && to_t.value > "00:00") {
        timeEnd.setDate(timeEnd.getDate()+1);
    }
    var diff = Math.abs(timeEnd - timeStart);
    return Math.floor((diff/1000)/60);

}

function getPriority(index) {
    var priority = "priority";
    if (index != 0) {
        priority += index;
    }
    var element = document.getElementById(priority);
    return element.value;
}

/*
displayOutputBFT : displays the output returned from the Best Places module
*/
function displayOutputBFT(data, names, ids, addresses) {
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    var output = document.getElementById("OUTPUT");
    var title = document.createElement("HEADER");
    title.setAttribute("id", "output_header"); 
    var y = document.createElement("H2");
    var t = document.createTextNode("Best Places Output");
    y.appendChild(t);
    title.appendChild(y);
    output.appendChild(title);
    // var title = document.createElement("HEADER");
    // title.innerHTML = type;
    let main_data = data[0];
    let sim_data = data[1];
    for (var j = 0; j < ids.length; j++) {
        let cur = main_data[ids[j]];
        if (cur[0][1] != 0) {
        var new_entry = document.createElement("div");
        new_entry.class = "relative";
        var newContent1 = document.createTextNode("These are the times for ");
        var newContent2 = document.createTextNode(" in order from least busy to most busy: ");

        //new
        var div_container = document.createElement("div");
        div_container.id = "popupparent";

        var container = document.createElement("span");
        var contentName;
        if (sim_data[ids[j]] == 1 || sim_data[ids[j]] == 0) {
            contentName = document.createTextNode(names[j]);
        }
        else {
            contentName = document.createTextNode("* " + names[j]);
        }
        
        container.appendChild(contentName);
        container.style.color = "red";

        // new
        div_container.append(container);
        var popup = document.createElement("div");
        popup.id = "popup";
        popup.textContent = "   " + addresses[j];
        div_container.append(popup);

        new_entry.appendChild(newContent1);
        // new_entry.appendChild(container);
        new_entry.appendChild(div_container);
        new_entry.appendChild(newContent2);
    for (var i = 0; i < cur.length; i++) {
        let cur_time = cur[i];
        if (cur_time[1] == 0) {
            break;
        }
        if (i < 3) {
            var bold = document.createElement("strong");
            var newOne = document.createTextNode(", ");
            var container = document.createElement("span");
            var time = document.createTextNode(cur_time[0] + ":00  ");
            bold.appendChild(time);
            container.appendChild(bold);
            container.style.color = "green";
            if (i != 0) {
                new_entry.appendChild(newOne);
                new_entry.appendChild(container);
            }
            else {
                new_entry.appendChild(container);
            }

        }
        else {
        var newOne = document.createTextNode(", " + cur_time[0] + ":00  ");
        new_entry.appendChild(newOne);
        }

        }
        output.appendChild(new_entry);

        }
        }
    // window.scrollBy(0, 500);
    this.output_displayed = true;
    document.getElementById("defaultOpen").disabled = false;
    document.getElementById("sched_button").disabled = false;

}

/*
displayOutputBST : displays the output returned from the Best Time module
*/
function displayOutputBST(data, place) {
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    var output = document.getElementById("OUTPUT");
    var title = document.createElement("HEADER");
    title.setAttribute("id", "output_header"); 
    var y = document.createElement("H2");
    var t = document.createTextNode("Best Time Output");
    y.appendChild(t);
    title.appendChild(y);
    output.appendChild(title);
    // var title = document.createElement("HEADER");
    // title.innerHTML = type;
    var new_entry = document.createElement("div");
    new_entry.class = "relative";
    var newContent1 = document.createTextNode("These are the times for ");
    var newContent2 = document.createTextNode(" in order from least busy to most busy: ");
    var container = document.createElement("span");
    var contentName = document.createTextNode(place);
    container.appendChild(contentName);
    container.style.color = "red";
    new_entry.appendChild(newContent1);
    new_entry.appendChild(container);
    new_entry.appendChild(newContent2);
    for (var i = 0; i < data.length; i++) {

        if (data[i][1] == 0) {
            break;
        }
        if (i < 3) {
            var bold = document.createElement("strong");
            var newOne = document.createTextNode(", ");
            var container = document.createElement("span");
            var time = document.createTextNode(data[i][0] + ":00  ");
            bold.appendChild(time);
            container.appendChild(bold);
            container.style.color = "green";
            if (i != 0) {
                new_entry.appendChild(newOne);
                new_entry.appendChild(container);
            }
            else {
                new_entry.appendChild(container);
            }

        }
        else {
        var newOne = document.createTextNode(", " + data[i][0] + ":00  ");
        new_entry.appendChild(newOne);
        }


    }
    output.appendChild(new_entry);
    // window.scrollBy(0, 500);
    this.output_displayed = true;
    document.getElementById("sched_button").disabled = false;
    document.getElementById("bft_button").disabled = false;

}

/*
displayOutputSchedule : displays the data returned from the Scheduler module
*/
function displayOutputSchedule(data, names) {
    if (this.output_displayed) {
        document.getElementById("OUTPUT").innerHTML = "";
        this.output_displayed = false;
    }
    var output = document.getElementById("OUTPUT");
    var title = document.createElement("HEADER");
    title.setAttribute("id", "output_header"); 
    var y = document.createElement("H2");
    var t = document.createTextNode("Scheduler Output");
    y.appendChild(t);
    title.appendChild(y);
    output.appendChild(title);
    // var title = document.createElement("HEADER");
    // title.innerHTML = type;
    var valid_array = data[0];
    var invalid_array = data[1];
    for (var i = 0; i < valid_array.length; i++) {
        let cur = valid_array[i];
        let name = names[cur[0]];
        let startTime = cur[1];
        let endTime = cur[2];

        var new_entry = document.createElement("div");
        new_entry.class = "relative";
        var from_time;
        var min_from = startTime % 60;
        var hrs_from = Math.floor(startTime / 60);
        if (min_from < 10) {
            let new_min_from = "0" + min_from;
            min_from = new_min_from;
        }
        from_time = hrs_from + ":" + min_from;

        var to_time;
        var min_to = endTime % 60;
        var hrs_to = Math.floor(endTime / 60);
        if (min_to < 10) {
            let new_min_to = "0" + min_to;
            min_to = new_min_to;
        }
        to_time = hrs_to + ":" + min_to;

        var newContent1 = document.createTextNode("You should go to ");
        var newContent2 = document.createTextNode(" between ");
        var newContent3 = document.createTextNode(" and ");
        var container = document.createElement("span");
        var contentName;
        if (cur[3] == 1 || cur[3] == 0) {
            contentName = document.createTextNode(name);
        }
        else {
            contentName = document.createTextNode("* " + name);
        }
        container.appendChild(contentName);
        container.style.color = "red";
        new_entry.appendChild(newContent1);
        new_entry.appendChild(container);
        new_entry.appendChild(newContent2);
        var time_container1 = document.createElement("span");
        var time_container2 = document.createElement("span");
        var f_node = document.createTextNode(from_time);
        var t_node = document.createTextNode(to_time);
        time_container1.appendChild(f_node)
        time_container1.style.color = "green";
        new_entry.appendChild(time_container1);
        new_entry.appendChild(newContent3);
        time_container2.appendChild(t_node);
        time_container2.style.color = "green";
        new_entry.appendChild(time_container2);
        output.appendChild(new_entry);
        }
        if (invalid_array.length > 0) {
            var new_entry = document.createElement("div");
            new_entry.class = "relative";
            var container = document.createElement("span");
            var newContent = document.createTextNode("We were unable to schedule the following places: ");
            container.appendChild(newContent);
            container.style.color = "red";
            new_entry.appendChild(container);
            for (var i = 0; i < invalid_array.length; i++) {
                let cur = invalid_array[i];
                let name = names[cur];
                var new_name;
                if (i == invalid_array.length - 1) {
                    new_name = document.createTextNode(name);


                }
                else {
                    new_name = document.createTextNode(name + ", ");
                }
                new_entry.appendChild(new_name);
            }

            output.appendChild(new_entry);


        }
    this.output_displayed = true;
    document.getElementById("defaultOpen").disabled = false;
    document.getElementById("bft_button").disabled = false;

}


/*
submitSCHEDULE : compiles place IDs from the global dictionary 'places' and matches
                 each place with the inputted times and priority numbers. Sends all
                 of the data to the Scheduler module.
*/
function submitSCHEDULE(){
    // TODO
    var names = {};
    var index = 1;
    var valid = true;
    payload = {};
    let all_times_valid = checkTimesValidity();
    if (all_times_valid) {
    loadingInterval = setInterval(loading, 250);
    this.output_displayed = true;
    window.scrollBy(0, 400);
    for (var i = 0; i < sched_id; i++) {
        var entry = "SCHEDULE_INPUT";
        if (i != 0) {
            var entry_t = "SCHEDULE_INPUT" + i;
            var res = document.getElementById(entry_t);
            if (res != null) {
                if (res.value != "") {
                    let valid_priority = validPriority(index);
                    if (valid_priority) {
                        let valid_times = validTimeDifference(index);
                        if (valid_times) {
                            if (places[i+1] == undefined) {
                                valid = false;
                                break;
                            }
                            names[places[i+1].place_id] = places[i+1].name;

                            let add = {
                            placeId : places[i+1].place_id,
                            time : getTimeDifference(index),
                            priority : getPriority(index),
                            type : places[i+1].types
                            }
                            payload[index] = add;
                            index += 1;
                        }
                        else {
                            valid = false;
                            break;
                        }
                    }
                    else {
                        valid = false;
                        break;
                    }
                }
                else {
                    alert("ERROR: PLEASE ENTER VALID PLACES BEFORE SUBMITTING");
                    valid = false;
                }
            }
        }
        else {
            // take as is
            var res = document.getElementById(entry);
            if (res != null) {
                if (res.value != "") {
                    let valid_priority = validPriority(0);
                    if (valid_priority) {
                        let valid_times = validTimeDifference(0);
                        if (valid_times) {
                            if (places[0] == undefined) {
                                valid = false;
                                break;
                            }
                            let add = {
                            placeId : places[0].place_id,
                            time : getTimeDifference(0),
                            priority : getPriority(0),
                            type : places[0].types
                            }
                            names[places[0].place_id] = places[0].name;
                            payload[0] = add;
                        }
                        else {
                            valid = false;
                            break;
                        }
                    }
                    else {
                        valid = false;
                        break;
                    }
                }
                else {
                    alert("ERROR: PLEASE ENTER VALID PLACES BEFORE SUBMITTING");
                    valid = false;
                }
            }
        }
    }
    if (valid) {
        document.getElementById("defaultOpen").disabled = true;
        document.getElementById("bft_button").disabled = true;
        $.ajax({
            url: "/scheduler/update",
            type: "POST",
            data: JSON.stringify(payload),
            contentType: "application/json",
            success: function(data) {
                clearInterval(loadingInterval);
                displayOutputSchedule(data, names);
            },
            statusCode: {
                500: function() {
                document.getElementById("defaultOpen").disabled = false;
                document.getElementById("bft_button").disabled = false;
                clearInterval(loadingInterval);
                displayFailureMessageSchedule1()

                }

            }
        })

    }
    else {
        clearInterval(loadingInterval);
        displayFailureMessageSchedule2()

    }
    }
}
