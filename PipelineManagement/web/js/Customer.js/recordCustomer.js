;(() => {
  const URL = window.location.href
  let isSubmitting = false
  const customer_id = +URL.split('/')[URL.split('/').length - 1]
  // const table = document.getElementById('customer-input-form')
  const input = document.querySelector('input')
  const textareaList = document.querySelectorAll('textarea')
  const submitBtn = document.getElementById("btn-submit")
  const title = document.querySelector('.title')
  let data = {}
  let handleSubmit = null
  const loadInputTOData = () => {
    customer_id
    ? data[input.name] = input.placeholder
    : data[input.name] = input.value
    textareaList.forEach(e => {
      data[e.name] = e.value
    })
  }
  const createCustomer = () => {
    isSubmitting = true
    console.log('add customer')
    loadInputTOData()
    if (!input.value) {
      const form = input.closest('.form-group')
      form.scrollIntoView()
      form.classList.toggle('has-error')
      setTimeout(() => {
        alert('請輸入顧客代號')
        form.classList.toggle('has-error')
        isSubmitting =false
      }, 500)
    }
    $.ajax({
      url: '/addCustomer',
      type: 'POST',
      data,
      dataType: 'json',
      success (json) {
        console.log('success')
        isSubmitting = false
      },
      fail (json) {
        console.log('fail')
        isSubmitting = false
      }
    })
  }
  const updateCustomer = ({ id }) => {
    isSubmitting = true
    console.log('update customer')
    loadInputTOData()
    $.ajax({
      url: `/updateCustomer/${id}`,
      type: 'POST',
      data,
      dataType: 'json',
      success (json) {
        console.log('success')
        isSubmitting = false    
      },
      fail (json) {
        console.log('fail')
        isSubmitting = false

      }
    })
  }
  const getCustomer = ({ id }) => {
    $.ajax({
      url: `/customers/${id}`,
      type: 'GET',
      dataType: 'json',
      success (json) {
        const result = json.results[0]
        data[input.name] = result[input.name]
        input.placeholder = data[input.name]
        textareaList.forEach((e, i) => {
          const { name } = e
          data[name] = result[name]
          e.value = data[name]
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
    // open input
    input.disabled = false
    // create customer 
    handleSubmit = () => {
      createCustomer()
    }
  }

  document.getElementById("btn-submit").onclick = function () {
    if(isSubmitting) return 
    handleSubmit()
  }
  document.getElementById("btn-cancel").onclick = function () {
    location.href = "/pages/Dashboard_Customer.html"
  }
})()