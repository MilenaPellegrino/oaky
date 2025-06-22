
let products = JSON.parse(localStorage.getItem('products')) || [];

document.addEventListener('DOMContentLoaded', function () {
    loadProducts();

    document.getElementById('product-form').addEventListener('submit', addProduct);
    document.getElementById('barcode-form').addEventListener('submit', searchByBarcode);
    document.getElementById('name-form').addEventListener('submit', searchByName);
    document.getElementById('update-prices-form').addEventListener('submit', updatePrices);
});

// Tabs
function openTab(tabName, btn) {
    const tabs = document.getElementsByClassName('tab-content');
    for (let tab of tabs) tab.style.display = 'none';

    const buttons = document.getElementsByClassName('tab-button');
    for (let b of buttons) b.classList.remove('active');

    document.getElementById(tabName).style.display = 'block';
    btn.classList.add('active');

    if (tabName === 'view-products') displayAllProducts();
}

// Mostrar formularios de búsqueda
function showSearch(type) {
    document.getElementById('barcode-search').style.display = 'none';
    document.getElementById('name-search').style.display = 'none';
    document.getElementById('search-results').innerHTML = '';
    document.getElementById(`${type}-search`).style.display = 'block';
}

// Agregar producto
function addProduct(e) {
    e.preventDefault();
    const barcode = document.getElementById('barcode').value;
    const name = document.getElementById('name').value || 'Sin nombre';
    const price = parseFloat(document.getElementById('price').value);
    const stock = parseInt(document.getElementById('stock').value);

    if (products.some(p => p.barcode === barcode)) {
        showMessage('Error: El código de barras ya existe', 'error');
        return;
    }

    products.push({ barcode, name, price, stock });
    saveProducts();
    document.getElementById('product-form').reset();
    showMessage('Producto agregado correctamente', 'success');
}

// Buscar por código
function searchByBarcode(e) {
    e.preventDefault();
    const barcode = document.getElementById('search-barcode').value;
    const product = products.find(p => p.barcode === barcode);
    displayResults(product);
}

// Buscar por nombre
function searchByName(e) {
    e.preventDefault();
    const name = document.getElementById('search-name').value.toLowerCase();
    const found = products.filter(p => p.name.toLowerCase().includes(name));

    if (found.length === 1) displayResults(found[0]);
    else if (found.length > 1) displayMultipleResults(found);
    else displayResults(null);
}

// Mostrar un resultado
function displayResults(product) {
    const div = document.getElementById('search-results');
    if (!product) {
        div.innerHTML = '<p>No se encontró el producto</p>';
        return;
    }
    div.innerHTML = `
        <div class="product-item">
            <p><strong>Código:</strong> ${product.barcode}</p>
            <p><strong>Nombre:</strong> ${product.name}</p>
            <p><strong>Precio:</strong> $${product.price.toFixed(2)}</p>
            <p><strong>Stock:</strong> ${product.stock}</p>
            <button onclick="editProduct('${product.barcode}')">Editar Precio</button>
            <button onclick="editStock('${product.barcode}')">Modificar Stock</button>
            <button onclick="deleteProduct('${product.barcode}')">Eliminar</button>
        </div>
    `;
}

// Editar producto
function editProduct(barcode) {
    const product = products.find(p => p.barcode === barcode);
    if (!product) return;

    const newPrice = prompt("Ingrese el nuevo precio para " + product.name + ":", product.price.toFixed(2));
    if (newPrice === null) return; // Si el usuario cancela
    
    const parsedPrice = parseFloat(newPrice);
    if (isNaN(parsedPrice)) {
        alert("Por favor ingrese un precio válido");
        return;
    }

    product.price = parsedPrice;
    saveProducts();
    
    // Actualizar la visualización
    const currentTab = document.querySelector('.tab-button.active').getAttribute('onclick').match(/'([^']+)'/)[1];
    if (currentTab === 'view-products') {
        displayAllProducts();
    } else {
        displayResults(product);
    }
    
    showMessage('Precio actualizado correctamente', 'success');
}

// Mostrar varios resultados
function displayMultipleResults(found) {
    const div = document.getElementById('search-results');
    let html = '<h3>Varios productos encontrados:</h3>';
    for (let p of found) {
        html += `
        <div class="product-item">
            <p><strong>Código:</strong> ${p.barcode}</p>
            <p><strong>Nombre:</strong> ${p.name}</p>
            <p><strong>Precio:</strong> $${p.price.toFixed(2)}</p>
        </div>`;
    }
    div.innerHTML = html;
}

