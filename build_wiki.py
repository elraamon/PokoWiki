import urllib.request
import re
import html

def fetch_and_build():
    url_habitats = 'https://www.eurogamer.es/pokemon-pokopia-habitats-preferidos-todos-pokedex-ecosistema-bioma-entorno'
    req = urllib.request.Request(url_habitats, headers={'User-Agent': 'Mozilla/5.0'})
    html_habitats = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

    url_crafts = 'https://www.eurogamer.net/pokemon-pokopia-crafting-recipes-list'
    req_crafts = urllib.request.Request(url_crafts, headers={'User-Agent': 'Mozilla/5.0'})
    html_crafts = urllib.request.urlopen(req_crafts).read().decode('utf-8', errors='ignore')

    tables_hab = re.findall(r'<table.*?>(.*?)</table>', html_habitats, re.DOTALL | re.IGNORECASE)
    tables_cra = re.findall(r'<table.*?>(.*?)</table>', html_crafts, re.DOTALL | re.IGNORECASE)

    rows_hab = re.findall(r'<tr.*?>(.*?)</tr>', tables_hab[0], re.DOTALL | re.IGNORECASE) if tables_hab else []
    
    html_output = """<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PokoWiki</title>
    <link rel="stylesheet" href="styles.css">
</head>

<body>
    <div class="window-container">
        <header>
            <img src="assets/logo.png" alt="PokoLogo" class="main-logo">
            <p>Wiki Pokémon Pokopia. (Base de datos no oficial)</p>
        </header>
        <nav>
            <div class="nav-links">
                <a href="#habitats" class="active">Hábitats</a>
                <a href="#crafteos">Crafteos</a>
                <a href="#pokedex">Pokédex (Próximamente)</a>
            </div>
            <button id="theme-toggle" class="theme-toggle" aria-label="Cambiar modo oscuro">
                <svg id="moon-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>
                <svg id="sun-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="display:none;"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>
            </button>
        </nav>
        <main>
            <section id="habitats">
                <div class="section-header-row">
                    <h2>Hábitats Preferidos</h2>
                    <input type="text" id="search-habitat" class="search-bar" placeholder="Buscar hábitat o Pokémon...">
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Imagen</th>
                                <th>Hábitat preferido</th>
                                <th>Pokémon (rareza)</th>
                                <th>Cómo crear</th>
                            </tr>
                        </thead>
                        <tbody>
"""
    
    
    TRANSLATIONS = {
        "Wooden Bed": "Cama de Madera", "Wooden Table": "Mesa de Madera", "Wooden Chair": "Silla de Madera", 
        "Wooden Stool": "Taburete de Madera", "Wooden Wall": "Pared de Madera", "Wooden Floor": "Suelo de Madera", 
        "Wooden Door": "Puerta de Madera", "Wooden Bench": "Banco de Madera", "Wooden Fencing": "Valla de Madera", 
        "Wooden Partition": "Separador de Madera", "Wooden Gate": "Puerta de Madera", "Wooden Posts": "Postes de Madera",
        "Wooden Crate": "Caja de Madera", "Wooden Path": "Camino de Madera", "Wooden Ladder": "Escalera de Madera",
        "Wooden Plate": "Plato de Madera", "Wooden Birdhouse": "Casita de Pájaro de Madera", "Wooden Enclosure": "Cerco de Madera",
        "Worn Wooden Crate": "Caja de Madera Desgastada", "Wooden Flooring": "Suelo de Madera", "Wooden Steps": "Escalones de Madera",

        "Iron Bed": "Cama de Hierro", "Iron Table": "Mesa de Hierro", "Iron Chair": "Silla de Hierro", 
        "Iron Stool": "Taburete de Hierro", "Iron Door": "Puerta de Hierro", "Iron Gate": "Puerta de Hierro",
        "Iron Pipe": "Tubería de Hierro", "Iron Steps": "Escalones de Hierro", "Iron Stand": "Soporte de Hierro",
        "Iron Plating": "Revestimiento de Hierro", "Iron Pipes": "Tuberías de Hierro", "Iron Ladder": "Escalera de Hierro",
        
        "Log Bed": "Cama de Tronco", "Log Table": "Mesa de Tronco", "Log Chair": "Silla de Tronco", 
        "Log Stool": "Taburete de Tronco", "Log Bench": "Banco de Tronco",
        
        "Straw Bed": "Cama de Paja", "Straw Table": "Mesa de Paja", "Straw Chair": "Silla de Paja", "Straw Stool": "Taburete de Paja",
        
        "Stone Bed": "Cama de Piedra", "Stone Table": "Mesa de Piedra", "Stone Chair": "Silla de Piedra", 
        "Stone Stool": "Taburete de Piedra", "Stone Wall": "Pared de Piedra", "Stone Bench": "Banco de Piedra", 
        "Stone Fencing": "Valla de Piedra", "Stone Steps": "Escalones de Piedra", "Stone Fireplace": "Chimenea de Piedra",
        "Stone Hipped Roof": "Tejado a Cuatro Aguas de Piedra", "Stone Tiling": "Alicatado de Piedra", "Stone Brick Wall": "Pared de Ladrillo de Piedra",
        "Flat Stone Roof": "Tejado Plano de Piedra", "Stone Roof Decoration": "Decoración de Tejado de Piedra", "Stone Roof Valley": "Valle de Tejado de Piedra",
        "Sloped Stone Roof": "Tejado Inclinado de Piedra", "Stone Flooring": "Suelo de Piedra", "Lined-Stone Flooring": "Suelo de Piedra Alineado",
        
        "Iron Ingot": "Lingote de Hierro", "Lumber": "Madera", "Vine Rope": "Cuerda de Liana",
        "Sturdy Stick": "Palo Robusto", "Glowing Stone": "Piedra Brillante", "Brick": "Ladrillo",
        "Stone": "Piedra", "Fluff": "Pelusa", "Iron Ore": "Mineral de Hierro", "Copper Ore": "Mineral de Cobre",
        "Gold Ingot": "Lingote de Oro", "Squishy Clay": "Arcilla Blanda", "Leaf": "Hoja", "Twine": "Cordel",
        "Glowing Mushroom": "Champiñón Brillante", "Paper": "Papel", "Sea Glass Fragments": "Fragmentos de Cristal de Mar",
        "Volcanic Ash": "Ceniza Volcánica", "Concrete": "Hormigón", "Tinkagear": "Engranaje Tink",
        "Small Log": "Tronco Pequeño", "Seashell": "Concha", "Beach Sand": "Arena de Playa",
        "Nonburnable Garbage": "Basura No Combust.", "Wastepaper": "Papel Usado", "Paint": "Pintura",
        
        "Skylight": "Tragaluz", "Magikarp Decoration": "Decoración de Magikarp", "Large Wooden Door": "Puerta Grande de Madera",
        "Plate": "Plato", "Marked Road (Vertical)": "Carretera Marcada (Vertical)", "Marked Road (Horizontal)": "Carretera Marcada (Horizontal)",
        "Stylish Tiling": "Alicatado Elegante", "Glossy Awning": "Toldo Brillante", "Chic Table": "Mesa Elegante", "Chic Chair": "Silla Elegante",
        "Berry Basket": "Cesta de Bayas", "Stardust": "Polvo Estelar", "Mushroom Lamp": "Lámpara Champiñón", "Plain Bed": "Cama Sencilla",
        "Mug": "Taza", "Study Desk": "Escritorio de Estudio", "Utility Pole": "Poste de la Luz", "Extravagant Pillar (Lower)": "Pilar Extravagante (Inferior)",
        "Extravagant Pillar (Middle)": "Pilar Extravagante (Medio)", "Extravagant Pillar (Upper)": "Pilar Extravagante (Superior)",
        "Sloped Tiled Roof": "Tejado Inclinado de Tejas", "Picnic Basket": "Cesta de Picnic", "Soft Seat": "Asiento Blando", "Sandbox": "Arenero",
        "Office Shelf": "Estante de Oficina", "Flat Tiled Roof": "Tejado Plano de Tejas", "Automatic Doors": "Puertas Automáticas",
        "Plain Stool": "Taburete Sencillo", "Signpost": "Poste de Señal", "Grass Flooring": "Suelo de Hierba", "Smelting Furnace": "Horno de Fundición",
        "Metallic Smelting Furnace": "Horno de Fundición Metálico", "Rope": "Cuerda", "Harbor Pole": "Poste de Puerto", "Harbor Streetlight": "Farola de Puerto",
        "Small Round Rug": "Alfombra Redonda Pequeña", "Striped Wall": "Pared a Rayas", "Plain Table": "Mesa Sencilla", "Handcar": "Vagoneta",
        "Party Bunting": "Banderines de Fiesta", "Decorative Bookshelf": "Estantería Decorativa", "Perch": "Percha", "Plain Lamp": "Lámpara Sencilla",
        "Growth Poster": "Póster de Crecimiento", "Frame": "Marco", "CD Player": "Reproductor de CD", "Workbench": "Mesa de Trabajo",
        "Extravagant Flowers": "Flores Extravagantes", "Exhibition Stand": "Stand de Exposición", "Office Cabinet": "Armario de Oficina",
        "Tiled Roof Decoration": "Decoración de Tejado de Tejas", "Tiled Roof Valley": "Valle de Tejado de Tejas", "Tiled Hipped Roof": "Tejado a Cuatro Aguas de Tejas",
        "CD Rack": "Estante para CDs", "Dowsing Machine": "Zahorí", "Wireless Power Transmitter Switch": "Interruptor de Transmisor Inalámbrico",
        "Wireless Power Transmitter": "Transmisor de Energía Inalámbrico", "Shell Lamp": "Lámpara de Concha", "Elevator Platform": "Plataforma de Ascensor",
        "Campfire": "Hoguera", "Wall Mirror": "Espejo de Pared", "Frying Pan": "Sartén", "Mirror Ball": "Bola de Espejos", "Stepping Stones": "Piedras de Paso",
        "Cooking Pot": "Olla", "Cannon": "Cañón", "Marble": "Mármol", "Party Platter": "Bandeja de Fiesta", "Resort Light": "Luz de Resort",
        "Simple Cushion": "Cojín Simple", "Hay Pile": "Montón de Heno", "Step Stool": "Taburete Escalón", "Swinging Doors": "Puertas Batientes",
        "Office Desk": "Escritorio de Oficina", "Brick Flooring": "Suelo de Ladrillo", "Ditto Flag": "Bandera de Ditto", "Brick Steps": "Escalones de Ladrillo",
        "Star Piece": "Trozo Estrella", "Grate Flooring": "Suelo de Rejilla", "Guest Room Bed": "Cama de Invitados", "Plain Chair": "Silla Sencilla",
        "Slender Candle": "Vela Fina", "Sign": "Letrero", "Spotlight": "Foco", "Underground Hatch": "Trampilla Subterránea", "Cart": "Carrito",
        "Garden Table": "Mesa de Jardín", "Garden Bench": "Banco de Jardín", "Garden Chair": "Silla de Jardín", "Garden Light": "Luz de Jardín",
        "Alarm Clock": "Despertador", "Storage Box": "Caja de Almacenaje", "Big Storage Box": "Caja de Almacenaje Grande", "Puffy-Tree Pillar": "Pilar de Árbol Hinchado",
        "Wreath": "Corona", "Refrigerator": "Nevera", "Concrete Wall": "Pared de Hormigón", "Concrete Pipe": "Tubería de Hormigón", "Concrete Mixer": "Hormigonera",
        "Mushroom Streetlight": "Farola Champiñón", "Small Stage": "Escenario Pequeño", "Fluorescent Light": "Luz Fluorescente", "House Partition": "Separador de Casa",
        "Punching Game": "Juego de Puñetazos", "Gravestone": "Lápida", "Wall Photo Frame": "Marco de Fotos de Pared", "Decorative Storage Shelf": "Estante de Almacenamiento Decorativo",
        "Copper Ingot": "Lingote de Cobre", "Cobblestone Wall": "Pared de Adoquines", "Woven Carpeting": "Moqueta Tejida", "Arched Tiling": "Alicatado Arqueado",
        "Garbage Bin": "Cubo de Basura", "Garbage Bags": "Bolsas de Basura", "Rustic Door": "Puerta Rústica", "Pinwheels": "Molinillos", "Deck Chair": "Tumbona",
        "Railway Track": "Vía de Tren", "Bread Oven": "Horno de Pan", "Glass Window": "Ventana de Cristal", "Ice Cream Poster": "Póster de Helado",
        "Community Box": "Caja Comunitaria", "Water Basin": "Pilón de Agua", "Walkway": "Pasarela", "Office Chair": "Silla de Oficina",
        "Vine Wall Decoration": "Decoración de Pared de Lianas", "Hot-Spring Spout": "Caño de Aguas Termales", "Magazine Rack": "Revistero",
        "Metal Chain": "Cadena de Metal", "Mini Bookcase": "Mini Librería", "Stylish Stool": "Taburete Elegante", "Boat Railing": "Barandilla de Barco",
        "Crystal Fragment": "Fragmento de Cristal", "Roof Support": "Soporte de Tejado", "Shower": "Ducha", "Industrial Bed": "Cama Industrial",
        "Laptop": "Portátil", "Square Tiling": "Alicatado Cuadrado", "Cutting Board": "Tabla de Cortar", "Mini Floodgate": "Mini Compuerta",
        "Photo Frame": "Marco de Fotos", "Toy Blocks": "Bloques de Juguete", "Plain Sofa": "Sofá Sencillo", "Scrap Cube": "Cubo de Chatarra",
        "Sash Window": "Ventana de Guillotina", "Planter": "Macetero", "Cash Register": "Caja Registradora", "Small Vase": "Jarrón Pequeño",
        "Office Table": "Mesa de Oficina", "Decorative Plant Shelf": "Estante de Plantas Decorativo", "Bridge Planks": "Tablones de Puente",
        "Crystal Ball": "Bola de Cristal", "Lift Platform": "Plataforma Elevadora", "Hatch Window": "Ventana de Trampilla",
        
        "Iron Pipe (Downward Curve)": "Tubería de Hierro (Curva Abajo)", "Iron Pipe (Upward Curve)": "Tubería de Hierro (Curva Arriba)",
        "Iron Pipe (Horizontal Curve)": "Tubería de Hierro (Curva Horizontal)", "Iron Pipe (Vertical Cross)": "Tubería de Hierro (Cruce Vertical)",
        "Iron Pipe (Horizontal Cross)": "Tubería de Hierro (Cruce Horizontal)", "Iron Pipe (Vertical T)": "Tubería de Hierro (T Vertical)",
        "Iron Pipe (Horizontal T)": "Tubería de Hierro (T Horizontal)", "Iron Pipe (Upward T)": "Tubería de Hierro (T Arriba)",
        "Iron Pipe (Downward T)": "Tubería de Hierro (T Abajo)", "Iron Pipe (Vertical)": "Tubería de Hierro (Vertical)", "Iron Pipe (Horizontal)": "Tubería de Hierro (Horizontal)",

        "Chesto Berry": "Baya Atania", "Rawst Berry": "Baya Safre", "Pecha Berry": "Baya Meloc", "Lum Berry": "Baya Ziuela", 
        "Aspear Berry": "Baya Perla", "Leppa Berry": "Baya Zanama",
        
        "Green Paint Balloon": "Globo de Pintura Verde", "Black Paint Balloon": "Globo de Pintura Negra", "Blue Paint Balloon": "Globo de Pintura Azul",
        "Navy Paint Balloon": "Globo de Pintura Azul Marino", "Yellow Paint Balloon": "Globo de Pintura Amarilla", "Cyan Paint Balloon": "Globo de Pintura Cian",
        "Gray Paint Balloon": "Globo de Pintura Gris", "Lime Paint Balloon": "Globo de Pintura Lima", "Orange Paint Balloon": "Globo de Pintura Naranja",
        "Pink Paint Balloon": "Globo de Pintura Rosa", "Plum Paint Balloon": "Globo de Pintura Ciruela", "Red Paint Balloon": "Globo de Pintura Roja",
        "Rose Paint Balloon": "Globo de Pintura Rosa", "Beige Paint Balloon": "Globo de Pintura Beige", "White Paint Balloon": "Globo de Pintura Blanca",
        "Aquamarine Paint Balloon": "Globo de Pintura Aguamarina", "Brown Paint Balloon": "Globo de Pintura Marrón", "Purple Paint Balloon": "Globo de Pintura Morada",
        
        "Yellow Firework": "Fuego Artificial Amarillo", "White Firework": "Fuego Artificial Blanco", "Red Firework": "Fuego Artificial Rojo",
        "Blue Firework": "Fuego Artificial Azul", "Green Firework": "Fuego Artificial Verde",

        "Red": "Rojo", "Blue": "Azul", "Green": "Verde", "Yellow": "Amarillo", "Black": "Negro",
        "White": "Blanco", "Pink": "Rosa", "Cyan": "Cian", "Lime": "Lima", "Orange": "Naranja",
        "Purple": "Morado", "Plum": "Ciruela", "Rose": "Rosa", "Beige": "Beige", "Brown": "Marrón",
        "Navy": "Azul Marino", "Gray": "Gris", "Aquamarine": "Aguamarina", "Balloon": "Globo",
        "Stool": "Taburete", "Table": "Mesa", "Chair": "Silla", "Bed": "Cama", "Wall": "Pared",
        "Floor": "Suelo", "Flooring": "Suelo", "Roof": "Tejado", "Door": "Puerta", "Window": "Ventana",
        "Decoration": "Decoración", "Harbor": "Portuario", "Streetlight": "Farola", "Bench": "Banco",
        "Fence": "Valla", "Fencing": "Valla", "Signpost": "Letrero", "Sign": "Señal", "Lamp": "Lámpara",
        "Rug": "Alfombra", "Cushion": "Cojín", "Mirror": "Espejo", "Pole": "Poste", "Pipe": "Tubería",
        "Pillar": "Pilar", "Wooden": "de Madera", "Iron": "de Hierro", "Log": "de Tronco",
        "Straw": "de Paja", "Tiled": "Alicatado", "Box": "Caja", "Firework": "Fuego Artificial",
        "Steps": "Escalones", "Berry": "Baya", "Harbur": "Portuario", " Harbur": " Portuario", "Harbour": "Portuario"
    }

    def traducir(texto):
        for en, es in TRANSLATIONS.items():
            texto = texto.replace(en, es)
        return texto

    # Process Habitats
    for row_content in rows_hab[1:]:
        cells = re.findall(r'<td.*?>(.*?)</td>', row_content, re.DOTALL | re.IGNORECASE)
        if len(cells) < 5: continue
        
        num = re.sub(r'<.*?>', '', cells[0]).strip()
        habitat = html.unescape(re.sub(r'<.*?>', '', cells[1]).strip())
        
        pokemons_raw = html.unescape(cells[2]).split('<br>')
        pokemons_clean = [re.sub(r'<.*?>', '', p).strip() for p in pokemons_raw if p.strip()]
        pokemon_html = "<ul class='pokemon-list'>" + "".join(f"<li>{p}</li>" for p in pokemons_clean) + "</ul>"
        
        como_crear_raw = html.unescape(cells[3]).split('<br>')
        como_crear_clean = [re.sub(r'<.*?>', '', c).strip() for c in como_crear_raw if c.strip()]
        como_crear_html = "<br>".join(como_crear_clean)
        
        img_cell = cells[4]
        img_match = re.search(r'data-uri="([^"]+)"', img_cell) or re.search(r'src="([^"]+)"', img_cell)
        img_html = ""
        if img_match:
            img_url = img_match.group(1)
            if not img_url.startswith('http'): img_url = f"https://assetsio.gnwcdn.com/{img_url}"
            if "?" in img_url: img_url = img_url.split("?")[0] + "?width=300&quality=85&format=jpg&auto=webp"
            img_html = f'<img src="{img_url}" alt="Hábitat {num}" class="habitat-img" loading="lazy">'
            
        html_output += f"""                            <tr>
                                <td data-label="Imagen">{img_html}</td>
                                <td data-label="Hábitat">{habitat}</td>
                                <td data-label="Pokémon">{pokemon_html}</td>
                                <td data-label="Cómo crear">{como_crear_html}</td>
                            </tr>\n"""

    html_output += """                        </tbody>
                    </table>
                </div>
            </section>
            
            <section id="crafteos" style="margin-top: 3rem;">
                <div class="section-header-row">
                    <h2>Recetas de Crafteo</h2>
                    <input type="text" id="search-crafteos" class="search-bar" placeholder="Buscar receta o material...">
                </div>
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Imagen</th>
                                <th>Receta</th>
                                <th>Materiales</th>
                            </tr>
                        </thead>
                        <tbody>
"""

    # Process Crafting Recipes (all tables)
    for table in tables_cra:
        rows = re.findall(r'<tr.*?>(.*?)</tr>', table, re.DOTALL | re.IGNORECASE)
        for row in rows[1:]: # Skip header
            cells = re.findall(r'<td.*?>(.*?)</td>', row, re.DOTALL | re.IGNORECASE)
            if len(cells) < 2: continue
            
            # cell 0: Recipe Name + Figure
            name_match = re.search(r'^(.*?)<figure', cells[0], re.DOTALL | re.IGNORECASE)
            name = name_match.group(1).strip() if name_match else re.sub(r'<.*?>', '', cells[0]).strip()
            name = traducir(name)
            
            img_match = re.search(r'data-uri="([^"]+)"', cells[0]) or re.search(r'src="([^"]+)"', cells[0])
            img_html = ""
            if img_match:
                img_url = img_match.group(1)
                if not img_url.startswith('http'): img_url = f"https://assetsio.gnwcdn.com/{img_url}"
                if "?" in img_url: img_url = img_url.split("?")[0] + "?width=300&quality=85&format=jpg&auto=webp"
                img_html = f'<img src="{img_url}" alt="{name}" class="habitat-img" loading="lazy">'
            
            # cell 1: Materials
            mats_raw = html.unescape(cells[1]).split('<br>')
            mats_clean = [traducir(re.sub(r'<.*?>', '', m).strip()) for m in mats_raw if m.strip()]
            mats_html = "<br>".join(mats_clean)
            
            html_output += f"""                            <tr>
                                <td data-label="Imagen">{img_html}</td>
                                <td data-label="Receta"><strong>{name}</strong></td>
                                <td data-label="Materiales">{mats_html}</td>
                            </tr>\n"""

    html_output += """                        </tbody>
                    </table>
                </div>
            </section>
        </main>
    </div>
    
    <button id="scrollTopBtn" title="Volver arriba">
        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m5 12 7-7 7 7"/><path d="M12 19V5"/></svg>
    </button>
    
    <!-- Modal para ampliar imágenes -->
    <div id="image-modal" class="modal">
        <span class="close-modal">&times;</span>
        <img class="modal-content" id="modal-img">
        <div id="modal-caption"></div>
    </div>
    
    <script>
        const themeToggle = document.getElementById('theme-toggle');
        const body = document.body;
        
        const moonIcon = document.getElementById('moon-icon');
        const sunIcon = document.getElementById('sun-icon');
        
        function updateIcons(isDark) {
            if (isDark) {
                moonIcon.style.display = 'none';
                sunIcon.style.display = 'block';
            } else {
                moonIcon.style.display = 'block';
                sunIcon.style.display = 'none';
            }
        }

        // Iniciar el tema comprobando localStorage
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'dark') {
            body.classList.add('dark-mode');
            updateIcons(true);
        } else {
            updateIcons(false);
        }

        themeToggle.addEventListener('click', () => {
            body.classList.toggle('dark-mode');
            const isDark = body.classList.contains('dark-mode');
            updateIcons(isDark);
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
        });
        
        // Active link switching logic based on scroll/click could go here
        const links = document.querySelectorAll('.nav-links a');
        links.forEach(link => {
            link.addEventListener('click', function() {
                links.forEach(l => l.classList.remove('active'));
                this.classList.add('active');
            });
        });

        // Lightbox logic
        const modal = document.getElementById("image-modal");
        const modalImg = document.getElementById("modal-img");
        const captionText = document.getElementById("modal-caption");
        const closeBtn = document.querySelector(".close-modal");

        document.querySelectorAll('.habitat-img').forEach(img => {
            img.addEventListener('click', function() {
                modal.style.display = "flex";
                modalImg.src = this.src.replace('?width=300', '?width=800'); // Trata de cargar a más resolución si es posible
                captionText.innerHTML = this.alt;
            });
        });

        closeBtn.addEventListener('click', () => {
            modal.style.display = "none";
        });

        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                modal.style.display = "none";
            }
        });

        // Funcionalidad Volver Arriba
        const scrollTopBtn = document.getElementById("scrollTopBtn");
        window.onscroll = function() {
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                scrollTopBtn.style.display = "flex";
            } else {
                scrollTopBtn.style.display = "none";
            }
        };

        scrollTopBtn.addEventListener("click", function() {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });

        // Funcionalidad de Búsqueda de Hábitats
        const searchInput = document.getElementById("search-habitat");
        const habitatTable = document.querySelector("#habitats table tbody");
        const habitatRows = habitatTable.getElementsByTagName("tr");

        searchInput.addEventListener("keyup", function() {
            const filter = searchInput.value.toLowerCase();
            for (let i = 0; i < habitatRows.length; i++) {
                const row = habitatRows[i];
                const textContent = row.textContent || row.innerText;
                if (textContent.toLowerCase().indexOf(filter) > -1) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            }
        });
        // Funcionalidad de Búsqueda de Crafteos
        const searchCrafteos = document.getElementById("search-crafteos");
        const crafteosTable = document.querySelector("#crafteos table tbody");
        const crafteosRows = crafteosTable.getElementsByTagName("tr");

        searchCrafteos.addEventListener("keyup", function() {
            const filter = searchCrafteos.value.toLowerCase();
            for (let i = 0; i < crafteosRows.length; i++) {
                const row = crafteosRows[i];
                const textContent = row.textContent || row.innerText;
                if (textContent.toLowerCase().indexOf(filter) > -1) {
                    row.style.display = "";
                } else {
                    row.style.display = "none";
                }
            }
        });
    </script>
</body>
</html>"""

    with open('d:\\Pokowiki\\index.html', 'w', encoding='utf-8') as f:
        f.write(html_output)
    print("Wiki successfully built!")

if __name__ == "__main__":
    fetch_and_build()
