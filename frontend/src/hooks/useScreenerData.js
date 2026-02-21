// frontend/src/hooks/useScreenerData.js

import { useState, useEffect, useCallback } from 'react';
import { CONFIG } from '../config';

export function useScreenerData() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastFetch, setLastFetch] = useState(null);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      // Tambahkan timestamp untuk mencegah browser men-cache file JSON lama
      const response = await fetch(`${CONFIG.DATA_URL}?t=${new Date().getTime()}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const jsonData = await response.json();
      setData(jsonData);
      setLastFetch(new Date());
    } catch (err) {
      console.error("Gagal menarik data:", err);
      setError("Gagal memuat data, mencoba lagi...");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Tarik data pertama kali saat web dibuka
    fetchData();

    // Set polling setiap 5 menit sesuai config
    const intervalId = setInterval(fetchData, CONFIG.REFRESH_INTERVAL);

    // Bersihkan interval saat komponen ditutup
    return () => clearInterval(intervalId);
  }, [fetchData]);

  return { data, loading, error, lastFetch, refetch: fetchData };
}