// Mensajes
function showMessage(text, type) {
    const msg = document.getElementById('message');
    msg.textContent = text;
    msg.className = `message ${type}`;
    setTimeout(() => {
        msg.textContent = '';
        msg.className = 'message';
    }, 3000);
}

function showUpdateMessage(text, type) {
    const msg = document.getElementById('update-message');
    msg.textContent = text;
    msg.className = `message ${type}`;
    setTimeout(() => {
        msg.textContent = '';
        msg.className = 'message';
    }, 3000);
}

// Guardar productos
function saveProducts() {
    localStorage.setItem('products', JSON.stringify(products));
}

// Cargar productos
function loadProducts() {
    products = JSON.parse(localStorage.getItem('products')) || [];
}

// Eliminar producto
function deleteProduct(barcode) {
    const confirmDelete = confirm("¿Estás seguro de que querés eliminar este producto?");
    if (!confirmDelete) return;

    products = products.filter(p => p.barcode !== barcode);
    saveProducts();
    document.getElementById('search-results').innerHTML = '<p>Producto eliminado correctamente.</p>';
}

// Ajustar precios
function updatePrices(e) {
    e.preventDefault();
    const percent = parseFloat(document.getElementById('percentage').value);
    if (isNaN(percent)) return;

    products = products.map(p => ({
        ...p,
        price: p.price * (1 + percent / 100)
    }));

    saveProducts();
    displayAllProducts();
    showUpdateMessage(`Precios aumentados un ${percent}%.`, 'success');
}

// PDF
function generatePDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const products = JSON.parse(localStorage.getItem('products')) || [];

    doc.text('Listado de Productos', 10, 10);

    doc.autoTable({
        head: [['Código', 'Nombre', 'Precio', 'Stock']],
        body: products.map(p => [
            p.barcode,
            p.name || 'Sin nombre',
            `$${parseFloat(p.price).toFixed(2)}`,
            p.stock != null ? p.stock : '0'
        ]),
        startY: 20
    });

    doc.save('productos.pdf');
}


// Importar CSV
function importCSV() {
    const fileInput = document.getElementById('csv-file');
    const file = fileInput.files[0];
    const importMsg = document.getElementById('import-message');

    if (!file) {
        importMsg.textContent = 'Seleccioná un archivo CSV';
        importMsg.className = 'message error';
        return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
        const lines = e.target.result.split('\n');
        let count = 0;
        for (let i = 1; i < lines.length; i++) {
            const line = lines[i].trim();
            if (!line) continue;

            const [barcode, name, price, stock] = line.split(',');

            if (products.some(p => p.barcode === barcode)) continue;

            const parsedPrice = parseFloat(price);
            const parsedStock = parseInt(stock);

            if (!barcode || isNaN(parsedPrice) || isNaN(parsedStock)) continue;

            products.push({
                barcode: barcode.trim(),
                name: (name || 'Sin nombre').trim(),
                price: parsedPrice,
                stock: parsedStock
            });
            count++;
        }

        saveProducts();
        fileInput.value = '';
        importMsg.textContent = `Se importaron ${count} productos correctamente.`;
        importMsg.className = 'message success';
    };

    reader.onerror = () => {
        importMsg.textContent = 'Error al leer el archivo.';
        importMsg.className = 'message error';
    };

    reader.readAsText(file);
}

// Mostrar todos
function displayAllProducts() {
    const container = document.getElementById('all-products');
    if (!container) return;

    if (products.length === 0) {
        container.innerHTML = '<p>No hay productos para mostrar.</p>';
        return;
    }

    let html = '';
    for (let p of products) {
        html += `
            <div class="product-item">
                <p><strong>Código:</strong> ${p.barcode}</p>
                <p><strong>Nombre:</strong> ${p.name}</p>
                <p><strong>Precio:</strong> $${p.price.toFixed(2)}</p>
                <p><strong>Stock:</strong> ${p.stock}</p>
                <button onclick="editProduct('${p.barcode}')">Editar Precio</button>
                <button onclick="deleteProduct('${p.barcode}')">Eliminar</button>
            </div>
        `;
    }
    container.innerHTML = html;
}

function generateExcel() {
    const products = JSON.parse(localStorage.getItem('products')) || [];

    // Creamos una hoja de cálculo con los datos
    const worksheetData = [
        ['Código', 'Nombre', 'Precio', 'Stock'],
        ...products.map(p => [
            p.barcode,
            p.name || 'Sin nombre',
            p.price.toFixed(2),
            p.stock != null ? p.stock : 0
        ])
    ];

    // Convertimos el arreglo a hoja de Excel
    const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);

    // Creamos un libro de Excel y agregamos la hoja
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, 'Productos');

    // Generamos el archivo y lo descargamos
    XLSX.writeFile(workbook, 'productos.xlsx');
}


