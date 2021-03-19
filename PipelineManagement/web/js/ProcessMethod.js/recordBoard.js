; (() => {
  const URL = window.location.href
  const idStr = 'method_id'
  const PageItemName = 'ProcessMethod'
  let isSubmitting = false
  const targetId = +URL.split('/')[URL.split('/').length - 1]

  // const table = document.getElementById('customer-input-form')
  const input = document.querySelector('input')
  const textareaList = document.querySelectorAll('textarea')
  const submitBtn = document.getElementById('btn-submit')
  const deleteBtn = document.getElementById('btn-delete')
  const title = document.querySelector('.title')
  let data = {}
  let handleSubmit = null
  const loadInputToData = () => {
    data[input.name] = input.value
    textareaList.forEach((e) => {
      data[e.name] = e.value
    })
  }
  const createItem = () => {
    isSubmitting = true
    console.log('add customer')
    loadInputToData()

    if (!input.value) {
      const form = input.closest('.form-group')
      form.scrollIntoView()
      form.classList.toggle('has-error')
      setTimeout(() => {
        alert('請輸入顧客代號')
        form.classList.toggle('has-error')
        isSubmitting = false
      }, 500)
      return 
    }
    console.log(data)
    $.ajax({
      url: '/processMethods/create',
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
      },
    })
  }
  const updateItem = ({ id }) => {
    isSubmitting = true
    console.log('update')
    loadInputToData()
    if (!input.value) {
      const form = input.closest('.form-group')
      form.scrollIntoView()
      form.classList.toggle('has-error')
      setTimeout(() => {
        alert('請輸入加工方式')
        form.classList.toggle('has-error')
        isSubmitting = false
      }, 500)
      return
    }
    console.log(data)
    $.ajax({
      url: `/processMethods/update/${id}`,
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
      },
    })
  }
  const deleteItem = ({ id }) => {
    isSubmitting = true
    console.log('delete')
    console.log(data)
    $.ajax({
      url: `/processMethods/delete/${id}`,
      type: 'GET',
      dataType: 'json',
      success (json) {
        console.log('success')
        isSubmitting = false
      },
      fail (json) {
        console.log('fail')
        isSubmitting = false
      },
    })
  }
  const getItem = ({ id }) => {
    $.ajax({
      url: `/processMethods/${id}`,
      type: 'GET',
      dataType: 'json',
      success (json) {
        const result = json.results[0]
        data[input.name] = result[input.name]
        input.value = data[input.name]
        textareaList.forEach((e, i) => {
          const { name } = e
          data[name] = result[name]
          e.value = data[name]
        })
      },
      fail (json) {
        console.log('fail')
      },
    })
  }
  if (targetId) {
    // update customer
    const str = '更新加工方式'
    title.innerText = str
    submitBtn.innerText = str
    getItem({ id: targetId })
    handleSubmit = () => {
      updateItem({ id: targetId })
    }
  } else {
    // open input
    // create customer
    deleteBtn.style.display='none'
    handleSubmit = () => {
      createItem()
    }
  }
  deleteBtn.onclick = () => {
    if (isSubmitting) return
    deleteItem({ id: targetId })
  }
  submitBtn.onclick = function (e) {
    if (isSubmitting) return
    handleSubmit()    
  }
  document.getElementById('btn-cancel').onclick = function () {
    location.href = `/pages/Dashboard_${PageItemName}.html`
  }
})()
