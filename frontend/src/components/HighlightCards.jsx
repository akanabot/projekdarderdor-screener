// frontend/src/components/HighlightCards.jsx

export default function HighlightCards({ dayData }) {
  if (!dayData || !dayData.results || dayData.results.length === 0) return null;

  // 1. Logika Top Pick (Ambil saham skor tertinggi)
  const topPick = dayData.results.reduce((max, stock) => max.score > stock.score ? max : stock);
  
  // Kalkulasi Trading Plan BSJP (Format Rupiah pembulatan)
  const buyPrice = topPick.price_close;
  const tpPrice = Math.round(buyPrice * 1.015); // Target +1.5%
  const clPrice = Math.round(buyPrice * 0.985); // Cutloss -1.5%
  const formatRp = (num) => "Rp " + num.toLocaleString('id-ID');

  // 2. Logika Market Sentiment
  const totalPassed = dayData.results.length;
  let sentimentStr = "NORMAL";
  let sentimentColor = "text-blue-600 bg-blue-50 border-blue-200";
  let sentimentDesc = "Peluang BSJP cukup berimbang. Tetap disiplin.";

  if (totalPassed >= 10) {
    sentimentStr = "BULLISH / OPTIMIS";
    sentimentColor = "text-green-600 bg-green-50 border-green-200";
    sentimentDesc = "Banyak saham potensial. Kondisi pasar mendukung.";
  } else if (totalPassed <= 3) {
    sentimentStr = "BEARISH / WAIT & SEE";
    sentimentColor = "text-red-600 bg-red-50 border-red-200";
    sentimentDesc = "Sangat sedikit yang lolos. Kurangi porsi modal / hindari entry.";
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
      
      {/* CARD 1: TOP PICK TRADING PLAN */}
      <div className="bg-white p-5 rounded-lg shadow-sm border border-gray-200 flex flex-col justify-between">
        <div>
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Top Pick Hari Ini</h3>
            <span className="bg-indigo-100 text-indigo-800 text-[10px] font-bold px-2 py-0.5 rounded">SKOR: {topPick.score}</span>
          </div>
          <div className="flex items-end gap-3 mb-4">
            <h2 className="text-3xl font-black text-gray-900 uppercase">{topPick.ticker_display}</h2>
            <p className="text-sm font-medium text-gray-500 mb-1">{topPick.signal}</p>
          </div>
        </div>
        
        <div className="grid grid-cols-3 gap-2 bg-gray-50 p-3 rounded border border-gray-100">
          <div>
            <p className="text-[10px] text-gray-500 font-bold uppercase">Beli (Close)</p>
            <p className="text-sm font-bold text-gray-800">{formatRp(buyPrice)}</p>
          </div>
          <div>
            <p className="text-[10px] text-green-600 font-bold uppercase">Take Profit</p>
            <p className="text-sm font-bold text-green-700">{formatRp(tpPrice)}</p>
          </div>
          <div>
            <p className="text-[10px] text-red-500 font-bold uppercase">Cutloss</p>
            <p className="text-sm font-bold text-red-600">{formatRp(clPrice)}</p>
          </div>
        </div>
      </div>

      {/* CARD 2: MARKET SENTIMENT */}
      <div className={`p-5 rounded-lg shadow-sm border flex flex-col justify-between ${sentimentColor}`}>
        <div>
          <div className="flex justify-between items-start mb-2">
            <h3 className="text-xs font-bold uppercase tracking-wider opacity-80">Market Sentiment</h3>
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-white bg-opacity-50">
              {totalPassed} Saham Lolos
            </span>
          </div>
          <h2 className="text-2xl font-black uppercase mt-1 mb-2">{sentimentStr}</h2>
        </div>
        <p className="text-sm font-medium opacity-90">
          {sentimentDesc}
        </p>
      </div>

    </div>
  );
}