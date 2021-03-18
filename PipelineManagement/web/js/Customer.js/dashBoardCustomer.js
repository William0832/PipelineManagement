;(() => {
  let data = []
  const tbody = $('#custom-table__content')

  const showCustomer = (targets) => {
    if(targets.length > 0) {
      tbody.empty()
      const inputCols = ['customer', 'testing', 'markpoint', 'stamp', 'package', 'contact']
      $.each(targets, (i, e) => {
        const { customer_id } = e
        const row = $('<tr>')
        row.append($('<a>').attr("href", `/pages/Dashboard_Customer/${customer_id}`).attr("target", "_blank")
          .append($('<span>')
            .addClass("glyphicon glyphicon-edit")
            .css("margin-top", "3px")))

        inputCols.forEach(col => {
          let text = e[col]
            ? e[col]
            : '-'
          row.append($('<td>').text(text))
        })
        tbody.append(row)
      })
      return
    }
    tbody.empty()
  }

  $.ajax({
    url: '/customers',
    type: 'GET',
    dataType: 'json',
    success (json) {
      const inputCols = ['customer', 'testing','markpoint','stamp','package','contact']
      data = json.results
      $.each(json.results, (i, e) => {
        // console.log(i,e)
        const { customer_id } = e
        const row = $('<tr>')
        row.append($('<a>').attr("href", `/pages/Dashboard_Customer/${customer_id}`).attr("target", "_blank")
          .append($('<span>')
          .addClass("glyphicon glyphicon-edit")
          .css("margin-top", "3px")))

        inputCols.forEach(col => {
          let text = e[col] 
            ? e[col]
            : '-'
          row.append($('<td>').text(text))
        })
        tbody.append(row)
      })
    },
    fail (json) { console.log("fail") }
  })
  let input = document.getElementById('search-customer-input')
  let searchBtn = document.querySelector('button.search')
  searchBtn.addEventListener('click',() => {
    let str = input.value.toLowerCase()
    const targets = data.filter(e => 
      e.customer &&
      e.customer.toLowerCase().includes(str)
    )
    showCustomer(targets)
  })
})()