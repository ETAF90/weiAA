function login(o) {

    window.location.href="get_access_token";
}
function logout() {
    if(confirm('确认退出weiAA？'))
    {
        window.location.href="logout";
    }
}

$(document).ready(function () {

    $('#show_act_panel_a').click(function () {
        $('#act_panel_b').hide();
        $('#act_panel_a').show();
    });
    $('#show_act_panel_b').click(function () {
        $('#act_panel_a').hide();
        $('#act_panel_b').show();
    });
    $('.etaf_vote_btn').click(function(){

        if(confirm("确认投票？")){
            plan_id = $(this).attr('id');
            plan_id = plan_id.slice(9);
            vote_btn_id = '#vote_btn_'+plan_id;
            vote_num_id = '#vote_num_'+plan_id;
            $.getJSON('/ajax_vote?plan_id='+plan_id, function(data){
                alert(data.message);
                $(vote_btn_id).attr('disabled','true');
                $(vote_num_id).html("票数："+data.vote_num);
            })
        }
    });

    $('.etaf_remind_join_btn').click(function(){

        member_id = $(this).attr('id');
        member_id = member_id.slice(21);
        act_id = $(this).attr('act_id');

        if(confirm("再提醒一遍?")){
            $.getJSON('/ajax_remind_join?member_id='+member_id+'&act_id='+act_id,function(data){
                alert(data.member_id+"\n"+data.message);
                $('#etaf_remind_join_btn_'+member_id).attr('disabled','true');
            })
        }
    });
    $('.etaf_remind_fee_btn').click(function(){

        member_id = $(this).attr('id');
        member_id = member_id.slice(20);
        act_id = $(this).attr('act_id');

        if(confirm("再提醒一遍?")){
            $.getJSON('/ajax_remind_fee?member_id='+member_id+'&act_id='+act_id,function(data){
                alert(data.member_id+"\n"+data.message);
                $('#etaf_remind_fee_btn_'+member_id).attr('disabled','true');
            })
        }
    });


    $('.etaf_remove_member_btn').click(function(){

        member_id = $(this).attr('id');
        member_id = member_id.slice(23);
        act_id = $(this).attr('act_id');
        if(confirm("确定删除该成员？")){
            $.getJSON('/ajax_remove_member?member_id='+member_id+'&act_id='+act_id,function(data){
                alert(data.member_id+"\n"+data.message);
                $('#tr_member_'+act_id+'_'+member_id).empty();
            })
        }
    });

    $('.etaf_finish').click(function(){
        act_id = $(this).attr('id');
        act_id = act_id.slice(11);
        if(confirm("确认已全部缴费并结束活动"))
        {
            window.location.href="finish_act?act_id="+act_id;
        }
    })
    $('.etaf_confirm_fee_btn').click(function(){
        etaf_confirm_fee_btn_id = $(this).attr('id');
        member_id  = $(this).attr('id');
        member_id  = member_id.slice(21);
        act_id  = $(this).attr('act_id');
        pay_flag_id = "#pay_flag_"+member_id;

        if(confirm("确认此参与者已缴费？"))
        {
            $.getJSON('ajax_confirm_fee?act_id='+act_id+'&member_id='+member_id,function(){
                alert("已确认该参与者缴费！");
                $(pay_flag_id).html("Yes");
                $(pay_flag_id).removeClass(" label-default");
                $(pay_flag_id).addClass("label-success");
                $('#'+etaf_confirm_fee_btn_id).attr('disabled','true');
            })
            //window.location.href="confirm_fee?act_id="+act_id+"&member_id="+member_id;
        }
    })
});
