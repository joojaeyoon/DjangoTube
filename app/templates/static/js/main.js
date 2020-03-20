const ul = $(".video_list");

let data = {};

function getVideos(res) {
  data = res;
  res.results.map(d => {
    const li = $("<li></li>");
    const div = $("<div></div>");
    const a = $("<a></a>");
    const img = $("<img/>");
    const time = $("<span></span>").text(d.time);
    const title = $("<p></p>").text(d.title);
    const views = $("<p></p>").text("조회수 " + d.view_count);

    a.attr("href", "/videos/" + d.slug);
    a.addClass("video_box");
    img.attr("src", d.thumbnail);
    img.addClass("thumbnail");
    time.addClass("video_time");

    a.append(img).append(time);
    div
      .append(a)
      .append(title)
      .append(views);
    li.append(div);
    ul.append(li);
  });
}

$.get("/api/videos", getVideos);

ul.on("scroll", () => {
  const max = ul.prop("scrollTopMax") * 0.8;
  const scrollPos = ul.scrollTop();

  if (max <= scrollPos && data.next !== null) {
    $.get(data.next, getVideos);
  }
});
