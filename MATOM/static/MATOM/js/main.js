function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
 //When submit is clicked
$(document).ready(function() {
    $("#menu-toggle").click(function (e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });
    //figuring out wha

    $(document).ready(function () {
        $("#menus").accordion({collapsible: true, active: false, heightStyle: "content"});
    });

});

$(document).ready(function()
    {
        $("#myTable").tablesorter();
    }
);

//TODO: use this to allow another ajax call to be activated as soon as the user leaves the
var example_form = '#id-comparisonForm';
var url = '/comparison/';
DoAction( example_form, url);



var example_form = '#id-EnrichmentForm';
var url = '/enrichment/';
DoAction( example_form, url);

var example_form = '#id-ScoreForm';
var url = '/score/';
DoAction( example_form, url);
    $('#div_id_test_motif').addClass('disableField');
    $('#div_id_uploaded_motif').addClass('disableField');

toggle_field();

//TODO: Remember to check this later
//var search_form = '#id-SearchForm';
//var urls = '/searchs/';
//SearchAction( search_form, urls);

function toggle_field() {
$(document).ready(function() {

      var option = $('input[name="formats"]:checked').val();
      if (option == 'paste'){
          $('#div_id_test_motif').removeClass('disableField');
          $('#div_id_uploaded_motif').addClass('disableField');
      }
      else if (option == 'upload'){
          $('#div_id_uploaded_motif').removeClass('disableField');
          $('#div_id_test_motif').addClass('disableField');
      }
    else{
          console.log("We got here")
      }
    var options = $('input[name="mode"]:checked').val();

    if (options == 'GIMME') {
        $('#div_id_score').addClass('disableField');
        $('#div_id_data').addClass('disableField');
        $('#div_id_uploaded_chipseq').addClass('disableField');
        }
    else {
        $('#div_id_score').removeClass('disableField');
        $('#div_id_data').removeClass('disableField');
        $('#div_id_uploaded_chipseq').removeClass('disableField');

        }
  $('input[name="formats"]').change(function() {

      var option = $('input[name="formats"]:checked').val();

      if (option == 'paste'){
          $('#div_id_test_motif').removeClass('disableField');
          $('#div_id_uploaded_motif').addClass('disableField');
      }
      else{
          $('#div_id_uploaded_motif').removeClass('disableField');
          $('#div_id_test_motif').addClass('disableField');
      }


      //alert($('input[name="formats"]:checked', '#id-seq').val());


   });

    $('input[name="mode"]').change(function () {

        var option = $('input[name="mode"]:checked').val();

        if (option == 'GIMME') {
            $('#div_id_score').addClass('disableField');
            $('#div_id_data').addClass('disableField');
            $('#div_id_uploaded_chipseq').addClass('disableField');
        }
        else {
            $('#div_id_score').removeClass('disableField');
            $('#div_id_data').removeClass('disableField');
            $('#div_id_uploaded_chipseq').removeClass('disableField');
        }
        //alert($('input[name="formats"]:checked', '#id-seq').val());



    });

    $('input[name="data"]').change(function() {

      var option = $('input[name="data"]:checked').val();

      if (option == 'PBM'){
          $('#div_id_uploaded_chipseq').addClass('disableField');
      }
      else{
          $('#div_id_uploaded_chipseq').removeClass('disableField');
      }


   });

    //$("input:radio:first").prop("checked", true).trigger("click");

});
}
function button_check() {

$(document).ready(function(){
    $("#search_form input[name='checked_tf']").change(function() {
         var option = $('input[name="checked_tf"]:checked').val();
    alert(option)
    });

});
}
var option = $("#search_form input[name='checked_tf']:checked").val();

console.log(option);

button_check();

$(document).ready(function(){

    $('#countrylist').change(function(e){
       // Your event handler
    });

    // And now fire change event when the DOM is ready
    //$('#countrylist').trigger('change');
});


