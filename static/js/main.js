    $('#payModal').on('show.bs.modal', function(e) {
      var price = $(e.relatedTarget).data('dollars');
      var tripID = $(e.relatedTarget).data('trip-id');
      var displayName = $(e.relatedTarget).data('trip-name');
      var path = $(e.relatedTarget).data('path');
    
      // Add name and map to modal
      $('.display-name').html(displayName);
      $('.path-img').attr('src', 'https://maps.googleapis.com/maps/api/staticmap?size=200x200&path=weight:5%7Ccolor:blue%7Cenc:'+path);

      // Set initial price on Charge btn
      price = price.toFixed(2);
      $('.charge').html('Charge $'+price);

      // Set radio button defaults when modal loads
      var $defaultRadio = $('input:radio[name="optionsAmount"]').eq(0);
      if($defaultRadio.is(':checked') === false) {
        $defaultRadio.prop('checked', true);
      }
      $('input:radio[name="friends"]').removeAttr('checked');
      
      // Update Charge button based on radio button
      $('input[name="optionsAmount"]').eq(0).attr('value', price);
      $('input[name="optionsAmount"]').eq(1).attr('value', (price/2).toFixed(2));

      $('input[name="optionsAmount"]').change(function(){
        $('.charge').html('Charge $'+ $(this).val());
      });

      // Submit payment to venmo API
      $('#payment').submit(function(e){
        e.preventDefault();
        $.ajax({
          method: "POST",
          url: "/payment",
          data: {'user_id': $('input[name="friends"]').val(), 'trip_id': tripID, 'price': $('input[name="optionsAmount"]').val()}
        })
        .done(function(data){
          console.log(data);
          // hide modal
          $('#payModal').modal('hide');
          // remove charge btn, replace with success
          $('#'+tripID + ' .btn').html('Success!');
          $('#'+tripID + ' button').prop('disabled', true);

        });
      });
    });
