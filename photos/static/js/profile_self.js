const profile_data = JSON.parse(document.getElementById('profile-data').textContent);
var follow_button = document.querySelector("#follow-button")
var following = profile_data.following


follow_button.addEventListener("click", function(){
    let url = "/make-follow"
    let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value
    data = new FormData()
    data.append("user_id", profile_data.profile_id)
    data.append("new_following", !following)
    console.log(following)
    console.log(profile_data.user_id)

    fetch(url,{
        method: "POST",
        headers: {
            "X-CSRFToken": csrf
        },
        body: data
    })
    .then(response => response.json())
    .then(function(result){
        following = result.follow

        if (following){
            follow_button.className = "btn btn-secondary follow-message-button"
            follow_button.innerHTML = "<i>Following</i>"
        }else{
            follow_button.className = "btn btn-info follow-message-button"
            follow_button.innerHTML = "Follow"
        }
    })
})