//$('input[name="checked_tf"]').change(function() {
//         var option = $('input[name="checked_tf"]:checked').val();
//    alert(option)
//    });

    //var option = $('input[name="formats"]:checked').val();



//function SearchAction( search_form, url) {
//    $(search_form).on('submit', function (e) {
//
//        //Prevent default submit. Must for Ajax post.Beginner's pit.
//        e.preventDefault();
//        //$('#hide-form').hide();
//        //$('#comp-img').show();
//
//        //Prepare csrf token
//        var csrftoken = getCookie('csrftoken');
//        var data = new FormData($(search_form)[0]);
//        console.log(data);
//        $.ajax({
//            url: url,
//            type: "POST",
//            //data: $(search_form).serialize(),
//            data: data,
//            cache: false,
//            contentType: false,
//            processData: false,
//            success: function (data) {
//
//                if (!(data['success'])) {
//                    console.log("Not successful submission");
//                    $(search_form).html(data['form_html']);
//                    //$('#comp-img').hide();
//
//                }
//                else{
//                    var new_data = $("#get-this", data['form_html']);
//                    //var success_url = data['success_url'];
//                    $("#get-this").html(new_data);
//                    console.log(new_data)
//                }
//            },
//            error: function (xhr, ajaxOptions, thrownError) {
//            console.log(xhr.status);
//           console.log(xhr.responseText);
//           console.log(thrownError);
//       }
//        });
//    });
//}

var search_form = '#id-SearchTfs';
var url = '/search-results/';
$(search_form).on('submit', function (e) {

    //Prevent default submit. Must for Ajax post.Beginner's pit.
    e.preventDefault();
    //$('#hide-form').hide();
    //$('#comp-img').show();

    //Prepare csrf token
    var csrftoken = getCookie('csrftoken');
    var data = new FormData($(search_form)[0]);
    console.log(data);
    $.ajax({
        url: url,
        type: "POST",
        //data: $(search_form).serialize(),
        data: data,
        cache: false,
        contentType: false,
        processData: false,
        success: function (data) {

            if (!(data['success'])) {
                console.log("Not successful submission");
                $(search_form).html(data['form_html']);
                //$('#comp-img').hide();

            }
            else{
                var new_data = $("#get-this", data['form_html']);
                //var success_url = data['success_url'];
                $("#get-this").html(new_data);
                console.log(new_data)
            }
        },
        error: function (xhr, ajaxOptions, thrownError) {
        console.log(xhr.status);
       console.log(xhr.responseText);
       console.log(thrownError);
   }
    });
});


