"use strict";

function addCourses(url) {
    // Does AJAX request to the backend
    let xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.responseType = 'json';
    xhr.send();

    xhr.onload = function() {
        let courses = xhr.response;
        addCards(courses, document.querySelector("#courses"));
    };
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
    }
}

window.onload = () => {
    addCourses("http://127.0.0.1:8000/api/courses/");
};