/**
 * TLDR; App shell (layout + route outlet).
 * TODO: Add protected routes, navigation, and page-level loading states.
 */

import React from "react";

import { AppLayout } from "./layouts/AppLayout.jsx";
import { AppRoutes } from "./routes/index.jsx";

export function App() {
  return (
    <AppLayout>
      <AppRoutes />
    </AppLayout>
  );
}

