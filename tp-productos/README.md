# Gestor de Productos — Frontend (Parte B)

Pantalla de **Productos** maquetada con **React + TypeScript + Tailwind CSS** (Vite). Solo presentación: sin `useState`, sin `useEffect`, sin ningún hook, sin llamadas a la API. Los datos son un array hardcodeado que simula el catálogo del backend (Parte A).

## Stack

- Vite 8 + React 19 + TypeScript 6
- Tailwind CSS v4 (`@tailwindcss/vite`, sin `tailwind.config.js` ni PostCSS)
- ESLint 10 (flat config) + `typescript-eslint` + `eslint-plugin-react-hooks`

## Puesta en marcha

```bash
pnpm install
pnpm dev       # http://localhost:5173
```

También funciona con `npm install && npm run dev` si no se cuenta con `pnpm`.

## Scripts disponibles

| Script            | Qué hace                                      |
| ----------------- | ---------------------------------------------- |
| `pnpm dev`         | Servidor de desarrollo con HMR                 |
| `pnpm build`       | Typecheck (`tsc -b`) + build de producción      |
| `pnpm preview`     | Sirve el build de `dist/` localmente           |
| `pnpm lint`        | ESLint sobre todo el proyecto                  |
| `pnpm typecheck`   | Solo chequeo de tipos, sin emitir (`tsc -b --noEmit`) |

## Estructura del proyecto

```
tp-productos/
├── index.html                 # <title>Gestor de Productos</title>, lang="es"
├── vite.config.ts             # plugins: react() + tailwindcss()
├── eslint.config.js           # flat config: no-explicit-any, react-hooks, react-refresh
└── src/
    ├── main.tsx                # bootstrap: createRoot + <App />
    ├── index.css               # @import "tailwindcss" + tokens de marca en @theme
    ├── App.tsx                 # composition root: arma el layout y pasa los datos por props
    ├── types/
    │   └── producto.ts         # interface Producto (dominio) — id, nombre, descripcion, precio
    ├── data/
    │   └── productos.ts        # Producto[] hardcodeado (4 productos)
    ├── lib/
    │   ├── formato.ts          # formatearPrecio(): Intl.NumberFormat es-AR
    │   └── estilos.ts          # clases Tailwind reutilizadas (estiloPanel, estiloCampo)
    └── components/
        ├── Navbar.tsx           # barra superior
        ├── Footer.tsx           # pie de página
        ├── ProductoCard.tsx     # tarjeta de un producto
        ├── ProductoList.tsx     # grilla responsive de ProductoCard
        ├── ProductoForm.tsx     # formulario de alta maquetado, sin estado
        └── CampoFormulario.tsx  # wrapper label + input/textarea, usado por ProductoForm
```

**Capas y dependencias:** `types/` no importa nada (es el dominio). `data/` y `lib/` dependen solo de `types/`. `components/` recibe todo por props — ninguno importa desde `data/`. `App.tsx` es el único archivo que conoce datos y componentes a la vez: arma el layout.

## Componentes

| Componente         | Props                                              | Notas                                              |
| ------------------ | --------------------------------------------------- | --------------------------------------------------- |
| `Navbar`            | `titulo: string`                                     | Ítems de menú son texto, no hay router              |
| `Footer`            | `autor: string`, `anio: number`                      | —                                                    |
| `ProductoList`      | `productos: Producto[]`                              | `key={producto.id}`, grilla 1/2/3 columnas          |
| `ProductoCard`      | `producto: Producto`                                 | Recibe el objeto completo, no props sueltos          |
| `ProductoForm`      | *(sin props)*                                        | Inputs no controlados, botón `type="button"`         |
| `CampoFormulario`   | `label`, `htmlFor`, `className?`, `children`         | Envuelve label + campo; usado 3 veces en `ProductoForm` |

## Decisiones de diseño

- **Tailwind v4 vía `@tailwindcss/vite`**: es la guía oficial actual para Vite. No hay `tailwind.config.js` ni `postcss.config.js` — los tokens de paleta viven en `src/index.css` dentro de `@theme`.
- **`interface Producto` con 4 campos únicamente** (`id`, `nombre`, `descripcion`, `precio`): es el contrato que pide la consigna. El backend expone más campos, pero acá no hay `fetch` que los consuma.
- **Datos hardcodeados en `src/data/productos.ts`**, importados por `App.tsx`: separa el dato (reemplazable el día que haya API) de la UI.
- **Componentes como `const` con arrow function** y export nombrado (no `React.FC`, no default export salvo donde se indica).
- **Sin estado ni hooks** (RN-09): el formulario usa inputs no controlados y el botón de guardar es `type="button"` para no disparar submit nativo.
- **`pnpm` como gestor de paquetes**: se versiona `pnpm-lock.yaml`, no `package-lock.json`.
