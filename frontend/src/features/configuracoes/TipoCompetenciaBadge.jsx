import Badge from "../../components/ui/Badge";

export default function TipoCompetenciaBadge({ tipo }) {
  const mapping = {
    TECNICA: { variant: "info", label: "Técnica" },
    COMPORTAMENTAL: { variant: "success", label: "Comportamental" },
    LIDERANCA: { variant: "warning", label: "Liderança" },
    ORGANIZACIONAL: { variant: "secondary", label: "Organizacional" },
  };

  const item = mapping[tipo] || { variant: "info", label: tipo || "N/A" };

  return <Badge variant={item.variant}>{item.label}</Badge>;
}
