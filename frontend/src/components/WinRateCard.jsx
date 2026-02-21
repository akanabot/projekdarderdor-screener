// frontend/src/components/WinRateCard.jsx

export default function WinRateCard({ dayData }) {
  // Jika tidak ada data, jangan tampilkan apa-apa
  if (!dayData || !dayData.results) return null;

  // Filter hanya saham yang sudah dievaluasi (memiliki label WIN/LOSS)
  const evaluatedStocks = dayData.results.filter(stock => stock.outcome);
  const totalEvaluated = evaluatedStocks.length;

  // Jika belum ada yang dievaluasi (misal data hari ini yang bursa esoknya belum buka)
  if (totalEvaluated === 0) return null;

  // Hitung statistik
  const wins = evaluatedStocks.filter(stock => stock.outcome === 'WIN').length;
  const losses = evaluatedStocks.filter(stock => stock.outcome === 'LOSS').length;
  const winRate = Math.round((wins / totalEvaluated) * 100);

  // Ganti warna dinamis berdasarkan performa
  const rateColor = 
    winRate >= 60 ? 'text-green-600' : 
    winRate >= 40 ? 'text-yellow-600' : 'text-red-600';

  return (
    <div className="bg-white p-5 rounded-lg shadow-sm border border-gray-200 mb-4 flex flex-col md:flex-row items-center justify-between gap-4">
      <div className="text-center md:text-left">
        <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider">
          Performa Sinyal ({dayData.date})
        </h3>
        <p className="text-xs text-gray-400 mt-1">
          Target: Hit profit minimal 1% pagi harinya
        </p>
      </div>
      
      <div className="flex gap-8 items-center bg-gray-50 px-6 py-3 rounded-lg border border-gray-100">
        <div className="text-center">
          <p className="text-[11px] text-gray-500 font-bold uppercase mb-1">Win Rate</p>
          <p className={`text-3xl font-black ${rateColor}`}>{winRate}%</p>
        </div>
        
        <div className="w-px h-10 bg-gray-200"></div> {/* Garis pemisah */}
        
        <div className="text-center">
          <p className="text-[11px] text-gray-500 font-bold uppercase mb-1">WIN ✅</p>
          <p className="text-2xl font-bold text-green-700">{wins}</p>
        </div>
        
        <div className="w-px h-10 bg-gray-200"></div> {/* Garis pemisah */}
        
        <div className="text-center">
          <p className="text-[11px] text-gray-500 font-bold uppercase mb-1">LOSS ❌</p>
          <p className="text-2xl font-bold text-red-700">{losses}</p>
        </div>
      </div>
    </div>
  );
}