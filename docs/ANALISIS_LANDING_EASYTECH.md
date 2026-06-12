# Análisis Landing EasyTech — Informe técnico

**Versión:** 1.0  
**Fecha:** junio 2026  
**Autor:** auditoría técnica (Sprint 1)  
**Alcance:** exclusivamente el sitio **easytech.services** y productos/servicios del **EasyTech Ecosystem**.  
**Referencias:** `docs/ROADMAP_LANDING_EASYTECH_2026.md`, `docs/MAPA_CTA.md`

---

## 1. Resumen ejecutivo

El sitio actual es una base sólida (HTML estático, estilo visual actual, SPA ligera, páginas de producto EasyTech iniciadas) pero **no comunica aún el EasyTech Ecosystem**: la navegación mezcla categorías, el landing prioriza productos sueltos y la captación está fragmentada.

Las decisiones aprobadas (ecosistema, Easy Converso oficial, prioridad Facturación Electrónica, mapa CTA sin formularios, header compartido antes del menú nuevo) son correctas y reducen riesgo.

**Recomendación:** ejecutar Sprint 2 (partials) antes de cualquier ampliación del menú. Estimar **4–6 semanas** de trabajo técnico + contenido comercial para sprints 2–6, dependiendo de entrega de flyers y copy.

---

## 2. Diagnóstico del estado actual

### 2.1 Stack y arquitectura

| Componente | Ubicación | Observación |
|------------|-----------|-------------|
| Páginas | 6 × `.html` en raíz | Sin carpeta `pages/` |
| Estilos | `assets/css/main.css`, `ramp-theme.css` | Coherente con el diseño actual del sitio |
| JS | `main.js`, `page-transitions.js`, `calendly-config.js` | SPA parcial, agenda en línea, demo stack |
| Imágenes | `assets/images/` | Mix PNG + SVG; algunos PNG referenciados ausentes |
| Documentación | `docs/` | Creada con este sprint |

**SPA (`page-transitions.js`):** intercambia `#page-main`, `document.title` y `body.className`. No actualiza `<meta description>`. Header/footer quedan fijos — favorable para partials inyectados una vez.

### 2.2 Páginas existentes

| Archivo | Líneas aprox. | Rol actual | Alineación con roadmap |
|---------|---------------|------------|------------------------|
| `index.html` | ~460 | Landing corporativo | Parcial — falta narrativa ecosistema |
| `soluciones.html` | ~395 | ERP / Easy Odoo | OK como base Sprint 4 |
| `econverso.html` | ~300 | Easy Converso | OK; renombrar copy a “Easy Converso” |
| `easynodeone.html` | ~290 | EasyNodeOne | OK |
| `agenda.html` | ~240 | Agenda en línea | OK |
| `contacto.html` | ~465 | Contacto | Duplica mucho de `index.html`; no es hub claro |

### 2.3 Menú actual vs menú objetivo

**Hoy (todas las páginas):**

```text
Producto ▼
  Capturas · Cómo encaja · Soluciones
  ERP EasyTech · Easy Converso · EasyNodeOne
Contacto ▼
  Agenda · Hablar con el equipo
```

**Problemas:**

- “Producto” no vende el ecosistema EasyTech; mezcla anclas del landing con plataformas.
- Easy Odoo aparece como plataforma y como solución.
- Faltan: Facturación Electrónica, Servicios profesionales, cuatro plataformas del catálogo.

**Objetivo (aprobado):** Inicio · Plataformas · Soluciones · Servicios profesionales · Contacto.

### 2.4 Captación real (sin formularios)

| Canal | Estado | Evidencia |
|-------|--------|-----------|
| WhatsApp | Activo | `wa.me/50766884938`, textos variables |
| Agenda en línea | Activo | `agenda.html`, `EASYTECH_CALENDLY_EVENT_URL` |
| Registro en portal | Activo | CTAs en `econverso.html`, `easynodeone.html` |
| Email | Activo | mailto easytechservices25@gmail.com |
| Formulario HTML | **No existe** | Ningún `<form>` en el repo |
| CRM embebido | **No visible** | Fuera del sitio estático |

Conclusión: el roadmap original asumía formularios; la realidad coincide con **`docs/MAPA_CTA.md`**.

### 2.5 Assets gráficos

**Presentes en repo (`assets/images/`):**

- `logo-easytech-services.png`, `demo-erp-odoo.png`, `hero-odoo-tableros-metricas.png`
- `hero-econverso-dashboard.png`, `demo-econverso-contactos.png`, logos SVG
- SVG de beneficios ERP, fallback informes tesorería

**Referenciados pero ausentes:**

| Asset | Impacto |
|-------|---------|
| `demo-cheques.png` | Demo stack muestra fallback |
| `demo-odoo-informes-tesoreria.png` | Cae a SVG genérico |
| `easynodeone-dashboard.png` | Cae a logo SVG |

**Riesgo de credibilidad:** copy “Todo lo que ves son capturas reales” con assets rotos.

