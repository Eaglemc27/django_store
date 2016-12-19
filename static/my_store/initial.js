$(function () {
        $.ajax({
            type : "GET",
            url : "product_grid",
            success : function searchSuccess(data, textStatus, jqXHR){
                $('#content').html(data)
            }
        })
    })