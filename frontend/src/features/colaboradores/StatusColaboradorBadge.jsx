import Badge from "../../components/ui/Badge";

export default function StatusColaboradorBadge({ status }) {
  const statusMap = {
    ATIVO: {
      label: "Ativo",
      variant: "success",
    },
    INATIVO: {
      label: "Inativo",
      variant: "secondary",
    },
    AFASTADO: {
      label: "Afastado",
      variant: "warning",
    },
    DESLIGADO: {
      label: "Desligado",
      variant: "danger",
    },
  };

  const config = statusMap[status] ?? {
    label: status || "Não informado",
    variant: "secondary",
  };

  return (
    <Badge variant={config.variant}>
      {config.label}
    </Badge>
  );
}
