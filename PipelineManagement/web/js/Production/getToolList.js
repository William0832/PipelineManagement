$(function () {
    console.log("Get Putline")

    // let urlParams = new URLSearchParams(window.location.search);
    // tam_alias = urlParams.get('tam_alias');


    

    $.ajax({
        // url: '/getServiceQuota/ec2',
        url: '/testing/getTools/all',
        type: 'GET',
        dataType: 'json',
        success: function (json) {
            // console.log("Get Customer List Table")
            console.log(json);

            // var total_count = 0;
            // var complete_survey_count = 0;
            // var complete_comment_count = 0;

            $.each(json.results, function (i, result) {

                // 

                // <th style="width:100px"></th>
                // <th style="width:100px">機台類別</th>
                // <th style="width:100px">機台編號</th>
                // <th style="width:100px">機台名稱</th>
                // <th style="width:300px">負責人</th>
                // <th style="width:100px">新增時間</th>
                // <th style="width:100px">是否已移除?</th>    
                var tool_type = result.tool_type;
                var tool_id = result.tool_id;
                var tool_name = result.tool_name;
                var tool_owner = result.tool_owner;


                

                var scene_class = "label label-default"; 
                


                var row = $('<tr>');

                row.append($('<a>').attr("href", "/pages/workitem.html").attr("target", "_blank").append($('<span>').addClass("glyphicon glyphicon-edit").css("margin-top","3px")));                

                row.append($('<td>').text(test_type));
                row.append($('<td>').text(date));
                row.append($('<td>').text(category));
                row.append($('<td>').text(customer));
                row.append($('<td>').text(part_no));
                row.append($('<td>').text(lot_no));
                row.append($('<td>').text(units));
                row.append($('<td>').text(process));
                row.append($('<td>').text(status));
                
                
                

                
            
                $('#productionKanbanTable').find('tbody').append(row);


            });

            // document.getElementById("loader-sq").style.display = "none";

        },
        fail: function (json) { console.log("fail"); }
    });
});


