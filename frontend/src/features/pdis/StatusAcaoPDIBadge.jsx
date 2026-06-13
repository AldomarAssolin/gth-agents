import Badge from "../../components/ui/Badge";
import { traduzirStatusAcaoPDI } from "./pdisFormatters";

export default function StatusAcaoPDIBadge({ status }) {
  const statusMap = {
    PENDENTE: {
      label: traduzirStatusAcaoPDI("PENDENTE"),
      variant: "warning",
    },
    EM_ANDAMENTO: {
      label: traduzirStatusAcaoPDI("EM_ANDAMENTO"),
      variant: "info",
    },
    CONCLUIDA: {
      label: traduzirStatusAcaoPDI("CONCLUIDA"),
      variant: "success",
    },
    CANCELADA: {
      label: traduzirStatusAcaoPDI("CANCELADA"),
      variant: "danger",
    },
  };

  const config = statusMap[status] ?? {
    label: status ? String(status) : "Não informado",
    variant: "secondary",
  };

  return (
    <Badge variant={config.variant}>
      {config.label}
    </Badge>
  );
}
