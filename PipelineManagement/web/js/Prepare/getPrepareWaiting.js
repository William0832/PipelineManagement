$(function () {
    console.log("Get Putline")

    // let urlParams = new URLSearchParams(window.location.search);
    // tam_alias = urlParams.get('tam_alias');


    

    $.ajax({
        // url: '/getServiceQuota/ec2',
        url: '/prepare/getPrepareWaitings',
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
                if(record_id){
                    old_date_obj = new Date(Date.parse(start_dt, "yyyy-mm-dd HH:mm:ss"));
                    new_date_obj = new Date();
                    //var utc1 = Date.UTC(new_date_obj.getFullYear(), new_date_obj.getMonth(), new_date_obj.getDate());
                    //var utc2 = Date.UTC(old_date_obj.getFullYear(), old_date_obj.getMonth(), old_date_obj.getDate());
                    delta = Math.round(((new_date_obj - old_date_obj)*10 / (1000 * 60 * 60)))/10;
                    // console.log(old_date_obj)
                    // console.log(new_date_obj)
                    if(tool_type == '工程'){
                        $('#prepare_waiting_eng').append($('<a href="#">'+part_no+'</a>  '+delta+'小時   <button onclick="checkInPrepareRecord('+record_id+', \''+tool_type+'\')">接單</button><br/> '));
                        
                    }
    
                    if(tool_type == '鑽孔'){
                        
                            $('#prepare_waiting_hole').append($('<a href="#">'+part_no+'</a>  '+delta+'小時   <button onclick="checkInPrepareRecord('+record_id+', \''+tool_type+'\')">接單</button><br/> '));
                    }
                    
    
                    if(tool_type == '組裝'){
                            $('#prepare_waiting_assemble').append($('<a href="#">'+part_no+'</a>  '+delta+'小時   <button onclick="checkInPrepareRecord('+record_id+', \''+tool_type+'\')">接單</button><br/> '));
                        
    
                    }
                    // if(tool_type == '完成'){
                    //     $('#prepare_ready').append($('<a href="#">'+part_no+'</a>  <br/> '));
                    //     console.log("完成的項目")
                    // }
                }
                
            
                

                
            
                


            });

            // document.getElementById("loader-sq").style.display = "none";

        },
        fail: function (json) { console.log("fail"); }
    });
});


