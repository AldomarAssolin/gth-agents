import Card from "../../components/ui/Card";
import Badge from "../../components/ui/Badge";
import { formatarDataBrasil } from "./evolucaoFormatters";

export default function DadosColaboradorCard({ colaborador }) {
  if (!colaborador) return null;

  const initials = colaborador.nome
    ? colaborador.nome
        .split(" ")
        .map((n) => n[0])
        .join("")
        .slice(0, 2)
        .toUpperCase()
    : "??";

  const getStatusVariant = (status) => {
    return status === "ATIVO" ? "success" : "danger";
  };

  return (
    <Card className="relative overflow-hidden bg-slate-900 border-slate-800">
      <div className="absolute top-0 right-0 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl pointer-events-none"></div>
      <div className="flex flex-col md:flex-row items-center md:items-start gap-5">
        <div className="flex items-center justify-center w-20 h-20 rounded-2xl bg-gradient-to-br from-indigo-500 to-violet-600 text-white font-bold text-2xl shadow-lg shadow-indigo-500/10 shrink-0">
          {initials}
        </div>
        <div className="flex-1 text-center md:text-left min-w-0">
          <div className="flex flex-col md:flex-row md:items-center gap-3">
            <h2 className="text-xl md:text-2xl font-bold text-white tracking-tight truncate">
              {colaborador.nome}
            </h2>
            <div className="inline-flex justify-center md:justify-start">
              <Badge variant={getStatusVariant(colaborador.status)}>
                {colaborador.status || "INATIVO"}
              </Badge>
            </div>
          </div>
          <p className="text-slate-400 text-sm mt-1 truncate">{colaborador.email}</p>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
            <div className="p-3 bg-slate-800/40 border border-slate-800 rounded-xl">
              <span className="block text-[11px] text-slate-500 font-semibold uppercase tracking-wider">Matrícula</span>
              <span className="block text-sm font-medium text-slate-200 mt-0.5">{colaborador.matricula || "Não informada"}</span>
            </div>
            <div className="p-3 bg-slate-800/40 border border-slate-800 rounded-xl">
              <span className="block text-[11px] text-slate-500 font-semibold uppercase tracking-wider">Admissão</span>
              <span className="block text-sm font-medium text-slate-200 mt-0.5">{formatarDataBrasil(colaborador.data_admissao)}</span>
            </div>
            <div className="p-3 bg-slate-800/40 border border-slate-800 rounded-xl">
              <span className="block text-[11px] text-slate-500 font-semibold uppercase tracking-wider">Setor</span>
              <span className="block text-sm font-medium text-slate-200 mt-0.5">
                {colaborador.setor_id ? `Setor: ID ${colaborador.setor_id}` : "Não informado"}
              </span>
            </div>
            <div className="p-3 bg-slate-800/40 border border-slate-800 rounded-xl">
              <span className="block text-[11px] text-slate-500 font-semibold uppercase tracking-wider">Função</span>
              <span className="block text-sm font-medium text-slate-200 mt-0.5">
                {colaborador.funcao_id ? `Função: ID ${colaborador.funcao_id}` : "Não informada"}
              </span>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
}
