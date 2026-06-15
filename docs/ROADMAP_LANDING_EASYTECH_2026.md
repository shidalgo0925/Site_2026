# Roadmap Landing EasyTech 2026

**Versión:** candidata para Git (decisiones aprobadas)  
**Fecha:** junio 2026  
**Alcance:** sitio estático EasyTech Services — reorganización comercial sin rehacer el stack

---

## Visión

EasyTech **no es una empresa de software con productos sueltos**. Es un **ecosistema comercial de soluciones tecnológicas** que integra plataformas, soluciones de negocio y servicios profesionales.

El sitio debe comunicar:

> **EasyTech Ecosystem**  
> Plataformas · Soluciones · Servicios profesionales

**Alcance del sitio:** exclusivamente **easytech.services** y el **EasyTech Ecosystem** (plataformas, soluciones y servicios profesionales de EasyTech).

Cualquier visitante debe entender en segundos qué ofrece el ecosistema y cómo dar el siguiente paso (WhatsApp, agenda, registro o correo).

---

## Objetivo del proyecto

Alinear el sitio web con la visión comercial actual:

- Reutilizar el 70–80 % del código, CSS y assets existentes.
- Reorganizar navegación, landing y páginas de producto.
- Conectar cada línea comercial a un destino de captación claro.
- Preparar base de contenido para IA comercial (Sprint 7).

**No** rehacer el landing desde cero. **No** cambiar el stack tecnológico.

---

## Principios de trabajo

| Principio | Detalle |
|-----------|---------|
| Reutilizar | HTML, CSS actual, JS (`main.js`, `page-transitions.js`), capturas, branding EasyTech |
| Ecosistema primero | La navegación vende el ecosistema EasyTech, no productos aislados |
| Captación real | WhatsApp, agenda ECalendar (`agenda.html`), registro en portal del producto, email; Turnstile en formularios |
| Mantenibilidad | Header y footer compartidos **antes** de ampliar el menú |
| CRM después | Mapa CTA primero; integración CRM en fase posterior |
| Sin push sin revisión | Cambios productivos validados antes de publicar |

---

## Catálogo comercial EasyTech

### Plataformas (SaaS del ecosistema)

| Plataforma | Estado web | Notas |
|------------|------------|-------|
| EasyNodeOne | Página existente | Gestor de servicios / EN1 |
| **Easy Converso** | Página existente | Producto oficial en producción |
| EClassOne | Por crear | |
| EThesisOne | Por crear | |
| EPOSOne | Por crear | |
| EPayRoll | Por crear | Estado comercial: próximamente |

### Soluciones (negocio / implementación)

| Solución | Estado web | Prioridad |
|----------|------------|-----------|
| Easy Odoo | `soluciones.html` (renombrar/reorganizar) | **1** |
| Facturación Electrónica Panamá | Por crear | **2** |

### Servicios profesionales

| Servicio | Estado web |
|----------|------------|
| Desarrollo de Software | Por crear |
| Consultoría TI | Por crear |

---

## Navegación objetivo

La barra principal vende el **ecosistema**, no un listado plano de SKUs.

```text
Inicio

Plataformas ▼
 ├─ EasyNodeOne
 ├─ Easy Converso
 ├─ EClassOne
 ├─ EThesisOne
 ├─ EPOSOne
 └─ EPayRoll

Soluciones ▼
 ├─ Easy Odoo
 └─ Facturación Electrónica Panamá

Servicios profesionales ▼
 ├─ Desarrollo de Software
 └─ Consultoría TI

Contacto
```

**Contacto** agrupa: agenda en línea, WhatsApp, correo EasyTech y acceso a `contacto.html`.

El hero y el landing deben reforzar la narrativa del ecosistema EasyTech (bloques por categoría, no tarjetas sueltas mezcladas).

---

## Prioridad comercial (orden de implementación)

1. Easy Odoo  
2. Facturación Electrónica Panamá  
3. Easy Converso  
4. EasyNodeOne  
5. EClassOne  
6. EThesisOne  
7. EPOSOne  
8. EPayRoll  

Servicios profesionales (Desarrollo, Consultoría) se publican cuando haya copy y CTA definidos; no compiten con las prioridades 1–4.

