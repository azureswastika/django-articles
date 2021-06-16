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

$('.comment').click(function () {
    const post = $(this).attr('post')
    anime({
        targets: '#comment' + post,
        translateY: -10,
        direction: 'alternate',
        duration: 100,
        easing: 'easeInOutSine'
      });
    window.location = `/post/${post}/`
})

$('.delete-post').click(function () {
    const post = $(this).attr('post')
    axios.get(`/post/${post}/delete/`).then(function (response) {
        if (response.data.deleted == true || response.data.deleted == false) {
            const animation = anime({
                targets: '#post' + post,
                opacity: 0,
                endDelay: 50,
                easing: 'easeInOutSine'
              })
              animation.finished.then(function () {
                $('#post' + post).remove();
              });
        }
    })
})