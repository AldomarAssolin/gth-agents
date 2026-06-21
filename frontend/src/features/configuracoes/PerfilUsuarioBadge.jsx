import Badge from "../../components/ui/Badge";

export default function PerfilUsuarioBadge({ perfil }) {
  const mapping = {
    ADMIN: { variant: "danger", label: "Admin" },
    RH: { variant: "success", label: "RH" },
    LIDER: { variant: "warning", label: "Líder" },
    COLABORADOR: { variant: "secondary", label: "Colaborador" },
  };

  const item = mapping[perfil] || { variant: "info", label: perfil || "N/A" };

  return <Badge variant={item.variant}>{item.label}</Badge>;
}
