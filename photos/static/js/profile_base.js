const profile_data = JSON.parse(document.getElementById('profile-data').textContent);
var follow_button = document.querySelector("#follow-button")
var follow_status = profile_data.follow_status
var follower_follow_button = document.querySelectorAll(".collection-follower-follow-button")
var follower_unfollow_button = document.querySelectorAll(".collection-follower-unfollow-button")


function follow_user(){
    follow_button.addEventListener("click", function(){
        let url = "/make-follow"
        let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value
        data = new FormData()
        data.append("user_id", profile_data.profile_id)
        data.append("new_follow_status", !follow_status)

        fetch(url,{
            method: "POST",
            headers: {
                "X-CSRFToken": csrf
            },
            body: data
        })
        .then(response => response.json())
        .then(function(result){
            follow_status = result.current_follow_status

            if (follow_status){
                follow_button.className = "btn btn-secondary follow-message-button"
                follow_button.innerHTML = "<i>Following</i>"
            }else{
                follow_button.className = "btn btn-info follow-message-button"
                follow_button.innerHTML = "Follow"
            }
        })
    })
}



function follower_follow_function(btn, current_follow_status){
    btn.onclick = function(){
        let url = "/make-follow"
        let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value
        let data = new FormData()
        data.append("user_id", parseInt(btn.value))
        data.append("new_follow_status", !current_follow_status)
        console.log("click")
        fetch(url,{
            method: "POST",
            headers: {
                "X-CSRFToken": csrf
            },
            body: data
        })
        .then(response => response.json())
        .then(function(result){
            current_follow_status = result.current_follow_status
            if (current_follow_status){
                btn.className = "collection-follower-unfollow-button btn btn-info"
                btn.innerHTML = "<i>Already Following</i>"
            }
            else{
                btn.className = "collection-follower-unfollow-button btn btn-success"
                btn.innerHTML = "Follow"
            }
            follower_follow_function(btn, current_follow_status)
        })
    }
}




follow_user()
for (let i=0; i< follower_follow_button.length; i++){
    follower_follow_function(follower_follow_button[i], false)
}
for (let i=0; i< follower_unfollow_button.length; i++){
    follower_follow_function(follower_unfollow_button[i], true)
}