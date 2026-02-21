// frontend/src/components/FilterBar.jsx

export default function FilterBar({ currentFilter, setFilter, currentSort, setSort, availableDates, selectedDate, setSelectedDate }) {
  const filterBtnClass = (isActive) => 
    `px-4 py-2 text-sm font-medium rounded-md transition-colors border ${
      isActive 
        ? "bg-blue-600 text-white border-blue-600 shadow-sm" 
        : "bg-white text-gray-700 border-gray-300 hover:bg-gray-50"
    }`;

  return (
    <div className="flex flex-col mb-4 bg-white p-3 rounded-lg shadow-sm border border-gray-200 gap-4">
      {/* Baris Atas: Pemilih Tanggal Histori */}
      <div className="flex items-center gap-3 pb-3 border-b border-gray-100">
        <label htmlFor="history-date" className="text-sm text-gray-700 font-bold whitespace-nowrap">📅 Histori Screening:</label>
        <select 
          id="history-date"
          value={selectedDate} 
          onChange={(e) => setSelectedDate(e.target.value)}
          className="bg-blue-50 border border-blue-200 text-blue-800 text-sm rounded-md focus:ring-blue-500 focus:border-blue-500 block p-2 w-full sm:w-auto cursor-pointer font-medium"
        >
          {availableDates.map(date => (
            <option key={date} value={date}>{date}</option>
          ))}
          {availableDates.length === 0 && <option value="">Belum ada data</option>}
        </select>
      </div>

      {/* Baris Bawah: Filter & Sort */}
      <div className="flex flex-col sm:flex-row justify-between items-center gap-4">
        <div className="flex gap-2 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
          <button className={filterBtnClass(currentFilter === 'ALL')} onClick={() => setFilter('ALL')}>Semua</button>
          <button className={filterBtnClass(currentFilter === 'STRONG')} onClick={() => setFilter('STRONG')}>Skor ≥70</button>
          <button className={filterBtnClass(currentFilter === 'MODERATE')} onClick={() => setFilter('MODERATE')}>Skor ≥50</button>
        </div>

        <div className="flex items-center gap-2 w-full sm:w-auto">
          <label htmlFor="sort" className="text-sm text-gray-600 font-medium">Sort:</label>
          <select 
            id="sort"
            value={currentSort} 
            onChange={(e) => setSort(e.target.value)}
            className="bg-white border border-gray-300 text-gray-700 text-sm rounded-md focus:ring-blue-500 focus:border-blue-500 block p-2 w-full sm:w-auto cursor-pointer"
          >
            <option value="score_desc">Skor ↓</option>
            <option value="score_asc">Skor ↑</option>
            <option value="change_desc">% Change ↓</option>
            <option value="ticker_asc">Ticker A-Z</option>
          </select>
        </div>
      </div>
    </div>
  );
}