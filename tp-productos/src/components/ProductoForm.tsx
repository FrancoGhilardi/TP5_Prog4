import { CampoFormulario } from "./CampoFormulario";
import { estiloCampo, estiloPanel } from "../lib/estilos";

export const ProductoForm = () => {
  return (
    <form className={estiloPanel}>
      <h2 className="text-base font-semibold text-texto">Nuevo producto</h2>

      <div className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
        <CampoFormulario label="Nombre" htmlFor="nombre">
          <input
            id="nombre"
            name="nombre"
            type="text"
            placeholder="Silla de Oficina"
            className={estiloCampo}
          />
        </CampoFormulario>

        <CampoFormulario label="Precio" htmlFor="precio">
          <input
            id="precio"
            name="precio"
            type="number"
            step="0.01"
            min="0"
            placeholder="150.50"
            className={estiloCampo}
          />
        </CampoFormulario>

        <CampoFormulario label="Descripción" htmlFor="descripcion" className="sm:col-span-2">
          <textarea
            id="descripcion"
            name="descripcion"
            rows={3}
            placeholder="Silla ergonómica con apoyabrazos regulables."
            className={estiloCampo}
          />
        </CampoFormulario>
      </div>

      <button
        type="button"
        className="mt-4 rounded-lg bg-marca-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-marca-700"
      >
        Guardar producto
      </button>
    </form>
  );
};
