// frontend/src/config.js

export const CONFIG = {
  // Ganti dengan raw URL dari repository Anda!
  // SEBELUMNYA

    DATA_URL: import.meta.env.VITE_DATA_URL || 
    "https://raw.githubusercontent.com/akanabot/projekdarderdor-screener/main/data/result.json",
  
  REFRESH_INTERVAL: 5 * 60 * 1000,   // 5 menit

  // Waktu screening (WIB, untuk info user)
  SCREENING_TIMES: ["14:30", "15:00", "15:30"],

  // Score thresholds
  SCORE_STRONG: 70,
  SCORE_MODERATE: 50,

  // Warna badge
  COLOR_STRONG: "green",
  COLOR_MODERATE: "yellow",
  COLOR_WEAK: "gray",
};