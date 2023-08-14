$(document).ready(function(){
    $('#loadMorecom').on('click',function(){
        var _currentProducts=$('.comment-box').length;
        var _limit=$(this).attr('data-limit');
        var _total=$(this).attr('data-total');

        $.ajax({
            url:"/load_more_data_comment",
            data:{
                limit:_limit,
                offset:_currentProducts
            },
            dataType:'json',
            beforeSend:function(){
                $('#loadMorecom').attr('disabled',true);
                $('.load-more-icon').addClass('fa-spin');
            },
            success:function(res){
                $('#product-reviews-content').prepend(res.data);
                $('#loadMorecom').attr('disabled',false);
                $('.load-more-icon').removeClass('fa-spin');

                var _totalShowing=$('.comment-box').length;
                if(_totalShowing==_total){
                    $('#loadMorecom').remove();
                }
            }
        });
    });
});