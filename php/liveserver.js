{/* 
Auto Refresh Page Contents using Javascript
Source: StackOverflow
<script type="text/javascript" src="liveserver.js"></script> 
*/}

window.addEventListener('load', function () {
    var xhr = null;

    function nap(time) {
        return new Promise((resolve) => setTimeout(resolve, time));
    };

    getXmlHttpRequestObject = function () {
        if (!xhr) {
            xhr = new XMLHttpRequest();
        }
        return xhr;
    };

    updateLiveData = function () {
        nap(3 * 1000).then(() => { // 3*1000 = 3 Seconds
            var d = new Date();
            var url = "?" + d.getTime();
            xhr = getXmlHttpRequestObject();
            xhr.onreadystatechange = evenHandler;
            xhr.open("GET", url, true);
            xhr.send(null);
        });
    };

    updateLiveData();

    function evenHandler() {
        if (xhr.readyState == 4 && xhr.status == 200) {
            document.body.innerHTML = xhr.responseText;
            setTimeout(updateLiveData(), 1000);
        }
    }
});