---

## Páginas del sitio

### Ya existentes

| Archivo | Rol actual | Rol objetivo |
|---------|------------|--------------|
| `index.html` | Landing corporativo | Vitrina **EasyTech Ecosystem** |
| `soluciones.html` | ERP EasyTech | **Easy Odoo** (renombrar o redirigir) |
| `econverso.html` | Easy Converso | Mantener; alinear naming “Easy Converso” |
| `easynodeone.html` | EasyNodeOne | Mantener |
| `agenda.html` | ECalendar V1 (booking 2 columnas) | ✅ UI en sitio; ⏳ API EN1 + Google Calendar |
| `contacto.html` | Hub de contacto parcial | Hub de captación del ecosistema |

### Crear o completar

| Archivo | Categoría |
|---------|-----------|
| `facturacion-electronica.html` | Soluciones |
| `easy-odoo.html` | Soluciones *(opcional si se renombra `soluciones.html`)* |
| `eclassone.html` | Plataformas |
| `ethesisone.html` | Plataformas |
| `eposone.html` | Plataformas |
| `epayroll.html` | Plataformas |
| `desarrollo-software.html` | Servicios profesionales |
| `consultoria-ti.html` | Servicios profesionales |

**No eliminar** páginas existentes; migrar con redirecciones o enlaces internos si cambian URLs.

---

## Estructura estándar de cada página de producto

1. Hero del producto (logo, H1, lede)  
2. Problema que resuelve  
3. Beneficios principales  
4. Capturas o flyer comercial  
5. Casos de uso  
6. CTA principal (según `docs/MAPA_CTA.md`)  
7. CTA secundario (agenda / WhatsApp / email)  
8. Enlace al ecosistema (otras plataformas o soluciones relacionadas)

Plantilla de referencia: `econverso.html`, `easynodeone.html`.

---

## Flujo comercial objetivo

```text
Landing EasyTech Ecosystem
        ↓
Página de plataforma / solución / servicio
        ↓
Captación (WhatsApp · Agenda · Registro · Email)
        ↓
[Fase posterior] Easy Converso → CRM → Cotización → ERP → Facturación
```

La fase CRM **no** forma parte de los sprints 1–6 del sitio estático.

---

## Captación

Canales reales del sitio:

| Canal | Implementación actual |
|-------|------------------------|
| WhatsApp | `wa.me/50766884938` con texto prellenado por producto |
| Agenda | **`agenda.html` + ECalendar** (`assets/js/ecalendar*.js`, `ecalendar.css`); modo demo (`mockMode`) hasta EN1 |
| Registro | Portal de registro de cada plataforma EasyTech (Easy Converso, EasyNodeOne, etc.) |
| Email | `mailto:easytechservices25@gmail.com` |
| Anti-spam | Cloudflare Turnstile (`site-captcha.js`) en formularios del sitio |

Mapa detallado: **`docs/MAPA_CTA.md`**.

**ECalendar — estado jun 2026**

| Fase | Estado | Notas |
|------|--------|-------|
| Landing UI (`agenda.html`) | ✅ Hecho | Layout 30% flujo \| 70% calendario; fecha, hora, datos, confirmación correo, captcha |
| API EN1 `/api/ecalendar/*` | ⏳ Pendiente | Ver `docs/INSTRUCCION_ECALENDAR_EN1_APPDEV.md` |
| Google Calendar (`easytechservices25@gmail.com`) | ⏳ Pendiente | Solo vía backend EN1 |
| CRM / leads desde agenda | ⏳ Fase posterior | V2 |

Calendly **deprecado** en `agenda.html`. Config legacy: `assets/js/calendly-config.js` (sin uso en agenda).

---

## Deuda técnica crítica: header y footer

Hoy cada `.html` duplica ~150 líneas de navegación y footer. Con 14+ páginas, **cualquier cambio de menú implica editar todos los archivos**.

**Decisión obligatoria antes del Sprint 3 (nuevo menú):**

Implementar **header compartido** y **footer compartido** sin cambiar el stack (HTML estático + JS existente).

