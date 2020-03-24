const videoList = $(".video_list");
const loginButton = $("#Login-button");

let data = null;

if (localStorage.getItem("token") !== null) {
  loginButton.text("Logout");
} else {
  $("#uploadButton").hide();
}

loginButton.on("click", function() {
  if (loginButton.text() === "Logout") {
    loginButton.prop("href", "/");
    localStorage.removeItem("token");
  }
});

function getVideos(res) {
  data = res;
  res.results.map(video => {
    const li = $("<li></li>");
    const videoDiv = $("<div></div>");
    const vidoe_link = $("<a></a>");
    const videoThumbnail = $("<img/>");
    const time = $("<span></span>").text(video.time);
    const title = $("<p></p>").text(video.title);
    const views = $("<p></p>").text("조회수 " + video.view_count);

    vidoe_link.attr("href", "/videos/" + video.slug);
    vidoe_link.addClass("video_box");
    videoThumbnail.attr("src", video.thumbnail);
    videoThumbnail.addClass("thumbnail");
    time.addClass("video_time");

    vidoe_link.append(videoThumbnail).append(time);
    videoDiv
      .append(vidoe_link)
      .append(title)
      .append(views);
    li.append(videoDiv);
    videoList.append(li);
  });
}

$.get("/api/videos", getVideos);

function CheckScroll() {
  const scrollTopMax = videoList.prop("scrollTopMax");
  const scrollTop = videoList.scrollTop();

  if (scrollTop == scrollTopMax && data.next !== null) {
    $.get(data.next, getVideos);
  }
}

videoList.on("scroll", CheckScroll);

$("#modalUploadInput").on("change", function(e) {
  filepath = e.target.value.split("\\");

  filename = filepath[filepath.length - 1];

  $("#modalUploadInputText").attr("placeholder", filename);
});

$("#modalUploadButton").on("click", function() {
  const form = $("#modalForm")[0];
  if (form.video.value === "") {
    return;
  }

  const formData = new FormData(form);

  const data = {
    csrfmiddlewaretoken: form.csrfmiddlewaretoken.value,
    title: form.title.value,
    description: form.description.value
  };

  $.ajax("/api/video/upload", {
    method: "POST",
    data: formData,
    processData: false,
    contentType: false
  })
    .done(function(res, statusText, xhr) {
      data.video = res.filepath;
    })
    .fail(function(xhr, statusText) {
      console.log(xhr);
    });
});
