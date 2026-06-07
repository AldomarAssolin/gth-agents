export default function ItemAvaliacaoForm({
  competencia,
  checked,
  onCheckChange,
  nota,
  onNotaChange,
  comentario,
  onComentarioChange,
  error
}) {
  const notaOptions = [
    { value: "", label: "Selecione a nota" },
    { value: "1", label: "1 - Muito abaixo do esperado" },
    { value: "2", label: "2 - Abaixo do esperado" },
    { value: "3", label: "3 - Adequado" },
    { value: "4", label: "4 - Acima do esperado" },
    { value: "5", label: "5 - Excelente" }
  ];

  return (
    <div className={`p-4 rounded-xl transition-all border ${
      checked ? "bg-slate-800/60 border-indigo-500/30" : "bg-slate-800/20 border-slate-700/50"
    }`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <input
            type="checkbox"
            id={`eval-${competencia.id}`}
            checked={checked}
            onChange={(e) => onCheckChange(e.target.checked)}
            className="mt-1 h-4 w-4 rounded border-slate-600 bg-slate-700 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
          />
          <div className="space-y-0.5">
            <label htmlFor={`eval-${competencia.id}`} className="font-semibold text-slate-100 cursor-pointer">
              {competencia.nome}
            </label>
            <div className="flex flex-wrap gap-2 text-xs font-medium mt-1">
              <span className="px-2 py-0.5 rounded-full bg-slate-700 text-slate-300">
                {competencia.tipo}
              </span>
              {competencia.peso !== undefined && (
                <span className="px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400">
                  Peso: {parseFloat(competencia.peso).toFixed(2)}
                </span>
              )}
            </div>
            {competencia.descricao && (
              <p className="text-slate-400 text-xs mt-2 leading-relaxed">
                {competencia.descricao}
              </p>
            )}
          </div>
        </div>
      </div>

      {checked && (
        <div className="mt-4 pt-4 border-t border-slate-700/50 grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor={`nota-${competencia.id}`} className="block text-xs font-semibold text-slate-300 mb-1.5">
              Nota <span className="text-red-400">*</span>
            </label>
            <select
              id={`nota-${competencia.id}`}
              value={nota}
              onChange={(e) => onNotaChange(e.target.value)}
              className={`w-full px-3 py-2 bg-slate-700 border rounded-lg text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all ${
                error?.nota ? "border-red-500 focus:ring-red-500" : "border-slate-600"
              }`}
            >
              {notaOptions.map((opt) => (
                <option key={opt.value} value={opt.value} className="bg-slate-800 text-slate-100">
                  {opt.label}
                </option>
              ))}
            </select>
            {error?.nota && <p className="text-xs text-red-400 mt-1">{error.nota}</p>}
          </div>

          <div>
            <label htmlFor={`comentario-${competencia.id}`} className="block text-xs font-semibold text-slate-300 mb-1.5">
              Comentário (opcional)
            </label>
            <input
              type="text"
              id={`comentario-${competencia.id}`}
              value={comentario}
              onChange={(e) => onComentarioChange(e.target.value)}
              placeholder="Ex: Demonstra domínio técnico no dia a dia."
              className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
            />
          </div>
        </div>
      )}
    </div>
  );
}
