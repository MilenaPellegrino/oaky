let products = JSON.parse(localStorage.getItem('products')) || [];

document.addEventListener('DOMContentLoaded', function() {
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

    if (products.some(p => p.barcode === barcode)) {
        showMessage('Error: El código de barras ya existe', 'error');
        return;
    }

    products.push({ barcode, name, price });
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
        </div>
    `;
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

// Mostrar todos
function displayAllProducts() {
    const div = document.getElementById('products-list');
    div.innerHTML = '';
    if (products.length === 0) {
        div.innerHTML = '<p>No hay productos cargados.</p>';
        return;
    }

    for (let p of products) {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <h3>${p.name}</h3>
            <p><strong>Código:</strong> ${p.barcode}</p>
            <p><strong>Precio:</strong> $${p.price.toFixed(2)}</p>`;
        div.appendChild(card);
    }
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
    showUpdateMessage(`Precios aumentados un ${percent}%`, 'success');
}

// PDF
function generatePDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();

    doc.setFontSize(20);
    doc.setTextColor(255, 133, 162);
    doc.text('Listado de Productos - Tienda de Bebés', 15, 20);

    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text(`Generado el: ${new Date().toLocaleDateString()}`, 15, 30);

    const headers = [['Código', 'Nombre', 'Precio']];
    const data = products.map(p => [p.barcode, p.name, `$${p.price.toFixed(2)}`]);

    doc.autoTable({
        head: headers,
        body: data,
        startY: 40,
    });

    doc.save('productos.pdf');
}
