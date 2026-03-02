/**
 * TLDR; Top-level layout wrapper for consistent app chrome.
 * TODO: Implement navigation (sidebar/topbar), breadcrumbs, and user menu.
 */

import React from "react";
import { Box, Container } from "@mui/material";

export function AppLayout({ children }) {
  return (
    <Box sx={{ minHeight: "100vh", bgcolor: "background.default", color: "text.primary" }}>
      <Container maxWidth="lg" sx={{ py: 3 }}>
        {children}
      </Container>
    </Box>
  );
}

