// Update result tag when new color or title picked
$('#titleColor').on('input', function () {
  $('#tag_result')[0].style.setProperty("color", $('#titleColor').val(), "important");
})
$('#backColor').on('input', function () {
  $('#tag_result').css("background-color", $('#backColor').val());
});
$('#tagTitle').on('input', function () {
  $('#tag_result').html($('#tagTitle').val());
});

// Parse rgb string to hex code
function cleanupRichText(richText) {
  return richText.replace(/rgb\((.+?)\)/ig, (_, rgb) => {
    return '#' + rgb.split(',')
      .map(str => parseInt(str, 10).toString(16).padStart(2, '0'))
      .join('')
  })
}

// Show update modal
$("#createEditModal").on('show.bs.modal', function (e) {
  $('.modal-footer > button').disabled = false;
  $('.modal-body > input').disabled = false;

  let tagId = $(e.relatedTarget).data('tag-id');

  let button = $('#createUpdateButton');
  button.show();
  if (tagId) {
    button.html('Update');
  } else {
    button.html('Save');
  }
  let tagTitle = "";
  let tagTitleColor = "#ffffff";
  let tagBackColor = "#000000";
  if (tagId) {
    tagTitle = $("#title_" + tagId).html();
    tagTitleColor = cleanupRichText($("#color_" + tagId + " > span").css("background-color"));
    tagBackColor = cleanupRichText($("#back_" + tagId + " > span").css("background-color"));
  }

  let str = 'Edit tag <span class="badge py-1 mb-2" id="tag_result" style="color: ' + tagTitleColor
    + ' !important;background-color: ' + tagBackColor
    + '">' + tagTitle + '</span>';
  $("#createEditModalLabel").html(str);
  if (tagId) {
    $("#tagId").html(tagId);
  }

  $("#tagTitle").val(tagTitle);
  $("#titleColor").val(tagTitleColor);
  $("#backColor").val(tagBackColor);
});