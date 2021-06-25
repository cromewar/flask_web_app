let duracion = document.getElementById('dur')
let terapeuta = document.getElementById('terap')
let tarifa = ''
if (terapeuta) {
    terapeuta.addEventListener('click', function () {
        tarifa = terapeuta.value.split('-')
        //alert(terapeuta.value
        document.getElementById('resultado').innerHTML = tarifa[1]
        document.getElementById('terapist').value = tarifa[0]

    })
}

duracion.addEventListener('click', function () {
    let costo = document.getElementById('resultado').innerHTML = tarifa[1] * duracion.value
    document.getElementById('cost').value = parseFloat(costo)
    let fecha = document.getElementById('date')
    let new_date = new Date(fecha.value)
    new_date.setHours(new_date.getHours() + parseInt(duracion.value))

    let final_date = new_date.toISOString()
    //let end = final_date.replaceAll("/", "-")
    document.getElementById('final_date').value = moment(final_date).format("YYYY-MM-DDTkk:mm")
})

// let send_buttom = document.getElementById("submit-terapia")
// if (send_buttom) {
//     send_buttom.addEventListener('click', function () {

//         // let x = compro( 'nueva fehca ' , 'arrays de las fecha ')

//         // if(x){
            
//         // }

//         let formulario = document.forms['formulario-terapia']
//        //alert(formulario.costo.value)
//         var myHeaders = new Headers();

//         myHeaders.append("Content-Type", "application/json");



//         var raw = JSON.stringify({

//             "cliente": formulario.cliente.value,

//             "terapeuta": formulario.terapeuta.value,

//             "fecha": formulario.fecha.value,

//             "duracion": formulario.duracion.value,

//             "fin": formulario.fin.value,

//             "costo": formulario.costo.value

//         });



//         var requestOptions = {

//             method: 'POST',

//             headers: myHeaders,

//             body: raw,

//             redirect: 'follow'

//         };



//         fetch("http://127.0.0.1:3000/terapia/add_therapy", requestOptions)

//             .then(response => response.text())

//             .then(result => {
                
//                 console.log(result)
                
//             })

//             .catch(error => console.log('error', error));
        
//     })

//     // const compro = ( newFecha , arrayFechas ) => {

//     // }
// }

