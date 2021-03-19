;(() => {
  let data = []
  const tbody = $("#dashboard-table__content")
  const fetchUrl = '/processMethods'
  const idStr = 'method_id'
  const PageItemName = 'ProcessMethod'
  const showItems = ({ targets }) => {
    if (targets.length > 0) {
      tbody.empty()
      const inputCols = [
        'method_name', 'method_description'
      ]
      $.each(targets, (i, e) => {
        const id = e[idStr]
        const itemUrl = `/pages/Record_${PageItemName}/${id}`
        const row = $("<tr>")
        const btn = $("<a>")
          .attr("href", itemUrl)
          .attr("target", "_blank")
          .attr("class", "btn btn-primary")
          .text("編輯")
        row.append($("<td>").append(btn));
        inputCols.forEach((col) => {
          const text = e[col] ? e[col] : "-"
          row.append($("<td>").text(text))
        });
        tbody.append(row)
      })
    }
  }

  $.ajax({
    url: fetchUrl,
    type: "GET",
    dataType: "json",
    success (json) {
      data = json.results;
      showItems({ targets: data });
    },
    fail (json) {
      console.log("fail");
    },
  })
  // Filter 
  // let input = document.getElementById("search-input")
  // let searchBtn = document.querySelector("button.search")
  // searchBtn.addEventListener("click", () => {
  //   let str = input.value.toLowerCase();
  //   const targets = data.filter(
  //     (e) => e.customer && e.customer.toLowerCase().includes(str)
  //   );
  //   showItems({ targets })
  // })
})()
