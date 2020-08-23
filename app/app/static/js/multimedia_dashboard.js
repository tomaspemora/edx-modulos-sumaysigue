
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


// Make the DIV element draggable:
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
    $('#separator-prog-diseno').on('mousedown', function(e){
        e.preventDefault();
        var $dragable = $(this),
            //startHeight = parseFloat($dragable.css('min-height')),
            startHeight = $dragable.offset().top;
            pY = e.pageY; 
            console.log(e.pageY - $(this).offset().top)
            console.log('pY->'+ pY );
        $(document).on('mouseup', function(e){
            $(document).off('mouseup').off('mousemove');
        });
        $(document).on('mousemove', function(me){
            me.preventDefault();
            //var mx = (me.pageY - pX);
            var my = - (me.pageY - pY);
            var tot =  parseFloat($dragable.next().css('height'))+parseFloat($dragable.prev().css('height')) 
            if ( Math.min(startHeight - my - parseFloat($('#section-top').css('min-height')),tot-20)>72){
              $dragable.prev().css({
                  'height': Math.min(startHeight - my - parseFloat($('#section-top').css('min-height')),tot-20)
              });
              $dragable.next().css({
                  'height' : tot -  parseFloat($dragable.prev().css('height'))
              });
              var tot2 =  parseFloat($dragable.next().css('height'))+parseFloat($dragable.prev().css('height'));
              //- parseFloat($('#section-top').css('min-height')) 
              console.log('prev->'+$dragable.prev().css('height')+' next->'+$dragable.next().css('height') +'tot1->'+tot+ ' tot2->' +tot2  + ' draggable->' + $dragable.css('height'))
          }
        });
                
    });

    $('[data-toggle="popover"]').popover();

    $('.semanitas').each(function(){
      $(this).after('<div class="semana-header col"><div class="semana-inner">'+getMonday($(this)[0].valueAsDate)+' al '+getFriday($(this)[0].valueAsDate)+'</div></div>');

    });


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
        console.log(element1.scrollLeft());
        //console.log(inner.offsetTop - element1[1].scrollTop)
        element2.scrollLeft(element1.scrollLeft());
        element3.scrollLeft(element1.scrollLeft());
      });
    }
    syncScroll($(div1), $(div2), $(div3));
    syncScroll($(div2), $(div1), $(div3));
    syncScroll($(div3), $(div2), $(div1));
});

