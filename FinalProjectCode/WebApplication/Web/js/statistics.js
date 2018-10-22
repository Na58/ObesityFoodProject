var url = "http://18.216.214.90:5000/";
//var url = "/json/"

var api1 = url+"food_obesity";
var api2 = url+"obesity";
var api3 = url+"food";

function compare(a,b){
  if (a[0] < b[0])
    return -1;
  if (a[0] > b[0])
    return 1;
  return 0;
}

function getData(url){
  $.ajax({
    type:'GET',
    url:url,
    dataType:'json',
    //data:{cmd:'coordinates'},
    //这里是ajax正常的做法 异步收到数据再渲染数据
    //这是js的坑 正常来说代码都是顺序执行的
    success:function(data){
      adult =  data.adult.sort(compare)
      child = data.child.sort(compare)
      renderAdult(adult)
      $("#adult-btn").click(function(){
        renderAdult(adult)
      })

      $("#child-btn").click(function(){
        renderChild(child)
      })
    }
  });
}

function renderAdult(adult){
var x = []
var y = []
$.each(adult,function(i,item){
  x.push(item[0])
  y.push(item[1])
})
var ctx = document.getElementById("chart1").getContext("2d");
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: x,
        datasets: [{
            label: 'Adult Obesity - Takeaway Food',
            data: y,
            borderColor: "rgb(75, 192, 192)",
            showLine:false
        }]
    },
});
}

function renderChild(child){
var x = []
var y = []
$.each(child,function(i,item){
  x.push(item[0])
  y.push(item[1])
})
var ctx = document.getElementById("chart1").getContext("2d");
var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: x,
        datasets: [{
            label: 'Child Obesity - Takeaway Food',
            data: y,
            borderColor: "#FF6384",
            showLine:false
        }]
    },
});
}
function getData2(url){
  $.ajax({
    type:'GET',
    url:url,
    dataType:'json',
    //data:{cmd:'coordinates'},
    success:function(data){
      renderBar(data.obesity_count)
    }
  });
}
function renderBar(data){
var a = []
var b = []
var c = []
$.each(data,function(i,item){
  a.push(item[0])
  b.push(item[1])
  c.push(item[2])
})
var ctx = document.getElementById("chart2").getContext("2d");
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: a,
        datasets: [{
            label: 'Child',
            data: b,
            backgroundColor: "#FF6384",

        },{
          label:'Adult',
          data:c,
          backgroundColor:"#36A2EB",
        }]
    },
});
}

function getData3(url){
  $.ajax({
    type:'GET',
    url:url,
    dataType:'json',
    //data:{cmd:'coordinates'},
    success:function(data){
      renderBar3(data.food_count)
    }
  });
}
function renderBar3(data){
var a = []
var b = []
$.each(data,function(i,item){
  a.push(item[0])
  b.push(item[1])
})
var ctx = document.getElementById("chart3").getContext("2d");
var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: a,
        datasets: [{
            label: 'Takeaway Food',
            data: b,
            backgroundColor: "#FF6384",
        },]
    },
});
}



$(document).ready(function() {
  //安全的做法 保证页面加载完 在执行函数
  getData(api1)
  getData2(api2)
  getData3(api3)
});
