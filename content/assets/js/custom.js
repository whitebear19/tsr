jQuery(function ($) {

    'use strict';
    
   
// ----------------------------------------------------------------
   


    (function() {

        var currentPage = 1;
        var pagenum = 1;     

        
       $(document).on('click','.btn_create_ticket',function()
       {            
            var checkvalid = true;       
            $(".required").each(function(){
                if($(this).val() == "")
                {                        
                    $(this).addClass('alertborder');
                    checkvalid = false;
                }
            });
            
            if(checkvalid)
            {
                var data = $("#form_ticket").serialize();
                $.ajax({
                    url: "/store",
                    method: 'post',
                    type: 'json',
                    data: data,
                    success: function(response) 
                    {
                        if(response.results)
                        {
                            swal({
                                title: "Successfully stored!",                                                                                
                                type: "success"
                            }).then(function() {
                                location.reload()
                            });
                        }
                        else if(!response.is_username)
                        {
                            swal({
                                title: "Username is exsist already!",                                                                                
                                type: "error",
                                text: "Please try another."
                            }).then(function() {
                                
                            });
                        }
                        else
                        {
                            swal({
                                title: "Something wrong!",                                                                                
                                type: "error"
                            }).then(function() {
                                location.reload()
                            });
                        }
                    }
                });
            }
        });
        
        $(document).on('click','.sel_nav_item',function()
        {            
            var item = $(this).data('item');   
            $(".sel_nav_item").removeClass("selected_nav_item");
            $(this).addClass("selected_nav_item");
            $(".sel_nav_part").css("display","none");
            $(".part_"+item).css("display","block");
        });
        

        $(document).ready(function(){            
            $(".btn-current-page").html(currentPage);
            $("#currentPage").val(currentPage);
            $(".total-page").html(pagenum);            
            $('#results_clustering').DataTable( {
                "order": [[ 3, "desc" ]]
            } );
            $('#results_view').DataTable( {
                "order": [[ 3, "desc" ]]
            } );
            
        });   
        


        $(document).on('click','.btn-next',function(){                    
            if(currentPage==pagenum)
            {                        
                return false;
            }
            currentPage++;
            $(".btn-current-page").html(currentPage);
            $("#currentPage").val(currentPage);
            get_tickets();
        });
        $(document).on('click','.btn-prev',function(){
            if(currentPage==1)
            {                        
                return false;
            }
            currentPage--;
            $(".btn-current-page").html(currentPage);
            $("#currentPage").val(currentPage);
            get_tickets();
        });
        $(document).on('click','.btn-start',function(){
            currentPage = 1;
            $(".btn-current-page").html(currentPage);
            $("#currentPage").val(currentPage);
            get_tickets();
        });
        $(document).on('click','.btn-end',function(){
            currentPage = pagenum;
            $(".btn-current-page").html(currentPage);
            $("#currentPage").val(currentPage);
            get_tickets();
        });

    }());

 

  
   
});


    

