// frontend/src/App.jsx
import { useState, useMemo, useEffect } from 'react';
import { useScreenerData } from './hooks/useScreenerData';
import StatusBar from './components/StatusBar';
import FilterBar from './components/FilterBar';
import WinRateCard from './components/WinRateCard';
import HighlightCards from './components/HighlightCards';
import ScreenerTable from './components/ScreenerTable';
import { CONFIG } from './config';

function App() {
  const { data, loading, error } = useScreenerData();
  const [filter, setFilter] = useState('ALL');
  const [sort, setSort] = useState('score_desc');
  const [selectedDate, setSelectedDate] = useState('');

  // Ekstrak daftar tanggal dari histori (di-reverse agar yang terbaru di atas)
  const availableDates = useMemo(() => {
    if (!data?.history) return [];
    return [...data.history].map(h => h.date).reverse();
  }, [data]);

  // Otomatis pilih tanggal paling baru saat data dimuat
  useEffect(() => {
    if (availableDates.length > 0 && !selectedDate) {
      setSelectedDate(availableDates[0]);
    }
  }, [availableDates, selectedDate]);

  // Ambil data untuk tanggal yang sedang dipilih
  const currentDayData = useMemo(() => {
    if (!data?.history || !selectedDate) return null;
    return data.history.find(h => h.date === selectedDate);
  }, [data, selectedDate]);

  // Status Data
  const metadata = currentDayData?.metadata;
  
  const isStaleData = useMemo(() => {
    if (!metadata?.generated_at) return false;
    // Jika melihat data histori (bukan hari ini), jangan anggap stale
    const today = new Date().toLocaleDateString('en-CA');
    if (selectedDate !== today) return false;

    const generatedTime = new Date(metadata.generated_at).getTime();
    const now = new Date().getTime();
    const hoursDiff = (now - generatedTime) / (1000 * 60 * 60);
    return hoursDiff > 4;
  }, [metadata, selectedDate]);

  // Logika Filter & Sort
  const processedStocks = useMemo(() => {
    if (!currentDayData?.results) return [];
    
    let filtered = currentDayData.results;
    if (filter === 'STRONG') {
      filtered = filtered.filter(s => s.score >= CONFIG.SCORE_STRONG);
    } else if (filter === 'MODERATE') {
      filtered = filtered.filter(s => s.score >= CONFIG.SCORE_MODERATE);
    }

    return [...filtered].sort((a, b) => {
      switch (sort) {
        case 'score_asc': return a.score - b.score;
        case 'score_desc': return b.score - a.score;
        case 'change_desc': return b.price_change_pct - a.price_change_pct;
        case 'ticker_asc': return a.ticker_display.localeCompare(b.ticker_display);
        default: return b.score - a.score;
      }
    });
  }, [currentDayData, filter, sort]);

  return (
    <div className="min-h-screen bg-gray-50 pb-12">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 pt-8">
        
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6 gap-4">
          <div>
            <h1 className="text-2xl font-extrabold text-gray-900 tracking-tight">IHSG Overnight Screener</h1>
            <p className="text-sm text-gray-500 mt-1">Strategi: Beli Sore | Jual Pagi</p>
          </div>
          <StatusBar metadata={metadata} />
        </div>

        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 mb-6 rounded shadow-sm">
            <p className="text-red-700">{error}</p>
          </div>
        )}
        
        {!error && metadata?.status === 'error' && (
          <div className="bg-yellow-50 border-l-4 border-yellow-500 p-4 mb-6 rounded shadow-sm">
            <p className="text-yellow-700 font-medium">⚠️ Data mungkin tidak terbaru (Gagal fetch bursa).</p>
          </div>
        )}

        {!error && isStaleData && (
          <div className="bg-orange-50 border-l-4 border-orange-500 p-4 mb-6 rounded shadow-sm">
            <p className="text-orange-700 font-medium">🕒 Data belum diperbarui hari ini. Screener berjalan otomatis tiap 14:30 WIB.</p>
          </div>
        )}

        {loading && !data ? (
          <div className="flex justify-center items-center h-48">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          </div>
        ) : (
          <>
            <FilterBar 
              currentFilter={filter} 
              setFilter={setFilter} 
              currentSort={sort} 
              setSort={setSort}
              availableDates={availableDates}
              selectedDate={selectedDate}
              setSelectedDate={setSelectedDate}
            />
            <WinRateCard dayData={currentDayData} />
            <HighlightCards dayData={currentDayData} />
            <ScreenerTable stocks={processedStocks} />
          </>
        )}

      </div>
    </div>
  );
}

export default App;