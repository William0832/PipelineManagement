;(() => {
  const URL = window.location.href
  const customer_id = +URL.split('/')[URL.split('/').length - 1]
  const table = document.getElementById('customer-input-form')
  const submitBtn = document.getElementById("btn-submit")
  const title = document.querySelector('.title')

  let handleSubmit = null
  const addCustomer = () => {
    console.log('add customer')
    const data = {}
    Array.from(table.children).forEach(e => {
      let input = e.querySelector('input') || e.querySelector('textarea')
      const { name, value } = input
      data[name] = value
    })
    // console.log(data)
    $.ajax({
      url: '/addCustomer',
      type: 'POST',
      data,
      dataType: 'json',
      success (json) {
        console.log('success')
      },
      fail (json) {
        console.log('fail')
      }
    })
  }
  const updateCustomer = ({ id }) => {
    console.log('update customer')
    const data = {}
    Array.from(table.children).forEach(e => {
      let input = e.querySelector('input') || e.querySelector('textarea')
      const { name, value } = input
      data[name] = value
    })
    $.ajax({
      url: `/updateCustomer/${id}`,
      type: 'POST',
      data,
      dataType: 'json',
      success (json) {
        console.log('success')
      },
      fail (json) {
        console.log('fail')
      }
    })
  }
  const getCustomer = ({ id }) => {
    console.log('get customer')
    const table = document.getElementById('customer-input-form')
    $.ajax({
      url: `/customers/${id}`,
      type: 'GET',
      dataType: 'json',
      success (json) {
        const [data] = json.results
        Array.from(table.children).forEach((e, i) => {
          const input = e.querySelector('input') || e.querySelector('textarea')
          const { name } = input
          input.value = data[name]
        })
      },
      fail (json) {
        console.log('fail')
      }
    })
  }
  if (customer_id) {
    // update customer
    const str = '更新客戶資料'
    title.innerText = str
    submitBtn.innerText = str
    getCustomer({ id: customer_id })
    handleSubmit = () => {
      updateCustomer({ id: customer_id })
    }
  } else {
    // create customer 
    handleSubmit = () => {
      addCustomer()
    }
  }

  document.getElementById("btn-submit").onclick = function () {
    handleSubmit()
  }
  document.getElementById("btn-cancel").onclick = function () {
    location.href = "/pages/Dashboard_Customer.html"
  }
})()