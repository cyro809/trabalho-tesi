var baseUrl = "http://"+location.hostname;
var letras = $('.artTops li a:first-child');
var letrasArray = []

for(var i=0;i<10;i++) {
    letrasArray.push(baseUrl+$(letras[i]).attr('href'));
}

console.log(letrasArray)