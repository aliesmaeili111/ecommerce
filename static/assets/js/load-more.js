$(document).ready(function(){
    $('#loadMore').on('click',function(){
        var _currentProducts=$('.blog-box').length;
        var _limit=$(this).attr('data-limit');
        var _total=$(this).attr('data-total');

        $.ajax({
            url:"load_more_data_blog",
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

                var _totalShowing=$('.blog-box').length;
                if(_totalShowing==_total){
                    $('#loadMore').remove();
                }
            }
        });
    });
});