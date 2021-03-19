; (async () => {
  const testStyleData = [
    {
      name: 'FLY飛針',
      value: 'FLY',
      testStyleData: [
        {
          name: '指定飛針ATG-S3',
          value: '指定飛針ATG-S3'
        }, {
          name: '指定飛針ATG-機台',
          value: '指定飛針ATG-機台'
        }
      ]
    },
    {
      name: 'EZG萬用',
      value: 'EZG',
      testStyleData: [
        {
          name: 'EZG代鑽',
          value: 'EZG代鑽'
        }, {
          name: 'EZG9層',
          value: 'EZG9層'
        },
        {
          name: 'EZG18層',
          value: 'EZG18層'
        }
      ]
    },
    {
      name: 'ATG萬用',
      value: 'ATG',
      testStyleData: [
        {
          name: 'ATG兩倍密',
          value: 'ATG兩倍密'
        }, {
          name: 'TAG兩倍密大治具',
          value: 'TAG兩倍密大治具'
        }
      ]
    },
    {
      name: 'LM1000萬用',
      value: 'LM1000',
      testStyleData: [
        {
          name: '單部測試',
          value: '單部測試',
        }, {
          name: '多部測試',
          value: '多部測試',
        }, {
          name: 'AB套測試',
          value: 'AB套測試',
        }
      ]
    }
  ]

  const inputEls = [
    ...document.querySelectorAll('input'),
    ...document.querySelectorAll('select')
  ]
  let btnCopy = document.getElementById("btn-copy-workitem")
  const btnSubmit = document.getElementById("btn-submit-workitem")
  let data = {}
  const testStyleWrapper = document.querySelector('.test-style-wrapper')
  const addWorkitem = () => {
    console.log('add click')
    customer_id = document.getElementById("customer_id").value
    part_no = document.getElementById("part_no").value
    lot_no = document.getElementById("lot_no").value
    creator = document.getElementById("creator").value
    test_style = document.getElementById("test_style").value

    $.ajax({
      url: '/addWorkitem',
      type: 'POST',
      data: {
        customer_id: customer_id,
        part_no: part_no,
        lot_no: lot_no,
        creator: creator,
        test_style: test_style
      },
      dataType: 'json',
      success: function (json) {
        if (json.result != "success") {
          console.log(json)
          console.log("Update detail")
          console.log(json)
          alert(json.message)
          location.reload()

        } else {
          console.log("Update detail")
          console.log(json)

          alert(json.message)

          location.href = "/pages/Dashboard_Prepare.html"
        }
      }
    })
  }
  const copyWorkitem = () => {
    console.log('copyWorkitem')
  }
  const getWorkitem = async ({ id }) => {
    await $.ajax({
      url: `/workitem/${id}`,
      method: 'GET',
      dataType: 'json',
      success (json) {
        data = { ...json.results[0] }
        console.log(data)
        console.log('success')
      },
      fail (json) {
        console.log('fail')
      }
    })
  }
  const addTestOptions = (targetId) => {
    let htmlStr = ''
    let testStyle = document.getElementById(targetId)
    let list = targetId === 'test_style'
      ? testStyleData
      : testStyleData.find(e => e.value === data['test_style']).testStyleData
    list.forEach(e => {
      htmlStr += `<option value="${e.value}"> ${e.name} </option>`
      data[targetId] = e.value
    })
    testStyle.innerHTML = htmlStr
  }
  const showWorkitem = () => {
    inputEls.forEach(e => {
      const key = e.id
        ? e.id
        : null
      if (key) {
        e.value = data[key]
      }
      // e.disabled = true

    })
  }
  const addOptionsInProcessMethods = async () => {
    await $.ajax({
      url: '/workitemProcessMethods',
      type: 'GET',
      datatype: 'json',
      success (json) {
        console.log('fetch workitemProcessMethods success')
        let methods = json.results
        let selectEl = document.getElementById('workitem-process-method')
        let htmlStr = ''
        methods.forEach(e => {
          htmlStr += `<option value="${e.method_id}">${e.method_name}</option>`
        })
        selectEl.innerHTML = htmlStr
      },
      fail (json) {
        console.log('fail')
        return null
      }
    })
  }
  const URL = window.location.href
  const work_item_id = +URL.split('/')[URL.split('/').length - 1]

  addOptionsInProcessMethods()
  addTestOptions('test_style')
  addTestOptions('test_style_sec')
  if (work_item_id) {
    // show detail
    btnSubmit.disabled = true
    await getWorkitem({ id: work_item_id })
    showWorkitem()
  } else {
    // create new 
    btnCopy.style.display = 'none'
  }

  if (btnCopy.style.display !== 'none') {
    btnCopy.onclick = () => {
      copyWorkitem()
    }
  }
  btnSubmit.onclick = () => {
    addWorkitem()
  }
  document.getElementById("btn-cancel").onclick = function () {
    location.href = "/pages/Dashboard_Workitem.html"
  }

  let testStep = document.getElementById('test-step')
  testStyleWrapper.addEventListener('change', (e) => {
    let target = e.target
    if (target.id === 'test_style') {
      data[target.id] = target.value
      addTestOptions('test_style_sec')
      if (data[target.id] !== 'lLM1000') {
        testStep.disabled = true
        testStep.value = 0

      } else {
        testStep.disabled = false
      }
    } else if (target.id === 'test_style_sec') {
      data[target.id] = target.value
      if (data['test_style'] === 'LM1000' && target.value !== 'AB套測試') {
        testStep.disabled = false
      } else {
        testStep.disabled = true
        testStep.value = 0

      }
    } else if (target.id === 'test-step') {
      data[target.id] = target.value
    }
  })
})()