
document.getElementById("boton_crear_categoria").onclick = async function () {
    let nombre_producto = await document.getElementById("post_nombre_producto").value;
    let numero_de_productos_subidos = await document.getElementById("post_numero_de_productos_subidos").value;
    let stock = await document.getElementById("post_stock").value;
    let link_de_imagen = await document.getElementById("post_link_de_imagen").value;
    let precio_unitario_de_producto = await document.getElementById("post_precio_unitario_de_producto").value;
    let descripcion = await document.getElementById("post_descripcion").value;
    let categorias = await document.getElementById("post_categorias").value;

    let json_response = {
        "nombre_de_categoria": [
        categorias
        ]
    }
    
    await axios.post("/productos/crear",json_response);
    location.href = "/";
};