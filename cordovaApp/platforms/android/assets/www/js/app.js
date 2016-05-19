var BASEURL = "http://192.168.0.14:8000"


function httpr(method, url, callback) {

    var xhr = new XMLHttpRequest();
            
    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200){
            callback(xhr.responseText);
        }
    }
    xhr.open(method, url, true);
    xhr.send();
}

function unicorn(alt) {
	
	var uri = BASEURL+"/unicorn/"+alt
	httpr("GET",uri,function(r){
		console.log(r);
	})
}

function custom() {

	var r = document.getElementById("r").value;
	var g = document.getElementById("g").value;
	var b = document.getElementById("b").value;
	var alt = document.getElementById("blink").alt;

	var uri = BASEURL+"/custom/"+r+"/"+g+"/"+b+"/"+alt
	httpr("GET",uri,function(r){
		console.log(r);
	})
}

function reset() {

	var uri = BASEURL+"/reset"
	httpr("GET",uri,function(r){
		console.log(r);
	})
}
document.getElementById("uniAlt").addEventListener("input", function(){unicorn(this.value);}, false);

document.getElementById("r").addEventListener("input", custom, false);
document.getElementById("g").addEventListener("input", custom, false);
document.getElementById("b").addEventListener("input", custom, false);

document.getElementById("blink").alt = 0;
document.getElementById("blink").addEventListener("click", function(){this.alt = this.alt ? 0 : 1 ; custom();}, false);

document.getElementById("reset").addEventListener("click", reset, false);
