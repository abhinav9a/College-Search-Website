function suggestions() {
  var college_name = $("#select_college").val();
  if (college_name.length > 2) {
    ajax_request(college_name);
  } else {
    $("#autocomplete").html("");
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
        $.each(data, function (index, value) {
          if (college_one == null) {
            lis +=
              '<li><a href="/compare-colleges?college_one=' +
              value.url +
              '" class="btn">' +
              value.college_name +
              "</a></li>";
          } else if (college_two == null) {
            lis +=
              '<li><a class="autocomplete-ui" href="/compare-colleges?college_one=' +
              college_one +
              "&college_two=" +
              value.url +
              '" class="btn">' +
              value.college_name +
              "</a></li>";
          } else if (college_three == null) {
            lis +=
              '<li><a class="autocomplete-ui" href="/compare-colleges?college_one=' +
              college_one +
              "&college_two=" +
              college_two +
              "&college_three=" +
              value.url +
              '" class="btn">' +
              value.college_name +
              "</a></li>";
          } else {
            lis +=
              '<li><a class="autocomplete-ui" href="/compare-colleges?college_one=' +
              college_one +
              "&college_two=" +
              college_two +
              "&college_three=" +
              college_three +
              "&college_four=" +
              value.url +
              '" class="btn">' +
              value.college_name +
              "</a></li>";
          }
        });
        $("#autocomplete").html(lis);
      } else {
      }
    },
  });
}

function closeFun(identifier) {
  id = identifier.getAttribute("data-count");

  url_params.delete(id);
  window.location.href =
    document.location.href.split("?")[0] + "?" + url_params.toString();
}

var starWidth = 30;

$.fn.stars = function () {
  return $(this).each(function () {
    $(this).html(
      $("<span />").width(
        Math.max(0, Math.min(5, parseFloat($(this).html()))) * starWidth
      )
    );
  });
};
$(document).ready(function () {
  $("span.stars").stars();
});
