import { useMemo } from "react";
import FeedbackCard from "./FeedbackCard";
import EmptyState from "../../components/ui/EmptyState";

export default function FeedbacksList({
  feedbacks = [],
  colaboradores = [],
  currentUser,
  showColaboradorName = false,
}) {
  const colaboradorMap = useMemo(() => {
    const map = {};
    colaboradores.forEach((colab) => {
      map[colab.id] = colab.nome;
    });
    return map;
  }, [colaboradores]);

  if (feedbacks.length === 0) {
    return (
      <EmptyState
        title="Sem feedbacks"
        message="Não há feedbacks registrados para este colaborador."
      />
    );
  }

  return (
    <div className="space-y-4">
      {/* Note about backend limitations */}
      <div className="bg-indigo-600/15 border border-indigo-500/20 rounded-xl p-3 text-xs text-indigo-300">
        Nota: Exibindo os feedbacks mais recentes do colaborador (limitação de até 5 registros do histórico de evolução no backend).
      </div>

      <div className="grid grid-cols-1 gap-4">
        {feedbacks.map((f) => (
          <FeedbackCard
            key={f.id || `feedback-${f.data_feedback || f.criado_em}`}
            feedback={f}
            currentUser={currentUser}
            colaboradorNome={
              showColaboradorName
                ? colaboradorMap[f.colaborador_id] || `Colaborador #${f.colaborador_id}`
                : ""
            }
          />
        ))}
      </div>
    </div>
  );
}
