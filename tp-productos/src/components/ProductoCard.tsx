import type { Producto } from "../types/producto";
import { formatearPrecio } from "../lib/formato";
import { estiloPanel } from "../lib/estilos";

interface ProductoCardProps {
  producto: Producto;
}

export const ProductoCard = ({ producto }: ProductoCardProps) => {
  return (
    <article className={`flex flex-col transition hover:shadow-md ${estiloPanel}`}>
      <h3 className="text-base font-semibold text-texto">{producto.nombre}</h3>
      <p className="mt-2 flex-1 text-sm leading-relaxed text-texto-suave">
        {producto.descripcion}
      </p>
      <p className="mt-4 text-xl font-bold text-marca-700">
        {formatearPrecio(producto.precio)}
      </p>
    </article>
  );
};
