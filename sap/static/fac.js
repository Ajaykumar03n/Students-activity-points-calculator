function submitCheckedData() {
    var checkedData = [];

    // Iterate through each table
    for (var i = 1; i <= 12; i++) {
        var tableId = "table" + i;
        var table = document.getElementById(tableId);
        var checkboxes = table.querySelectorAll("input[name='checkbox']");

        // Iterate through checkboxes in the current table
        checkboxes.forEach(function(checkbox) {
            if (checkbox.checked) {
                var row = checkbox.closest("tr"); // Get the closest ancestor <tr> element
                var cells = row.getElementsByTagName("td"); // Get all <td> elements in the row
                
                var rowData = {};
                // Customize this section to match the structure of each table
                for (var j = 0; j < cells.length; j++) {
                    var columnName = table.rows[0].cells[j].innerText.toLowerCase().replace(/\s+/g, ''); // Get column name from table header
                    rowData[columnName] = cells[j].innerText;
                }
                
                checkedData.push(rowData);
            }
        });
    }

    // Perform custom logic or submit data to the server
    // For example, you can submit checkedData to the server using AJAX
    console.log(checkedData); // Output checked data to console (for testing)
}

