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


// deleting intermediary row, must update all other rows and their ids

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

function updateRowDelIndexes(row) {
    for (var i = row; i < del_rows.length; i++) {
        del_rows[i].name = "row" + (i);
    }
    console.log('ROW TO DELETE: ' + row);
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
    console.log(times);
    if (times.length > 1) {
      for (var j = 1; j < times.length; j++) {
        if (times[j][0] < times[j-1][1] && times[j][0] > times[j-1][0]) {
          alert("ENTRIES OVERLAP: PLEASE MAKE SURE NONE OF YOUR ACTIVITIES OVERLAP IN TIME")
          return false;
        }
        }
    }
    return true;
}

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

// add a priority attribute to each row
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


function displayMode(evt, mode) {
    var i, tabcontent, tablinks;
    document.getElementById("OUTPUT").innerHTML = "";

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


function addAutoRow() {
    jQuery(document).ready(function ($) {
        $(function() {
            var new_sched_input = $("#SCHEDULE_INPUT" + sched_id)[0];
            auto_rows[current_row-1] = new google.maps.places.Autocomplete(new_sched_input);
            auto_rows[current_row-1].setFields(['address_components', 'geometry', 'icon', 'name', 'id']);
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
        console.log(address);
        console.log(place);
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
        console.log(address);
        console.log(place);
        places[0] = place;

        });
    })
    })
}

/* 
scheduler output: ["place: start time:endtime"]
bestTime [(hour, ratio)]
bestPlace { location:(hour, ratio)}
*/


function submitBST(displayOutput){
    let entry = auto_bst.getPlace();
    var valid = true;
    if (BST.value == "") {
        alert("ERROR: PLEASE ENTER A VALID PLACE BEFORE SUBMITTING")
        valid = false;
      }
    let payload = {
        placeId: entry.place_id,
        location: entry.geometry.location,
        type: entry.types
    }
    let output = document.getElementById("BST_OUTPUT");

    if (valid) {
    $.ajax({
        url: "/times/bestTime",
        type: "POST",
        data: JSON.stringify(payload),
        contentType: "application/json",
        success: function(data) {
            displayOutputBST(data, entry.name);
        }
    })
    }
}

function submitBFT(){
    // TODO
    var valid = true;
   //  var entry = auto_bft.getPLace()
    var entry = document.getElementById("BFT_INPUT");
    if (entry.value == "") {
      alert("ERROR: PLEASE ENTER A TYPE BEFORE SUBMITTING")
      valid = false;
    }
        let payload = {
            type : entry.value
        }

        if (valid) {
        $.ajax({
            url: "/times/bestPlace",
            type: "POST",
            data: JSON.stringify(payload),
            contentType: "application/json",
            success: function(data) {
                displayOutputBFT(data);
            },
            fail: function(data) {

                displayFailureMessage()

            }
        });
        }

}

