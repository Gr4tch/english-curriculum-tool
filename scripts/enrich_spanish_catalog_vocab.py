import json
import re
from pathlib import Path

# Load extracted glossary
glossary_path = Path("output/spanish/glossary.json")
glossary = json.loads(glossary_path.read_text(encoding="utf-8"))
g_lower = {k.lower(): v for k, v in glossary.items()}

# Curated canonical definitions for compounds, inflections, and historical concepts
SUPPLEMENTAL_DEFINITIONS = {
    "milicias": "grupos de hombres locales que se organizaron para proteger a su pueblo o colonia",
    "proclamación de 1763": "ley británica que prohibía a los colonos norteamericanos establecerse al oeste de los montes Apalaches",
    "ley de alojamiento": "ley del Parlamento que obligaba a los colonos a proporcionar vivienda y suministros a los soldados británicos",
    "ley del timbre": "ley británica de 1765 que exigía un sello fiscal en todos los documentos legales y periódicos en las colonias",
    "leyes declaratoria": "ley del Parlamento de 1766 que afirmaba su total autoridad para aprobar leyes que obligaran a las colonias",
    "leyes de extranjería y sedición": "cuatro leyes aprobadas en 1798 por los federalistas que limitaban la inmigración y restringían la libertad de expresión contra el gobierno",
    "partido de suelo libre": "partido político formado en 1848 dedicado a impedir la expansión de la esclavitud en los territorios occidentales",
    "halcones de guerra": "miembros del Congreso, en su mayoría del sur y del oeste, que presionaron por la guerra contra Gran Bretaña en 1812",
    "hessians (hesianos)": "soldados alemanes mercenarios contratados por Gran Bretaña para luchar contra los patriotas norteamericanos",
    "lexington y concord": "primeros enfrentamientos militares armados de la Guerra de Independencia entre tropas británicas y milicianos coloniales en 1775",
    "rebelión del whisky": "levantamiento armado de 1794 de granjeros en Pensilvania en protesta contra el impuesto federal sobre el licor",
    "habeas corpus": "orden judicial que protege a las personas contra el encarcelamiento ilegal o arbitrario al exigir que comparezcan ante un juez",
    "ironclads (barcos blindados)": "buques de guerra acorazados con gruesas planchas de hierro, utilizados por primera vez durante la Guerra Civil",
    "forty-niners": "buscadores de oro que viajaron a California en 1849 tras el descubrimiento de oro en Sutter's Mill",
    "sirvientes ligados por contratos": "personas que firmaban un acuerdo legal para trabajar sin paga durante un número de años a cambio de su viaje a América",
    "estados fronterizos": "estados esclavistas (Delaware, Maryland, Kentucky y Misuri) que permanecieron leales a la Unión durante la Guerra Civil",
    "ciudades en auge": "poblaciones mineras o comerciales que crecían casi de la noche a la mañana tras el hallazgo de recursos valiosos",
    "colonias reales": "colonias inglesas gobernadas directamente por la corona británica a través de un gobernador y un consejo designados por el rey",
    "autores de la constitución": "grupo de 55 delegados coloniales que se reunieron en Filadelfia en 1787 para redactar la Constitución de los Estados Unidos",
    "escuelas comunes": "escuelas públicas gratuitas financiadas con impuestos locales para educar a niños de todas las clases sociales",
    "factores de expulsión o atracción": "razones que impulsan a las personas a salir de su país natal (expulsión) o las atraen hacia un nuevo destino (atracción)",
    "reclutamiento forzado": "práctica de la armada real británica de capturar por la fuerza a marineros mercantes norteamericanos para obligarlos a servir en barcos británicos",
    "sindicatos de oficios": "asociaciones de trabajadores calificados que se unían para negociar mejores salarios, jornadas laborales y condiciones de trabajo",
    "marshals": "agentes policiales del gobierno federal encargados de ejecutar órdenes judiciales y arrestar a fugitivos",
    "autonomía": "derecho o capacidad de una comunidad, estado o institución para gobernarse a sí misma con sus propias leyes",
    "cultivos comerciales": "cultivos agrícolas producidos principalmente para ser vendidos en el mercado y generar ganancias en lugar de ser consumidos por el agricultor",
    "materias primas": "recursos naturales o productos agrícolas básicos en su estado natural que se procesan o manufacturan para fabricar bienes acabados",
    "recursos naturales": "materiales o sustancias que se encuentran de forma natural en el medio ambiente y que los seres humanos pueden aprovechar económicamente",
    "tierras fronterizas": "zonas limítrofes entre asentamientos coloniales y territorios controlados por pueblos indígenas u otras potencias",
    "tasas de aduana": "impuestos cobrados por el gobierno sobre los bienes y productos que entran o salen de un puerto o frontera",
    "eslóganes": "frases o lemas breves y llamativos utilizados en campañas políticas, boicots o movimientos sociales para movilizar al público",
    "galeones": "grandes barcos de vela con múltiples cubiertas utilizados principalmente por España para el comercio transatlántico y el transporte de tesoros",
    "pontones": "embarcaciones flotantes o barcazas utilizadas para sostener puentes temporales para el paso de tropas y suministros",
    "terraplenes": "muros o terraplenes defensivos construidos con tierra y escombros para proteger a los soldados en fortificaciones",
    "independencia": "libertad política de una nación o pueblo para gobernarse a sí mismo sin estar bajo el control de otra potencia extranjera",
    "persiguió": "hostigar, acosar o castigar sistemáticamente a un grupo de personas por sus creencias religiosas o políticas",
    "reclamaciones": "demandas formales de reparación o quejas oficiales expresadas ante una autoridad gubernamental",
    "leales": "colonos norteamericanos que se opusieron a la independencia y se mantuvieron fieles a la corona británica",
    "derechos": "facultades, libertades y protecciones fundamentales reconocidas a los individuos frente al poder del gobierno",
    "evacuaran": "desalojar, retirar o abandonar ordenadamente una posición militar, fuerte o ciudad ante el avance enemigo",
    "exenciones": "liberaciones o privilegios concedidos por ley que eximen a personas de ciertas obligaciones, como el servicio militar",
    "raciones": "porciones fijas de alimentos, víveres y provisiones asignadas diariamente a cada soldado o persona en tiempo de guerra",
}

