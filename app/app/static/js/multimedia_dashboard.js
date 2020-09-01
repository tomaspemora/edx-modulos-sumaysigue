
function getMonday(d) {
  d = new Date(d);
  var day = d.getDay(),
      diff = d.getDate() - day + (day == 0 ? -6:1); // adjust when day is sunday

  var final_date = new Date(d.setDate(diff));
  return final_date.toString("d-MMM-yyyy")
}
function getFriday(d) {
  d = new Date(d);
  var day = d.getDay(),
      diff = d.getDate() - day + (day == 0 ? -2:1); // adjust when day is sunday

  var final_date = new Date(d.setDate(diff));
  return final_date.toString("d-MMM-yyyy")
}


// 
// implementación sistema arrastrable para formulario add task
//

dragElement(document.getElementById("addtask"));

function dragElement(elmnt) {
  var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
  if (document.getElementById(elmnt.id + "headerDraggable")) {
    // if present, the header is where you move the DIV from:
    document.getElementById(elmnt.id + "headerDraggable").onmousedown = dragMouseDown;
  } else {
    // otherwise, move the DIV from anywhere inside the DIV:
    elmnt.onmousedown = dragMouseDown;
  }

  function dragMouseDown(e) {

    e = e || window.event;
    //e.preventDefault();
    // get the mouse cursor position at startup:
    pos3 = e.clientX;
    pos4 = e.clientY;
    document.onmouseup = closeDragElement;
    // call a function whenever the cursor moves:
    document.onmousemove = elementDrag;
  }

  function elementDrag(e) {
    e = e || window.event;
    //e.preventDefault();
    // calculate the new cursor position:
    pos1 = pos3 - e.clientX;
    pos2 = pos4 - e.clientY;
    pos3 = e.clientX;
    pos4 = e.clientY;
    // set the element's new position:
    if (elmnt.style.top == ""){
      a = 1;
    }
    elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
    elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
    elmnt.style.bottom = 'unset';
    elmnt.style.right = 'unset';
  }

  function closeDragElement() {
    // stop moving when mouse button is released:
    document.onmouseup = null;
    document.onmousemove = null;
  }
}




