$('.like').click(function () {
    const post = $(this).attr('post')
    axios.get('/post/like/' + post).then(function (response) {
        $('#count' + post).text(response.data.count)
        if (response.data.liked == true) {
            $('#likebtn' + post).attr('src', '/static/svg/liked.svg')
        } else {
            $('#likebtn' + post).attr('src', '/static/svg/like.svg')
        }
    })
})