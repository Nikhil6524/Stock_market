import { createContext, useContext, useState } from "react";
import type { PropsWithChildren } from "react";

type Screen = "dashboard";

type AppContextValue = {
  activeScreen: Screen;
  setActiveScreen: (screen: Screen) => void;
};

const AppContext = createContext<AppContextValue | undefined>(undefined);

export function AppProvider({ children }: PropsWithChildren): JSX.Element {
  const [activeScreen, setActiveScreen] = useState<Screen>("dashboard");
  return (
    <AppContext.Provider value={{ activeScreen, setActiveScreen }}>
      {children}
    </AppContext.Provider>
  );
}

export function useAppContext(): AppContextValue {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within AppProvider.");
  }
  return context;
}

