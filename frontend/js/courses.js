"use strict";

function getCards() {
    // Does AJAX request to the backend, returns json
}

function addCards(cards, cardsElement) {
    for (let card of cards) {
        let colElement = document.createElement("div");
        colElement.setAttribute("class", "col");

        let cardElement = document.createElement("div");
        cardElement.setAttribute("class", "course card h-100");

        let cardImageElement = document.createElement("img");
        cardImageElement.setAttribute("class", "card-img-top");
        cardImageElement.setAttribute("src", `./images/${card.image}`);
        cardElement.appendChild(cardImageElement);

        let cardTitleElement = document.createElement("h5");
        cardTitleElement.setAttribute("class", "card-title");
        cardTitleElement.textContent = card.name;

        let cardDescriptionElement = document.createElement("p");
        cardDescriptionElement.setAttribute("class", "card-text");
        cardDescriptionElement.textContent = card.description;

        let cardBodyElement = document.createElement("div");
        cardBodyElement.setAttribute("class", "card-body");
        cardBodyElement.appendChild(cardTitleElement);
        cardBodyElement.appendChild(cardDescriptionElement);
        cardElement.appendChild(cardBodyElement);

        let ratingElement = document.createElement("span");
        ratingElement.setAttribute("class", "rating ms-3 mb-3");
        
        for (let starCount = 0; starCount < 5; starCount++) {
            let starElement = document.createElement("span");

            if (starCount < card.rating) {
                starElement.setAttribute("class", "fa fa-star checked");
            } 
            else {
                starElement.setAttribute("class", "fa fa-star");
            }
            ratingElement.appendChild(starElement);
        }
        cardElement.appendChild(ratingElement);

        let linkElement = document.createElement("a");
        linkElement.setAttribute("class", "stretched-link");
        linkElement.setAttribute("href", "#");
        cardElement.appendChild(linkElement);

        colElement.appendChild(cardElement);
        cardsElement.appendChild(colElement);

        // cardsElement.innerHTML += 
        //     `<div class="col">
        //         <div class="course card h-100">
        //             <img src="./images/${card.image}" class="card-img-top" alt="Course preview">
        //             <div class="card-body">
        //                 <h5 class="card-title">${card.name}</h5>
        //                 <p class="card-text">${card.description}</p>
        //                 <!-- https://www.vecteezy.com/free-photos -->
        //             </div>
        //             <div class="rating ms-3 mb-3">
        //                 ${stars}
        //             </div>
        //             <a href="#" class="stretched-link"></a>
        //         </div>
        //     </div>`.trim();
    }
}

window.onload = () => {
    let courses = [
        {id: 0, name: "Test1", description: "Description", rating: 5, image: "python-course-preview.webp", author: 1},
        {id: 1, name: "Test2", description: "Description2", rating: 4, image: "python-course-preview.webp", author: 1},
    ];
    addCards(courses, document.querySelector("#courses"));
};