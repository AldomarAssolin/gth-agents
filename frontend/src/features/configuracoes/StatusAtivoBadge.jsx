import Badge from "../../components/ui/Badge";

export default function StatusAtivoBadge({ ativo }) {
  return (
    <Badge variant={ativo ? "success" : "secondary"}>
      {ativo ? "Ativo" : "Inativo"}
    </Badge>
  );
}
