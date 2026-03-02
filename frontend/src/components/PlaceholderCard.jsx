/**
 * TLDR; Small reusable placeholder component for scaffolding screens.
 * TODO: Replace with real components as features are implemented.
 */

import React from "react";
import { Paper, Typography } from "@mui/material";

export function PlaceholderCard({ title, children }) {
  return (
    <Paper sx={{ p: 2 }}>
      <Typography variant="subtitle1" sx={{ mb: 1 }}>
        {title}
      </Typography>
      {children}
    </Paper>
  );
}

