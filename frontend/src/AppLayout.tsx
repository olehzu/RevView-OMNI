import type { ReactNode } from "react";

/** The shell every page renders in: the product name and a main region. */
function AppLayout({ children }: { children: ReactNode }) {
  return (
    <>
      <header className="app-header">
        <span className="app-name">RevView/OMNI</span>
      </header>
      <main>{children}</main>
    </>
  );
}

export default AppLayout;
