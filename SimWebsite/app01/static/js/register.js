
$(document).ready(function(){
 
    // 开始写 jQuery 代码...
    var login = document.getElementById("account-login-btn");
    var signup = document.getElementById("account-register-btn");
    var account = document.getElementsByClassName("account")[0];


    $(signup).click(function(){

        $(".welcome-mask").css({
            transform:'translateX(100%)',
        });
        $(".content-sheet").css({
            transform:'translateX(-50%)',
        });
    });

    $(login).click(function(){

        console.log("login");
        $(".welcome-mask").css({
            transform:'translateX(0)',
        });
        $(".content-sheet").css({
            transform:'translateX(0)',
        });
    });




    $(".account-input").blur(function(self){
        $(".input-placeholder").removeClass("float-above")
        $(".input-placeholder").addClass("focus-on")
    });
    $(".account-input").blur(function(){
        $(".input-placeholder").removeClass("float-above")
        $(".input-placeholder").addClass("focus-on")
    });


    

  
 });

 