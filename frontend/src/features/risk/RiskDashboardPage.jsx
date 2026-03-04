/**
 * TLDR; Risk dashboard UI scaffold (charts + summaries).
 * TODO: Implement risk metric visualizations and integrate `/risk` endpoints per SRS FR4.
 */

import React from "react";
import { Paper, Stack, Typography } from "@mui/material";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function RiskDashboardPage() {
  const placeholderData = [];

  return (
    <Paper sx={{ p: 3 }}>
      <Stack spacing={2}>
        <Typography variant="h5">Risk Dashboard</Typography>
        <Typography color="text.secondary">
          Scaffold only — connect to backend and render metrics.
        </Typography>
        <ResponsiveContainer width="100%" height={240}>
          <LineChart data={placeholderData}>
            <XAxis dataKey="x" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="y" stroke="#1976d2" dot={false} />
          </LineChart>
        </ResponsiveContainer>
      </Stack>
    </Paper>
  );
}

