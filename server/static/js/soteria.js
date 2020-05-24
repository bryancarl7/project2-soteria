document.getElementById("defaultOpen").click();
// var from = document.getElementById('appt')
// var to = document.getElementById('appt2')
var auto_listeners = [];
var auto_rows = [];
var current_row = 1;
var sched_id = 1;
var del_rows = [];
//var table = document.getElementById("schedule-table");
initialize();
var rowIndex = 1;
// var apptIndex = 1;

function deleteRow() {
    var table = document.getElementById("schedule-table");
    let name = this.name;
    let row = parseInt(name.substring(3));
    table.deleteRow(row);
    del_rows.splice(row-1, 1);

    updateRowDelIndexes(row-1);

    current_row -= 1;

    // var i = row.parentNode.parentNode.rowindex;
    // console.log(i);
    // console.log(row.parentNode.parentNode)
    // table.deleteRow(i-1);

}


function updateRowDelIndexes(row) {

    for (var i = row; i < del_rows.length; i++) {

        del_rows[i].name = "row" + (i+1);

    }
    removeAutoRow(row);
}
// add a priority attribute to each row
function insertRow(delete_function) {
    // $('#schedule-table').append('<tr><td><input type = "text" id = "SCHEDULE_INPUT"/></td><td><label for = "appt">From: </label></td><td> <input type="time" id="appt" name="appt" min="09:00" max="18:00" required> </td><td><label for = "appt2">To: </label></td><td> <input type="time" id="appt2" name="appt" min="09:00" max="18:00" required></td><td><input type = "button" id = "delete" value = "Delete this row" onclick = "deleteRow(this)"></td><td><input type = "button" id = "add" value = "Add another row" onclick = "insertRow()"></td></tr>');
    // initialize();

    var table = document.getElementById("schedule-table");

    var row = table.insertRow(-1)
    var cell = row.insertCell(0);
    var t1 = document.createElement("input");
    t1.id = "SCHEDULE_INPUT" + sched_id;
    t1.type = "text";
    cell.appendChild(t1);
    addAutoRow();

    var cell2 = row.insertCell(1);
    var from = document.createElement("label");
    from.htmlFor = "from" + current_row;
    from.innerHTML = "From: ";
    cell2.appendChild(from);

    var cell3 = row.insertCell(2);
    var appt_from = document.createElement("input");
    appt_from.id = "from" + current_row;
    appt_from.type = "time";
    appt_from.min = "09:00";
    appt_from.max = "18:00";
    cell3.appendChild(appt_from);

    var cell4 = row.insertCell(3);
    var to = document.createElement("label");
    to.htmlFor = "to" + current_row;
    to.innerHTML = "To: ";
    cell4.appendChild(to);

    var cell5 = row.insertCell(4);
    var appt_to = document.createElement("input");
    appt_to.id = "to" + current_row;
    appt_to.type = "time";
    appt_to.min = "09:00";
    appt_to.max = "18:00";
    cell5.appendChild(appt_to);

    var cell5 = row.insertCell(5);
    var del = document.createElement("input");
    del.type = "button";
    del.id = "delete";
    del.name = "row" + current_row;
    del.value = "Delete this row";
    del.onclick = delete_function;
    cell5.appendChild(del);
    del_rows.push(del);

    current_row += 1;
    sched_id += 1;
    /*
    console.log(table.rows);
    console.log(table.rows[0]);

    var new_row = table.rows[1].cloneNode(true);
    var len = table.rows.length;
    new_row.cells[0].innerHTML = len;

    console.log(new_row.cells);
    console.log(new_row.cells[0]);
    console.log(new_row.cells[1]);
    console.log(new_row.cells[2]);
    console.log(new_row.cells[3]);

    console.log(new_row.cells[0].getElementsByTagName('tr'));
    console.log(new_row.cells[0].getElementsByTagName('input')[0]);

    var inp1 = new_row.cells[0].getElementsByTagName('input')[0];
    console.log(inp1);
    inp1.id += len;
    inp1.value = '';
    //var inp2 = new_row.cells[2].getElementsByTagName('input')[0];
    //inp2.id += len;
    //inp2.value = '';
    table.appendChild(new_row);
    */
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
            console.log(del_row);
            console.log(auto_listeners[del_row]);
            google.maps.event.removeListener(auto_listeners[del_row]);
            google.maps.event.clearInstanceListeners(auto_rows[del_row]);

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

            var new_auto_row;
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
            });
        })
        console.log($("#SCHEDULE_INPUT" + current_row)[0]);
    })

 }

function initialize() {
    jQuery(document).ready(function ($) {
    $(function() {
        var auto_bst;
        var auto_bft;
        var auto_schedule;
        var bst_input = $("#BST_INPUT")[0];
        var bft_input = $("#BFT_INPUT")[0];
        var schedule_input = $("#SCHEDULE_INPUT")[0];

        auto_bst = new google.maps.places.Autocomplete(bst_input);
        auto_bft = new google.maps.places.Autocomplete(bft_input);
        auto_schedule = new google.maps.places.Autocomplete(schedule_input);
        auto_bst.setFields(['address_components', 'geometry', 'icon', 'name', 'id']);
        auto_bft.setFields(['address_components', 'geometry', 'icon', 'name', 'id']);
        auto_schedule.setFields(['address_components', 'geometry', 'icon', 'name', 'id']);

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
        });

        // auto_bft listener
        auto_bft.addListener('place_changed', function() {
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
        auto_rows[0] = place;
        console.log(address);
        console.log(place);
        });

    })
    })
}
