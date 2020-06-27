// Muestra un menu debajo de elemento seleccionado
class RowMenu 
    {
    // Contructor con los elementos donde saldra el menú (selector ó objeto jQuery)   
    constructor(elems) 
        {
        var self = this;
        $(elems).on('click', function (ev) {
            ev.stopPropagation();
            self.$elem = $(this);
            self.Show(ev);
            });

        this.items = [];
        }

    // Adiciona un elemento al menú y la función que debe ser llamada al seleccionar el item    
    AddItem(title, callback) 
        {
        this.items.push({ "title": title, "callback": callback });
        }

    // Se llama cuando una de los elementos es seleccionado    
    Show(evt) 
        {
        this.$elem.addClass("selrow");

        this.CreateBackScren();
        this.CreateMenu();
        }

    // Crea una pantalla de fondo trasparete sobre toda la pantalla    
    CreateBackScren()   
        {
        var $body = $("body");
        var hW = window.innerHeight;
        var hD = $body.outerHeight();
        var W = hD > hW ? hD : hW;

        var html = '<div style="position:absolute; z-index:1000; top:0px; left:0px; width:100%; height:' + W + 'px;"> </div>';
        this.$back = $(html);

        $body.append(this.$back);

        var self = this;
        this.$back.on('click', function (ev) { self.Hide(); });
        }

    // Crea el menu con todos los item defnidos    
    CreateMenu() 
        {
        this.$mnu = $('<div id="row-mnu"></div>');
        this.$lst = $('<ul class="nav"></ul>');

        this.$mnu.append(this.$lst);
        this.$mnu.on('click', function (ev) 
            { 
            ev.stopPropagation();
            self.Hide(); 
            });

        var self = this;
        for (var i = 0; i < this.items.length; ++i) 
            {
            var title = this.items[i].title;
            var item = $('<li role="presentation" idx="' + i + '"><a href="#">' + title + '</a></li>');
            this.$lst.append(item);

            item.on('click', function (ev) {
                ev.stopPropagation();
                self.SelItem(this);
                });
            }

        var cell0 = this.$elem.children().first();
        cell0.css("position", "relative");
        cell0.append(this.$mnu);

        this.$mnu.animate({ height: "40px" }, 400);
        this.$lst.animate({ bottom: "0" }, 400);
        }

    // Se llama cuando se selecciona uno de los items del menú    
    SelItem(elem) 
        {
        var idx = +$(elem).attr('idx');
        this.Hide(this.items[idx].callback);
        }

    // Oculta el menu y la panalla de fondo, llama la función de notificación se es necesario    
    Hide(selfun) 
        {
        var self = this;
        this.$lst.animate({ bottom: "40px" }, 400);
        this.$mnu.animate({ height: "0px" }, 400, function () {
            self.$elem.removeClass("selrow");

            self.$mnu.remove();
            self.$back.remove();

            if (selfun) selfun(self.$elem);
            });
        }
    }

// Sincroniza los tamaños de las columnas, de la tabla de datos y la de totales    
function TotalesRz()
    {
    var lst1 = $('.main-frame .table-list tr:last-child td');
    var lst2 = $('.main-frame .table-totals tr:last-child td');
        
    var wTb1 = $('.main-frame .table-list').outerWidth();
    $('.main-frame .table-totals').outerWidth(wTb1);  
        
    for( var i=0; i<lst1.length; ++i )
        {
        var wCol =  lst1.eq(i).outerWidth();
        lst2.eq(i).outerWidth(wCol);
        }
    }


// Esto es una prueba la aplicación de anuncios
// GetLink( "linkToUpdate" ) ó  GetLink( "linkToDelete" )  
function GetLink( sTipo )
    {
    var links = document.getElementsByTagName("a");
    for( var i=0; i<links.length; ++i ) 
        {
        var attrs = links[i].attributes;
        var attr = attrs["data-cy"];
        if( attr && attr.value==sTipo )
            return "https://www.revolico.com" + attrs["href"].value;
        }

    return "";    
    }





