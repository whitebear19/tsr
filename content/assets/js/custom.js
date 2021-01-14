jQuery(function ($) {

    'use strict';
    
   
// ----------------------------------------------------------------
   


    (function() {

        var currentPage = 1;
        var pagenum = 1;     
        var filename = '';
        var token = $('input[name="csrfmiddlewaretoken"]').val();
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
        
        $(document).on('click','.btn_generate_samples',function(){
            if(filename == '')
            {
                swal({
                    title: "You did not upload file.",                            
                    text: "Please upload csv file",
                    type: "error"
                }).then(function() {
                   
                });
            }
            else
            {                
                $("#loading").css("display","block");
                var formdata = new FormData;
                formdata.append('filename',filename);
                $.ajax({
                    headers: { "X-CSRFToken": token },
                    url:"/process_csv",
                    type: 'post',
                    dataType: 'json',
                    data: formdata,
    
                    processData: false,
                    contentType: false,
                    success: function(response){                  
                        $("#loading").css("display","none");
                        $(".selected_file_name").val("");
                        $('#btn_sample_upload').val("");
                        filename = '';
                        if(response.results)
                        {                        
                            swal({
                                title: "Process success!",                            
                                type: "success"
                            }).then(function() {
                               
                            });
                        }  
                        else
                        {
                            swal({
                                title: "Something wrong!",                            
                                text: "Please try again.",
                                type: "error"
                            }).then(function() {
                               
                            });
                        }
                        var data = response.data;                     
                        if(data.length>0)
                        {
                            for (let index = 0; index < data.length; index++) {                           
                                var html = '';
                                html = `
                                    <div class="alert alert-success alert-dismissible fade show" role="alert">
                                        <strong><i class="fas fa-check"></i></strong> 
                                        ${data[index]}
                                        <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                        <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                `;
                                $(".show_results").append(html);
                            }
                            
                        }
    
                    }
                });
            }
        });

        $('#btn_sample_upload').change(function () {
            filename = this.files[0].name;
            $(".selected_file_name").val(filename);    
            var formdata = new FormData;
            formdata.append('attach',this.files[0]);
            
            $("#loading").css("display","block");
            $.ajax({
                headers: { "X-CSRFToken": token },
                url:"/upload_csv",
                type: 'post',
                dataType: 'json',
                data: formdata,

                processData: false,
                contentType: false,
                success: function(response){                  
                    $("#loading").css("display","none");                    
                    $('#btn_sample_upload').val("")
                    if(response.results)
                    {                        
                        swal({
                            title: "Upload success!",                            
                            type: "success"
                        }).then(function() {
                           
                        });
                    }  
                    else
                    {
                        swal({
                            title: "Something wrong!",                            
                            text: "Please try again.",
                            type: "error"
                        }).then(function() {
                           
                        });
                    }
                    var data = response.data; 
                    filename = data;   
                }
            });
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


    

