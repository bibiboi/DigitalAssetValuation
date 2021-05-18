

function ScrollToControl(position)
{
 
 var scrollPos = position;
 scrollPos = scrollPos - document.documentElement.scrollTop;
 var remainder = scrollPos % 50;
 var repeatTimes = (scrollPos - remainder) / 50;
 ScrollSmoothly(scrollPos,repeatTimes);
 window.scrollBy(0,remainder);
}

var repeatCount = 0;
var cTimeout;
var timeoutIntervals = new Array();
var timeoutIntervalSpeed;

function ScrollSmoothly(scrollPos,repeatTimes)
{
 if(repeatCount < repeatTimes)
 {
 window.scrollBy(0,50);
 }
 else
 {
 repeatCount = 0;
 clearTimeout(cTimeout);
 return;
 }
repeatCount++;
cTimeout = setTimeout("ScrollSmoothly('"+scrollPos+"','"+repeatTimes+"')",20);
}

function process(){
	console.log(1);
	window.location.href="processed.html";
}