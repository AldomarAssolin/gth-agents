import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import PageHeader from "../components/layout/PageHeader";
import Badge from "../components/ui/Badge";
import Card from "../components/ui/Card";
import EmptyState from "../components/ui/EmptyState";
import { buscarColaboradorPorId } from "../features/colaboradores/colaboradoresService";

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

export default function EvolucaoColaboradorPage() {
  const { id } = useParams();
  const [nomeColaborador, setNomeColaborador] = useState("Carregando...");
  const evolucoes = mockEvolucoes[id] || [];

  useEffect(() => {
    const controller = new AbortController();

    async function fetchName() {
      try {
        const colab = await buscarColaboradorPorId(id, { signal: controller.signal });
        setNomeColaborador(colab.nome);
      } catch (err) {
        if (err.code !== "ERR_CANCELED" && err.name !== "CanceledError") {
          setNomeColaborador("Não encontrado");
        }
      }
    }

    fetchName();

    return () => {
      controller.abort();
    };
  }, [id]);


  return (
    <div className="space-y-6">
      <div className="flex items-center">
        <Link
          to={`/colaboradores/${id}`}
          className="text-slate-400 hover:text-white transition-colors text-sm font-semibold flex items-center space-x-1.5"
        >
          <span>&larr; Voltar para Detalhes</span>
        </Link>
      </div>

      <PageHeader
        title="Histórico de Evolução"
        description={`Registro de feedforwards, feedbacks e avaliações de ${nomeColaborador}`}
      />

      <div className="space-y-4">
        {evolucoes.length === 0 ? (
          <EmptyState
            title="Nenhum registro de evolução"
            message="Não há avaliações ou feedbacks registrados para este colaborador até o momento."
          />
        ) : (
          evolucoes.map((evolucao, index) => (
            <Card
              key={index}
              className="flex flex-col md:flex-row justify-between items-start md:items-center space-y-4 md:space-y-0"
            >
              <div className="space-y-2">
                <div className="flex items-center space-x-3">
                  <Badge variant="info">
                    {evolucao.tipo}
                  </Badge>
                  <span className="text-sm text-slate-400">{evolucao.data}</span>
                </div>
                <p className="text-slate-300 text-sm leading-relaxed">{evolucao.anotacao}</p>
              </div>
              <div className="text-right shrink-0">
                <span className="text-xs text-slate-500 block font-semibold uppercase tracking-wider">Nota / Score</span>
                <span className="text-lg font-bold text-emerald-400">{evolucao.score}</span>
              </div>
            </Card>
          ))
        )}
      </div>
    </div>
  );
}
