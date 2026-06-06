import { useParams, Link } from "react-router-dom";
import Layout from "../layouts/Layout";

const mockEvolucoes = {
  1: [
    { data: "2024-05-10", tipo: "Feedforward", score: "4.5 / 5.0", anotacao: "Excelente evolução técnica em arquitetura limpa e testes unitários." },
    { data: "2024-02-15", tipo: "Feedback 360", score: "4.0 / 5.0", anotacao: "Boa comunicação com a equipe e entrega de valor consistente." }
  ],
  2: [
    { data: "2024-04-18", tipo: "Feedforward", score: "4.8 / 5.0", anotacao: "Domínio de React e Tailwind CSS excelente. Iniciando mentoria." }
  ],
  3: []
};

const mockColaboradoresMap = {
  1: "João Silva",
  2: "Maria Santos",
  3: "Pedro Souza",
};

export default function EvolucaoColaboradorPage() {
  const { id } = useParams();
  const nomeColaborador = mockColaboradoresMap[id] || "Não encontrado";
  const evolucoes = mockEvolucoes[id] || [];

  return (
    <Layout>
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <Link
            to={`/colaboradores/${id}`}
            className="text-slate-400 hover:text-white transition-colors"
          >
            &larr; Voltar para Detalhes
          </Link>
        </div>

        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white">Evolução do Colaborador</h1>
          <p className="text-indigo-400 mt-1">Histórico de acompanhamento de {nomeColaborador}</p>
        </div>

        <div className="space-y-4">
          {evolucoes.length === 0 ? (
            <div className="bg-slate-800 rounded-xl border border-slate-700 shadow-md p-6 text-center text-slate-400">
              Nenhum registro de evolução encontrado para este colaborador.
            </div>
          ) : (
            evolucoes.map((evolucao, index) => (
              <div
                key={index}
                className="bg-slate-800 rounded-xl border border-slate-700 shadow-md p-6 flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0"
              >
                <div className="space-y-2">
                  <div className="flex items-center space-x-3">
                    <span className="text-sm text-indigo-400 font-semibold bg-indigo-500/10 px-2.5 py-0.5 rounded-full border border-indigo-500/25">
                      {evolucao.tipo}
                    </span>
                    <span className="text-sm text-slate-400">{evolucao.data}</span>
                  </div>
                  <p className="text-slate-300">{evolucao.anotacao}</p>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400 block font-medium">Nota / Score</span>
                  <span className="text-lg font-bold text-emerald-400">{evolucao.score}</span>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </Layout>
  );
}
