function deleteRow() {
    var table = document.getElementById("schedule-table");
    let name = this.name;
    let row = parseInt(name.substring(3));
    table.deleteRow(row);
    del_rows.splice(row-1, 1);

    updateRowDelIndexes(row-1);
    current_row -= 1;

}


function updateRowDelIndexes(row) {
    for (var i = row; i < del_rows.length; i++) {
        del_rows[i].name = "row" + (i+1);
    }
    removeAutoRow(row);
}

function compare(a, b) {

    return a[1] - b[1];

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
             alert("ERROR: PLEASE ENTER VALID TIMES BEFORE ADDING MORE ROWS / SUBMITTING");
             return false;
            }
            times.push([from_t.value, to_t.value])
        }
        else {
            // take as is
            from_t = document.getElementById(from);
            to_t = document.getElementById(to);
            if (from_t.value == "" || to_t.value == "") {
             alert("ERROR: PLEASE ENTER VALID TIMES BEFORE ADDING MORE ROWS / SUBMITTING");
             return false;
            }
            times.push([from_t.value, to_t.value])

        }

    }
    times.sort(compare);
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
             alert("ERROR: PLEASE ENTER VALID PLACES BEFORE ADDING MORE ROWS / SUBMITTING");
             return false;
            }

            }
        }
        else {
            // take as is
            entry_t = document.getElementById(entry);
            if (entry_t.value == "") {
             alert("ERROR: PLEASE ENTER VALID TIMES BEFORE ADDING MORE ROWS / SUBMITTING");
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
                    alert("ERROR: PLEASE ENTER VALID PLACES BEFORE ADDING MORE ROWS / SUBMITTING");
                    return false;
                }

                }
            }
            else {
                // take as is
                entry_t = document.getElementById(entry);
                if (entry_t.value == "") {
                    alert("ERROR: PLEASE ENTER VALID TIMES BEFORE ADDING MORE ROWS / SUBMITTING");
                    return false;
                }

            }

        }

        return true;

        }
// add a priority attribute to each row
function insertRow(delete_function) {

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
    console.log($(document).ready(function($){}(jQuery)));
    jQuery(document).ready(function ($) {
        console.log("currently here");
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
            console.log(address);
            console.log(place);
            places[current_index] = place;

            });
        })
        console.log($("#SCHEDULE_INPUT" + current_row)[0]);
    })

 }

function initialize() {
    jQuery(document).ready(function ($) {
    $(function() {
        var auto_bst;
        // var auto_bft;
        var auto_schedule;
        var bst_input = $("#BST_INPUT")[0];
        // var bft_input = $("#BFT_INPUT")[0];
        var schedule_input = $("#SCHEDULE_INPUT")[0];

        auto_bst = new google.maps.places.Autocomplete(bst_input);
        // auto_bft = new google.maps.places.Autocomplete(bft_input);
        auto_schedule = new google.maps.places.Autocomplete(schedule_input);
        auto_bst.setFields(['address_components', 'geometry', 'icon', 'name', 'id', 'type']);
        // auto_bft.setFields(['address_components', 'geometry', 'icon', 'name', 'id']);
        auto_schedule.setFields(['address_components', 'geometry', 'icon', 'name', 'id', 'type']);

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
    let BST = document.getElementById("BST_INPUT");

    console.log(BST.value);
    if (BST.value == "") {
        alert("ERROR: PLEASE ENTER A VALID PLACE BEFORE SUBMITTING")
      }
      console.log(bst_place);

    let lat;
    let long;

    navigator.geolocation.getCurrentPosition(function f(args){
        console.log("Args: " + args);
        console.log("Arg Obj: " + Object.keys(args))
        lat = args.latitude
        long = args.longitude

        payload = {
            "latitude" : lat,
            "longitude" : long,
            "place" : bst_place
        }
        let output = document.getElementById("BST_OUTPUT");

        console.log(payload);

        $.ajax({
            url: "/times/bestTime",
            type: "POST",
            data: JSON.stringify(payload),
            contentType: "application/json",
            success: function(data) {
                displayOutput(data, 'BST');
            }
        })
    });
}

function submitBFT(){
    // TODO
    var entry = document.getElementById("BFT_INPUT");
    if (entry.value == "") {
      alert("ERROR: PLEASE ENTER A TYPE BEFORE SUBMITTING")
    }
        var payload = {
            "latitude" : lat,
            "longitude" : long,
            "type" : entry.value
        }

        $.ajax({
            url: "/times/bestTime",
            type: "POST",
            data: JSON.stringify(payload),
            contentType: "application/json",
            success: function(data) {
                displayOutput(data, 'BST');
            }
        })
    console.log(entry.value);
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

    var timeStart = new Date(today + " " + from_t.value).val();
    var timeEnd = new Date(today + " " + to_t.value).val();

    return timeEnd - timeStart;

}

function getPriority(index) {
    let priority = "priority" + index;
    var element = document.getElementById(priority);
    return element.value;
}

function submitSCHEDULE(){
    // TODO
    var index = 1;
    var output = [];
    for (var i = 0; i < sched_id; i++) {
        var entry = "SCHEDULE_INPUT";

        if (i != 0) {
            // update ids
            entry += i;
            entry_t = document.getElementById(entry);
            if (entry_t !== null) {

                let payload = {
                    "place" : places[index],
                    "time" : getTimeDifference(index),
                    "priority" : getPriority(index)
                }

            }
        }
        else {
            // take as is
            entry_t = document.getElementById(entry);
            if (entry_t.value == "") {
             alert("ERROR: PLEASE ENTER VALID TIMES BEFORE ADDING MORE ROWS / SUBMITTING");
             return false;
            }

        }
    }
    console.log(places);

}
