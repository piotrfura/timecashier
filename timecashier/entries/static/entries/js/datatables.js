$(document).ready(function() {
    let table = new DataTable('#table_entries', {
        "pageLength":10,
        "order": [[ 1, "desc" ], [ 2, "desc" ]],
        dom: 'Bfrtip',
            buttons: [
                'pageLength','copy', 'csv',
            ]
    });
});
$(document).ready(function() {
    let table = new DataTable('#table_active_entries', {
        "order": [[ 1, "desc" ]],
        "pageLength":5,
        "searching": false,
        "paging": false,
        "info": false,
        "lengthChange":false
    });
});