$(document).ready(function(){

    //
    // barra para cambiar tamaño de las secciones (arastable y cambios de tamaño)
    // 

    $('#separator-prog-diseno').on('mousedown', function(e){
        e.preventDefault();
        var $dragable = $(this),
            startHeight = $dragable.offset().top;
            pY = e.pageY; 
        $(document).on('mouseup', function(e){
            $(document).off('mouseup').off('mousemove');
        });
        $(document).on('mousemove', function(me){
            me.preventDefault();
            //var mx = (me.pageY - pX);
            var my = - (me.pageY - pY);
            var tot =  parseFloat($dragable.next().css('height'))+parseFloat($dragable.prev().css('height')) 
            if ( Math.min(startHeight - my - parseFloat($('#section-top').css('min-height')),tot-20)>72){
              
              // Máxima altura para el bloque de tasks de diseño dado por las filas de cada diseñador.
              var totalHeight = 0;
              $dragable.prev().children('#col-separator-diseno').children().each(function(){
                  totalHeight = totalHeight + $(this).outerHeight(true);
              });

              $dragable.prev().css({
                  'height': Math.min(Math.min(startHeight - my - parseFloat($('#section-top').css('min-height')),tot-20),totalHeight)
              });
              $dragable.next().css({
                  'height' : tot -  parseFloat($dragable.prev().css('height'))
              });
              var tot2 =  parseFloat($dragable.next().css('height'))+parseFloat($dragable.prev().css('height'));
              
            }
        });        
    });

    //
    // Popover de cada task
    //

    $('[data-toggle="popover"]').popover({template:'<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>',html:true,content:function(){return $(this).html();},delay:{ "show": 50, "hide": 50 },trigger:'click'});
      $('[data-toggle="popover"]').on('click', function(){
        $('[data-toggle="popover"]').not(this).popover('hide');
    });

    //
    // Aca se agregan los divs correspondiente a cada semana, sacnado la info del input agregado en jinja
    //

    $('.semanitas').each(function(){
      $(this).after('<div class="semana-header col"><div class="semana-inner">'+getMonday($(this)[0].valueAsDate)+' al '+getFriday($(this)[0].valueAsDate)+'</div></div>');

    //
    // Modificar los heights de los tags de encargados en función de los cambios en las rows de tasks
    //

    $('.row-de-semanas').each(function(){
        var elmnt = $(this)[0];
        new ResizeSensor(elmnt, function(){ 
            //console.log(elmnt);
            $('div[id^="encargado-"]').each(function(){
              $('#tag-'+$(this).attr('id')).height($(this).height());
            });
            // ACA IMPLEMENTAR LOS CAMBIOS DE ALTURA PARA LOS TAGS DE ENCARGADOS  
        });
      });
     $('div[id^="encargado-"]').each(function(){
              $('#tag-'+$(this).attr('id')).height($(this).height());
            });


    }); // fin document ready


//
// Sincronización de los scrolls horizontales semanas - diseño - programación
//

    var div1 = "#col-separator-diseno"
    var div2 = "#col-separator-programacion"
    var div3 = "#col-header-semanas"

    //$(div1).scroll(function () { $(div2).scrollLeft($(div1).scrollLeft()); });
    //$(div2).scroll(function () { $(div1).scrollLeft($(div2).scrollLeft()); });


    var ignoreScrollEvents = false
    function syncScroll(element1, element2,element3) {
      element1.scroll(function (e) {
        var ignore = ignoreScrollEvents
        ignoreScrollEvents = false
        if (ignore) return

        ignoreScrollEvents = true
        //console.log(element1.scrollLeft());
        //console.log(inner.offsetTop - element1[1].scrollTop)
        element2.scrollLeft(element1.scrollLeft());
        element3.scrollLeft(element1.scrollLeft());
      });
    }
    syncScroll($(div1), $(div2), $(div3));
    syncScroll($(div2), $(div1), $(div3));
    syncScroll($(div3), $(div2), $(div1));


//
// Sincronización de los scroll verticales tag-diseno <> tasks-diseno y tags-prog <> tasks-programacion
//


    var div1_1 = "#headers-diseno"
    var div1_2 = "#col-separator-diseno"
    var div2_1 = "#headers-programacion"
    var div2_2 = "#col-separator-programacion"

    var ignoreScrollEvents2 = false
    function syncScrollVert(element1, element2) {
      element1.scroll(function (e) {
        var ignore = ignoreScrollEvents2
        ignoreScrollEvents2 = false
        if (ignore) return

        ignoreScrollEvents2 = true
        element2.scrollTop(element1.scrollTop());
        //element2.scrollTop(element1.scrollTop());
      });
    }
    syncScrollVert($(div1_1), $(div1_2));
    syncScrollVert($(div1_2), $(div1_1));
    syncScrollVert($(div2_1), $(div2_2));
    syncScrollVert($(div2_2), $(div2_1));


/*...
  Luego de esto ir al backend.
*/


//
// Implementación del sistema de drag and drop de los tasks
//

  $('div[class^="i"]').each(function(){
    var $el = $(this);
     $el.draggable({
          //connectToSortable: ".semanas",
          revert: "invalid",
          cursor: "grabbing",
          helper: "clone",
          containment:$el.parent().parent().parent(),
          opacity: 1,
          zIndex: 2,
          drag: function(event,ui){
            $(this).css('z-index',2);$(this).parent().append($(this));
            
          },
          stop: function(){$(this).css('z-index','');$(this).parent().append($(this));$(this).css('position','');}

    });
  });



  $('.semanas-diseno, .semanas-prog').droppable(
    {

      drop: function(event, ui) {
          //console.log($(this).attr('class').match(/semanas-(diseno|prog)/g)[0] );
          //console.log(ui.draggable.parent().attr('class').match(/semanas-(diseno|prog)/g)[0]);
          if($(this).attr('class').match(/semanas-(diseno|prog)/g)[0] == ui.draggable.parent().attr('class').match(/semanas-(diseno|prog)/g)[0]){
            ui.draggable.detach().appendTo($(this));
          }
        }
    }

    );
});