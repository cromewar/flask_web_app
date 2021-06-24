let date = document.getElementById('date_text').value
    document.getElementById('dat').value = moment(date).format("YYYY-MM-DDTkk:mm")

let cost = document.getElementById('resultado').innerHTML
let cst = parseFloat(cost)
let duracion = document.getElementById('duracion_from_back').value
let price = cst/duracion
console.log(price)

let edit_duration = document.getElementById('dur')
edit_duration.addEventListener('click', function(){
    let final_price =  price * edit_duration.value
    document.getElementById('resultado').innerHTML = String(final_price)

    let fecha = document.getElementById('dat')

    let new_date = new Date(fecha.value)
    new_date.setHours(new_date.getHours() + parseInt(edit_duration.value))
    
    let final_date = new_date.toISOString()
    //let end = final_date.replaceAll("/", "-")
    document.getElementById('final_date').value = moment(final_date).format("YYYY-MM-DDTkk:mm")
    let finald = document.getElementById('final_date').value
    console.log(finald)
})



