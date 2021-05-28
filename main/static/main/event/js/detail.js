const csrftoken = Cookies.get('csrftoken');

// Add or remove tag
$(document.body).on('click', '.addTag', function () {
  let tag = $(this);
  tag.removeClass('addTag');
  tag.addClass('removeTag');
  let tag_id = tag.children().attr('id');
  $('#currentTags').append(tag[0]);
  updateTag(tag_id);
}).on('click', '.removeTag', function () {
  let tag = $(this);
  tag.removeClass('removeTag');
  tag.addClass('addTag');
  let tag_id = tag.children().attr('id');
  $('#allTags').append(tag[0]);
  updateTag(tag_id);
});

// Send ajax update tag
function updateTag(tag_id) {
  let slug = $('#slug').html();
  let ids = [];
  $('.removeTag > span').each(function () {
    ids.push(parseInt($(this).attr('id'), 10));
  })

  let req_data = {};
  req_data.tags = ids;

  $.ajax({
    headers: {
      'X-CSRFTOKEN': csrftoken
    },
    url: "/api/event/" + slug + "/",
    data: req_data,
    type: 'PATCH',
    credentials: 'include',
    success: function (result, status, xhr) {
      console.log("Tags updated");
    },
    traditional: true // Do not add [] to array
  });
}
