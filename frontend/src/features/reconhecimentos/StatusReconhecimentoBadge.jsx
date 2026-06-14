import Badge from "../../components/ui/Badge";

export default function StatusReconhecimentoBadge({ ativo, className = "" }) {
  return (
    <Badge variant={ativo ? "success" : "danger"} className={className}>
      {ativo ? "Ativo" : "Cancelado"}
    </Badge>
  );
}
