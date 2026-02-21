// frontend/src/components/StatusBar.jsx

export default function StatusBar({ metadata }) {
  if (!metadata) return null;

  // Indikator warna dot berdasarkan status
  const dotColor = 
    metadata.status === 'ok' ? 'bg-green-500' : 
    metadata.status === 'partial' ? 'bg-yellow-500' : 'bg-red-500';

  // Format waktu dari ISO ke WIB
  const formatTime = (isoString) => {
    if (!isoString) return '--:--';
    const date = new Date(isoString);
    // Kita ambil jam dan menit saja
    return date.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', timeZone: 'Asia/Jakarta' });
  };

  return (
    <div className="flex items-center text-xs md:text-sm text-gray-500 bg-white px-3 py-1.5 rounded-full border border-gray-200 shadow-sm">
      <span className={`w-2 h-2 rounded-full ${dotColor} mr-2 animate-pulse`}></span>
      <span>Update terakhir: <span className="font-semibold">{formatTime(metadata.generated_at)} WIB</span> &bull; &#10227; auto-refresh 5m</span>
    </div>
  );
}