$('.like').click(function () {
    const post = $(this).attr('post')
    axios.get(`/post/${post}/like/`).then(function (response) {
        $('#count' + post).text(response.data.count)
        if (response.data.liked == true) {
            $('#likebtn' + post).attr('src', '/static/svg/liked.svg')
        } else {
            $('#likebtn' + post).attr('src', '/static/svg/like.svg')
        }
        anime({
            targets: '#likebtn' + post,
            translateY: -10,
            direction: 'alternate',
            duration: 100,
            easing: 'easeInOutSine'
          });
    })
})

$('.delete-post').click(function () {
    const post = $(this).attr('post')
    axios.get(`/post/${post}/delete/`).then(function (response) {
        if (response.data.deleted == true || response.data.deleted == false) {
            const animation = anime({
                targets: '#post' + post,
                opacity: 0,
                endDelay: 50,
              })
              animation.finished.then(function () {
                $('#post' + post).remove();
              });
        }
    })
})