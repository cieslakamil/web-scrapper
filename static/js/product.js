$(document).ready(function() {
    $('#product-opinions-table thead tr').clone(true).appendTo('#product-opinions-table thead');
    $('#product-opinions-table thead tr:eq(1) th').each(function(i) {
        var title = $(this).text();
        $(this).html('<input type="text" placeholder="Filtruj ' + title + '" />');

        $('input', this).on('keyup change', function() {
            if (table.column(i).search() !== this.value) {
                table
                    .column(i)
                    .search(this.value)
                    .draw();
            }
        });
    });

    var table = $('#product-opinions-table').DataTable({
        "scrollX": true,
        orderCellsTop: true,
        fixedHeader: true
    });
});