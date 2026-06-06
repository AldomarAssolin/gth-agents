export default function Table({ headers = [], children, className = "" }) {
  return (
    <div className={`bg-slate-800 rounded-xl border border-slate-700 shadow-md overflow-x-auto ${className}`}>
      <table className="w-full text-left border-collapse min-w-full">
        <thead>
          <tr className="bg-slate-700/50 border-b border-slate-700 text-slate-300 text-sm font-semibold">
            {headers.map((header, idx) => (
              <th key={idx} className="px-6 py-4">
                {header}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-slate-700 text-slate-200">
          {children}
        </tbody>
      </table>
    </div>
  );
}