Opciones aceptables (ver análisis en `docs/ANALISIS_LANDING_EASYTECH.md`):

- Partials en `assets/partials/` + carga por `fetch` al DOMContentLoaded  
- Script de build mínimo (concatenación en deploy)  
- Cualquier alternativa que mantenga HTML/CSS/JS en producción

---

## Plan de sprints (versión aprobada)

### Sprint 1 — Análisis

**Entregables:**

- `docs/ANALISIS_LANDING_EASYTECH.md`  
- `docs/MAPA_CTA.md`  
- Inventario de páginas, assets y brechas  
- Propuesta de arquitectura (partials, URLs, taxonomía)

**Regla:** no modificar código de producción.

---

### Sprint 2 — Header y footer compartidos

- Extraer nav y footer a partials  
- Cargar/inyectar en todas las páginas existentes  
- Verificar SPA (`page-transitions.js`) y mega menú mobile  
- Sin cambiar aún la estructura del menú comercial

---

### Sprint 3 — Nuevo menú y landing ecosistema

- Menú: Plataformas · Soluciones · Servicios profesionales · Contacto  
- Reorganizar `index.html` como vitrina del ecosistema  
- Actualizar footer acorde al catálogo  
- Unificar nomenclatura (“Easy Converso”, “Easy Odoo”, “EasyTech Ecosystem”)

**Estado:** ✅ mayormente completado (jun 2026).

---

### Sprint 3b — ECalendar landing (agenda)

- Reemplazar Calendly por UI propia en `agenda.html`  
- Layout booking 2 columnas: flujo izquierda \| calendario derecha  
- Validación correo, Turnstile, productos del ecosistema  
- Modo demo hasta conectar EN1

**Estado:** ✅ completado (jun 2026). **Siguiente:** backend EN1 según `docs/INSTRUCCION_ECALENDAR_EN1_APPDEV.md`.

### Sprint 4 — Prioridades comerciales 1 y 2

- `facturacion-electronica.html` (nueva)  
- Easy Odoo: completar/reorganizar `soluciones.html` (o `easy-odoo.html`)  
- CTAs según mapa; sección `#cta` en landing

---

### Sprint 5 — Prioridades 3 y 4

- Completar `econverso.html` (naming, CTAs, ecosistema)  
- Completar `easynodeone.html`  
- Assets faltantes (capturas, flyers)

---

### Sprint 6 — Resto del catálogo

- EClassOne, EThesisOne, EPOSOne, EPayRoll  
- Desarrollo de Software, Consultoría TI  
- EPOSOne / EPayRoll según madurez comercial (“Próximamente” donde aplique)

---

### Sprint 7 — IA comercial

- Catálogo estructurado (JSON/YAML): producto, descripción, beneficios, público, modelo, CTA, FAQ  
- **Sin** conectar IA en producción todavía

---

## Restricciones

- No rehacer el landing desde cero  
- No cambiar el stack (HTML + CSS + JS vanilla)  
- No eliminar páginas existentes  
- No rediseño global sin aprobación  
- Formulario HTML **solo** en `agenda.html` (ECalendar); resto del sitio sin forms nuevos  
- No conectar CRM/IA en sprints 1–6  
- No push a producción sin revisión

---

## Documentación en Git

| Documento | Propósito |
|-----------|-----------|
| `docs/ROADMAP_LANDING_EASYTECH_2026.md` | Este roadmap (versión candidata) |
| `docs/ANALISIS_LANDING_EASYTECH.md` | Diagnóstico técnico y propuesta de implementación |
| `docs/MAPA_CTA.md` | Producto → destino de captación |
| `docs/PROPUESTA_TECNICA_ECALENDAR_V1.md` | Propuesta ECalendar (Google Calendar, flujo) |
| `docs/INSTRUCCION_ECALENDAR_EN1_APPDEV.md` | Implementación API ECalendar en EN1 |

---

## Objetivo final

Convertir el sitio en una **vitrina comercial clara del EasyTech Ecosystem**, conectada al proceso de ventas existente (WhatsApp, agenda, registro, email), mantenible a medida que crece el catálogo, y lista para escalar a CRM e IA comercial en fases posteriores.
