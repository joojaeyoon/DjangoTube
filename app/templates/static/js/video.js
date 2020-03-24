const comments = $(".comment-content");

let commentData = {
  next: `/api/videos/${video_id}/comments`
};

let date = video_date;

date = date.split(",");
date = date[1] + " " + date[0];

$(".video-date").text(date);

function appendComment(comment, appendFirst) {
  const icon = $("<div class='comment-icon'></div>");
  const time = $("<span class='comment-time'></span>").text(
    " " + renderTimestamp(comment.created_at)
  );
  const author = $("<span class='comment-author'></span>")
    .text(comment.author)
    .append(time);
  const text = $("<span class='comment-text'></span>").text(comment.text);
  const info = $("<div class='comment-info'></div>")
    .append(author)
    .append(text);
  const commentDiv = $("<div class='comment'></div>")
    .append(icon)
    .append(info);

  if (appendFirst) {
    comments.prepend(commentDiv);
  } else {
    comments.append(commentDiv);
  }
}

function getComments(res) {
  commentData = res;
  $(".comment-overall").text("댓글 " + res.count + "개");

  res.results.map(comment => {
    appendComment(comment, false);
  });
}
$.get(`/api/videos/${video_id}/comments`, getComments);

$("#comment-form").on("submit", function(e) {
  e.preventDefault();
  const text = e.target.commentFormText.value;

  if (text === "") return;

  const data = {
    token: localStorage.getItem("token"),
    text: e.target.commentFormText.value,
    csrfmiddlewaretoken: e.target.csrfmiddlewaretoken.value
  };

  $.ajax(`/api/videos/${video_id}/comment`, {
    method: "POST",
    data: data
  })
    .done(function(res, statusText, xhr) {
      appendComment(res, true);

      const count =
        Number(
          $(".comment-overall")
            .text()
            .match(/\d/g)
            .join("")
        ) + 1;

      $(".comment-overall").text("댓글 " + count + "개");
    })
    .fail(function(xhr, statusText) {
      // console.log(xhr);
    });

  e.target.commentFormText.value = "";
});

$(window).on("scroll", function() {
  const scrollTop = $("html").scrollTop();
  const scrollTopMax = $("html").prop("scrollTopMax");

  if (scrollTop == scrollTopMax && commentData.next !== null) {
    $.get(commentData.next, getComments);
  }
});

if (localStorage.getItem("token") === null) {
  $("#comment-form").hide();
}
