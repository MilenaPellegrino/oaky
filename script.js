// Base de datos simple (se guarda en localStorage)
let products = JSON.parse(localStorage.getItem('products')) || [];

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Cargar productos existentes
    loadProducts();
    
    // Configurar formularios
    document.getElementById('product-form').addEventListener('submit', addProduct);
    document.getElementById('barcode-form').addEventListener('submit', searchByBarcode);
    document.getElementById('name-form').addEventListener('submit', searchByName);
});

// Funciones para cambiar pestañas
function openTab(tabName) {
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = 'none';
    }
    
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    document.getElementById(tabName).style.display = 'block';
    event.currentTarget.classList.add('active');
}

// Mostrar formulario de búsqueda según opción
function showSearch(type) {
    document.getElementById('barcode-search').style.display = 'none';
    document.getElementById('name-search').style.display = 'none';
    document.getElementById('search-results').innerHTML = '';
    
    document.getElementById(`${type}-search`).style.display = 'block';
}

// Añadir nuevo producto
function addProduct(e) {
    e.preventDefault();
    
    const barcode = document.getElementById('barcode').value;
    const name = document.getElementById('name').value || 'Sin nombre';
    const price = parseFloat(document.getElementById('price').value);
    
    // Validar que el código de barras no exista
    const exists = products.some(product => product.barcode === barcode);
    if (exists) {
        showMessage('Error: El código de barras ya existe', 'error');
        return;
    }
    
    // Añadir producto
    products.push({ barcode, name, price });
    saveProducts();
    
    // Limpiar formulario y mostrar mensaje
    document.getElementById('product-form').reset();
    showMessage('Producto agregado correctamente', 'success');
}

// Buscar por código de barras
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
    const foundProducts = products.filter(p => 
        p.name.toLowerCase().includes(name)
    );
    
    if (foundProducts.length === 1) {
        displayResults(foundProducts[0]);
    } else if (foundProducts.length > 1) {
        displayMultipleResults(foundProducts);
    } else {
        displayResults(null);
    }
}

// Mostrar resultados de búsqueda
function displayResults(product) {
    const resultsDiv = document.getElementById('search-results');
    
    if (!product) {
        resultsDiv.innerHTML = '<p>No se encontró el producto</p>';
        return;
    }
    
    resultsDiv.innerHTML = `
        <div class="product-item">
            <p><strong>Código:</strong> ${product.barcode}</p>
            <p><strong>Nombre:</strong> ${product.name}</p>
            <p><strong>Precio:</strong> $${product.price.toFixed(2)}</p>
        </div>
    `;
}

// Mostrar múltiples resultados
function displayMultipleResults(products) {
    const resultsDiv = document.getElementById('search-results');
    let html = '<h3>Varios productos encontrados:</h3>';
    
    products.forEach(product => {
        html += `
            <div class="product-item">
                <p><strong>Código:</strong> ${product.barcode}</p>
                <p><strong>Nombre:</strong> ${product.name}</p>
                <p><strong>Precio:</strong> $${product.price.toFixed(2)}</p>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = html;
}

// Mostrar mensajes
function showMessage(text, type) {
    const messageDiv = document.getElementById('message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    
    setTimeout(() => {
        messageDiv.textContent = '';
        messageDiv.className = 'message';
    }, 3000);
}

// Guardar productos en localStorage
function saveProducts() {
    localStorage.setItem('products', JSON.stringify(products));
}

// Cargar productos desde localStorage
function loadProducts() {
    products = JSON.parse(localStorage.getItem('products')) || [];
}

// Mostrar todos los productos
function displayAllProducts() {
    const productsList = document.getElementById('products-list');
    productsList.innerHTML = '';
    
    if (products.length === 0) {
        productsList.innerHTML = '<p>No hay productos cargados.</p>';
        return;
    }
    
    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'product-card';
        productCard.innerHTML = `
            <h3>${product.name}</h3>
            <p><strong>Código:</strong> ${product.barcode}</p>
            <p><strong>Precio:</strong> $${product.price.toFixed(2)}</p>
        `;
        productsList.appendChild(productCard);
    });
}

// Generar PDF
function generatePDF() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    
    // Título
    doc.setFontSize(20);
    doc.setTextColor(255, 133, 162);
    doc.text('Listado de Productos - Tienda de Bebés', 15, 20);
    
    // Fecha
    doc.setFontSize(10);
    doc.setTextColor(100);
    doc.text(`Generado el: ${new Date().toLocaleDateString()}`, 15, 30);
    
    // Tabla de productos
    const headers = [['Código', 'Nombre', 'Precio']];
    const data = products.map(p => [p.barcode, p.name, `$${p.price.toFixed(2)}`]);
    
    doc.autoTable({
        head: headers,
        body: data,
        startY: 40,
        styles: {
            cellPadding: 5,
            fontSize: 10,
            valign: 'middle',
            halign: 'left'
        },
        headStyles: {
            fillColor: [255, 133, 162],
            textColor: 255
        },
        alternateRowStyles: {
            fillColor: [255, 235, 238]
        },
        columnStyles: {
            0: { cellWidth: 40 },
            1: { cellWidth: 100 },
            2: { cellWidth: 30 }
        }
    });
    
    // Guardar PDF
    doc.save('productos_tienda_bebes.pdf');
}

// Modifica la función openTab para mostrar productos cuando se active esa pestaña
function openTab(tabName) {
    const tabContents = document.getElementsByClassName('tab-content');
    for (let i = 0; i < tabContents.length; i++) {
        tabContents[i].style.display = 'none';
    }
    
    const tabButtons = document.getElementsByClassName('tab-button');
    for (let i = 0; i < tabButtons.length; i++) {
        tabButtons[i].classList.remove('active');
    }
    
    document.getElementById(tabName).style.display = 'block';
    event.currentTarget.classList.add('active');
    
    // Si es la pestaña de ver productos, actualiza la lista
    if (tabName === 'view-products') {
        displayAllProducts();
    }
}

// Configurar formulario de actualización de precios
document.getElementById('update-prices-form').addEventListener('submit', updatePrices);

// Función para actualizar precios según porcentaje
function updatePrices(e) {
    e.preventDefault();
    
    const percentage = parseFloat(document.getElementById('percentage').value);
    
    if (isNaN(percentage) || percentage < 0) {
        showUpdateMessage('Por favor ingrese un porcentaje válido', 'error');
        return;
    }
    
    // Confirmar con el usuario antes de aplicar cambios
    if (confirm(`¿Está seguro que desea aumentar todos los precios en ${percentage}%?`)) {
        // Aplicar aumento a todos los productos
        products.forEach(product => {
            product.price = product.price * (1 + percentage / 100);
        });
        
        saveProducts();
        displayAllProducts();
        showUpdateMessage(`Precios actualizados con un aumento del ${percentage}%`, 'success');
        document.getElementById('update-prices-form').reset();
    }
}

// Mostrar mensajes en el formulario de actualización
function showUpdateMessage(text, type) {
    const messageDiv = document.getElementById('update-message');
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    
    setTimeout(() => {
        messageDiv.textContent = '';
        messageDiv.className = 'message';
    }, 3000);
}