var prevsong=0;
var data_currentsong="";

function on_load() {
    elapsed_time();
}

function my_ajax() {
    get_currentsong();
}

function get_currentsong() {
    if(typeof(data_currentsong) != 'undefined' && typeof(data_currentsong.pos) != 'undefined') {
	prevsong=data_currentsong.pos;
    }
    $.get("/currentsong",function(data,status) {
	data_currentsong=JSON.parse(data);
	set_current_song();
    });
}

function my_get(url) {
    $.get(url, function(data, status) {
	alert("Data: " + data);
    });
}

function previous() {
    my_post("/command/previous");
    get_currentsong();
}

function next() {
    my_post("/command/next");
    get_currentsong();
}

function play() {
    if (data_currentsong.state == 'play') {
	my_post("/command/pause");
    } else {
	my_post("/command/play");
    }
}

function my_post(url) {
    $.post(url, function(data, status) {
	return data;
    });
}

function elapsed_time() 
{
    get_currentsong();
    t=setTimeout(function(){elapsed_time()},1000);
}

function set_current_song() {
    document.getElementById("playlist_row_" + prevsong).setAttribute("class", "playlist");
    document.getElementById("playlist_row_" + data_currentsong.pos).setAttribute("class", "playing");
    var title=data_currentsong.title;
    var album=data_currentsong.album;
    document.getElementById("current_title").innerHTML=title;
    document.getElementById("current_album").innerHTML=album;
    set_time("length", data_currentsong.length);
    set_time("elapsed", data_currentsong.elapsed);
}

function set_time(element, l) {
    var s=Math.floor(l % 60);
    var m=Math.floor(l / 60); 
    s=checkTime(s);
    document.getElementById(element).innerHTML=m+":"+s;
}

function checkTime(i)
{
    if (i<10)
    {
	i="0" + i;
    }
    return i;
}
