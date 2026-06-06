import { api } from "../../services/api";

export async function getDashboardMVP() {
  const response = await api.get("/dashboard/mvp");
  return response.data;
}
