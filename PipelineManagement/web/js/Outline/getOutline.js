$(function () {
  console.log("Get Putline");

  // let urlParams = new URLSearchParams(window.location.search);
  // tam_alias = urlParams.get('tam_alias');

  $.ajax({
    // url: '/getServiceQuota/ec2',
    url: "/outline/getOutline",
    type: "GET",
    dataType: "json",
    success: function (json) {
      // console.log("Get Customer List Table")
      console.log(json);

      // var total_count = 0;
      // var complete_survey_count = 0;
      // var complete_comment_count = 0;

      $.each(json.results, function (i, result) {
        var id = result.id;
        var seq = result.seq;
        var outline = result.outline;
        var short_outline = result.short_outline;
        var scene = result.scene_name;

        var scene_property = result.scene_property;
        var roles = result.roles;

        var scene_class = "label label-default";

        var row = $("<tr>");
        row.append($('<td class="sorter">').text(seq));
        // row.append($('<td style="padding-left:20px;padding-right:20px" contenteditable="true">').text(outline));
        row.append(
          $('<td style="padding-left:20px;padding-right:20px">').text(outline)
        );
        row.append($('<td style="color:DodgerBlue">').text(scene));
        row.append($("<td>").text(scene_property));

        var td_role = $("<td>");
        $.each(roles, function (i, role) {
          var role_alias = role.role_alias;
          var role_photo_link = role.role_photo_link;
          var role_img = $(
            '<img src="/assets/photo/' +
              role_photo_link +
              '" width="30px" title="' +
              role_alias +
              '" style="margin:2px 2px 2px 2px">'
          );
          td_role.append(role_img);
        });
        row.append(td_role);

        $("#outlineTable").find("tbody").append(row);
      });

      // document.getElementById("loader-sq").style.display = "none";
    },
    fail: function (json) {
      console.log("fail");
    },
  });
});
