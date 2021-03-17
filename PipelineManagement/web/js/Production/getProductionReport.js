$(function () {
    console.log("Get Putline")

    // let urlParams = new URLSearchParams(window.location.search);
    // tam_alias = urlParams.get('tam_alias');


    

    $.ajax({
        // url: '/getServiceQuota/ec2',
        url: '/product/getProductionReport',
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
                var shift = result.shift;
                var productionDate = result.productionDate;
                var customer = result.customer;
                var part_no = result.part_no;
                var program_name = result.program_name;
                var param_v = result.param_v;
                var param_phm = result.param_phm;
                var param_mohm = result.param_mohm;
                var test_point_count = result.test_point_count;
                var work_item_count = result.work_item_count;
                var retest_rate = result.retest_rate;
                var batch_number = result.batch_number;
                var first_piece_pintrack = result.first_piece_pintrack;
                var test_200 = result.test_200;
                var testing_count = result.testing_count;
                var test_result_ok_count = result.test_result_ok_count;
                var test_result_ng_count = result.test_result_ng_count;
                var yield = result.yield;
                var defect = result.defect;
                var test_start_time = result.test_start_time;
                var test_end_time = result.test_end_time;
                var abnormal_event = result.abnormal_event;
                var event_start_time = result.event_start_time;
                var event_end_time = result.event_end_time;
                var tester = result.tester;
                var test_machine = result.test_machine;
                

                var scene_class = "label label-default"; 
                


                var row = $('<tr>');
                // row.append($('<td class="sorter">').text(seq));        
                // row.append($('<td style="padding-left:20px;padding-right:20px" contenteditable="true">').text(outline));
                // row.append($('<td style="padding-left:20px;padding-right:20px">').text(outline));
                // row.append($('<td style="color:DodgerBlue">').text(scene));
                // row.append($('<td>').text(scene_property));

                // var td_role = $('<td>')
                // $.each(roles, function (i, role) {

                //     var role_alias = role.role_alias;
                //     var role_photo_link = role.role_photo_link;
                //     var role_img = $('<img src="/assets/photo/'+role_photo_link+'" width="30px" title="'+role_alias+'" style="margin:2px 2px 2px 2px">');
                //     td_role.append(role_img)
                    
                // });
                
                // <a href="#">
                //     <span class="glyphicon glyphicon-list-alt"></span>
                // </a>

                row.append($('<a>').attr("href", "/pages/workitem.html").attr("target", "_blank").append($('<span>').addClass("glyphicon glyphicon-edit").css("margin-top","3px")));                

                row.append($('<td>').text(shift));
                row.append($('<td>').text(productionDate));
                row.append($('<td>').text(customer));
                row.append($('<td>').text(part_no));
                row.append($('<td>').text(program_name));
                row.append($('<td>').text(param_v));
                row.append($('<td>').text(param_phm));
                row.append($('<td>').text(param_mohm));
                row.append($('<td>').text(test_point_count));
                row.append($('<td>').text(work_item_count));
                row.append($('<td>').text(retest_rate));
                row.append($('<td>').text(batch_number));
                row.append($('<td>').text(first_piece_pintrack));
                row.append($('<td>').text(test_200));
                row.append($('<td>').text(testing_count));
                row.append($('<td>').text(test_result_ok_count));
                row.append($('<td>').text(test_result_ng_count));
                row.append($('<td>').text(yield));
                row.append($('<td>').text(defect));
                row.append($('<td>').text(test_start_time));
                row.append($('<td>').text(test_end_time));
                row.append($('<td>').text(abnormal_event));
                row.append($('<td>').text(event_start_time));
                row.append($('<td>').text(event_end_time));
                row.append($('<td>').text(tester));
                row.append($('<td>').text(test_machine));
                
                
                

                
            
                $('#productionReportTable').find('tbody').append(row);


            });

            // document.getElementById("loader-sq").style.display = "none";

        },
        fail: function (json) { console.log("fail"); }
    });
});


