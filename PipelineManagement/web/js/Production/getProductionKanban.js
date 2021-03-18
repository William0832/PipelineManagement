;$(function () {
    console.log("Get Putline")
    $.ajax({
        url: '/workitem/getWorkitems',
        type: 'GET',
        dataType: 'json',
        success: function (json) {

            $.each(json.results, function (i, result) {
                var test_type = result.test_type;
                var date = result.create_dt;
                var category = result.test_style;
                var customer = result.customer_id;
                var part_no = result.part_no;
                var lot_no = result.lot_no;
                var units = result.units;
                var process = result.process;
                var status = result.status;
                // var remark = result.remark;
                // var scene_class = "label label-default"; 

                var row = $('<tr>')
                row.append(
                    $('<a>')
                    .attr("href", "/pages/workitem.html")
                    .attr("target", "_blank").append(
                        $('<span>')
                        .addClass("glyphicon glyphicon-edit").
                        css("margin-top","3px")
                    )
                )               

                row.append($('<td>').text(test_type))
                row.append($('<td>').text(date))
                row.append($('<td>').text(category))
                row.append($('<td>').text(customer))
                row.append($('<td>').text(part_no))
                row.append($('<td>').text(lot_no))
                row.append($('<td>').text(units))
                row.append($('<td>').text(process))
                row.append($('<td>').text(status))
                $('#productionKanbanTable').find('tbody').append(row)
            })
        },
        fail: function (json) { console.log("fail")}
    })
})


