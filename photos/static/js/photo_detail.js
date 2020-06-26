const photo_detail = JSON.parse(document.getElementById('photo-data').textContent);
const photo_id = photo_detail.photo_id

var stat_numbers = document.querySelectorAll(".stat-number")

var like_button = document.querySelector("#like-button")
var like_number = document.querySelector("#like-number")
var like_icon = document.querySelector("#like-icon")
var liked = photo_detail.liked

var favorite_button = document.querySelector("#favorite-button")
var favorite_icon = document.querySelector("#favorite-icon")
var favorited = photo_detail.favorited

var follow_button = document.querySelector("#follow-button")
var follow_status = photo_detail.follow_status
var following_user_id = photo_detail.user_id

var download = document.querySelector("#download")
var download_form = document.querySelector("#download-form")

like_button.addEventListener("click", function(){
    console.log("akjdksjadk")
    let url = "/update-like/"
    let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value
    data = new FormData()
    data.append('photo_id', photo_id)
    data.append("new_like_status", !liked)
    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf
        },
        body: data
    })
    .then(response => response.json())
    .then(function(result){
        liked = result.liked
        let new_like_number = result.new_like_number
        like_number.innerHTML = new_like_number

        if (liked === true){
            like_icon.src = "/static/img/liked.png"
        }
        else{
            like_icon.src = "/static/img/like.png"
        }
    })
})



favorite_button.addEventListener("click", function(){
    let url = "/update-favorite/"
    let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value
    data = new FormData()
    data.append('photo_id', photo_id)
    data.append("new_favorite_status", !favorited)
    fetch(url, {
        method: "POST",
        headers: {
            "X-CSRFToken": csrf
        },
        body: data
    })
    .then(response => response.json())
    .then(function(result){
        favorited = result.favorited
        console.log(result)

        if (favorited === true){
            favorite_icon.src = "/static/img/favorited.png"
        }
        else{
            favorite_icon.src = "/static/img/favorite.png"
        }
    })
})

if (follow_button){
    follow_button.addEventListener("click", function(){
        let url = '/make-follow'
        let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value
        let data = new FormData()
        data.append("user_id", following_user_id)
        data.append("new_follow_status", !follow_status)
    
        fetch(url, {
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
                follow_button.className = "btn btn-secondary"
                follow_button.innerHTML = "<i>Following</i>"
            }
            else{
                follow_button.className = "btn btn-outline-info"
                follow_button.innerHTML = "Follow"
            }
        })
    })
}



download_form.addEventListener("submit", function(e){
    e.preventDefault()
    let size = ""
    let width = 0
    let height = 0
    let options = download_form.querySelectorAll("[name=download-size")
    for (i=0; i<options.length; i++){
        if (options[i].checked){
            if (options[i].value === "custom"){
                width = download_form.querySelector("[name=width").value
                height = download_form.querySelector("[name=height").value
            }
            else{
                width = options[i].value.split("x")[0]
                height = options[i].value.split("x")[1]
            }
        }
    }
    
    let url = new URL("/photo-download/" + photo_id + "/" + width + "-" + height + "/", window.location.href)
    window.location = url
})



for(i=0; i<stat_numbers.length; i++){
    stat_numbers[i].innerHTML = parseInt(stat_numbers[i].innerHTML).toLocaleString()
}