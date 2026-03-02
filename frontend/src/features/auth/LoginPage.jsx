/**
 * TLDR; Login page UI scaffold.
 * TODO: Implement form, validation, and call backend `/auth/login`.
 */

import React from "react";
import { Paper, Stack, TextField, Typography, Button } from "@mui/material";

export function LoginPage() {
  return (
    <Paper sx={{ p: 3 }}>
      <Stack spacing={2}>
        <Typography variant="h5">Login</Typography>
        <TextField label="Email" fullWidth />
        <TextField label="Password" type="password" fullWidth />
        <Button variant="contained">Sign in</Button>
      </Stack>
    </Paper>
  );
}