//Manipulate the forms and return results via ajax
function DoAction( example_form, url) {
    $(example_form).on('submit', function (e) {

        //Prevent default submit. Must for Ajax post.Beginner's pit.
        e.preventDefault();
        $('#hide-form').hide();
        $('#comp-img').show();

        //Prepare csrf token
        var csrftoken = getCookie('csrftoken');
                var data = new FormData($(example_form)[0]);
        console.log(data);
        $.ajax({
            url: url,
            type: "POST",
            //data: $(example_form).serialize(),
            data: data,
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {

                if (!(data['success'])) {
                    $('#comp-img').hide();

                    // Here we replace the form, for the
                    $(example_form).html(data['form_html']);

                    var error = data['meme_error'];
                    console.log(error);
                    var error_message = data['error_message'][error];
                    console.log(error_message);
                    //FIXME: most of these test need to be optimized. One thing should be tested at a time.
                    // Eliminate all the errors
                    if (error == 'REQUIRED') {
                        console.log("Required");
                        $('#hide-form').show();

                        $('#div_id_test_motif').addClass('disableField');
                        $('#div_id_uploaded_motif').addClass('disableField');
                        toggle_field();
                    }
                    else if (error == 'NO_TF' || error == "NO_CHIP" || error == "NO_TFID" || error == "NO_PBM") {

                        $('#div_id_tf').addClass('has-error');
                        $('#div_id_tf .controls').append('<span id="error_1_id_tf" ' +
                            'class="help-block"><strong>'+error_message+'</strong></span>');
                        $('#hide-form').show();

                        $('#div_id_test_motif').addClass('disableField');
                        $('#div_id_uploaded_motif').addClass('disableField');
                        toggle_field();


                    }
                    else if (error == 'MEME_ERROR'){
                        console.log("meme error");
                        var option = $('input[name="formats"]:checked').val();
                        console.log(option);
                          if (option == "paste"){

                                $('#div_id_test_motif').addClass('has-error');

                                $('#div_id_test_motif .controls').append('<span id="error_1_id_tf" ' +
                                    'class="help-block"><strong>'+error_message+'</strong></span>');

                                $('#hide-form').show();
                                toggle_field();
                               }
                        else{

                              $('#div_id_uploaded_motif').addClass('has-error');
                              $('#div_id_uploaded_motif .controls').append('<span id="error_1_id_tf" ' +
                                  'class="help-block"><strong>'+error_message+'</strong></span>');

                              $('#hide-form').show();
                              toggle_field();
                          }

                    }

                    else if (error == "BED_ERROR"){
                        $('#div_id_uploaded_chipseq').addClass('has-error');
                        $('#div_id_uploaded_chipseq .controls').append('<span id="error_1_id_tf" ' +
                            'class="help-block"><strong>'+error_message+'</strong></span>');
                        $('#hide-form').show();
                        toggle_field();


                    }

                   else if (error == "FEW_MOTIFS"){

                        $('#hide-form').show();

                        $('#div_id_test_motif').addClass('disableField');
                        $('#div_id_uploaded_motif').addClass('disableField');
                        toggle_field();
                        alert("Require more than three motifs for comparison");

                    }
                    else if (error == "ERROR"){
                        $('#hide-form').show();

                        alert("Something went wrong");
                        $('#div_id_test_motif').addClass('disableField');
                        $('#div_id_uploaded_motif').addClass('disableField');
                        toggle_field();

                    }
                    else if (error == 'NOT_AVAILABLE'){
                        $('#hide-form').show();

                        alert(error_message);
                        $('#div_id_test_motif').addClass('disableField');
                        $('#div_id_uploaded_motif').addClass('disableField');
                        toggle_field();
                    }


                    else{
                        $('#hide-form').show();

                        alert("Something went wrong here");
                        $('#div_id_test_motif').addClass('disableField');
                        $('#div_id_uploaded_motif').addClass('disableField');
                        toggle_field();
                    }

                }
                else {
                    //$('#comp-img').hide();
                    //var new_data = $("#get-this", data['form_html']);
                    var success_url = data['success_url'];
                    //$("#get-this").html(new_data);
                    //$("#new_url").append("<h4><a href="+success_url+" >Bookmark this link to access your results later</a>");
                    //$("#menus").accordion({collapsible: true, active: false, heightStyle: "content"});
                     //if(url!=window.location){
                            //window.history.pushState({path:url},'',url);
                            //}
                    console.log(success_url);
                    window.location.href = success_url;
                    //$(window).bind('popstate', function() {
                    //$.ajax({url:location.pathname+'?rel=tab',success: function(new_data){
                        //$('#hide-form').show();
                    //$('#get-this').html(new_data);
                    //}});
//});
                    // Here you can show the user a success message or do whatever you need

                    //$(example_form).find('.success-message').show();
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                console.log("We got to the error");
                    console.log(xhr.status);
                    console.log(xhr.responseText);
                    console.log(thrownError);
                    //TODO: Get the error message returned at this point...return the right

                    $('#comp-img').hide();
                    $('#hide-form').show();

                    $('#div_id_test_motif').addClass('disableField');
                    $('#div_id_uploaded_motif').addClass('disableField');
                    toggle_field();
                    alert("Something fishy happened, lets start again");

                    //$(example_form).find('.error-message').show()
                }
            });
        });
}
