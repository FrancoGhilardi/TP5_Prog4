interface FooterProps {
  autor: string;
  anio: number;
}

export const Footer = ({ autor, anio }: FooterProps) => {
  return (
    <footer className="border-t border-borde bg-superficie py-6 text-center text-sm text-texto-suave">
      © {anio} {autor}. Todos los derechos reservados.
    </footer>
  );
};
