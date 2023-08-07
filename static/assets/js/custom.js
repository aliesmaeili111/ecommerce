$(document).ready(function(){
    $('#loadMore').on('click',function(){
        var _currentProducts=$('.product-box').length;
        var _limit=$(this).attr('data-limit');
        var _total=$(this).attr('data-total');

        $.ajax({
            url:"/load-more-data",
            data:{
                limit:_limit,
                offset:_currentProducts
            },
            dataType:'json',
            beforeSend:function(){
                $('#loadMore').attr('disabled',true);
                $('.load-more-icon').addClass('fa-spin');
            },
            success:function(res){
                $('#filteredProducts').append(res.data);
                $('#loadMore').attr('disabled',false);
                $('.load-more-icon').removeClass('fa-spin');

                var _totalShowing=$('.product-box').length;
                if(_totalShowing==_total){
                    $('#loadMore').remove();
                }
            }
        });
    });
});


$(document).on('click','.delete-item',function(){
    var _pId=$(this).attr('data-item');
    var _vm=$(this);
    console.log(_pId);
    $.ajax({
        url: "/delete-cart-item",
        data:{
            'id':_pId,
        },
        dataType: 'json',
        beforeSend:function(){
            _vm.attr('disabled',true);
        },
        success:function(res){
            $('.cart-list').text(res.totalitems);
            _vm.attr('disabled',false);
            $("#cartList").html(res.data);
        }
    });
});