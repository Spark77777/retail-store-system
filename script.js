let products = JSON.parse(localStorage.getItem("products")) || [];

function saveData() {
    localStorage.setItem("products", JSON.stringify(products));
}

function addProduct() {
    let name = document.getElementById("name").value;
    let price = document.getElementById("price").value;
    let qty = document.getElementById("qty").value;

    if (!name || !price || !qty) {
        alert("Fill all fields");
        return;
    }

    products.push({ name, price, qty: parseInt(qty) });
    saveData();
    displayProducts();
}

function sellProduct(index) {
    let quantity = prompt("Enter quantity to sell:");

    if (quantity <= products[index].qty) {
        products[index].qty -= quantity;
        saveData();
        displayProducts();
    } else {
        alert("Not enough stock!");
    }
}

function displayProducts() {
    let table = document.getElementById("productTable");
    table.innerHTML = "";

    products.forEach((p, i) => {
        table.innerHTML += `
            <tr>
                <td>${p.name}</td>
                <td>${p.price}</td>
                <td>${p.qty}</td>
                <td><button onclick="sellProduct(${i})">Sell</button></td>
            </tr>
        `;
    });
}

displayProducts();
