
var carros = [
    {
        "modelo": "Fiat Uno",
        "preco": 15000,
        "cidade": "Belo Horizonte",
        "id_carro": 0
    }, {
        "modelo": "Palio Go",
        "preco": 20000,
        "cidade": "Belo Horizonte",
        "id_carro": 1
    }, {
        "modelo": "BMW",
        "preco": 500000,
        "cidade": "Leite",
        "id_carro": 2
    }
];

$(document).ready(function(){
	cidade = $('#cidade').text();
	carros.forEach(function(c){
		//if(c.cidade === cidade){
			console.log('<option class="" value="'+c.cidade+'-'+c.id_carro+'">'+c.modelo+' - '+c.id_carro+'</option>');		
			carros.push('<option class="" value="'+c.cidade+'-'+c.id_carro+'">'+c.modelo+' - '+c.id_carro+'</option>');
		//}
	});

	$('#select-carros').html(carros.join(''));
});


function filtrarCarros(){
	cidade = $('#cidade').text();
	carros.forEach(function(c){
		if(c.cidade === cidade){
			console.log('<option class="" value="'+c.id_carro+'">'+c.modelo+' - '+c.id_carro+'</option>');
			carros.push('<option class="" value="'+c.id_carro+'">'+c.modelo+' - '+c.id_carro+'</option>');
		}
	});

	$('#select-carros').html(carros.join(''));
}