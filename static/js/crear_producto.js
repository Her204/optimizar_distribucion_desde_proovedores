axios.get("/categorias").then(r=>{
    r.data.categorias.forEach(function(cat) {
        let select = document.getElementById("post_categorias");
        let option =  document.createElement("option");
        option.setAttribute("value", cat.nombre_categoria);
        let optionTexto = document.createTextNode(cat.nombre_categoria);
        option.appendChild(optionTexto);
 
        select.appendChild(option);
    })
})

axios.get("/usuario/todos_los_usuarios").then(r=>{
    r.data.forEach(function(cat) {
        let select = document.getElementById("post_usuarios");
        let option =  document.createElement("option");
        option.setAttribute("value", cat.nombre_de_usuario);
        let optionTexto = document.createTextNode(cat.nombre_de_usuario);
        option.appendChild(optionTexto);
 
        select.appendChild(option);
    })
})

document.getElementById("boton_crear_producto").onclick = async function () {
    let nombre_producto = await document.getElementById("post_nombre_producto").value;
    let numero_de_productos_subidos = await document.getElementById("post_numero_de_productos_subidos").value;
    let stock = await document.getElementById("post_stock").value;
    //let link_de_imagen = await document.getElementById("post_link_de_imagen").value;
    let link_de_imagen = await document.getElementById("post_link_de_imagen").files[0]; 
    let precio_unitario_de_producto = await document.getElementById("post_precio_unitario_de_producto").value;
    let descripcion = await document.getElementById("post_descripcion").value;
    let categorias = await document.getElementById("post_categorias").value;
    let usuarios = await document.getElementById("post_usuarios").value;
    
    let formData = new FormData();
    formData.append('file', link_de_imagen);

    let response = await axios.post('/guardar_imagen_productos',
        formData,
        {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    console.log(link_de_imagen)
    let json_response = {
        "nombre_producto": nombre_producto,
        "numero_de_productos_subidos": parseInt(numero_de_productos_subidos),
        "stock": parseInt(stock),
        "link_de_imagen": response.data,
        "precio_unitario_de_producto": parseInt(precio_unitario_de_producto),
        "descripcion": descripcion,
        "categorias": [
        categorias
        ],
        "usuarios":
        [usuarios
        ]
    }
    
    await axios.post("/productos/crear",json_response);
    location.href = "/";
};
