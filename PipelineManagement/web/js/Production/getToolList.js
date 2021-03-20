; (() => {
    let data = []
    const tbody = $("table tbody")
    const fetchUrl = '/testing/getTools/all'
    // const idStr = null
    const PageItemName = 'Tool'
    const showItems = ({ targets }) => {
        const inputCols = [
            'tool_type', 'tool_id', 'tool_name', 'owner', 'update_dt', 'enable'
        ]
        tbody.empty()
        $.each(targets, (i, e) => {
            // const id = e[idStr]
            const tempId = i+1
            const itemUrl = `/pages/${PageItemName}/${tempId}`
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
    filter.querySelector('a').addEventListener('click', () => {
        let toolType = filter.elements[0].value.toLowerCase()
        let keyword = filter.elements[1].value.toLowerCase()
        let targets = data.filter(
            e => e['tool_type'].toLowerCase().includes(toolType)
        )
        targets = targets.filter(e => {
            let matchValues = Object.values(e)
                .filter(v => v 
                    ? v.toLowerCase().includes(keyword)
                    : false
                )
            if(matchValues.length > 0) return true
            return false
        })
        showItems({ targets })
    })
})()
