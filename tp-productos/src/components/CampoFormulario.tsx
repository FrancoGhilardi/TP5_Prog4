import type { ReactNode } from "react";

interface CampoFormularioProps {
  label: string;
  htmlFor: string;
  className?: string;
  children: ReactNode;
}

export const CampoFormulario = ({
  label,
  htmlFor,
  className,
  children,
}: CampoFormularioProps) => {
  return (
    <div className={`flex flex-col gap-1 ${className ?? ""}`}>
      <label htmlFor={htmlFor} className="text-sm font-medium text-texto">
        {label}
      </label>
      {children}
    </div>
  );
};
