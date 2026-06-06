export default function EmptyState({ title = "Nenhum resultado encontrado", message = "Tente ajustar sua busca ou adicione um novo registro.", className = "" }) {
  return (
    <div className={`flex flex-col items-center justify-center p-8 bg-slate-800/50 border border-dashed border-slate-700 rounded-xl text-center space-y-3 ${className}`}>
      <svg
        className="h-10 w-10 text-slate-500"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
        stroke="currentColor"
      >
        <path
          strokeLinecap="round"
          strokeLinejoin="round"
          strokeWidth="1.5"
          d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
      <div>
        <h4 className="font-semibold text-slate-300 text-sm">{title}</h4>
        {message && <p className="text-slate-400 text-xs mt-1">{message}</p>}
      </div>
    </div>
  );
}
