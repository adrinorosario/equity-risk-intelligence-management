/**
 * TLDR; Portfolio list/management UI scaffold.
 * TODO: Implement portfolio CRUD and equity management per SRS FR2/FR3.
 */

import React from "react";
import { Paper, Stack, Typography, Button } from "@mui/material";

export function PortfolioListPage() {
  return (
    <Paper sx={{ p: 3 }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography variant="h5">Portfolios</Typography>
        <Button variant="contained">New portfolio</Button>
      </Stack>
      <Typography sx={{ mt: 2 }} color="text.secondary">
        Scaffold only — implement list rendering + create/update flows.
      </Typography>
    </Paper>
  );
}

