const csrftoken = Cookies.get('csrftoken');

// Add spinner while ajax performed
$(document)
  .ajaxStart(function () {
    $('.modal-footer > button').disabled = true;
    $('#createUpdateButton').html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Loading...');
  })
  .ajaxStop(function () {
    setTimeout(function () {
      $('.modal-footer > button').disabled = false;
      $('.modal-body > input').disabled = true;
      $('#createUpdateButton').hide();
    }, 500);
  });

// Send delete request
$('.deleteButton').click(function (e) {
  let row_id = $(e.target).parents().eq(3).attr('id');
  $.ajax({
    headers: {
      'X-CSRFTOKEN': csrftoken
    },
    url: "/api/tag/delete/" + row_id + "/",
    data: {},
    type: 'DELETE',
    credentials: 'include',
    success: function (result, status, xhr) {
      setTimeout(function () {
        window.location.href = "/api/tag/";
      }, 300);
    },
  });
});

// Send partial update request
$('#createUpdateButton').click(function () {
  let pk = $('#tagId').html();
  let method = 'POST';
  let uri = "/api/tag/create/";
  let request_data = generateCreateData();

  if (pk) {
    method = 'PATCH';
    uri = "/api/tag/update/" + pk + "/";
    request_data = generateUpdateData(pk);
  }

  $.ajax({
    headers: {
      'X-CSRFTOKEN': csrftoken
    },
    url: uri,
    data: request_data,
    type: method,
    credentials: 'include',
    success: function (result, status, xhr) {
      if (xhr.status === 201) {
        setTimeout(function () {
          window.location.href = "/api/tag/";
        }, 500);
      } else {
        setTimeout(function () {
          // Update tag from response data
          $("#title_" + result.id).html(result.title);
          $("#back_" + result.id + " > span").css("background-color", result.back_color);
          $("#color_" + result.id + " > span").css("background-color", result.title_color);
          let res = $("#res_" + result.id + " > span");
          res[0].style.setProperty("color", result.title_color, "important");
          res.css("background-color", result.back_color);
        }, 500);
      }
    },
  });
});

function generateUpdateData(pk) {
  let data = {'pk': pk};
  let title = $('#tagTitle').val()
  if (title) {
    data.title = title;
  }
  let titleColor = $('#titleColor').val()
  if (titleColor) {
    data.title_color = titleColor;
  }
  let backColor = $('#backColor').val()
  if (backColor) {
    data.back_color = backColor;
  }
  return data;
}

function generateCreateData() {
  return {
    'title': $('#tagTitle').val(),
    'title_color': $('#titleColor').val(),
    'back_color': $('#backColor').val(),
  };
}