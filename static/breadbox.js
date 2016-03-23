var current              = 'breadbox';
var current_sim          = 0.0;
var current_with_article = 'a breadbox';

$(document).ready(function() {
    $('#input').find('input').focus();

    addLine("I'm thinking of something...",'line','blue');
    addLine("Is it a breadbox?",'line','white');
    addLine("No, it's not.",'line','blue');
});

$('#input').cssConsole({
    inputName:'console',
    charLimit: 60,
    onEnter: function(){
        execCommand($('#input').find('input').val(),
                    function() {
                        $('#input').cssConsole('reset');
                        $('#input').find('input').focus();
                    },
                    function() {
                        $('#input').cssConsole('destroy');
                        $('.label').remove();
                    });
    }
});

$('.container').on('click', function() {
    $('#input').find('input').focus();
});

function addLine(input, style, color) {
    if($('.console div').length==lineLimit) {
        $('.console div').eq(0).remove();
    }
    style = typeof style !== 'undefined' ? style : 'line';
    color = typeof color !== 'undefined' ? color : 'white';
    $('.console').append('<div class="'+style+' '+color+'">'+input+'</div>');
}

function execCommand(input,cont,stop){
    var input = input.trim();

    if (input.indexOf("give up") != -1) {

        addLine("I give up! What is it?",'line','white');
        reply = "I was thinking of '"+secret+"'... "
        if (definitions.length > 1) {
            addLine(reply+"It's",'line','blue');
            $(definitions).each(function(index,item) {
                if (index == definitions.length - 1) {
                    addLine("- "+item+".",'margin','blue');
                } else {
                    addLine("- "+item+";",'margin','blue');
                }
            });
        } else if (definitions.length == 1) {
            addLine(reply+"It's "+definitions[0]+".",'line','blue');
        }
        stop();

    } else {
        if (input.indexOf(' ') != -1) {
            addLine("I have to warn you, compound words scare me a little... ",'line','red');
            addLine("so try to avoid words with spaces in them!",'line','red');
        }
        var input = input.replace(/[!?\.\\/,:;]/g,'').split(' ');
        var next  = input[input.length - 1];

        $.getJSON('/guess/'+secret+'/'+next,function(data) {
            var next_sim          = data['similarity'];
            var next_with_article = data['a_or_an'];

            addLine("Is it more like "+current_with_article+
                    " or more like "+next_with_article+"?",'line','white');

            if (next == secret) {
                addLine("That's <i>exactly</i> what I was thinking of!",'line','blue');
                stop();
            }
            else if (next_sim > current_sim) {
                addLine("It's more like "+next_with_article+"!",'line','blue');
                current              = next;
                current_sim          = next_sim;
                current_with_article = next_with_article;
                cont();
            }
            else if (next_sim <= current_sim) {
                addLine("It's more like "+current_with_article+"...",'line','blue');
                cont();
            }
        });
    }
}
