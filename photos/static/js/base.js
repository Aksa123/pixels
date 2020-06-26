var navbar_search_form = document.querySelector("#navbar-search-form")

navbar_search_form.addEventListener("submit", function(e){
    e.preventDefault()
    let search_keyword = navbar_search_form.querySelector("#navbar-search").value
    window.location.href = "/search/" + search_keyword +"/"
})