**Reutilización de capturas:** varias tarjetas del grid usan la misma PNG con `alt` distinto (Ventas = Facturación = POS). Corregir en Sprint 3–4.

### 2.6 Contenido y marca

| Issue | Severidad |
|-------|-----------|
| Meta “Operá” vs H1 “Opera” (voseo/tuteo) | Media |
| Acentos faltantes (`dias`, `operacion`, `automatizacion`) | Media |
| “Seis aplicaciones” con 8 tarjetas | Alta (copy incorrecto) |
| Hero CTA → solo login EasyNodeOne | Alta (desalineado con ecosistema) |
| `index.html` sin sección `#cta` final | Alta |
| Bloque `company-scale` duplicado vs `soluciones.html` | Baja |
| Sin OG tags, favicon, canonical | Media (SEO/social) |

### 2.7 Deuda técnica crítica: header/footer duplicados

Cada página incluye el mismo bloque de header (~130 líneas) y footer (~35 líneas). **6 archivos hoy → 14+ con el catálogo completo.**

Cambio de menú = **N archivos editados manualmente** + riesgo de enlaces inconsistentes.

**Esta es la prioridad técnica #1** (Sprint 2 aprobado).

---

## 3. Brechas contra el roadmap aprobado

| Área | Brecha | Sprint |
|------|--------|--------|
| Narrativa ecosistema | Landing vende productos sueltos | 3 |
| Menú comercial | 2 dropdowns vs 5 categorías | 3 |
| Easy Odoo | Existe pero taxonomía confusa | 4 |
| Facturación Electrónica | Sin página (prioridad #2) | 4 |
| Easy Converso oficial | Naming inconsistente | 5 |
| 4 plataformas + 2 servicios | 8 páginas faltantes | 4–6 |
| Mapa CTA unificado | CTAs dispersos, hero desalineado | 3–6 |
| Header/footer DRY | Duplicación total | **2** |
| Catálogo IA | No existe | 7 |
| CRM | No en sitio | Post–Sprint 7 |

---

## 4. Propuesta de implementación

### 4.1 Sprint 2 — Header y footer compartidos (recomendación técnica)

**Opción recomendada:** partials + fetch (sin build obligatorio en dev).

```text
assets/partials/
  header.html      ← nav completa + header-actions
  footer.html      ← footer estándar
assets/js/site-chrome.js   ← fetch + inject + reinit nav dropdowns
```

**Flujo:**

1. Al `DOMContentLoaded`, si `#site-header` / `#site-footer` existen como placeholders vacíos, cargar partials.
2. Tras inyectar, llamar `initNavDropdowns()` (extraer de `main.js` o invocar vía `reinitPage`).
3. En `page-transitions.js`, **no** reemplazar header/footer al hacer swap de `#page-main` (comportamiento actual compatible).

**Alternativa:** script Node/PowerShell pre-deploy que concatena partials → HTML estático final. Más robusto offline (`file://`); más paso en deploy.

**Criterio de aceptación Sprint 2:**

- Un solo archivo fuente para nav y footer.
- Las 6 páginas actuales renderizan igual visualmente.
- Mega menú desktop + acordeón mobile funcionan tras SPA.
- Agenda en línea y páginas con `body.page-*` conservan clases.

### 4.2 Sprint 3 — Menú ecosistema + landing

**Cambios en `index.html`:**

1. Hero: mensaje **EasyTech Ecosystem** (plataformas + soluciones + servicios profesionales).
2. Sustituir grid de 8 tarjetas mezcladas por **4 bloques de categoría** con 2–3 destacados cada uno (según prioridad comercial).
3. Añadir sección `#cta` (patrón de `soluciones.html`): WhatsApp + Agenda.
4. Corregir copy numérico, voseo Panamá, acentos.

**Menú:** implementar estructura del roadmap; mega menú con columnas por categoría.

### 4.3 Sprint 4 — Easy Odoo + Facturación Electrónica

- Crear `facturacion-electronica.html` desde plantilla `soluciones.html` / `econverso.html`.
- Decisión URL Easy Odoo:
  - **Opción A (menor riesgo):** mantener `soluciones.html`, actualizar títulos a “Easy Odoo”.
  - **Opción B:** crear `easy-odoo.html`, dejar `soluciones.html` como redirect o hub (requiere reglas servidor o meta refresh).

Recomendación: **Opción A** en v1; redirect en v2 si hace falta SEO limpio.

### 4.4 Sprints 5–6 — Resto del catálogo

Clonar plantilla de producto; contenido desde flyers comerciales. CTAs estrictamente según `MAPA_CTA.md`.

### 4.5 Sprint 7 — IA comercial

Crear `docs/catalogo-comercial.yaml` (o `assets/data/catalogo.json`) sincronizado con páginas web. Campos: slug, nombre, categoría, descripción, beneficios, público, modelo, ctas, faq.

---

## 5. Archivos a modificar (por sprint)

### Sprint 2

| Acción | Archivos |
|--------|----------|
| Crear | `assets/partials/header.html`, `footer.html`, `assets/js/site-chrome.js` |
| Modificar | `index.html`, `soluciones.html`, `econverso.html`, `easynodeone.html`, `agenda.html`, `contacto.html` |
| Modificar | `main.js` (opcional: export init nav tras inject) |

### Sprint 3

| Acción | Archivos |
|--------|----------|
| Modificar | `assets/partials/header.html`, `footer.html` |
| Modificar | `index.html`, `ramp-theme.css` (si mega menú crece) |
| Modificar | `contacto.html` (rol hub) |

### Sprint 4–6

| Acción | Archivos |
|--------|----------|
| Crear | `facturacion-electronica.html`, `eclassone.html`, … |
| Modificar | `soluciones.html`, `econverso.html`, `easynodeone.html` |
| Assets | PNG/flyers por producto en `assets/images/` |

### Sprint 7

| Crear | `docs/catalogo-comercial.yaml` |

---

## 6. Riesgos

| Riesgo | Prob. | Impacto | Mitigación |
|--------|-------|---------|------------|
| Editar 14 HTML sin partials | Alta | Alto | Sprint 2 obligatorio |
| Mega menú ilegible en mobile | Media | Medio | Acordeones; limitar ítems visibles |
| Falta copy/flyers nuevos productos | Alta | Alto | Publicar “Próximamente” solo EPayRoll; resto espera material |
| Assets rotos | Alta | Medio | Inventario Sprint 1; no prometer “capturas reales” sin PNG |
| `fetch` partials en `file://` | Media | Bajo | Servir con http local; o build estático |
| SPA + header inject timing | Media | Medio | Inject antes de `initNavDropdowns`; probar navegación |
| Nomenclatura inconsistente | Media | Medio | Tabla oficial en roadmap |
| Facturación Electrónica legal/comercial | Media | Alto | Validar copy con área comercial antes de publicar |

---

## 7. Estimación de tiempo

| Sprint | Esfuerzo dev | Dependencias |
|--------|--------------|--------------|
| 1 Análisis | 1–2 días | — *(este documento)* |
| 2 Partials | 2–3 días | Decisión fetch vs build |
| 3 Menú + landing | 3–5 días | Copy ecosistema aprobado |
| 4 Easy Odoo + Factura electr. | 3–5 días | Copy + flyer facturación |
| 5 Converso + EN1 | 2–3 días | Assets EN1 |
| 6 Resto catálogo | 7–10 días | Flyers por plataforma |
| 7 Catálogo IA | 1–2 días | Páginas estables |

**Total:** ~20–32 días hábiles (4–6 semanas), asumiendo contenido comercial en paralelo.

---

## 8. Inventario rápido (Sprint 1)

### Páginas

- Existentes: 6  
- Por crear: 8 (`facturacion-electronica`, `eclassone`, `ethesisone`, `eposone`, `epayroll`, `desarrollo-software`, `consultoria-ti`; opcional `easy-odoo`)

### Formularios

- HTML: 0  
- Agenda en línea: 1 (`agenda.html`)  
- WhatsApp: múltiples enlaces  
- Registro en portal: Easy Converso, EasyNodeOne

### Prioridad comercial vs cobertura web

```text
1. Easy Odoo           ████████░░  ~80%  (soluciones.html)
2. Fact. Electrónica   ░░░░░░░░░░   0%
3. Easy Converso       ████████░░  ~85%  (econverso.html)
4. EasyNodeOne         ████████░░  ~80%
5–8. Resto plataformas     ░░░░░░░░░░   0%
```

---

## 9. Recomendación final

1. **Aprobar los tres documentos en Git** (`ROADMAP`, `ANALISIS`, `MAPA_CTA`) como baseline.  
2. **No iniciar Sprint 3** (menú nuevo) hasta cerrar Sprint 2 (partials).  
3. **Sprint 4 primero en contenido de alto ROI:** Facturación Electrónica + refuerzo Easy Odoo.  
4. **Unificar voseo + “Easy Converso” + “Easy Odoo”** en un pase de copy transversal en Sprint 3.  
5. **Resolver assets rotos** antes de re-lanzar campañas comerciales.  
6. **CRM e IA:** explícitamente fuera de alcance hasta Sprint 7 y decisión posterior.

El roadmap aprobado es ejecutable, coherente con el repo actual y corrige los supuestos erróneos (formularios, productos aislados). El cuello de botella no es diseño ni framework: es **mantenibilidad del chrome (nav/footer)** y **contenido comercial por línea de producto**.

---

## 10. Próximos pasos inmediatos

- [ ] Revisión comercial de `docs/MAPA_CTA.md` (textos WhatsApp)  
- [ ] Decisión fetch vs build para partials (Sprint 2)  
- [ ] Decisión URL Easy Odoo: `soluciones.html` vs `easy-odoo.html`  
- [ ] Entrega de flyer/copy Facturación Electrónica Panamá  
- [ ] Comenzar Sprint 2 en rama dedicada; sin push a producción sin revisión
