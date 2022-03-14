var input_box = document.getElementsByClassName("search-input")[0];
var autocomplete = document.getElementById("autocomplete");

function suggestions() {
  var college_name = $("#search").val();
  if (college_name.length > 2) {
    ajax_request(college_name);
  } else {
    $("#autocomplete").html("");
    showSuggestions();
    autocomplete.style.display = "none";
  }
}

function ajax_request(college_name) {
  search_data = {
    college_name: college_name,
  };
  $.ajax({
    type: "get",
    url: "ajax/search",
    data: search_data,
    dataType: "json",
    success: function (data) {
      var lis = "";
      var comeon = "";
      if (data.length > 0) {
        // college found
        $.each(data, function (index, college) {
          lis +=
            '<li><a href="/colleges/' +
            college.url +
            '" class="btn">' +
            college.college_name +
            "</a></li>";
        });
        $("#autocomplete").html(lis);
      }
      showSuggestions();
    },
  });
}

function showMore() {
  active_tab = document.getElementsByClassName("active")[1];
  var span = active_tab.getElementsByTagName("span");
  var less = span[0];
  var more = span[1];
  var btnText = document.getElementById("show-more-Btn");

  if (less.style.display === "none") {
    less.style.display = "inline";
    btnText.innerHTML = "Show more";
    more.style.display = "none";
    less.scrollIntoView();
  } else {
    less.style.display = "none";
    btnText.innerHTML = "Show less";
    more.style.display = "flex";
  }
}

function changeStatus(clicked_tab) {
  active_tab = document.getElementsByClassName("active");

  active_tab[0].classList.remove("active");
  clicked_tab.classList.add("active");

  // Tab content
  // Remove active class from previous active tab content
  active_tabcontent_id = active_tab[1].getAttribute("id");
  document.getElementById(active_tabcontent_id).classList.remove("active");

  // Add active class to clicked tab content
  clicked_tabcontent_id = clicked_tab.getAttribute("data-target");
  document.getElementById(clicked_tabcontent_id).classList.add("active");
  document.getElementById("show-more").style.display = "none";
  document.getElementById("show-less").style.display = "inline";
  document.getElementById("show-more-Btn").innerHTML = "Show more";
}


input_box.addEventListener("focus", function() {
    showSuggestions();
})


input_box.addEventListener("focusout", function() {
  input_box.classList.remove("input-focus");
  autocomplete.style.display = "none";
})

function showSuggestions() {
  if(autocomplete.hasChildNodes()){
    input_box.classList.add("input-focus");
    autocomplete.style.display = "block"; 
  }
  else
    input_box.classList.remove("input-focus");
}


$("#inquiryForm").on("submit", function(event) {
  event.preventDefault();

  $.ajax({
    url: "inquiry",
    type: "POST",
    data: $(this).serialize(),
    encode: true,
    success: function(response) {
      $("#msg").html(`<div class="alert alert-success alert-dismissible fade show" role="alert">`
        + response.message +   
        `<button type="button" class="close" data-dismiss="alert" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>`);
      
      $("#inquiryForm")[0].reset();
      $("#closeInquiryForm").click();

      $("#name_error").html("");
      $("#email_error").html("");
      $("#contact_number_error").html("");
      $("#message_error").html("");

      $("#id_name").removeClass("errors");
      $("#id_email").removeClass("errors");
      $("#id_contact_number").removeClass("errors");
      $("#id_message").removeClass("errors");
    },
    error: function(response) {
      $("#name_error").html("<ul><li>" + response.responseJSON.name[0].message + "</li></ul>");
      $("#email_error").html("<ul><li>" + response.responseJSON.email[0].message + "</li></ul>");
      $("#contact_number_error").html("<ul><li>" + response.responseJSON.contact_number[0].message + "</li></ul>");
      $("#message_error").html("<ul><li>" + response.responseJSON.message[0].message + "</li></ul>");

      $("#id_name").addClass("errors");
      $("#id_email").addClass("errors");
      $("#id_contact_number").addClass("errors");
      $("#id_message").addClass("errors");
    }
  });
});



// document.getElementById("id_name").removeAttribute("required")
// document.getElementById("id_contact_number").removeAttribute("required")
// document.getElementById("id_email").removeAttribute("required")
// document.getElementById("id_message").removeAttribute("required")
// document.getElementById("submitInquiryForm").click()


document.getElementsByClassName("carousel-item")[0].classList.add("active")

