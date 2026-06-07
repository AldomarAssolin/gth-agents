import Badge from "../../components/ui/Badge";

export default function StatusMetaBadge({ status }) {
  const statusMap = {
    PENDENTE: {
      label: "Pendente",
      variant: "info",
    },
    EM_ANDAMENTO: {
      label: "Em andamento",
      variant: "warning",
    },
    CONCLUIDA: {
      label: "Concluída",
      variant: "success",
    },
    ATRASADA: {
      label: "Atrasada",
      variant: "danger",
    },
    CANCELADA: {
      label: "Cancelada",
      variant: "secondary",
    },
  };

  const config = statusMap[status] ?? {
    label: status ? String(status) : "Status não informado",
    variant: "secondary",
  };

  return (
    <Badge variant={config.variant}>
      {config.label}
    </Badge>
  );
}
