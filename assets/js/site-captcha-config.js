/**
 * CAPTCHA sitio completo — easytech.services
 * Cloudflare Turnstile. Reemplazar siteKey en producción (dashboard Cloudflare).
 * EN1/backend debe validar captcha_token con TURNSTILE_SECRET_KEY.
 */
window.EASYTECH_SITE_CAPTCHA_CONFIG = {
  provider: "turnstile",
  siteKey: "1x00000000000000000000AA",
  required: true,
  theme: "light",
  language: "es",
};
