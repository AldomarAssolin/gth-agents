import Select from "../../components/ui/Select";

export default function TipoAvaliacaoSelect({ value, onChange, error, label = "Tipo de Avaliação", id = "tipo", ...props }) {
  const options = [
    { value: "", label: "Selecione o tipo de avaliação" },
    { value: "AUTOAVALIACAO", label: "Autoavaliação" },
    { value: "AVALIACAO_LIDER", label: "Avaliação do líder" },
    { value: "AVALIACAO_TECNICA", label: "Avaliação técnica" },
    { value: "AVALIACAO_360", label: "Avaliação 360°" }
  ];

  return (
    <Select
      id={id}
      label={label}
      value={value}
      onChange={onChange}
      options={options}
      error={error}
      {...props}
    />
  );
}
