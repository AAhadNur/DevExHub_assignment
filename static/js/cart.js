
let updateBtns = document.getElementsByClassName('update-cart')

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        let productID = this.dataset.product
        let stock = this.dataset.product.stock_status
        let action = this.dataset.action

        if(user === 'AnonymousUser') {
            addCookieItem(productID, action, stock)
        }else {
            updateUserOrder(productID, action, stock)
        }
    })
}


function addCookieItem(productID, action, stock) {

    if (stock >= 1){
        if (action == 'add'){
            if (cart[productID] == undefined) {
                cart[productID] = {'quantity':1}
            } else {
                cart[productID]['quantity'] += 1
            }
        }
    }
    
    if (action == 'remove') {
        cart[productID]['quantity'] -= 1

        if ( cart[productID]['quantity'] <= 0 ) {
            delete cart[productID]
        }
    }

    console.log('cart : ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}


function updateUserOrder(productID, action) {

    let url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers:{
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'productID':productID, 'action':action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        location.reload()
    })
}