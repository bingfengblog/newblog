function replyto(id, user)
{
    document.getElementById("reply_to_user").innerHTML = "回复：<span style='color:#2099AB; font-weight: bold;'>" + user + "</span>&nbsp;<a href='#reply_to_user' onclick='cancelreply()' style='color: #BABABA;text-decoration: none;'>(撤消)</a>";
    document.getElementById("reply_to_comment").value = id;
}

function cancelreply()
{
    document.getElementById("reply_to_user").innerHTML = "";
    document.getElementById("reply_to_comment").value = "";
}


var timer_to_top, timer_to_bottom;

function GoTop(){
    timer_to_top = setInterval("RunToTop()", 10);  
}

function RunToTop(){  
    currentPosition  = document.documentElement.scrollTop || document.body.scrollTop;
    scrollHeight     = Math.min(document.body.scrollHeight, document.documentElement.scrollHeight);
    clientHeight     = Math.min(document.body.clientHeight, document.documentElement.clientHeight);
    currentPosition-=clientHeight;
    if(currentPosition > 0)
    {
        window.scrollTo(0, currentPosition);  
    }
    else
    {
        window.scrollTo(0, 0);
        clearInterval(timer_to_top);
    }  
}
function GoBottom(){
    timer_to_bottom = setInterval("RunToBottom()", 10);
}
function RunToBottom(){
    currentPosition  = document.documentElement.scrollTop || document.body.scrollTop;
    scrollHeight     = Math.min(document.body.scrollHeight, document.documentElement.scrollHeight);
    clientHeight     = Math.min(document.body.clientHeight, document.documentElement.clientHeight);
    currentPosition+=clientHeight;
    
    if (currentPosition < scrollHeight)
    {
        window.scrollTo(0, currentPosition);
    }
    else
    {
        clearInterval(timer_to_bottom);
    }
}

function loadall(id){
  $.ajax({
      type: "POST",
      url: "/blog/"+id+"/",
      data: {
           'ajax_id': id,
      },
      success: function(data){
    	  $("#"+id).html(data)
    	  $("#link_"+id).hide()
      },
      error: function(XMLHttpRequest, textStatus, errorThrown){
    	  alert("IS Error: " + errorThrown + XMLHttpRequest.responseText); 
      },
   });
   
}












