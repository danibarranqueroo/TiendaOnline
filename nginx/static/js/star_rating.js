document.addEventListener('DOMContentLoaded', async () => {
    const span_para_estrellas = document.querySelectorAll('span.sp');

    span_para_estrellas.forEach(async (ele) => {
        const productId = ele.getAttribute('data-product-id');

        try {
            const response = await fetch(`/api/productos/${productId}`);
            const data = await response.json();

            const rating = data.rating.rate;
            ele.innerHTML = generarHTMLDeEstrellas(rating, productId);
            
            const stars = ele.querySelectorAll('.fa-star');
            stars.forEach((star, index) => {
                star.dataset.index = index; // Añadir data-index a cada estrella

                star.addEventListener('click', async () => {
                    const newRating = parseInt(star.getAttribute('data-index')) + 1;
                    const prodId = star.getAttribute('data-product-id');
            
                    // Comprobar si el usuario ya ha votado
                    if (localStorage.getItem(`voted_${prodId}`)) {
                        star.parentNode.querySelector('.vote-message').textContent = 'Ya has votado'; // Seleccionar el mensaje utilizando querySelector
                        console.error('Ya has votado');
                        return;
                    }
            
                    try {
                        const putResponse = await fetch(`/api/productos/${prodId}/${newRating}`, {method: 'PUT'});
                        if (putResponse.status === 202) {
                            const updatedResponse = await fetch(`/api/productos/${prodId}`);
                            const updatedData = await updatedResponse.json();
                            const updatedRating = updatedData.rating.rate;
                            star.parentNode.innerHTML = generarHTMLDeEstrellas(updatedRating, prodId);
            
                            // Marcar que el usuario ya ha votado
                            localStorage.setItem(`voted_${prodId}`, 'true');
                        } else {
                            console.error('Error al enviar la calificación');
                        }
                    } catch (error) {
                        console.error('Error al enviar la calificación', error);
                    }
                });

                star.addEventListener('mouseover', (event) => {
                    const index = parseInt(event.target.dataset.index);
                    const stars = ele.querySelectorAll('.fa-star');
                
                    stars.forEach((star, i) => {
                        if (i <= index) {
                            star.classList.add('checked');
                        } else {
                            star.classList.remove('checked');
                        }
                    });
                });                
        
                ele.addEventListener('mouseout', () => {
                    const rating = data.rating.rate;
                    const stars = ele.querySelectorAll('.fa-star');

                    stars.forEach((star, i) => {
                        if (i < rating) {
                            star.classList.add('checked');
                        } else {
                            star.classList.remove('checked');
                        }
                    });
                });
            });
            
        } catch (error) {
            console.error('Error al obtener la calificación del producto', error);
        }
    });
});

function generarHTMLDeEstrellas(rating, prodId) {
    let starsHTML = '';
    for (let i = 0; i < 5; i++) {
        if (i < rating) {
            starsHTML += `<span class="fa fa-star checked" data-index="${i}" data-product-id="${prodId}"></span>`;
        } else {
            starsHTML += `<span class="fa fa-star" data-index="${i}" data-product-id="${prodId}"></span>`;
        }
    }
    starsHTML += '<p class="vote-message text-danger"></p>'; // Agregar elemento para el mensaje
    return starsHTML;
}

// function generarHTMLDeEstrellas(rating) {
//     let starsHTML = '';
//     for (let i = 0; i < 5; i++) {
//         if (i < rating) {
//             starsHTML += '<span class="fa fa-star checked"></span>';
//         } else {
//             starsHTML += '<span class="fa fa-star"></span>';
//         }
//     }
//     return starsHTML;
// }
