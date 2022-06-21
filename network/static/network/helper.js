function confirm(id) {
    var edit_cancel_button = document.querySelector(`#edit-${id}-cancel`);
    var edit_confirm_button = document.querySelector(`#edit-${id}-confirm`);
    var edit_confirm_message = document.querySelector(`#edit-${id}-confirm-message`);

    if (edit_confirm_button.disabled) {
        edit_confirm_button.disabled = false;
        edit_confirm_message.style.display = 'block';
        edit_cancel_button.innerHTML = "Don't cancel";
    } else {
        edit_confirm_button.disabled = true;
        edit_confirm_message.style.display = 'none';
        edit_cancel_button.innerHTML = "Cancel";
    }
}

function edit(id) {
    var edit_button = document.querySelector(`#edit-${id}-button`);
    var edit_box = document.querySelector(`#edit-${id}-box`);
    var edit_form = document.querySelector(`#edit-${id}-form`);
    var edit_submit = document.querySelector(`#edit-${id}-submit`);
    var post_post = document.querySelector(`#post-${id}`);
    var edit_cancel_button = document.querySelector(`#edit-${id}-cancel`);
    var edit_confirm_button = document.querySelector(`#edit-${id}-confirm`);
    var edit_confirm_message = document.querySelector(`#edit-${id}-confirm-message`);

    if (edit_box.style.display == 'none') {

        post_post.style.display = 'none';
        edit_box.style.display = 'block';
        edit_button.disabled  = true;
        edit_form.value = document.querySelector(`#post-${id}`).innerHTML;
    } else {
        post_post.style.display = 'block';
        edit_box.style.display = 'none';
        edit_button.disabled  = false;

        edit_confirm_button.disabled = true;
        edit_confirm_message.style.display = 'none';
        edit_cancel_button.innerHTML = "Cancel";
    }

    edit_submit.addEventListener('click', () => {
        fetch('/edit/' + id, {
            method: 'PUT',
            body: JSON.stringify({
                post: edit_form.value
            })
          });
        
          edit_box.style.display = 'none';
          post_post.style.display = 'block';
          edit_button.disabled  = false;

          edit_confirm_button.disabled = true;
          edit_confirm_message.style.display = 'none';
          edit_cancel_button.innerHTML = "Cancel";

          document.querySelector(`#post-${id}`).innerHTML = edit_form.value;
    });
}


function update_like_button(id) {
    var like_button = document.querySelector(`#like-${id}-button`);
    var like_heart = document.querySelector(`#like-${id}-heart`);
    var like_count = document.querySelector(`#like-${id}-count`);

    fetch('/like_helper/'+ id)
        .then(response => response.json())
        .then(data => helper(data));

    function helper(data) {
        if (data['message'] == 'error') {
            like_heart.style.color = 'black';
            like_heart.innerHTML = "&#9829; LIKE";
        } else if (data['message'] == 'success') {
            like_heart.style.color = 'red';
            like_heart.innerHTML = "&#9829; UNLIKE";
        } else {
            // DO NOTHING
            // For error checking
        }
    }

}


function like(id) {
    var like_button = document.querySelector(`#like-${id}-button`);
    var like_heart = document.querySelector(`#like-${id}-heart`);
    var like_count = document.querySelector(`#like-${id}-count`);

    like_button.addEventListener('click', () => {

        async function like_unlike() {
            const response = await fetch('/like_helper/'+ id);
            const data = await response.json();
            console.log(data);

            function update_like_button(data) {
                if (data['message'] == 'error') {
                    const request_options = {
                        method: 'PUT',
                        body: JSON.stringify({
                            like: true
                        })
                      };
                    fetch('/like/' + id, request_options);

                    like_heart.style.color = 'red';
                    like_heart.innerHTML = "&#9829; UNLIKE";
                } else if (data['message'] == 'success') {
                    const request_options = {
                        method: 'PUT',
                        body: JSON.stringify({
                            like: false
                        })
                      };
                    fetch('/like/' + id, request_options);

                    like_heart.style.color = 'black';
                    like_heart.innerHTML = "&#9829; LIKE";
                } else {
                    // DO NOTHING
                    // For error checking
                }
                return false;
            }

            const first = await update_like_button(data);
            return false;
        }

        async function update_like_count() {
            const response = await fetch('/like/'+ id);
            const post = await response.json();
            console.log(post);

            like_count.innerHTML = post.likes + " Likes";
            return false;
        }

        async function start() {
            const first = await like_unlike();
            const second = await update_like_count();
        }

        start();
    });

}