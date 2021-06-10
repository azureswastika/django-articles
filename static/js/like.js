$('.like').click(function () {
    const post = $(this).attr('post')
    axios.get(`/post/${post}/like/`).then(function (response) {
        $('#count' + post).text(response.data.count)
        if (response.data.liked == true) {
            $('#likebtn' + post).attr('src', '/static/svg/liked.svg')
        } else {
            $('#likebtn' + post).attr('src', '/static/svg/like.svg')
        }
    })
})

$('.delete-post').click(function () {
    const post = $(this).attr('post')
    axios.get(`/post/${post}/delete/`).then(function (response) {
        if (response.data.deleted == true) {
            $('#post' + post).remove()
        }
    })
})