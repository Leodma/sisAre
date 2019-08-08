function Confirmar(mensagem, id){
    let mesage =  confirm(mensagem);
    console.log(id);

    if (mesage == true){
       window.location.replace('/excluir_usuario/'+ id, { id });
       }
}



function mascara(i,t){

  let v = i.value;

  if(isNaN(v[v.length-1])){
     i.value = v.substring(0, v.length-1);
     return;
  }

  
  if(t == "cpf"){
     i.setAttribute("maxlength", "14");
     if (v.length == 3 || v.length == 7) i.value += ".";
     if (v.length == 11) i.value += "-";
  }


  if(t == "processo"){
    i.setAttribute("maxlength", "20");
    if (v.length == 5) i.value += ".";
    else if (v.length == 12) i.value += "/";
    else if (v.length == 17) i.value += "-";
 }

}


