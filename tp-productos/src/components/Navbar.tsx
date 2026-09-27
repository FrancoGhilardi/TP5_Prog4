interface NavbarProps {
  titulo: string;
}

export const Navbar = ({ titulo }: NavbarProps) => {
  return (
    <header className="bg-marca-600 text-white shadow-sm">
      <nav className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <span className="text-lg font-semibold tracking-tight">{titulo}</span>
        <ul className="flex gap-6 text-sm text-marca-100">
          <li>Productos</li>
          <li>Categorías</li>
          <li>Proveedores</li>
        </ul>
      </nav>
    </header>
  );
};
