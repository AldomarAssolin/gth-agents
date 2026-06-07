import Badge from "../../components/ui/Badge";

export default function PrioridadeMetaBadge({ prioridade }) {
  const prioridadeMap = {
    BAIXA: {
      label: "Baixa",
      variant: "secondary",
    },
    MEDIA: {
      label: "Média",
      variant: "info",
    },
    ALTA: {
      label: "Alta",
      variant: "warning",
    },
    CRITICA: {
      label: "Crítica",
      variant: "danger",
    },
  };

  const config = prioridadeMap[prioridade] ?? {
    label: prioridade ? String(prioridade) : "Não informada",
    variant: "secondary",
  };

  return (
    <Badge variant={config.variant}>
      {config.label}
    </Badge>
  );
}
