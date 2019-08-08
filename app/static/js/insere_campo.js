
    let subformulario = document.getElementById('subforms-container');
    let campos_subformulario = document.getElementById('subforms-container').getElementsByClassName('subformulario');





function insereCampo(campo){
    
    let ultimo_campo = campo[campo.length -1];
    let index = parseInt(ultimo_campo.dataset.index);
    let novoindex = index + 1;

    //pega o ultimo e clona e clona.
    copia_campo = campo.cloneNode(true);
    copia_campo.setAttribute('id', `cpf-${novoindex}-form`);
    subformulario.appendChild(copia_campo);
}

function deletaCampo(el){
    //console.log(el)
    elemento = el;
    pai = el.closest('.subformulario');
    pai.parentNode.removeChild(pai);

}

