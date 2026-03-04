/**
 * TLDR; Reporting UI scaffold (generate/export reports).
 * TODO: Implement report generation workflow and exports per SRS FR5.
 */

import React from "react";
import { Paper, Stack, Typography, Button } from "@mui/material";

export function ReportsPage() {
  return (
    <Paper sx={{ p: 3 }}>
      <Stack direction="row" justifyContent="space-between" alignItems="center">
        <Typography variant="h5">Reports</Typography>
        <Button variant="contained">Generate report</Button>
      </Stack>
      <Typography sx={{ mt: 2 }} color="text.secondary">
        Scaffold only — implement report list + export actions.
      </Typography>
    </Paper>
  );
}

