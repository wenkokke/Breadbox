var current              = 'breadbox';
var current_sim          = 0.0;
var current_with_article = 'a breadbox';

$(document).ready(function() {
    $('#breadbox-input').find('input').focus();

    addLine("I'm thinking of something...",'line','blue');
    addLine("Is it a breadbox?",'line','white');
    addLine("No, it's not.",'line','blue');
});

$('#breadbox-input').cssConsole({
    inputName:'console',
    charLimit: 60,
    onEnter: function(){
        execCommand($('#breadbox-input').find('input').val(),
                    function() {
                        $('#breadbox-input').cssConsole('reset');
                        $('#breadbox-input').find('input').focus();
                    },
                    function() {
                        $('#breadbox-input').cssConsole('destroy');
                        $('.breadbox-label').remove();
                    });
    }
});

$('.breadbox-container').on('click', function() {
    $('#breadbox-input').find('input').focus();
});

function addLine(input, style, color) {
    if($('.breadbox-console div').length==lineLimit) {
        $('.breadbox-console div').eq(0).remove();
    }
    style = typeof style !== 'undefined' ? style : 'line';
    color = typeof color !== 'undefined' ? color : 'white';
    $('.breadbox-console').append('<div class="breadbox-'+style+' breadbox-'+color+'">'+input+'</div>');
}

function execCommand(input,cont,stop) {
    var input = input.trim();

    if (input == "help") {

        help();
        cont();

    } else if (input.indexOf("give up") != -1) {

        addLine("I give up! What is it?",'line','white');
        reply = "I was thinking of "+secret_with_article+"... ";
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
        } else if (definitions.length == 0) {
            addLine(reply,'line','blue');
        }
        stop();

    } else {
        if (input.indexOf(' ') != -1) {
            addLine("I have to warn you, compound words scare me a little... ",'line','red');
            addLine("so try to avoid words with spaces in them!",'line','red');
        }
        var input = input.replace(/[!?\.\\/,:;]/g,'').split(' ');
        var next  = input[input.length - 1];

        $.ajax({
            url         : breadbox_url+'guess/'+secret+'/'+next,
            type        : "GET",
            dataType    : "json",
            success     : function(data) {
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
            }
        });
    }
}

function help() {
    addLine("&nbsp;");
    addLine("Breadbox is an experimental cousin of 20 Questions, "+
            "also known as Plenty Questions, which is played by two "+
            "or more players. In this case, it's you against the computer! "+
            "It's played as follows:",'margin','blue');
    addLine("&nbsp;");
    addLine("&nbsp;&nbsp;&bull;&nbsp;The computer thinks of a word (I already did this!)"
            ,'margin','blue');
    addLine("&nbsp;&nbsp;&bull;&nbsp;As your first question, you <i>have to ask</i>"+
            " \"Is it a breadbox?\"",'margin','blue');
    addLine("&nbsp;&nbsp;&bull;&nbsp;Obviously, I wouldn't have chosen a breadbox, "+
            "so I say \"No, it's not.\"",'margin','blue');
    addLine("&nbsp;");
    addLine("From then on, all your questions have to be of the form..."
            ,'margin','blue');
    addLine("&nbsp;");
    addLine("&nbsp;&nbsp;&nbsp;&nbsp;Is it more like a <i>breadbox</i>, "+
            "or more like...?",'margin','white');
    addLine("&nbsp;");
    addLine("...where <i>breadbox</i> is replaced with whatever your current guess is.",
            'margin','blue');
    addLine("&nbsp;");
    addLine("And remember, you can always type 'give up', and I'll tell you what I "+
            "was thinking of! ^^",'margin','blue');
    addLine("Once you win (or give up), just reload the page to play another game.",
            'margin','blue');
    addLine("&nbsp;");
}
