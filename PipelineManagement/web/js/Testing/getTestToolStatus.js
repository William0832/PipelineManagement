$(function () {
    console.log("Get Putline")

    // let urlParams = new URLSearchParams(window.location.search);
    // tam_alias = urlParams.get('tam_alias');


    

    $.ajax({
        // url: '/getServiceQuota/ec2',
        url: '/testing/getTestToolStatus',
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
                var tool_type = result.tool_type;
                var tool_id = result.tool_id;
                var tool_name = result.tool_name;
                var owner = result.owner;
                var record_id = result.record_id;
                var status = result.status;
                var work_item_id = result.work_item_id;
                var start_dt = result.start_dt;
                
                var customer_id = result.customer_id;
                var part_no = result.part_no;
                var lot_no = result.lot_no;
                



                var scene_class = "label label-default"; 
                


                // var row = $('<tr>');

                // row.append($('<a>').attr("href", "/pages/workitem.html").attr("target", "_blank").append($('<span>').addClass("glyphicon glyphicon-edit").css("margin-top","3px")));                

                // row.append($('<td>').text(test_type));
                // row.append($('<td>').text(date));
                // row.append($('<td>').text(category));
                // row.append($('<td>').text(customer));
                // row.append($('<td>').text(part_no));
                // row.append($('<td>').text(lot_no));
                // row.append($('<td>').text(units));
                // row.append($('<td>').text(process));
                // row.append($('<td>').text(state));
                
                var cost_time = '????????????';
                console.log(start_dt)
                if(start_dt !=null){
                    old_date_obj = new Date(Date.parse(start_dt, "yyyy-mm-dd HH:mm:ss"));
                    new_date_obj = new Date();
                    //var utc1 = Date.UTC(new_date_obj.getFullYear(), new_date_obj.getMonth(), new_date_obj.getDate());
                    //var utc2 = Date.UTC(old_date_obj.getFullYear(), old_date_obj.getMonth(), old_date_obj.getDate());
                    delta = Math.round(((new_date_obj - old_date_obj)*10 / (1000 * 60 * 60)))/10;
                    console.log(old_date_obj);
                    console.log(new_date_obj);
                    console.log(delta)
                    // alert(delta);
                    cost_time = delta + " ??????";
                }else{
                    cost_time = "";
                }
                

                var panel = $('<panel>')
                var table = $('<table>')
                var button = $('<button onclick="location.href=\'/pages/Record_Test.html\'">??????</button>')
                table.append($('<tr>').append($('<td>').append($('<label>').text(tool_id))).append($('<td>').css("padding-left","15px").append($('<label>').text('????????????'))).append($('<td>').text(owner)));
                
                if(record_id){
                    panel.addClass("panel_working");
                    table.append($('<tr>').append($('<td>').append($('<label>').text('???????????????: '))).append($('<td>').text(part_no)));
                    table.append($('<tr>').append($('<td>').append($('<label>').text('????????????: '))).append($('<td>').text(cost_time)).append(button));    
                }else{
                    panel.addClass("panel_idle");
                    // table.append($('<tr>').append($('<td>').append($('<label>').text('????????????: '))).append($('<td>').text(cost_time)));
                }
                
                panel.append(table);


                if(tool_type == '??????'){
                    $('#tool_universal').append(panel);
                }

                if(tool_type == '??????'){
                    $('#tool_fly').append(panel);

                }
                

                


            });

            // document.getElementById("loader-sq").style.display = "none";

        },
        fail: function (json) { console.log("fail"); }
    });
});


