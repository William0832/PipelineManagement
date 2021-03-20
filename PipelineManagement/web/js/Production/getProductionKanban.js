$(function () {
  let data = []
  const showWorkitems = (data) => {
    $.each(data, function (i, result) {
      const { work_item_id } = result
      var test_type = result.test_type
      var date = result.create_dt
      var category = result.test_style
      var customer = result.customer_id
      var part_no = result.part_no
      var lot_no = result.lot_no
      var units = result.units
      var process = result.process
      var status = result.status
      // var remark = result.remark;
      // var scene_class = "label label-default";

      var row = $('<tr>')
      row.append(
        $('<a>')
          .attr('href', `/pages/workitem/${work_item_id}`)
          .attr('target', '_blank')
          .attr('class', 'btn btn-primary')
          .text('檢視')
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
  }
  const workitemsFilter = () => {
    let partNoInput = document.getElementById('part-no-input').value.toLowerCase()
    let customerInput = document.getElementById('customer-input').value.toLowerCase()
    let copyData = JSON.parse(JSON.stringify(data))
    console.log(data)
    result = Array.from(copyData).filter(e => {
      let partNoValue = e['part_no'].toLowerCase()
      let customerValue =e['customer_id'].toLowerCase()
      return partNoValue.includes(partNoInput) && customerValue.includes(customerInput)
    })
    showWorkitems(result)
  }
  console.log('Get Putline')
  $.ajax({
    url: '/workitem/getWorkitems',
    type: 'GET',
    dataType: 'json',
    success: function (json) {
      data = [...json.results]
      showWorkitems(data)
    },
    fail: function (json) {
      console.log('fail')
    },
  })
  document.querySelector('.btn-search').addEventListener('click', () => {
    workitemsFilter()
  })
})
