function getLikes(post_class, post_id) {
    $.ajax({
            url: 'http://localhost:8000/like',
            type: 'post',
            data: {
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                post_id: post_id
            },
            success: function(response) {
                document.getElementById("post_card_likes_".concat(post_id)).innerHTML = response.likes;

            }
            });
}