def clean_word(w: str) -> str:
    # Remove surrounding quotes, punctuation
    return re.sub(r'^[^\w]+|[^\w]+$', '', w).strip()

def lookup_spanish_def(w: str) -> str:
    cw = clean_word(w).lower()
    if not cw:
        return ""
    if cw in SUPPLEMENTAL_DEFINITIONS:
        return SUPPLEMENTAL_DEFINITIONS[cw]
    if cw in g_lower:
        return g_lower[cw]
    # Check simple inflection forms
    if cw.endswith("es") and cw[:-2] in g_lower:
        return g_lower[cw[:-2]]
    if cw.endswith("s") and cw[:-1] in g_lower:
        return g_lower[cw[:-1]]
    if cw.endswith("as") and (cw[:-2] + "o") in g_lower:
        return g_lower[cw[:-2] + "o"]
    if cw.endswith("a") and (cw[:-1] + "o") in g_lower:
        return g_lower[cw[:-1] + "o"]
    if cw.endswith("os") and (cw[:-2] + "o") in g_lower:
        return g_lower[cw[:-2] + "o"]
    # Check verbs
    verb_endings = [("aron", "ar"), ("eron", "er"), ("ieron", "ir"), ("aban", "ar"), ("ían", "ir"), ("ó", "ar"), ("ió", "ir")]
    for end, repl in verb_endings:
        if cw.endswith(end):
            stem = cw[:-len(end)] + repl
            if stem in g_lower:
                return g_lower[stem]
    # Check supplemental again with cleaned word
    for k, v in SUPPLEMENTAL_DEFINITIONS.items():
        if k in cw or cw in k:
            return v
    return ""

def enrich_catalog():
    cat_path = Path("output/spanish/catalog.json")
    catalog = json.loads(cat_path.read_text(encoding="utf-8"))
    
    total_vocab = 0
    enriched_vocab = 0
    
    for sec in catalog:
        clean_vocab_list = []
        for v in sec.get("official_vocab", []):
            w = v.get("word", "").strip()
            # Filter bad tokens
            if w in (". Un", "Leyes", "Partido de los") or len(clean_word(w)) <= 2:
                if w == "Leyes":
                    w = "Leyes de Extranjería y Sedición"
                elif w == "Partido de los":
                    w = "Partido de Suelo Libre"
                else:
                    continue
            
            defn = lookup_spanish_def(w)
            if not defn:
                # If still not found, check if existing definition is already descriptive
                cur_d = v.get("definition", "")
                if cur_d and not cur_d.lower().startswith("concepto histórico clave") and not cur_d.lower().startswith("key historical"):
                    defn = cur_d
                else:
                    defn = f"Concepto y término histórico fundamental estudiado en las páginas {sec['printed_pages']}."
            
            clean_vocab_list.append({
                "word": w,
                "type": v.get("type", "Vocabulario de contenido"),
                "definition": defn,
                "page": v.get("page", sec["start_page"]),
            })
            total_vocab += 1
            if not defn.startswith("Concepto y término histórico fundamental"):
                enriched_vocab += 1
                
        sec["official_vocab"] = clean_vocab_list

    cat_path.write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Catalog updated! Total vocab entries: {total_vocab}, Authentically defined: {enriched_vocab} ({enriched_vocab/total_vocab*100:.1f}%)")

if __name__ == "__main__":
    enrich_catalog()
