import type { Producto } from "../types/producto";
import { ProductoCard } from "./ProductoCard";

interface ProductoListProps {
  productos: Producto[];
}

export const ProductoList = ({ productos }: ProductoListProps) => {
  if (productos.length === 0) {
    return (
      <p className="rounded-xl border border-dashed border-borde p-8 text-center text-sm text-texto-suave">
        No hay productos para mostrar.
      </p>
    );
  }

  return (
    <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {productos.map((producto) => (
        <ProductoCard key={producto.id} producto={producto} />
      ))}
    </section>
  );
};
