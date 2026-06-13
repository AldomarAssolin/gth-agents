import Badge from "../../components/ui/Badge";
import { traduzirStatusPDI } from "./pdisFormatters";

export default function StatusPDIBadge({ status }) {
  const statusMap = {
    RASCUNHO: {
      label: traduzirStatusPDI("RASCUNHO"),
      variant: "secondary",
    },
    ATIVO: {
      label: traduzirStatusPDI("ATIVO"),
      variant: "info",
    },
    CONCLUIDO: {
      label: traduzirStatusPDI("CONCLUIDO"),
      variant: "success",
    },
    CANCELADO: {
      label: traduzirStatusPDI("CANCELADO"),
      variant: "danger",
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
