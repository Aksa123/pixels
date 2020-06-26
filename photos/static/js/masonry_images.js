const page_detail = JSON.parse(document.getElementById('data_js').textContent)
const url = page_detail.url
var page = 1
var masonry_container = document.querySelector("#masonry-container")
var target = document.querySelector('#last-image')


// masonry using macy.js
var macy = Macy({
    container: '#masonry-container',
    trueOrder: false,
    waitForImages: true,
    margin: 10,
    columns: 4,
    breakAt: {
        1200: 5,
        940: 3,
        520: 2,
        400: 1
    }
});


let options = {
    // root: document.querySelector('#scrollArea'),
    rootMargin: '0px',
    threshold: 0
  }
  

var callback = (entries, observer) => {
    entries.forEach(entry => {
      // Each entry describes an intersection change for one observed
      // target element:
      //   entry.boundingClientRect
      //   entry.intersectionRatio
      //   entry.intersectionRect
      //   entry.isIntersecting
      //   entry.rootBounds
      //   entry.target
      //   entry.time
    
    if (entry.isIntersecting){
        console.log("ajax is called!")
        entry.target.removeAttribute("id")
        let csrf = document.querySelector("[name=csrfmiddlewaretoken]").value
        let data = new FormData()
        page += 1
        data.append('page', page)

        fetch(url, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: data
        })
        .then(response => response.json())
        .then(function(result){
            let new_photos = result.new_photos
            for (let i=0; i< new_photos.length; i++){
                if (i===new_photos.length-1 && new_photos.length >= 20){
                    masonry_container.innerHTML += 
                    "<div class='masonry-image-container'>" +
                    "<a href='/photo/" + new_photos[i].id + "/'><img class='masonry-image' id='last-image' src='" + new_photos[i].src + "'></a>" +
                    "</div>"
                }
                else{
                masonry_container.innerHTML += 
                    "<div class='masonry-image-container'>" +
                    "<a href='/photo/" + new_photos[i].id + "/'><img class='masonry-image' src='" + new_photos[i].src + "'></a>" +
                    "</div>"
                }
                
            }
            macy.runOnImageLoad(function(){
                console.log("mansory recalculate once all images are loaded")
                macy.recalculate(true, true)
            })
            target = document.querySelector('#last-image')
            observer.observe(target)


        })       
    }
    })
}
var observer = new IntersectionObserver(callback, options)
observer.observe(target)