
$(document).ready(function(){
	if (document.querySelector('.custom-file-input') != null){
		document.querySelector('.custom-file-input').addEventListener('change',function(e){
		  var fileName = document.getElementById("select_archivo").files[0].name;
		  var prevSibling = e.target.previousElementSibling
		  prevSibling.innerText = fileName
		})
	}
});


var formatCode = function(code, stripWhiteSpaces, stripEmptyLines) {
    "use strict";
    var whitespace          = ' '.repeat(4);             // Default indenting 4 whitespaces
    var currentIndent       = 0;
    var char                = null;
    var nextChar            = null;


    var result = '';
    for(var pos=0; pos <= code.length; pos++) {
        char            = code.substr(pos, 1);
        nextChar        = code.substr(pos+1, 1);

        // If opening tag, add newline character and indention
        if(char === '<' && nextChar !== '/') {
            result += '\n' + whitespace.repeat(currentIndent);
            currentIndent++;
        }
        // if Closing tag, add newline and indention
        else if(char === '<' && nextChar === '/') {
            // If there're more closing tags than opening
            if(--currentIndent < 0) currentIndent = 0;
            result += '\n' + whitespace.repeat(currentIndent);
        }

        // remove multiple whitespaces
        else if(stripWhiteSpaces === true && char === ' ' && nextChar === ' ') char = '';
        // remove empty lines
        else if(stripEmptyLines === true && char === '\n' ) {
            //debugger;
            if(code.substr(pos, code.substr(pos).indexOf("<")).trim() === '' ) char = '';
        }

        result += char;
    }

    return result;
}

/*$('#tipo_edx').change(function(){
	$('div[id^=form-]').each(function(){
		$(this).hide()
	});
	$('#form-'+$(this).val()).show()
	$('#tipo_edx_hidden').val($(this).val());
	$('#form-button').show()
});
*/