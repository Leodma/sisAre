function ajustaIndice(removeIndice) {
    var $forms = $('.subform');

    $forms.each(function(i) {
        var $form = $(this);
        var index = parseInt($form.data('index'));
        var newIndex = index - 1;

        if (index < removeIndice) {
            // Ignora se o indice chegara 1
            return true;
        }

        // Escolhe o ID
        $form.attr('id', $form.attr('id').replace(index, newIndex));
        $form.data('index', newIndex);

        // Alterando o ID dos inputs
        $form.find('input').each(function(j) {
            var $item = $(this);
            $item.attr('id', $item.attr('id').replace(index, newIndex));
            $item.attr('name', $item.attr('name').replace(index, newIndex));
        });
    });
}

/**
 * Remove a subform.
 */
function removeForm() {
    var $removedForm = $(this).closest('.subform');
    var removeIndice = parseInt($removedForm.data('index'));

    $removedForm.remove();

    // Atualiza Indice
    ajustaIndice(removeIndice);
}

/**
 * Adicionando um novo subform.
 */
function addForm() {
    var $templateForm = $('#cpf-0-form');

    if (!$templateForm) {
        console.log('[ERROR] Template não localizado');
        return;
    }

    // Recuperando o ultimo índice
    var $lastForm = $('.subform').last();

    var newIndex = 0;

    if ($lastForm.length > 0) {
        newIndex = parseInt($lastForm.data('index')) + 1;
    }

    // Maximo de 20 campos
    if (newIndex > 20) {
        console.log('[WARNING] Não é permitido adicionar mais de 20 responsáveis');
        return;
    }

    // Adicionando elementos
    var $newForm = $templateForm.clone();

    $newForm.attr('id', $newForm.attr('id').replace('_', newIndex));
    $newForm.data('index', newIndex);

    $newForm.find('input').each(function(idx) {
        var $item = $(this);

        $item.attr('id', $item.attr('id').replace('_', newIndex));
        $item.attr('name', $item.attr('name').replace('_', newIndex));
    });

    // Append
    $('#subforms-container').append($newForm);
    $newForm.addClass('subform');
    $newForm.removeClass('is-hidden');

    $newForm.find('.remove').click(removeForm);
}

function insereCampo(){


    $('#add').click(addForm);
    $('.remove').click(removeForm);
};