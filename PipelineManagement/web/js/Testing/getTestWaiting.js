$(function () {
    console.log("取得待測試資料")

   

    

    $.ajax({
        // url: '/getServiceQuota/ec2',
        url: '/testing/getTestWaitings',
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
                var test_record_id = result.test_record_id;
                var status = result.status;
                var work_item_id = result.work_item_id;
                var start_dt = result.start_dt;
                
                var customer_id = result.customer_id;
                var part_no = result.part_no;
                var lot_no = result.lot_no;

                var work_item_status = result.work_item_status;
                



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
                if(test_record_id){
                    old_date_obj = new Date(Date.parse(start_dt, "yyyy-mm-dd HH:mm:ss"));
                    new_date_obj = new Date();
                    //var utc1 = Date.UTC(new_date_obj.getFullYear(), new_date_obj.getMonth(), new_date_obj.getDate());
                    //var utc2 = Date.UTC(old_date_obj.getFullYear(), old_date_obj.getMonth(), old_date_obj.getDate());
                    delta = Math.round(((new_date_obj - old_date_obj)*10 / (1000 * 60 * 60)))/10;
                    // console.log(old_date_obj)
                    // console.log(new_date_obj)
                    // if(tool_type == '萬用' || tool_type == '飛針' ){
                    //     $('#testing_waitings').append($('<a href="#">'+part_no+'</a>  '+delta+'小時   <button onclick="checkInPrepareRecord('+record_id+', \''+tool_type+'\')">指派機台</button><br/> '));
                        
                    // }

                    var onclick_event_name = "checkInTestRecord";
                    if (tool_type =="飛針"){
                        onclick_event_name = "checkInFlyTestRecord";
                    }
                
                    var button = '<button onclick="'+onclick_event_name+'('+test_record_id+', \''+tool_type+'\')">指派機台</button><br/> ';
                    if(work_item_status == '待測試(無資料)'){
                        var button = '<button onclick="'+onclick_event_name+'('+test_record_id+', \''+tool_type+'\')" disabled>等待治具中</button><br/> ';
                    }

                    $('#testing_waitings').append($('<a href="#">'+part_no+' ('+tool_type+')</a>  '+delta+'小時   '+button));
    
                    
                }
                
            
                

                
            
                


            });

            // document.getElementById("loader-sq").style.display = "none";

        },
        fail: function (json) { console.log("fail"); }
    });
});


