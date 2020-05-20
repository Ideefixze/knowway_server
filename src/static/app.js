var interval = 5000;  // 1000 = 1 second, 3000 = 3 seconds
function doAjax() {
    $.ajax({
            type: 'POST',
            url: '/addPoints',
            data: {link:window.location.href,time:"1"},
            dataType: 'text',
            success: function (data) {
                document.getElementById("points").innerHTML=data; 
            },
            complete: function (data) {
                setTimeout(doAjax, interval);
            }
    });
}
setTimeout(doAjax, interval);