# Mapa CTA — EasyTech Ecosystem

**Versión:** 1.1  
**Fecha:** junio 2026  
**Sitio:** easytech.services  
**Alcance:** destino de captación por línea comercial EasyTech — **sin formularios HTML en el sitio**

---

## Canales de captación

| Canal | ID | Destino base | Uso |
|-------|-----|--------------|-----|
| WhatsApp | `whatsapp` | `https://wa.me/50766884938` | Ventas consultivas, demos, servicios |
| Agenda | `agenda` | `agenda.html` | Reuniones comerciales / técnicas |
| Registro | `registro` | Portal del producto EasyTech | Self-service, trial |
| Email | `email` | `mailto:easytechservices25@gmail.com` | Consultas formales, respaldo |
| Próximamente | `proximamente` | — | Sin CTA de conversión; solo interés |

Configuración técnica de la agenda: `assets/js/calendly-config.js`.

---

## Convenciones

### WhatsApp

Siempre incluir `text` prellenado por producto para trazabilidad manual hasta conectar CRM.

Plantilla:

```text
https://wa.me/50766884938?text={mensaje_codificado}
```

### Agenda

Enlace interno preferido: `agenda.html`.

### Registro

Usar el enlace de registro ya publicado en la página de cada plataforma EasyTech (botón primario en `econverso.html`, `easynodeone.html`, etc.). Nueva pestaña con `rel="noopener noreferrer"`.

### Solicitar demo

Combinación estándar: **WhatsApp (primario)** + **Agenda (secundario)**.  
En UI: botón primario + botón ghost “Agendar cita”.

---

## Mapa por producto

### Soluciones

| Producto | CTA primario | CTA secundario | CTA terciario | Página |
|----------|--------------|----------------|---------------|--------|
| **Easy Odoo** | WhatsApp | Agenda | Email | `soluciones.html` → `easy-odoo.html` *(decisión URL)* |
| **Facturación Electrónica Panamá** | WhatsApp | Agenda | Email | `facturacion-electronica.html` *(crear)* |

**WhatsApp sugerido — Easy Odoo:**

```text
Quiero información sobre Easy Odoo (ERP EasyTech)
```

**WhatsApp sugerido — Facturación Electrónica:**

```text
Quiero información sobre Facturación Electrónica Panamá con EasyTech
```

---

### Plataformas

| Producto | CTA primario | CTA secundario | Notas | Página |
|----------|--------------|----------------|-------|--------|
| **Easy Converso** | Registro | WhatsApp · Agenda | En producción | `econverso.html` |
| **EasyNodeOne** | Registro | WhatsApp · Agenda | | `easynodeone.html` |
| **EClassOne** | Solicitar demo | WhatsApp · Agenda | Sin registro público aún | `eclassone.html` *(crear)* |
| **EThesisOne** | Solicitar demo | WhatsApp · Agenda | | `ethesisone.html` *(crear)* |
| **EPOSOne** | Solicitar demo | WhatsApp · Agenda | | `eposone.html` *(crear)* |
| **EPayRoll** | Próximamente | Email *(opcional)* | Sin conversión activa | `epayroll.html` *(crear)* |

**Registro:** tomar el href del CTA principal de la página del producto (no duplicar URLs en este documento).

**WhatsApp sugerido — Solicitar demo (EClassOne, EThesisOne, EPOSOne):**

```text
Quiero una demo de {nombre_producto} — EasyTech
```

---

### Servicios profesionales

| Servicio | CTA primario | CTA secundario | Página |
|----------|--------------|----------------|--------|
| **Desarrollo de Software** | WhatsApp | Agenda · Email | `desarrollo-software.html` *(crear)* |
| **Consultoría TI** | WhatsApp | Agenda · Email | `consultoria-ti.html` *(crear)* |

**WhatsApp sugerido — Desarrollo:**

```text
Consulta sobre desarrollo de software con EasyTech
```

**WhatsApp sugerido — Consultoría:**

```text
Consulta sobre consultoría TI con EasyTech
```

---

## Mapa por página transversal

| Página | CTAs |
|--------|------|
| `index.html` | Ecosistema EasyTech → categorías; CTA global: Agenda + WhatsApp genérico |
| `contacto.html` | WhatsApp · Agenda · Email · Registro (Easy Converso · EasyNodeOne) |
| `agenda.html` | Agenda en línea · Email · WhatsApp (fallback) |

**WhatsApp genérico (landing / footer):**

```text
Hola EasyTech
```

---

## Matriz resumida (vista rápida)

```text
Easy Odoo               → WhatsApp → Agenda → Email
Facturación Electrónica → WhatsApp → Agenda → Email
Easy Converso           → Registro → WhatsApp → Agenda
EasyNodeOne             → Registro → WhatsApp → Agenda
EClassOne               → Solicitar demo (WhatsApp + Agenda)
EThesisOne              → Solicitar demo (WhatsApp + Agenda)
EPOSOne                 → Solicitar demo (WhatsApp + Agenda)
EPayRoll                → Próximamente
Desarrollo de Software  → WhatsApp → Agenda
Consultoría TI          → WhatsApp → Agenda
```

---

## Estado actual vs objetivo

| Producto EasyTech | CTA hoy en sitio | Brecha |
|-------------------|------------------|--------|
| Easy Odoo | WhatsApp + Agenda en `soluciones.html` | OK parcial; falta página Facturación |
| Easy Converso | Registro + contacto | OK; unificar nombre “Easy Converso” |
| EasyNodeOne | Registro + login | OK; hero landing apunta solo a EasyNodeOne |
| EClassOne–EPayRoll | — | Sin página |
| Facturación Electr. | — | **Prioridad 2, sin presencia** |
| Landing `index.html` | Registro EasyNodeOne en hero | Desalineado con ecosistema; falta `#cta` global |

---

## Reglas de implementación (Sprint 3–6)

1. Cada página de producto tiene **mínimo un CTA primario** según esta tabla.  
2. Servicios y soluciones consultivas: **WhatsApp primero**, agenda segundo.  
3. Plataformas con trial: **Registro primero**, WhatsApp para implementación con EasyTech.  
4. EPayRoll: badge “Próximamente”; opcional enlace email “Avísame cuando esté disponible”.  
5. No agregar `<form>` HTML hasta nueva decisión explícita.  
6. Todos los `wa.me` deben usar mensaje prellenado distinto por producto.  
7. CRM: fase posterior; este mapa es la fuente de verdad hasta entonces.

---

## Fase posterior — CRM (fuera de alcance actual)

Cuando se conecte CRM interno EasyTech, este documento se extiende con:

- Campo `utm_campaign` / `product_slug` por enlace  
- Webhook de agenda → CRM  
- Lead capture vía Easy Converso  
- Formulario embebido en ERP EasyTech *(si se aprueba)*

No implementar en sprints 1–6.
