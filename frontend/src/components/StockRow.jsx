// frontend/src/components/StockRow.jsx
import ScoreBadge from './ScoreBadge';

export default function StockRow({ data }) {
  const formatRp = (num) => "Rp " + num.toLocaleString('id-ID');
  
  const isPositive = data.price_change_pct > 0;
  const isNegative = data.price_change_pct < 0;
  const pctColor = isPositive ? "text-green-600" : isNegative ? "text-red-600" : "text-gray-900";
  const pctSign = isPositive ? "+" : "";

  // Logika Evaluasi Winrate
  const hasOutcome = data.outcome !== undefined;
  const isWin = data.outcome === "WIN";

  return (
    <tr className="border-b hover:bg-gray-50 transition-colors">
      <td className="p-3 font-bold uppercase text-gray-900">{data.ticker_display}</td>
      <td className="p-3 text-gray-800">{formatRp(data.price_close)}</td>
      <td className={`p-3 font-medium ${pctColor}`}>
        {pctSign}{data.price_change_pct}%
      </td>
      <td className="p-3">
        <ScoreBadge score={data.score} />
      </td>
      <td className="p-3 hidden md:table-cell text-gray-600">{data.rsi_14}</td>
      <td className="p-3 hidden md:table-cell text-gray-600">{data.volume_ratio}&times;</td>
      
      <td className="p-3">
        <div className="flex flex-col items-start gap-1">
          <span className="font-medium text-sm text-gray-700">{data.signal}</span>
          
          {/* Label Evaluasi Historis */}
          {hasOutcome && (
            <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${
              isWin ? 'bg-green-100 text-green-700 border border-green-200' : 'bg-red-100 text-red-700 border border-red-200'
            }`}>
              {isWin ? '✅ WIN' : '❌ LOSS'} ({data.actual_gain_pct > 0 ? '+' : ''}{data.actual_gain_pct}%)
            </span>
          )}
        </div>
      </td>
    </tr>
  );
}