function displayFailureMessage() {
    var output = document.getElementById("OUTPUT");
    var title = document.createElement("HEADER");
    title.setAttribute("id", "output_header"); 
    var y = document.createElement("H2");
    var t = document.createTextNode("Error: could not find popular times data for the given place / type");
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
    console.log(priority);
    console.log(element);
    console.log(document.getElementById("schedule-table"))
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
    var diff = Math.abs(timeEnd - timeStart);
    console.log(diff);
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

function displayOutputBFT(data) {

    var output = document.getElementById("OUTPUT");
    var title = document.createElement("HEADER");
    title.setAttribute("id", "output_header"); 
    var y = document.createElement("H2");
    var t = document.createTextNode("Best Single Time Output");
    y.appendChild(t);
    title.appendChild(y);
    output.appendChild(title);
    // var title = document.createElement("HEADER");
    // title.innerHTML = type;
    for (var i = 0; i < data.length; i++) {

        var new_entry = document.createElement("div");
        new_entry.class = "relative";
        var from_time;
        var min_from = data[i].startTime % 60;
        var hrs_from = Math.floor(data[i].startTime / 60);
        if (min_from < 10) {
            let new_min_from = "0" + min_from;
            min_from = new_min_from;
        }
        from_time = hrs_from + ":" + min_from;

        var to_time;
        var min_to = data[i].endTime % 60;
        var hrs_to = Math.floor(data[i].endTime / 60);
        if (min_to < 10) {
            let new_min_to = "0" + min_to;
            min_to = new_min_to;
        }
        to_time = hrs_to + ":" + min_to;
        var newContent = document.createTextNode("You should go to " + data[i].place + " between " + from_time + " and " + to_time);
        new_entry.appendChild(newContent);
        output.appendChild(new_entry);

    }
    window.scrollBy(0, 500);
    this.output_displayed = true;
    console.log(output);


}

function displayOutputBST(data, place) {

    var output = document.getElementById("OUTPUT");
    var title = document.createElement("HEADER");
    title.setAttribute("id", "output_header"); 
    var y = document.createElement("H2");
    var t = document.createTextNode("Best Single Time Output");
    y.appendChild(t);
    title.appendChild(y);
    output.appendChild(title);
    // var title = document.createElement("HEADER");
    // title.innerHTML = type;
    var new_entry = document.createElement("div");
    new_entry.class = "relative";
    var newContent = document.createTextNode("These are the times for " + place + " in order from least busy to most busy: ");
    new_entry.appendChild(newContent);
    for (var i = 0; i < data.length; i++) {

        if (data[i][1] == 0) {
            break;
        }
        if (i < 3) {
            var bold = document.createElement("strong");
            var newOne = document.createTextNode((i+1) + ") ");
            var time = document.createTextNode(data[i][0] + ":00  ");
            bold.appendChild(time);
            new_entry.appendChild(newOne);
            new_entry.appendChild(bold);

        }
        else {
        var newOne = document.createTextNode((i+1) + ") " + data[i][0] + ":00  ");
        new_entry.appendChild(newOne);
        }


    }
    output.appendChild(new_entry);
    window.scrollBy(0, 500);
    this.output_displayed = true;
    console.log(output);


}

function displayOutputSchedule(data) {

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
    for (var i = 0; i < data.length; i++) {

        var new_entry = document.createElement("div");
        new_entry.class = "relative";
        var from_time;
        var min_from = data[i].startTime % 60;
        var hrs_from = Math.floor(data[i].startTime / 60);
        if (min_from < 10) {
            let new_min_from = "0" + min_from;
            min_from = new_min_from;
        }
        from_time = hrs_from + ":" + min_from;

        var to_time;
        var min_to = data[i].endTime % 60;
        var hrs_to = Math.floor(data[i].endTime / 60);
        if (min_to < 10) {
            let new_min_to = "0" + min_to;
            min_to = new_min_to;
        }
        to_time = hrs_to + ":" + min_to;
        var newContent = document.createTextNode("You should go to " + data[i].place + " between " + from_time + " and " + to_time);
        new_entry.appendChild(newContent);
        output.appendChild(new_entry);

    }
    window.scrollBy(0, 500);
    this.output_displayed = true;
    console.log(output);


}
function submitSCHEDULE(){
    // TODO
    var index = 1;
    var output = [];
    var valid = true;
    payload = {};
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
                            // SEND TYPE ALONG WITH THE PLACE ID
                            // console.log(places[i+1]);
                            let add = {
                            placeId : places[i+1].id,
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
                            // console.log(places[0]);
                            let add = {
                            placeId : places[0].id,
                            time : getTimeDifference(0),
                            priority : getPriority(0),
                            type : places[0].types
                            }
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
    console.log(payload);
        $.ajax({
            url: "/scheduler/update",
            type: "POST",
            data: JSON.stringify(payload),
            contentType: "application/json",
            success: function(data) {
                let d = [
                    {place: "Screen Door", startTime: 750, endTime: 880},
                    {place: "Yoga Studio", startTime: 600, endTime: 660},
                    {place: "Yoga Studio", startTime: 600, endTime: 660},
                    {place: "Yoga Studio", startTime: 600, endTime: 660},
                    {place: "Yoga Studio", startTime: 600, endTime: 660},
                    {place: "Yoga Studio", startTime: 600, endTime: 660},
                    {place: "Yoga Studio", startTime: 600, endTime: 660},
                    {place: "Yoga Studio", startTime: 600, endTime: 660},
                    {place: "Yoga Studio", startTime: 600, endTime: 660},
                    {place: "Yoga Studio", startTime: 600, endTime: 660},

                ]
                displayOutputSchedule(d);
            }
        })

    }

}
