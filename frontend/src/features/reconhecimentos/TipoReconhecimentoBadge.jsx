import Badge from "../../components/ui/Badge";
import { traduzirTipoReconhecimento } from "./reconhecimentosFormatters";

export default function TipoReconhecimentoBadge({ tipo, className = "" }) {
  const getVariant = (tipoValue) => {
    switch (tipoValue) {
      case "DESTAQUE":
        return "info";
      case "META_ATINGIDA":
        return "success";
      case "EVOLUCAO_TECNICA":
        return "info";
      case "COMPORTAMENTO_POSITIVO":
        return "success";
      case "CONCLUSAO_TREINAMENTO":
        return "info";
      case "CONCLUSAO_PDI":
        return "info";
      case "REDUCAO_RETRABALHO":
        return "warning";
      case "APOIO_EQUIPE":
        return "success";
      case "POTENCIAL_LIDERANCA":
        return "warning";
      case "OUTRO":
      default:
        return "secondary";
    }
  };

  return (
    <Badge variant={getVariant(tipo)} className={className}>
      {traduzirTipoReconhecimento(tipo)}
    </Badge>
  );
}
