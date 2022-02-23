$(document).ready(function() {
    let table = new DataTable('#table_entries', {
        "pageLength":10,
        "order": [[ 3, "desc" ]],
        dom: 'Bfrtip',
            buttons: [
                'pageLength','copy', 'csv',
            ],
        "responsive": true,
        "columnDefs": [
        { responsivePriority: 5, targets: 0 },
        { responsivePriority: 1, targets: 1 },
        { responsivePriority: 3, targets: 2 },
        { responsivePriority: 3, targets: 3 },
        { responsivePriority: 4, targets: 4 },
        { responsivePriority: 2, targets: 5 },
    ]
    });
});
$(document).ready(function() {
    let table = new DataTable('#table_active_entries', {
        "pageLength":1,
        "sort": false,
        "searching": false,
        "paging": false,
        "info": false,
        "lengthChange":false,
        "responsive": true,
    });
});
$(document).ready(function() {
    let table = new DataTable('#table_entries_last', {
        "pageLength":5,
        "order": [[ 3, "desc" ]],
        "paging": false,
        "searching": false,
        "lengthChange":false,
        "info": false,
        "responsive": {details: false},
        "columnDefs": [
        { responsivePriority: 6, targets: 0 },
        { responsivePriority: 1, targets: 1 },
        { responsivePriority: 5, targets: 2 },
        { responsivePriority: 2, targets: 3 },
        { responsivePriority: 3, targets: 4 },
        { responsivePriority: 4, targets: 5 },
    ]
    });
});

$(document).ready(function() {
    let table = new DataTable('#table_clients', {
        "pageLength":10,
        "order": [[ 1, "asc" ]],
        dom: 'Bfrtip',
            buttons: [
                'pageLength',
            ],
        "responsive": true,
        "columnDefs": [
        { responsivePriority: 5, targets: 0 },
        { responsivePriority: 1, targets: 1 },
        { responsivePriority: 3, targets: 2 },
        { responsivePriority: 3, targets: 3 },
        { responsivePriority: 4, targets: 4 },
        { responsivePriority: 2, targets: 5 },
    ]
    });
});