import { Navbar } from "./components/Navbar";
import { Footer } from "./components/Footer";
import { ProductoForm } from "./components/ProductoForm";
import { ProductoList } from "./components/ProductoList";
import { productos } from "./data/productos";

export const App = () => {
  return (
    <div className="flex min-h-screen flex-col bg-fondo text-texto">
      <Navbar titulo="Gestor de Productos" />

      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">
        <h1 className="text-2xl font-bold tracking-tight">
          Catálogo de productos
        </h1>
        <p className="mt-1 text-sm text-texto-suave">
          {productos.length} productos en el catálogo
        </p>

        <div className="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-[1fr_20rem]">
          <ProductoList productos={productos} />
          <aside>
            <ProductoForm />
          </aside>
        </div>
      </main>

      <Footer autor="Franco Ghilardi" anio={2026} />
    </div>
  );
};
