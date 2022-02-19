$(document).ready(function() {
    let table = new DataTable('#table_entries', {
        "pageLength":10,
        "order": [[ 3, "desc" ]],
        dom: 'Bfrtip',
            buttons: [
                'pageLength','copy', 'csv',
            ]
    });
});
$(document).ready(function() {
    let table = new DataTable('#table_active_entries', {
        "pageLength":1,
        "searching": false,
        "paging": false,
        "info": false,
        "lengthChange":false
    });
});
$(document).ready(function() {
    let table = new DataTable('#table_entries_last', {
        "pageLength":3,
        "order": [[ 3, "desc" ]],
        "paging": true,
        "searching": false,
        "lengthChange":false,
        "info": false,
    });
});