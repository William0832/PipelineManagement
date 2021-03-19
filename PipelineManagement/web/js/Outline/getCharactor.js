$(function () {
    console.log("Get Charactor")

    // let urlParams = new URLSearchParams(window.location.search);
    // tam_alias = urlParams.get('tam_alias');




    $.ajax({
        // url: '/getServiceQuota/ec2',
        url: '/role/getRoles',
        type: 'GET',
        dataType: 'json',
        success: function (json) {
            // console.log("Get Customer List Table")
            console.log(json);

            // var total_count = 0;
            // var complete_survey_count = 0;
            // var complete_comment_count = 0;

            $.each(json.results, function (i, result) {

                var role_id = result.role_id;
                var role_name = result.role_name;
                var role_alias = result.role_alias;
                var role_description = result.role_description;
                var role_photo_link = result.role_photo_link;




                var row = $('<tr>');
                row.append($('<td >').text(role_id));
                row.append($('<td >').append($('<img src="/assets/photo/' + role_photo_link + '" width="30px" title="' + role_alias + '" style="margin:2px 2px 2px 2px">')));
                row.append($('<td >').text(role_name + "/" + role_alias));
                row.append($('<td >').text(role_description));



                $('#charactorTable').find('tbody').append(row);


            });

            // document.getElementById("loader-sq").style.display = "none";

        },
        fail: function (json) { console.log("fail"); }
    });
});


