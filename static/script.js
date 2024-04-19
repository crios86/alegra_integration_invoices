document.addEventListener('DOMContentLoaded', function() {
    // Obtener los nombres de los clientes del backend
    fetch('/customer_names')
        .then(response => response.json())
        .then(data => {
            // Almacenar los nombres de los clientes en una variable global
            window.customer_names = data;
            
            // Agregar opciones de nombres de clientes a la fila inicial del formulario
            var selectCustomer = document.querySelector('select[name="razon_social"]');
            window.customer_names.forEach(function(name) {
                var option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                selectCustomer.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching customer names:', error));

    // Obtener los nombres de los productos del backend
    fetch('/product_names')
        .then(response => response.json())
        .then(data => {
            // Almacenar los nombres de los productos en una variable global
            window.product_names = data;
            
            // Agregar opciones de nombres de productos a la fila inicial del formulario
            var selectProduct = document.querySelector('select[name="nombre_producto"]');
            window.product_names.forEach(function(name) {
                var option = document.createElement('option');
                option.value = name;
                option.textContent = name;
                selectProduct.appendChild(option);
            });
        })
        .catch(error => console.error('Error fetching product names:', error));
});

document.getElementById('addInvoiceRow').addEventListener('click', function() {
    var tableBody = document.querySelector('#invoiceTable tbody');
    var newRow = tableBody.insertRow();

    newRow.innerHTML = `
        <td>
            <select name="razon_social">
                <!-- Opciones se generarán dinámicamente -->
            </select>
        </td>
        <td>
            <select name="nombre_producto">
                <!-- Opciones se generarán dinámicamente -->
            </select>
        </td>
        <td><input type="number" name="cantidad" required></td>
        <td><input type="text" name="nombre_establecimiento" required></td>
        <td><input type="text" name="num_orden" required></td>
        <td><button type="button" class="remove-row">Eliminar</button></td>
    `;
    
    // Agregar opciones de nombres de clientes al select de la nueva fila
    var selectCustomer = newRow.querySelector('select[name="razon_social"]');
    window.customer_names.forEach(function(name) {
        var option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        selectCustomer.appendChild(option);
    });

    // Agregar opciones de nombres de productos al select de la nueva fila
    var selectProduct = newRow.querySelector('select[name="nombre_producto"]');
    window.product_names.forEach(function(name) {
        var option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        selectProduct.appendChild(option);
    });
});

document.getElementById('clearFormButton').addEventListener('click', function() {
    var formContainer = document.getElementById('miFormulario');
    var inputs = formContainer.querySelectorAll('input');

    inputs.forEach(function(input) {
        input.value = '';
    });

    // Restablecer las opciones del select al limpiar el formulario
    var selectCustomer = formContainer.querySelector('select[name="razon_social"]');
    selectCustomer.innerHTML = ''; // Limpiar opciones existentes
    window.customer_names.forEach(function(name) {
        var option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        selectCustomer.appendChild(option);
    });

    var selectProduct = formContainer.querySelector('select[name="nombre_producto"]');
    selectProduct.innerHTML = ''; // Limpiar opciones existentes
    window.product_names.forEach(function(name) {
        var option = document.createElement('option');
        option.value = name;
        option.textContent = name;
        selectProduct.appendChild(option);
    });

    var tableBody = document.querySelector('#invoiceTable tbody');
    var rows = tableBody.querySelectorAll('tr');
    for (var i = 1; i < rows.length; i++) {
        tableBody.removeChild(rows[i]);
    }
});

document.getElementById('actualizarClientes').addEventListener('click', function() {
    // Mostrar la barra de progreso
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('progressBar').style.display = 'block';

    // Cambiar el texto del botón a "Actualizando..."
    document.getElementById('actualizarClientes').innerText = 'Actualizando...';
    document.getElementById('actualizarClientes').disabled = true;

    // Simulación de progreso de actualización (en este caso, 2 segundos)
    var width = 0;
    var interval = setInterval(function() {
        width += 10;
        document.getElementById('progressBar').style.width = width + '%';
        if (width >= 100) {
            clearInterval(interval);
            // Actualizar el mensaje de progreso y restaurar el botón
            document.getElementById('progressMessage').innerText = 'Clientes actualizados';
            document.getElementById('actualizarClientes').innerText = 'Actualizar Clientes';
            document.getElementById('actualizarClientes').disabled = false;
            // Ocultar el mensaje después de 5 segundos
            setTimeout(function() {
                document.getElementById('progressMessage').innerText = '';
            }, 5000);
        }
    }, 200);
});

document.getElementById('actualizarProductos').addEventListener('click', function() {
    // Mostrar la barra de progreso
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('progressBar').style.display = 'block';

    // Cambiar el texto del botón a "Actualizando..."
    document.getElementById('actualizarProductos').innerText = 'Actualizando...';
    document.getElementById('actualizarProductos').disabled = true;

    // Simulación de progreso de actualización (en este caso, 5 segundos)
    var width = 0;
    var interval = setInterval(function() {
        width += 10;
        document.getElementById('progressBar').style.width = width + '%';
        if (width >= 100) {
            clearInterval(interval);
            // Ejecutar la función para actualizar productos en el backend
            fetch('/actualizar_productos')
                .then(response => response.text())
                .then(data => {
                    // Actualizar el mensaje de progreso y restaurar el botón
                    document.getElementById('progressMessage').innerText = data;
                    document.getElementById('actualizarProductos').innerText = 'Actualizar Productos';
                    document.getElementById('actualizarProductos').disabled = false;
                    // Ocultar el mensaje después de 5 segundos
                    setTimeout(function() {
                        document.getElementById('progressMessage').innerText = '';
                    }, 5000);
                })
                .catch(error => console.error('Error updating products:', error));
        }
    }, 500);
});

document.querySelector('#invoiceTable').addEventListener('click', function(e) {
    if (e.target.classList.contains('remove-row')) {
        var row = e.target.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }
});

// Agregar evento de entrada al campo de búsqueda
document.getElementById('searchInput').addEventListener('input', function() {
    var searchTerm = this.value.toLowerCase();
    var select = document.querySelector('select[name="razon_social"]');
    var options = select.options;

    for (var i = 0; i < options.length; i++) {
        var option = options[i];
        var text = option.textContent.toLowerCase();
        var optionVisible = text.includes(searchTerm); // Verificar si el término de búsqueda está incluido en el texto de la opción

        // Mostrar u ocultar la opción según el término de búsqueda
        if (optionVisible) {
            option.style.display = ''; // Mostrar opción
        } else {
            option.style.display = 'none'; // Ocultar opción
        }
    }
});
