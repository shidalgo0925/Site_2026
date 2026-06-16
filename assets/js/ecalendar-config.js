/**
 * ECalendar — configuración frontend (Site_2026).
 * Cuando EN1 esté listo: mockMode = false y apiBase en portal-urls (appdev/appprd).
 */
window.EASYTECH_ECALENDAR_CONFIG = {
  mockMode: false,
  apiBase: "https://appdev.easynodeone.com/api/ecalendar",
  timezone: "America/Panama",
  defaultDurationMinutes: 30,
  durationOptions: [30],
  showUnavailableSlots: false,
  leadTimeHours: 4,
  mockLeadTimeHours: 0,
  horizonDays: 30,
  workingHours: {
    weekdays: ["mon", "tue", "wed", "thu", "fri"],
    start: "09:00",
    end: "17:00",
  },
  whatsappBase: "https://wa.me/50766884938",
};