function editStock(barcode) {
    const product = products.find(p => p.barcode === barcode);
    if (!product) return;

    const newStock = prompt(`Stock actual: ${product.stock}\nIngresá el nuevo stock:`, product.stock);
    if (newStock !== null && !isNaN(newStock)) {
        product.stock = parseInt(newStock);
        saveProducts();
        alert('Stock actualizado correctamente');

        // Actualizar visualización según la pestaña activa
        const currentTab = document.querySelector('.tab-button.active').getAttribute('onclick').match(/'([^']+)'/)[1];
        if (currentTab === 'view-products') {
            displayAllProducts();
        } else {
            displayResults(product);
        }
    }
}

function showSearch(type) {
    document.getElementById('barcode-search').style.display = type === 'barcode' ? 'block' : 'none';
    document.getElementById('name-search').style.display = type === 'name' ? 'block' : 'none';
    document.getElementById('search-results').innerHTML = '';
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('barcode-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const barcode = document.getElementById('search-barcode').value.trim();
        showProductDetails(barcode, 'barcode');
    });

    document.getElementById('name-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const name = document.getElementById('search-name').value.trim().toLowerCase();
        showProductDetails(name, 'name');
    });
});

function showProductDetails(searchValue, type) {
    const products = JSON.parse(localStorage.getItem('products')) || [];
    const foundIndex = products.findIndex(p =>
        type === 'barcode' ? p.barcode === searchValue : (p.name || '').toLowerCase() === searchValue
    );
    const results = document.getElementById('search-results');

    if (foundIndex === -1) {
        results.innerHTML = '<p>Producto no encontrado.</p>';
        return;
    }

    const product = products[foundIndex];

    results.innerHTML = `
        <p><strong>Nombre:</strong> ${product.name || 'Sin nombre'}</p>
        <p><strong>Precio:</strong> $<span id="price-value">${product.price}</span></p>
        <input type="number" id="new-price" placeholder="Nuevo precio" step="0.01" min="0">
        <button onclick="updatePrice(${foundIndex})">Actualizar Precio</button>

        <p><strong>Stock:</strong> <span id="stock-value">${product.stock}</span></p>
        <div>
            <button onclick="adjustStock(${foundIndex}, 1)">➕</button>
            <button onclick="adjustStock(${foundIndex}, -1)">➖</button>
        </div>
        <input type="number" id="new-stock" placeholder="Nuevo stock" min="0">
        <button onclick="updateStock(${foundIndex})">Modificar Stock</button>

        <br><br>
        <button style="color: red;" onclick="deleteProduct(${foundIndex})">🗑️ Eliminar Producto</button>
    `;
}

function adjustStock(index, change) {
    const products = JSON.parse(localStorage.getItem('products')) || [];
    if (!products[index]) return;

    products[index].stock = Math.max(0, (products[index].stock || 0) + change);
    localStorage.setItem('products', JSON.stringify(products));

    document.getElementById('stock-value').textContent = products[index].stock;
}

function updateStock(index) {
    const newStock = parseInt(document.getElementById('new-stock').value);
    if (isNaN(newStock) || newStock < 0) {
        alert("Stock inválido");
        return;
    }

    const products = JSON.parse(localStorage.getItem('products')) || [];
    products[index].stock = newStock;
    localStorage.setItem('products', JSON.stringify(products));

    document.getElementById('stock-value').textContent = newStock;
}

function updatePrice(index) {
    const newPrice = parseFloat(document.getElementById('new-price').value);
    if (isNaN(newPrice) || newPrice < 0) {
        alert("Precio inválido");
        return;
    }

    const products = JSON.parse(localStorage.getItem('products')) || [];
    products[index].price = newPrice;
    localStorage.setItem('products', JSON.stringify(products));

    document.getElementById('price-value').textContent = newPrice.toFixed(2);
}

function deleteProduct(index) {
    if (!confirm("¿Estás seguro que querés eliminar este producto?")) return;

    const products = JSON.parse(localStorage.getItem('products')) || [];
    products.splice(index, 1);
    localStorage.setItem('products', JSON.stringify(products));

    document.getElementById('search-results').innerHTML = '<p>Producto eliminado.</p>';
}


