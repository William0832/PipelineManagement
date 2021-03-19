(() => {
  let data = [];
  const tbody = $("#dashboard-table__content");

  const showCustomer = ({ targets }) => {
    if (targets.length > 0) {
      tbody.empty();
      const inputCols = [
        "customer",
        "testing",
        "markpoint",
        "stamp",
        "package",
        "contact",
      ];
      $.each(targets, (i, e) => {
        const { customer_id } = e;
        const row = $("<tr>");
        const btn = $("<a>")
          .attr("href", `/pages/Record_Customer/${customer_id}`)
          .attr("target", "_blank")
          .attr("class", "btn btn-primary")
          .text("編輯");
        row.append($("<td>").append(btn));
        inputCols.forEach((col) => {
          const text = e[col] ? e[col] : "-";
          row.append($("<td>").text(text));
        });
        tbody.append(row);
      });
    }
  };

  $.ajax({
    url: "/customers",
    type: "GET",
    dataType: "json",
    success(json) {
      data = json.results;
      showCustomer({ targets: data });
    },
    fail(json) {
      console.log("fail");
    },
  });
  let input = document.getElementById("search-customer-input");
  let searchBtn = document.querySelector("button.search");
  searchBtn.addEventListener("click", () => {
    let str = input.value.toLowerCase();
    const targets = data.filter(
      (e) => e.customer && e.customer.toLowerCase().includes(str)
    );
    showCustomer({ targets });
  });
})();
