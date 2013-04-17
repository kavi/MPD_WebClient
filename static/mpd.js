var MPD = {};

MPD.prevsong=0;
MPD.data_currentsong="";

MPD.on_load = function() {
    MPD.update();
    MPD.get_collection();
}

MPD.get_currentsong = function() {
    if(typeof(MPD.data_currentsong) != 'undefined' && typeof(MPD.data_currentsong.pos) != 'undefined') {
	MPD.prevsong=MPD.data_currentsong.pos;
    }
    $.get("/currentsong",function(data,status) {
	MPD.data_currentsong=JSON.parse(data);
	set_current_song();
    });
}

MPD.get_collection = function() {
    $.get("/collection",function(data,status) {
	MPD.collection = JSON.parse(data);
//	$("#collection").append("Collection");
//	$("#collection").append(MPD.collection);
	var new_table=$('<table id="tbl_collection"></table>');
	$("#collection").append(new_table);
	for (i = 0;i < MPD.collection.length;i++) {
	    song = MPD.collection[i];
	    var new_row=$('<tr id="tbl_collection_' + i + '"></tr>');
	    new_row.append('<td>' + song.title + '</td>').append('<td>' + song.album + '</td>').append('<td>' + song.artist + '</td>');
	    $("#tbl_collection").append(new_row);
//	    $("#collection").append(song.title);
	}
    });
}

function previous() {
    my_post("/command/previous");
}

function next() {
    my_post("/command/next");
}

function play() {
    if (MPD.data_currentsong.state == 'play') {
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

MPD.update = function() {
    MPD.get_currentsong();
//    t=setTimeout(function(){MPD.update()},1000);
}

function set_current_song() {
    document.getElementById("playlist_row_" + MPD.prevsong).setAttribute("class", "playlist");
    document.getElementById("playlist_row_" + MPD.data_currentsong.pos).setAttribute("class", "playing");
    var title=MPD.data_currentsong.title;
    var album=MPD.data_currentsong.album;
    document.getElementById("current_title").innerHTML=title;
    document.getElementById("current_album").innerHTML=album;
    set_time("length", MPD.data_currentsong.length);
    set_time("elapsed", MPD.data_currentsong.elapsed);
}

function set_time(element, t) {
    var s=Math.floor(t % 60);
    var m=Math.floor(t / 60); 
    s=zero_pad(s);
    document.getElementById(element).innerHTML=m+":"+s;
}

function zero_pad(i)
{
    if (i<10)
    {
	i="0" + i;
    }
    return i;
}
