;(()=>{
  const navbar = document.querySelector('nav')
  let htmlStr =`
    <div class="container-fluid">
      <div class="navbar-header">
        <a class="navbar-brand" href="/index.html">金律鑫 MES</a>
      </div>
      <ul class="nav navbar-nav">
        <li><a href="/pages/Dashboard_Workitem.html">生產報表</a></li>
        <li><a href="/pages/Dashboard_Prepare.html">製程看板</a></li>
        <li><a href="/pages/Dashboard_Customer.html">客戶資料</a></li>
        <li><a href="/pages/Dashboard_ProcessMethod.html">加工方式</a></li>
        <li><a href="/pages/Dashboard_Test.html">生產看板</a></li>
        <li><a href="/pages/Report_Test.html">生產稼動表</a></li>
        <li><a href="/pages/Dashboard_Tool.html">機台清單報表</a></li>
      </ul>
    </div>
  `
  navbar.innerHTML = htmlStr

  navbar.querySelectorAll('li').forEach(e=>{
    if (e.children[0].href === location.href) {
      e.classList.toggle('active')
    }
  })

})()