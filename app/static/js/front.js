/*
function searchKey() {
    var keyword = $('.input-group input').val();
    var url = 'http://'+ window.location.host + '/search';
    if (keyword.length>15)
        alert("关键字太多!");
    else
        $.post(url, {'key':keyword});
}
*/


function searchKey() {
    var keyword = $('.input-group input').val();

    location.href = "/search/?keyword=" + encodeURIComponent(keyword)

}

