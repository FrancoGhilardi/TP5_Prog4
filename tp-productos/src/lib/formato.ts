const formateadorARS = new Intl.NumberFormat("es-AR", {
  style: "currency",
  currency: "ARS",
});

export function formatearPrecio(precio: number): string {
  return formateadorARS.format(precio);
}
