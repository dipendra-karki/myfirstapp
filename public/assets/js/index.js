$(document).ready(function(){


    $editCarModal = $('#edit-car-modal')
    $editCarModal.find('form').on('submit', onEditCar.bind($editCarModal));

      
    //Display Cars Table  

        setInterval(function(){
            displayCars();
         }, 5000);
                
            
            
   //Display Cars Table *   

        function displayCars(){
        
            $.ajax({
                url: "http://localhost:5000/api/cars",
                type: "GET",
                headers: {
                    'Accept': 'application/json',
                  },
                success: function(result){
            
                    if (result) {
                        renderCarList(result)
                    }
                }
            });
            
        }
            
            
            
    //Search Cars Table          
   
    
        $('#search').keyup(function(){
        
            var search = $.trim($('#search').val());
            //console.log(search);        
            $.ajax({
                url:"http://localhost:5000/api/cars/search",
                data:{search:search},
                type: 'POST',
                headers: {
                    'Accept': 'application/json'
                    },
                success:function(data){
                    console.log(data)
                    if(data){
                        // $.each(data, function(index, value){
                        //     console.log(index,value);
                            renderSearchList(data);
                        // })
                    }

                },
                error: function(){
                    $('#result').html("<p class ='alert alert-danger' data-dismiss='alert'> Not found try again</li>");
                }
                          
            });
        });
               
     // This code add cars to database table cars       
                   
        $("#add-car-form").submit(function(evt){
            evt.preventDefault();
            var data = $(this).serialize();
  
            $.ajax({
                url:"http://localhost:5000/api/cars",
                method:"POST",
                data: data,
                headers:{
                    "Accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                success: function(result){
                    $("#car-result").html("<p class='alert alert-success' data-dismiss='alert'>successfully submitted</p>");
                    //evt.target.reset();
                }

            });  
      
        });


        function renderCarList(data) {
            $('#car-list-table').find('tbody').loadTemplate('#car-list-item-tpl', data);
          }
          
        function renderSearchList(data) {
            $('#result').find('tbody').loadTemplate('#search-list-item-tpl', data);
          }
        
          
        $('#car-list-table').on('click', 'button.remove-btn', function(e) {
            console.log($(this).data('id'));

            $.ajax({
                url: `http://localhost:5000/api/cars/${$(this).data('id')}`,
                method: 'DELETE',
                headers: {
                    'Accept': 'application/json',
                }
            })
            .then(() => {
                displayCars();
            });
          })
      


        $('#car-list-table').on('click', 'button.edit-btn', function(e) {
            console.log($(this).data('id'))
      
            $.ajax({
                url: `http://localhost:5000/api/cars/${$(this).data('id')}`,
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                }
            })
                .then(data => {
                    $('#edit-car-modal').find('input').each((index, input) => {
                    $(input).val(data[$(input).attr('name')])
                })
            })
      
        })


        function onEditCar(e) {
            e.preventDefault()
            const formData = Array.from(new FormData(e.target)).reduce((result, [key, value]) => {
                    result[key] = value;
                    return result
                }, {});
          
            // formData = $(this).serialize()
            console.log(formData);
            $.ajax({
                url: `http://localhost:5000/api/cars/${formData['id']}`,
                method: 'PUT',
                data: formData,
                headers: {
                    'Accept': 'application/json'
                }
            })
            .then(() => {
                displayCars();
            });
          
            this.modal('hide')
            e.target.reset()
          }
        

    }); // Document ready function end
       