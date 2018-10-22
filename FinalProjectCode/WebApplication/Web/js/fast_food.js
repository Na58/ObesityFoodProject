var map;
var local_json = 'http://localhost:3000/GEO.json'
var remote_json = 'http://18.216.214.90:5000/GEO.json'

function initMap() {
  map = new google.maps.Map(document.getElementById('map'),{
    zoom: 4,
    center: {lat: -28, lng: 137}
  });

  map.data.loadGeoJson(remote_json);
  map.data.setStyle(function(feature){
    var color = feature.getProperty('color');
    var op = feature.getProperty('food_op');
    return {
      fillColor: color,
      fillOpacity: op,
      strokeWeight: 1
    };
  });
  map.data.addListener('mouseover', function(event) {
    var name = event.feature.getProperty('name');
    console.log(name);
    document.getElementById('tooltiptext').textContent = "Currently at: \n" + name;
    return {visible:true};
  });
}
/*
var arr = []
var locale = []
var url = "http://18.216.214.90:5000/locale";

function getData(){
  $.ajax({
    type:'GET',
    url:url,
    dataType:'json',
    //这里用了async同步的代码 因为要多次去拿数据 避免代码写的你看不懂
    //这是js的坑 需要会调来一个函数来响应请求
    //你可以直接用flask的代码把数据写在页面上存在一个变量里面
    //就不用使用ajax去多次拿数据了 也不用搞什么跨域的问题啦
    async:false,
    //data:{cmd:'coordinates'},
    success:function(data){
      arr = data.locale_list
    }
  });
  //arr = [20000,20002];
  //你的服务器不行 我自己下载了两份数据 然后就可以继续开发了。
  //你用的时候要把这里注释掉
  $.each(arr,function(i,item){
    $.ajax({
      type:'GET',
      url:url + '/' + item + '/ob',
      //url:'json/'+item,
      dataType:'json',
      async:false,
      success:function(data){
        var o = {}
        //需要学习下python的dict 你这里最好把数据整理好再输出
        //看我下面乱写一堆来拆解你的数据的 丑陋～～
        o.number = Object.keys(data)[0];
        o.name = Object.values(data)[0][0];
        o.obesity = Object.values(data)[0][2]
        var coords = Object.values(data)[0][1]
        var c = []

        $.each(coords,function(i,item){
          var o = {}
          o.lat = item[1]
          o.lng = item[0]
          c.push(o)
        })
        o.coords = c
        locale.push(o)
      }
    })
  })
}
getData()
//这里找不到去哪拿肥胖率的数据了  我自己瞎编一个
//在地图里面那个 fillOpacity 是控制透明度的 用这个值除以100就好了
//locale[0].obesity = 80.4
//locale[1].obesity = 40.5
console.log(locale)
//locale = locale.slice(0,3)

function initMap() {
	var map = new google.maps.Map(document.getElementById('map'), {
		zoom: 11,
		center: {lat: -37.815018, lng: 144.946014},
		mapTypeId: 'terrain'
	});

  $.each(locale,function(i,item){
    var city = new google.maps.Polygon({
      paths:item.coords ,
      strokeColor: '#FF0000',
      strokeOpacity: 0,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: item.obesity/100
    });
    city.setMap(map);

  })
}
*/
